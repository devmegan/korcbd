from django.shortcuts import render

# Create your views here.


def profile(request):
    """ view returns profile page to user """
    context = {}
    return render(request, 'profiles/profile.html', context)