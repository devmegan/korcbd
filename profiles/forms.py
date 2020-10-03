from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """ placeholders for form fields """
        super().__init__(*args, **kwargs)
        placeholders = {
            'profile_phone_number': 'Phone Number',
            'profile_postcode': 'Post Code',
            'profile_town_or_city': 'Town or City',
            'profile_street_address1': 'Street Address 1',
            'profile_street_address2': 'Street Address 2',
            'profile_county': 'County/State/Province',
        }

        self.fields['profile_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'profile_country':
                if self.fields[field].required:
                    # add asterisk to required fields
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # set values for fields
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # style fields to match stripe element
            self.fields[field].widget.attrs['class'] = 'stripe-style-input form-control rounded-0 my-2'
            # remove form field labels
            self.fields[field].label = False