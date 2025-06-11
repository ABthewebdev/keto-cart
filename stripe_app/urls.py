from django.urls import path
from .views import *

urlpatterns = [
    path("", shop_view, name="shop"),
    path("product/<product_id>/", product_view, name="product"),
    path("payment_successful/", payment_successful, name='payment_successful'),
    path("payment_cancelled/", payment_cancelled, name="payment_cancelled"),
    path('add_to_cart/<product_id>', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout_view, name='checkout')
]