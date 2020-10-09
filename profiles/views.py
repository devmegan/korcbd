from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from cart.models import Order
from .forms import UserProfileForm
# Create your views here.


@login_required
def profile(request):
    """ view returns profile page to user and handles updating profile info """
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile has been updated')
        else:
            messages.error(
                request,
                'Failed to update profile. Please check the form is valid'
            )
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'orders': orders,
        'viewing_profile_page': True,
    }
    return render(request, 'profiles/profile.html', context)


def order_history(request, order_reference):
    """ view to return details of previous order to user """
    order = get_object_or_404(Order, order_reference=order_reference)
    messages.info(
        request,
        (f'This is a past order confirmation for order {order_reference}')
    )
    context = {
        'order': order,
        'viewing_order_history': True,
    }
    return render(request, 'cart/checkout_success.html', context)
