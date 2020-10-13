from django.shortcuts import render
from blog.models import Post
# from django.core.exceptions import DoesNotExist
from django.contrib import messages
from cart.models import Order

# Create your views here.


def index(request):
    """ view returns index page """

    blog_posts = None
    track_order = None

    blog_posts = Post.objects.all().order_by('id')[:3]

    # handle order tracking requests
    if request.POST:
        order_ref = request.POST['order-ref-track']
        try:
            track_order = Order.objects.get(order_reference=order_ref)
        except Order.DoesNotExist:
            messages.error(
                request,
                f"{order_ref} doesn't match an order placed with us. \
                Please check the order reference is correct. \
                If the problem continues, please get in touch."
            )

    context = {
        'blog_posts': blog_posts,
        'track_order': track_order,
    }
    return render(request, 'home/index.html', context)
