from django.urls import path

from .views import (
    ProductListView, 
    #ProductDetailView,
    #ProductABSListView,
    ProductDetailSlugView,
    #ProductFeaturedListView,
    #ProductFeaturedDetailView,
    ProductDownloadView,
)

app_name = "products"
urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    #path('list/abs/', ProductABSListView.as_view(), name='product-abs-list'),
    #path('list/<pk>/', ProductDetailView.as_view(), name='product-detail'),
    #path('featured/', ProductFeaturedListView.as_view(), name='product-featured-list'),
    #path('featured/<pk>/', ProductFeaturedDetailView.as_view(), name='product-featured-detail'),
    path('<slug>/', ProductDetailSlugView.as_view(), name='detail'),
    path('<slug>/<pk>/', ProductDownloadView.as_view(), name='download'),
]



#<!--  <a href="{% url 'products:detail' slug=instance.slug  %}" class="btn btn-warning">URL shortcut</a> -->