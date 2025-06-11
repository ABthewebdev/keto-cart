import stripe
from django.shortcuts import reverse
from django.conf import settings

def get_product_details(product):
    price_id = product.get("default_price")

    if not price_id:
        raise ValueError(f"Product {product['id']} has no default_price set.")

    price = stripe.Price.retrieve(price_id)

    return {
        'id': product['id'],
        'name': product.get('name', 'Unnamed Product'),
        'image': product.get('images', [''])[0] if product.get('images') else '',
        'description': product.get('description', ''),
        'price': price['unit_amount'] / 100 if price.get('unit_amount') else 0
    }

def create_checkout_session(cart, customer_email):
    line_items = []
    for item in cart:
        prices = stripe.Price.list(product=item['id'])
        price = prices.data[0]
        line_items.append({
            'price': price.id,
            'quantity': item['quantity']
        })
    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        payment_method_types=['card'],
        mode='payment',
        customer_creation='always',
        success_url=f'{settings.BASE_URL}{reverse("payment_successful")}?session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url=f'{settings.BASE_URL}{reverse("payment_cancelled")}',
        customer_email=customer_email,
    )
    return checkout_session