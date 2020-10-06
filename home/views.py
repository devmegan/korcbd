from django.shortcuts import render
from blog.models import Post

# Create your views here.


def index(request):
    """ view returns index page """
    blog_posts = Post.objects.all().order_by('id')[:3]
    context = {
        'blog_posts': blog_posts,
    }
    return render(request, 'home/index.html', context)

