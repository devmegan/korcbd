from django.shortcuts import render
from .models import AboutSection
# Create your views here.


def about(request):
    """ view returns about page with about sections """
    about_sections = None
    about_sections = AboutSection.objects.all()
    context = {
        'about_sections': about_sections
    }
    return render(request, 'about/about.html', context)
