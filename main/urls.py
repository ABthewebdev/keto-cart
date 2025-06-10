from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path('hx_menu_cart/', hx_menu_cart, name="hx_menu_cart"),
    path('cart_page/', cart_page, name="cart_page"),
    path('update_checkout/<product_id>', update_checkout, name="update_checkout"),
    path('remove_from_checkout/<product_id>', remove_from_cart, name='remove_from_cart')
]