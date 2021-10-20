from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
from products.views import UserProductHistoryView

from accounts.views import (
    AccountHomeView,
    AccountEmailActivateView,
    UserDetailUpdateView,
)

from marketing.views import MarketingPreferenceUpdateView

app_name = "accounts"
urlpatterns = [
    #path('<pk>/',views.contact_detail_view, name="detail"),
    path('', AccountHomeView.as_view(), name="home"),
    #path('business/add/', clientForm, name="add-client"),
    path('settings/email/',MarketingPreferenceUpdateView.as_view(),name='marketing-pref'),
    path('details/', UserDetailUpdateView.as_view(), name="user-update"),
    #Product History
    path('history/products/', UserProductHistoryView.as_view(),name='history-product'),
    #Email
    path('email/confirm/<key>/', AccountEmailActivateView.as_view(),name='email-activate'),
    path('email/resend-activation/', AccountEmailActivateView.as_view(),name='resend-activation'),
    # Customer
    #path('profile/<int:id>/', views.customerProfile, name="customer-profile"),
    # path('customer/<int:id>/update/', views.updateCustomer, name="update-customer"),
    # path('customer/<int:id>/settings/', views.customerSettings, name="customer-settings"),
    #path('todo/', views.todo, name="accounts-todo"),
    # Auth

]
