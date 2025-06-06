from django.urls import path
from .views import *

urlpatterns = [
    path("", shop_view, name="shop"),
    path("product/<int:product_id>/", product_view, name="product"),
    path("payment_successful/", payment_successful, name='payment_successful'),
    path("payment_cancelled/", payment_cancelled, name="payment_cancelled")
]