from django.shortcuts import render, redirect
from stripe_app.cart import Cart
import stripe
from stripe_app.utils import get_product_details

def home(request):
    return render(request, "main/home.html", {})

def hx_menu_cart(request):
    return render(request, 'main/menu-cart.html')

def cart_page(request):
    quantity_range = list(range(1, 11))
    return render(request, 'main/cart-page.html', {"quantity_range": quantity_range})


def update_checkout(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.add(product_id, quantity)

    product = stripe.Product.retrieve(product_id)
    product_details = get_product_details(product)
    product_details['total_price'] = product_details['price'] * quantity

    response = render(request, 'main/partials/checkout-total.html', {'product': product_details})
    response['HX-Trigger'] = 'hx_menu_cart'
    return response

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_page')