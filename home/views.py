from django.shortcuts import render
from blog.models import Post
from profiles.models import UserProfile

# Create your views here.


def index(request):
    profile = None
    blog_posts = None
    """ view returns index page """
    blog_posts = Post.objects.all().order_by('id')[:3]

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

    context = {
        'blog_posts': blog_posts,
        'profile': profile,
    }
    return render(request, 'home/index.html', context)
