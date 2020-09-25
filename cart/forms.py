from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """ placeholders for form fields """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Post Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                # add asterisk to required fields
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # set values for fields
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # style fields to match stripe element
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # remove form field labels
            self.fields[field].label = False