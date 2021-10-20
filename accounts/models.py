from datetime import timedelta
import os
from django.db.models import Q
from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
import datetime
from django.utils import timezone
from django import forms
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.core.mail import send_mail
from django.template.loader import get_template

from djangoapi.utils import random_string_generator, unique_key_generator
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)

# Create your models here.
class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, is_active=True,staff=False,admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        if not password:
            raise ValueError('Users must have a password')

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=self.normalize_email(first_name),
            last_name=self.normalize_email(last_name),
        )
        user_obj.set_password(password)
        user_obj.staff = staff
        user_obj.admin = admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, first_name, last_name, email, password=None, is_active=True,staff=True,admin=False):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.staff = True
        user.admin = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name, last_name, password,is_active=True,staff=True,admin=True):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    #full_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = "email"  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['first_name','last_name']  # ['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    # def get_full_name(self):
    #     if self.full_name:
    #         return self.full_name
    #     return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active




class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        # does my object have a timestamp in here
        end_range = now
        return self.filter(
                activated = False,
                forced_expired = False
              ).filter(
                timestamp__gt=start_range,
                timestamp__lte=end_range
              )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
                    Q(email=email) | 
                    Q(user__email=email)
                ).filter(
                    activated=False
                )



class EmailActivation(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    email           = models.EmailField()
    key             = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    forced_expired  = models.BooleanField(default=False)
    expires         = models.IntegerField(default=7) # 7 Days
    timestamp       = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable() # 1 object
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            # pre activation user signal
            user = self.user
            user.is_active = True
            user.save()
            # post activation signal for user
            self.activated = True
            self.save()
            return True
        return False

    # gives the ability to regenerate a key
    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False


    def send_activation(self):
        #BASE_HTTP = 'http://127.0.0.1:8000'
        if not self.activated and not self.forced_expired:
            if self.key:
                # in the settings file, different for local vs production
                base_url = getattr(settings,'BASE_URL','https://www.technicallycpa.com/')
                key_path = reverse("accounts:email-activate", kwargs={'key': self.key}) # use reverse
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                #templates we prepared
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = '1-Click Email Verification'
                #in the settings/config
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    # this means the message didn't go through
                    fail_silently=False,
                )
                if sent_mail:
                    print(f"SENT MAIL {sent_mail}")
                    return sent_mail
                sendgrid_mail = Mail(
                    from_email=getattr(settings,'EMAIL_HOST_USER'),
                    to_emails=recipient_list,
                    subject=subject,
                    html_content=html_)
                try:
                    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                    response = sg.send(sent_mail)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print(e)
                if response:
                    print(f"sendgrid_mail {sent_mail}")
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                    return sendgrid_mail
                return False
        return False



def pre_save_email_activation(sender, instance, *args, **kwargs):
    #if NOT active AND not EXPIRED
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_reciever, sender=User)

