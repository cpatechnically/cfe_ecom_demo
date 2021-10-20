"""djangoapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

# account app if present
#from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from .views import home_page, about_page, contact_page, context_demo, example_nav, react_page
from carts.views import cart_detail_api_view
from billing.views import payment_method_view, payment_method_createview

from django.views.generic.base import TemplateView, RedirectView
from orders.views import LibraryView
from analytics.views import SalesView, SalesAjaxView


from accounts.views import LoginView, RegisterView, guest_register_view


urlpatterns = [
    path('', home_page, name="index"),
    path('example/nav', example_nav, name="example-nav"),
    path('admin/', admin.site.urls),
    path('context/', context_demo),
    path('about/', about_page, name="about"),
    path('billing/payment-method/', payment_method_view,name="billing-payment-method"),
    path('billing/payment-method/create/', payment_method_createview,name="billing-payment-method-endpoint"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('library/', LibraryView.as_view(), name="library"),
    path('api/carts/', cart_detail_api_view, name="api-carts"),
    path('checkout/address/create/', checkout_address_create_view,
        name="checkout_address_create"),  # Not a view, just an ENDPOINT that will redirect
    # Not a view, just an ENDPOINT that will redirect
    path('checkout/address/reuse/', checkout_address_reuse_view,
        name="checkout_address_reuse"),
    path('register/', RegisterView.as_view(), name="register"),
    path('register/guest/', guest_register_view, name="guest_register"),
    path('contact/', contact_page, name="contact"),
    path('products/', include('products.urls', namespace="products")),
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include('accounts.urls', namespace="account")),
    #Passwords module - This is OVERRIDING the django default
    path('accounts/', include('accounts.passwords.urls')),
    path('carts/', include('carts.urls', namespace="carts")),
    # REACT views
    path('orders/', include('orders.urls', namespace="orders")),
    path('search/', include('search.urls', namespace="search")),
    # path('updates/', include('updates.urls')),
    # path('status/', include('status.urls')),
    # path('api-token-auth/', obtain_jwt_token),
    # path('api-token-auth/refresh/', refresh_jwt_token),
    # path('api/status/', include('status.api.urls')),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
