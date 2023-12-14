# yourapp/context_processors.py
from django.shortcuts import redirect
from shoppingcart.models import CartItem  # Import your CartItem model

def cart_item_count(request):
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(cart__user=request.user).count()
    else:
        cart_item_count = 0
    print(cart_item_count)

    return {'cart_item_count': cart_item_count}
from product.models import Wishlist,WishlistItem# Import your WishlistItem model

# context_processors.py

def wishlist_item_count(request):
    if request.user.is_authenticated:
        wishlist_items_count = WishlistItem.objects.filter(wished_item__user=request.user).count()
    else:
        wishlist_items_count = 0

    return {'wishlist_items_count': wishlist_items_count}




