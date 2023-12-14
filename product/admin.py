from django.contrib import admin
# from django.utils.html import format_html
from product.models import *
from parler.admin import TranslatableAdmin
# from parler.admin import TranslatableTabularInline


class ProductAdmin(TranslatableAdmin):
    list_display = ['title', 'product_cover_image', 'price', 'category', 'id']

class CategoryAdmin(TranslatableAdmin):
    list_display=['title','category_image','id']

# class CartAdmin(TranslatableAdmin):
#     list_display=['price']

# class CartItemAdmin(TranslatableAdmin):
#     list_display=['image','price','total']   

# class ReviewAdmin(TranslatableAdmin):
#     list_display=['product','rating'] 

# class WishlistAdmin(admin.ModelAdmin):
#     list_display = [ 'user']

# class WishlistItemAdmin(admin.ModelAdmin):
#     list_display = [ 'wished_item','product']

class AddressAdmin(TranslatableAdmin):
    list_display=['user','address'] 

admin.site.register(Category,CategoryAdmin)
# admin.site.register(Cart,CartAdmin)
# admin.site.register(CartItem,CartItemAdmin)
# admin.site.register(Review,ReviewAdmin)
admin.site.register(Product,ProductAdmin)
# admin.site.register(Wishlist,WishlistAdmin)
# admin.site.register(WishlistItem,WishlistItemAdmin)

from django.contrib import admin
from django.contrib.auth.models import Group

class CustomGroupAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        # Disable the "Groups" module in the admin interface
        return False

# Unregister the default Group admin and register the custom admin
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)




