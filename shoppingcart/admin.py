from django.contrib import admin
from .models import *


class cartAdmin(admin.ModelAdmin):
    list_display=['id',"user"]

# admin.site.register(Product,ProductAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display=['id',"quantity"]

class OrderAdmin(admin.ModelAdmin):
    list_display=['id']

class OrderItemAdmin(admin.ModelAdmin):
    list_display=['id','quantity','price','order']


admin.site.register(Address)
admin.site.register(Cart,cartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)