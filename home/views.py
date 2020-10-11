from django.shortcuts import render
from blog.models import Post
from django.contrib import messages
from profiles.models import UserProfile
from cart.models import Order

# Create your views here.


def index(request):
    """ view returns index page """

    profile = None
    blog_posts = None
    track_order = None

    blog_posts = Post.objects.all().order_by('id')[:3]

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

    # handle order tracking requests
    if request.POST:
        order_ref = request.POST['order-ref-track']
        try:
            track_order = Order.objects.get(order_reference=order_ref)
        except:
            messages.error(
                request,
                f"{order_ref} doesn't match an order placed with us. \
                Please check the order reference is correct. \
                If the problem continues, please get in touch."
            )

    context = {
        'blog_posts': blog_posts,
        'profile': profile,
        'track_order': track_order,
    }
    return render(request, 'home/index.html', context)
