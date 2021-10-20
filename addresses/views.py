from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
# Create your views here.
from .forms import AddressForm
from .models import Address
from billing.models import BillingProfile


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form
    }
    # print(request.user.is_authenticated())
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    # redirect to the CHECKOUT view
    if form.is_valid():
        print("checkout address form submitted", request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = request.POST.get(
                "address_type", "shipping")
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            print(address_type + "_address_id")
            # from cart views
            #billing_address_id = request.session.get("billing_address_id", None)
            #shipping_address_id = request.session.get("shipping_address_id", None)

        else:
            print("error in checkout address")
            return redirect("carts:checkout")

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("carts:checkout")


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context = {}
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post or None
        if request.method == "POST":
            print("checkout address USE ", request.POST)
            shipping_address = request.POST.get("shipping_address", None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
                request)
            if shipping_address is not None:
                qs = Address.objects.filter(
                    billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type +
                                    "_address_id"] = shipping_address
                    print(address_type + "_address_id")
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)

    return redirect("carts:checkout")
