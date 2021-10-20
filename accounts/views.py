from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.utils.http import is_safe_url
from django.urls import reverse
from django.utils.safestring import mark_safe

# Login/related authentication parameters
from django.contrib.auth import authenticate, login, logout, get_user_model

#Mixins
from djangoapi.mixins import NextUrlMixin, RequestFormAttachMixin

#Views
from django.views.generic.edit import FormMixin
from django.views.generic import (
    View,
    FormView,
    UpdateView,
    ListView,
    DetailView,
    CreateView,
    DeleteView,
)

# Flash messages
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.contrib.auth.models import Group

#relative imports
from .models import (
    GuestEmail, 
    EmailActivation,
)
from .forms import (
    LoginForm, 
    RegisterForm, 
    GuestForm,
    ReactivateEmailForm,
    UserUpdateForm,
    #QuickRegisterForm,
    #UserAdminCreationForm,
)
# from .decorators import (
#     unauthenticated_user,
#     allowed_users,
#     admin_only,
# )
from .signals import user_logged_in


# def home_page(request):
#     context = {
#     }
#     return render(request, "accounts/home.html", context)


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user



class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            #Get the EXACT email activation key
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                #gets a single key
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                #Email is already activated, but might need to reset pw
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login") 
        context = {'form': self.get_form(),'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user 
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key }
        return render(self.request, 'registration/activation-error.html', context)


class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'accounts/detail-update-view.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView,
                        self).get_context_data(*args, **kwargs)
        context['title'] = 'Change Your Account Details'
        return context

    def get_success_url(self):
        return reverse("accounts:home")


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/account/'
    template_name = 'accounts/login.html'
    default_next = '/account/'

    def form_valid(self, form):
        success_url = '/account/'
        #becuase the user is attached to the form at the form level, we now have the form object
        #ALSO dont have to check if valid/authenticated b/c it will only come here if it passes the form validation
        next_path = self.get_next_url()
        return redirect(success_url)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = 'login/'



def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    print("Guest form submitted", request.POST)
    
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email  = form.cleaned_data.get("email")
        #using this to store the email in our database
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")



# class LoginView(FormView):
#     form_class = LoginForm
#     success_url = '/'
#     template_name = 'accounts/login.html'

#     def form_valid(self, form):
#         request = self.request
#         next_ = request.GET.get("next")
#         next_post = request.POST.get("next")
#         redirect_path = next_ or next_post or None
#         print("accounts views ln 43 User logged in", request.POST,' next_:',next_ ,' next_post: ',next_post)
        
#         email  = form.cleaned_data.get("email")
#         password  = form.cleaned_data.get("password")
#         user = authenticate(request, username=email, password=password)
#         print('accounts views login page, ln 53',user,'redirect_path:', redirect_path)
#         #print(request.user.is_authenticated())
#         if user is not None:
#             #print(request.user.is_authenticated())
#             login(request, user)
#             try:
#                 #deleting the guest email Id since user is not a guest
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             # Redirect to a success page.
#             #context['form'] = LoginForm()
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         return super(LoginView,self).form_invalid(form)


# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }
    
#     #print(request.user.is_authenticated())
#     next_ = request.GET.get("next")
#     next_post = request.POST.get("next")
#     print("accounts views ln 43 User logged in", request.POST,' next_:',next_ ,' next_post: ',next_post)
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         print(form.cleaned_data)
#         username  = form.cleaned_data.get("username")
#         password  = form.cleaned_data.get("password")
#         user = authenticate(request, username=username, password=password)
#         print('accounts views login page, ln 53',user,'redirect_path:', redirect_path)
#         #print(request.user.is_authenticated())
#         if user is not None:
#             #print(request.user.is_authenticated())
#             login(request, user)
#             try:
#                 #deleting the guest email Id since user is not a guest
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             # Redirect to a success page.
#             #context['form'] = LoginForm()
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             # Return an 'invalid login' error message.
#             print("Error")

#     return render(request, "accounts/login.html", context)


# class RegisterView(CreateView):
#     form_class = RegisterForm
#     template_name = 'accounts/register.html'
#     success_url = 'accounts/login.html'

# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     if form.is_valid():
#         # print(form.cleaned_data)
#         # username  = form.cleaned_data.get("username")
#         # email  = form.cleaned_data.get("email")
#         # password  = form.cleaned_data.get("password")
#         # new_user  = User.objects.create_user(username, email, password)
#         # print(new_user)
#         #because model form -----
#         form.save()

#     return render(request, "accounts/register.html", context)