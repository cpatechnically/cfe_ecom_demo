# accounts.passwords.urls.py 
#from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns  = [
# url(r'^password/change/$', 
#         auth_views.PasswordChangeView.as_view(), 
#         name='password_change'),
# url(r'^password/change/done/$',
#         auth_views.PasswordChangeDoneView.as_view(), 
#         name='password_change_done'),
# url(r'^password/reset/$', 
#         auth_views.PasswordResetView.as_view(), 
#         name='password_reset'),
# url(r'^password/reset/done/$', 
#         auth_views.PasswordResetDoneView.as_view(), 
#         name='password_reset_done'),
# url(r'^password/reset/\
#         (?P<uidb64>[0-9A-Za-z_\-]+)/\
#         (?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
#         auth_views.PasswordResetConfirmView.as_view(), 
#         name='password_reset_confirm'),

# url(r'^password/reset/complete/$', 
#         auth_views.PasswordResetCompleteView.as_view(), 
#         name='password_reset_complete'),

# User is authenticated, they volunatrily change their password
path('password_change/', auth_views.PasswordChangeView.as_view(
    template_name='registration/password_change_form.html'), name='password_change'),
# You went through the pw change form, then you are redirected here
path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
    template_name='registration/password_change_done.html'), name='password_change_done'),
# You went through the pw change form, then you are redirected here
path('password_reset/', auth_views.PasswordResetView.as_view(
    template_name='registration/password_reset_form.html'), name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    template_name='registration/password_reset_done.html'), name='password_reset_done'),
path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
    template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]