from django import forms
from .models import AboutSection


class AboutSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'

        widgets = {
            'section_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a section subheading'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write the section text here',
            }),
        }
