from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from .forms import OrderForm
from basket.contexts import basket_contents
import stripe


def checkout(request):
    """
    Handles checkout logic and stripe
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "Your bag is empty")
        return redirect(reverse('products'))

    current_basket = basket_contents(request)
    total = current_basket['total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        
     }

    return render(request, template, context,)