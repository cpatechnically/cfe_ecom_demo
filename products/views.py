from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect


from carts.models import Cart

# Create your views here.
from .models import Product, ProductFile

from analytics.mixins import ObjectViewedMixin


# PRODUCTS
class UserProductHistoryView(LoginRequiredMixin, ListView):
    template_name = "products/user-history.html"
    #template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        # print(context)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        #getting the viewset of product views of the user.
        views = request.user.objectviewed_set.by_model(Product, model_queryset=False)  #all().filter(content_type='product')
        #viewed_ids = [x.object_id for x in views]
        return views #Product.objects.filter(pk__in=viewed_ids)


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured() #from custom model manager


class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/featured-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductListView(ListView):
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    #def get_context_data(self, *args, **kwargs):
        #context = super(ProductListView, self).get_context_data(*args, **kwargs)
        #cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        #context['cart'] = cart_obj
        #return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()



class ProductABSListView(ListView):
    template_name = "products/list_absurl.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    #def get_context_data(self, *args, **kwargs):
        #context = super(ProductListView, self).get_context_data(*args, **kwargs)
        #cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        #context['cart'] = cart_obj
        #return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)


class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance


import os
from wsgiref.util import FileWrapper
from django.conf import settings
from mimetypes import guess_type
from django.conf import settings
from orders.models import ProductPurchase


class ProductDownloadView(View):
    def get(self,*args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not found")
        download_obj = downloads_qs.first()
        # permission checks
        
        can_download = False
        user_ready  = True
        if download_obj.user_required:
            if not request.user.is_authenticated:
                user_ready = False

        purchased_products = Product.objects.none()
        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            # not free
            request = self.request
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to download this item")
            return redirect(download_obj.get_default_url())

        aws_filepath = download_obj.generate_download_url()
        print(aws_filepath)
        return HttpResponseRedirect(aws_filepath)
        # file_root = settings.PROTECTED_ROOT
        # filepath = download_obj.file.path # .url /media/
        # final_filepath = os.path.join(file_root, filepath) # where the file is stored
        # with open(final_filepath, 'rb') as f:
        #     wrapper = FileWrapper(f)
        #     mimetype = 'application/force-download'
        #     gussed_mimetype = guess_type(filepath)[0] # filename.mp4
        #     if gussed_mimetype:
        #         mimetype = gussed_mimetype
        #     response = HttpResponse(wrapper, content_type=mimetype)
        #     response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.name)
        #     response["X-SendFile"] = str(download_obj.name)
        #     return response
        #return redirect(download_obj.get_default_url())