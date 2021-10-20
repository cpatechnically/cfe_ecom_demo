from django.dispatch import Signal
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

user_logged_in = Signal(providing_args=['request','instance'])