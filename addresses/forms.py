from django.forms import ModelForm
from .models import Address

class AddressForm(ModelForm):
    class Meta:
        model = Address
        #fields = #"__all__" 
        fields = [
            #'billing_profile', #Associate to user automatically
            #'address_type', Should be automatic from local
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code',
        ]