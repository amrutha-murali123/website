from .views import *
from django.urls import path


app_name = 'shoppingcart'

urlpatterns=[
 
    path('remove_from_cart/<str:product_id>/', remove_cart, name='remove_cart'),
    path('update_cart_item_quantity/<int:item_id>/', update_cart_item_quantity, name='update_cart_item_quantity'),
    path('cart/', cart_view, name='cart'),
    path('checkout/',CheckoutView.as_view(), name='checkout'),
    path('add_address/',AddAddressView.as_view(), name='add_address'),
    path('order_history/', order_history, name='order_history'),
    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),
    
]

    
    


