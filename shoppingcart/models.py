import uuid
from django.db import models
from users.models import UserProfile
from product.models import Product



class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def update_total(self):
        cart_items = self.cart.all()
        cart_total = sum(item.total for item in cart_items)
        self.total = cart_total
        self.save()



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="cart")
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,null=True,related_name='cart_item')
    total=models.DecimalField(max_digits=8,decimal_places=2,default=0)

    def save(self, *args, **kwargs):
        # Check if the product is not None before calculating the total
        if self.product is not None:
            self.total = self.quantity * self.product.price
        else: 
            self.total=0
        super().save(*args, **kwargs)
        self.cart.update_total()


    def __str__(self):
        return f"{self.product.title} ({self.quantity})"



class Order(models.Model):
    STATUS_CHOICES = (
        ('Placed', 'Placed'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )
    # product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    # quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='order',null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,default='Placed',null=True)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    payment_mode=models.CharField(max_length=100,null=True)


    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    status_choices=[('processing', 'Processing'),
            ('shipped', 'Shipped'), 
            ('delivered', 'Delivered')]   
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True,related_name="orderitem")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)
    # line_total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    # status = models.CharField(max_length=100, choices=status_choices, default='processing',null=True)

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='address')
    name = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=20,null=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f" {self.name}  {self.street_address}"
    
    




