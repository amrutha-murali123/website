from django.db import models
from django.utils.html import mark_safe

from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import *


STATUS = [
    ('in_review', _('In Review')),
    ('approved', _('Approved')),
    ('rejected', _('Rejected')),
]

RATING = [
    (1, "⭐☆☆☆☆"),
    (2, "⭐⭐☆☆☆"),
    (3, "⭐⭐⭐☆☆"),
    (4, "⭐⭐⭐⭐☆"),
    (5, "⭐⭐⭐⭐⭐"),
]




class Category(TranslatableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image=models.ImageField(upload_to="category/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    translations = TranslatedFields(
    title=models.CharField(max_length=100),
    )


    class Meta:
        verbose_name_plural="categories"#: This attribute allows you to specify the plural name of the model for use in the Django admin interface. In this case, it's set to "categories". So, in the admin interface, instead of seeing "Categorys" (the default pluralization), you will see "Categories"


    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))   # automatically append here i mean the imagefield
    

    def __str__(self):
        return self.title
    

class Tags(TranslatableModel):
    pass


class Product(TranslatableModel):  # Ensure TranslatableModel is imported and properly installed
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=2.99)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    cover_image = models.ImageField(upload_to='product_covrer_images/')
    imagesone=models.ImageField(null=True,upload_to="product-images/")
    imagestwo=models.ImageField(null=True,upload_to="product-images/")
    imagesthree=models.ImageField(null=True,upload_to="product-images/")
    imagesfour=models.ImageField(null=True,upload_to="product-images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    in_stock = models.IntegerField(default=0)

    translations = TranslatedFields(
        title=models.CharField(max_length=100, default=_("this is pear")),  
        description=RichTextUploadingField(null=True, blank=True, default=_("this is the product")),  
        Specifications=RichTextUploadingField(null=True, blank=True),
        product_status=models.CharField(choices=STATUS, max_length=10, default="in_review")
    )
 


    class Meta:
        verbose_name_plural="products"


    def product_cover_image(self):
        return mark_safe(f'<img src="{self.cover_image.url}" width="50" height="50" />')   # automatically append here i mean the imagefield
    


class Review(TranslatableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user=models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name="reviews")
    rating=models.FloatField(choices=RATING,default=None)
    translations = TranslatedFields(
    description= models.TextField(max_length=100,blank=True),
    

    )




    class Meta:
        verbose_name_plural="product reviews"


    

    def __str__(self):
        return self.product.title
    
    def get_reating(self):
        return self.rating   

class Wishlist(models.Model):
   id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='wishlist')
    
   def _str_(self):
      return self.id
   

class WishlistItem(models.Model):
   id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   wished_item=models.ForeignKey(Wishlist,on_delete=models.CASCADE,related_name='wishlistitems')
   product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

   def _str_(self):
        return str(self.id)
   
