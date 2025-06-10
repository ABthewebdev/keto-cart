from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from .cart import Cart
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .utils import *
from .models import *
from .forms import *
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

def shop_view(request):
    products_list = stripe.Product.list()
    products = []
    for product in products_list:
        products.append(get_product_details(product))
    return render(request, 'stripe_app/shop.html', {"products": products})

def product_view(request, product_id):
    product = stripe.Product.retrieve(product_id)
    product_details = get_product_details(product)
    cart = Cart(request)
    product_details['in_cart'] = product_id in cart.cart_session
    
    return render(request, 'stripe_app/product.html', {'product': product_details})


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    
    product = stripe.Product.retrieve(product_id)
    product_details = get_product_details(product)
    product_details['in_cart'] = product_id in cart.cart_session

    response = render(request, 'stripe_app/partials/cart-button.html', {'product': product_details})
    response['HX-Trigger'] = 'hx_menu_cart'
    return response


def payment_successful(request):
    checkout_session_id = request.GET.get('session_id', None)

    if checkout_session_id:
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer_id = session.customer
        customer = stripe.Customer.retrieve(customer_id)

        line_item = stripe.checkout.Session.list_line_items(checkout_session_id).data[0]
        UserPayment.objects.get_or_create(
            user = request.user,
            stripe_customer = customer_id,
            stripe_checkout_id = checkout_session_id,
            stripe_product_id = line_item.price.product,
            product_name = line_item.description,
            quantity = line_item.quantity,
            price = line_item.price.unit_amount / 100.0,
            currency = line_item.price.currency,
            has_paid = True
        )
    return render(request, 'stripe_app/payment_successful.html', {'customer': customer})

def payment_cancelled(request):
    return render(request, 'stripe_app/payment_cancelled.html')

@login_required
def checkout_view(request):
    form = ShippingForm(initial={'email': request.user.email})
    return render(request, 'stripe_app/checkout.html', {'form': form})
    
@csrf_exempt
@require_POST
def stripe_webhook(request):
    event = None
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    if not sig_header:
        return HttpResponse(status=400)
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the event
    print('Unhandled event type {}'.format(event['type']))
    
    return JsonResponse({'success': True})