from django.shortcuts import render

# Create your views here.

def about(request):
    """ view returns about page """
    return render(request, 'about/about.html')