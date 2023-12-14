from .models import Address
from django import forms



class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['name', 'phone_number', 'street_address', 'city', 'postal_code', 'state']