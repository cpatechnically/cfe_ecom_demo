from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render
from .models import Order, ProductPurchase
from billing.models import BillingProfile



class OrderListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        #my_profile = BillingProfile.objects.new_or_get(self.request)
        #get billing profile from order model manager
        return Order.objects.by_request(self.request)


class OrderDetailView(LoginRequiredMixin, DetailView):
    
    def get_object(self):
        #return Order.objects.get(id=self.kwargs.get('id'))
        #return Order.objects.get(slug=self.kwargs.get('slug'))
        #qs = self.get_queryset()
        #print(qs)
        qs = Order.objects.by_request(
            self.request
            ).filter(
                order_id = self.kwargs.get('order_id')
            )
        if qs.count() == 1:
            return qs.first()
        raise Http404


class LibraryView(LoginRequiredMixin, ListView):
    template_name = 'orders/library.html'
    def get_queryset(self):
        # print(ProductPurchase.objects.products_by_request(self.request))
        return ProductPurchase.objects.by_request(self.request).digital()
        #return Order.objects.by_request(self.request)


class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET 
            product_id = request.GET.get('product_id', None)
            if product_id is not None:
                product_id = int(product_id)
                ownership_ids = ProductPurchase.objects.products_by_id(request)
                if product_id in ownership_ids:
                    return JsonResponse({'owner': True})
            return JsonResponse({'owner': False})
        raise Http404