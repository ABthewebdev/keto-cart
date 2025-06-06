from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from .utils import *

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import *
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

def shop_view(request):
    products_list = stripe.Product.list()
    products = []
    for product in products_list:
        products.append(product_details(product))
    return render(request, 'stripe_app/shop.html')

def product_view(request):
    product_id = 'prod_PzfeBs9rwa8Rno'
    product = stripe.Product.retrieve(product_id)
    prices = stripe.Price.list(product=product_id)
    price = prices.data[0]
    product_price = price.unit_amount / 100.0

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f'{settings.BASE_URL}{reverse("login")}?next={request.get_full_path()}')
        
        price_id = request.POST.get('price_id')
        quantity = int(request.POST.get('quantity'))
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': price_id,
                    'quantity': quantity,
                },
            ],
            payment_method_types = ['card'],
            mode = 'payment',
            customer_creation = 'always',
            success_url = f'{settings.BASE_URL}{reverse("payment_successful")}?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url = f'{settings.BASE_URL}{reverse("payment_cancelled")}',
        )
        return redirect(checkout_session.url, code=303)
        
    return render(request, 'stripe_app/product.html', {'product': product, 'product_price': product_price})

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