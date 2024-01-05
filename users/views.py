from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from .email import *
from django.core.cache import cache

from django.views import View
import random
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from product.models import *
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import gettext as _


from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from product.models import Wishlist, WishlistItem
from product.models import *
from django.shortcuts import render, redirect
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from shoppingcart.models import *
from xhtml2pdf import pisa







   
class ProductListView(View):
   def get(self,request):
    sortoption=request.GET.get('sort')
    print(sortoption)
    
    if sortoption=='price_low':
        products=Product.objects.all().order_by('price')
    elif sortoption=='price_high':
       products=Product.objects.all().order_by('-price')
    elif sortoption=="new":
       products=Product.objects.all().order_by('created_at')
    else:
        products=Product.objects.all()

    context={
        "products":products
    }
    return render(request,'product-list.html',context)
   

   

class HomeView(View):
    """

    This is the homepage of project .this page tells about all categories 
    and overall information about the website.

    """
    
    def get(self, request):
        
        """

            Handles GET requests to display a list of products with specified categories.
    This view retrieves a list of products, each belonging to specific categories (e.g., 'Duffles', 'Backpack', 'Luggage Bags', 'Student Travel').
    The retrieved products are then passed to the template for rendering. 
      Caching:The context containing product information is cached using the key 'home_view_context' for 300 seconds (5 minutes).
      usage:This view is typically used to display a limited set of products from specific categories on a webpage.

      
        """
        

        # TODO:USE CACHE TO PASS CONTEXT,doc string # did*************
        # try:
        # products = Product.objects.all()[:4]
        categories=Category.objects.all().prefetch_related('products')[:4]# i did pre

        context = {
            # "products": products,
            # 'duffles_category':duffles_category,
            # 'backpack_category':backpack_category,
            # 'LuggageBags_category':LuggageBags_category,
            # 'StudentTravel_category':StudentTravel_category,
            'categories':categories,
            'hello':_('Hello'),
        }
    
        

        cache.set('home_view_context', context, 300)
        return render(request, 'home.html', context)




class CategoryProductListView(View):
    """
       View for displaying a list of products in a specific category.

    This view retrieves the category based on the provided title,
    and then fetches the associated products. It attempts to retrieve
    the data from cache first and falls back to the database if needed.

    """
    def get(self, request, category_title):
        """
         Handle GET requests.

    This method is responsible for processing GET requests. It retrieves
    the category based on the provided title, and then fetches the associated
    products. It first attempts to retrieve the data from cache, falling back
    to the database if needed. 

        """
        
        # Use get_object_or_404 to retrieve the category based on the title
        # try:
        # categories= get_object_or_404(Category, title=category_title)
        # category = get_object_or_404(Category.translations, title=category_title)
        category_title = get_object_or_404(Category.objects.translated(title=category_title))
        # except:
        #    return redirect('custom_404')

        # Filter products based on the category
        # Try to retrieve the data from the cache
        cache_key = f'category_product_list:{category_title}'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # If data is cached, use it
            context = cached_data

        else:
            # If not cached, fetch from database
            # Assume you want to filter products based on some condition,
            # for example, if the category is active
            is_active = True

            if is_active:
                products = Product.objects.filter(category=category_title).select_related('category')
               
            else:
                products = []  # Provide a default value or handle the case where no products are found

            context = {
                'category': Category,
                'products': products
            }
            # Cache the data for 300 seconds (5 minutes)
            cache.set(cache_key, context, 300)

        return render(request, 'category-product-list.html', context)



class SignupView(View):

    """

    View for user registration.    This view handles both GET and POST requests related to user registration.
    GET request renders the signup form, while POST request processes user registration.

    """

    def get(self, request):
        return render(request, 'signup.html')
    """

    Render the signup form.This method is triggered on a GET request to display the signup form.

    """

    def post(self, request):

        """
        Process user registration.This method is triggered on a POST request to process user registration.
        It validates the registration data, sends an OTP email, and stores the registration details in the cache

        """

        email = request.POST.get("email")
        name = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        try:
            userobj = UserProfile.objects.get(email=email)
            messages.warning(
                request, "You are already registered. Please login.")
            return redirect("login")
        except UserProfile.DoesNotExist:
            pass

        if pass1 != pass2:
            messages.warning(request, "Password does not match.")
            return redirect("register")

        otp = str(random.randint(100000, 999999))
        send_otp_email(email, name, otp)
        # key = hashlib.sha256(email.encode()).hexdigest()
        # cache.set(key, {'email': email, 'name': name,
        #                 'password': pass1, 'otp': otp}, timeout=600)
        
        request.session['signup_data'] = {'email': email, 'name': name,'password': pass1, 'otp': otp}

        return redirect("otp")



class VerifyOtpView(View):
    def get(self, request):
        # Render the OTP verification form
        signup_data =  request.session.get('signup_data',{})
        print(signup_data,"verify get")

        return render(request, "otp.html")

    def post(self, request):


        """
    Process the OTP and complete user registration.
    This method is triggered on a POST request to verify the OTP and complete user registration.
    It checks if the received OTP matches the one sent during registration.
    If the OTP is valid, it creates a new user, deletes the registration details from the cache, and redirects to the login page

        """

        receivedotp = request.POST.get("otp")
        # signup_data = cache.get(key)
        signup_data =  request.session.get('signup_data',{})
        print(signup_data,"verify")
        if not signup_data:
            messages.warning(request, 'OTP expired or invalid')
            return redirect('otp')
        otp = signup_data.get('otp')
        name = signup_data.get('name')
        email = signup_data.get('email')
        password = signup_data.get('password')
        if receivedotp != otp:
            messages.warning(request, "OTP mismatch")
            return redirect("otp")

        user = UserProfile.objects.create_user(
            username=name, email=email, password=password
        )
        user.save()
        # cache.delete(key)
        del request.session['signup_data']
        return redirect("login")    # locking mechanism refer

class ResendOTP(View):
  
  """
    This view is triggered when a user requests to resend the OTP during the registration process.
    It generates a new OTP, sends it to the user's email, and updates the cache with the new OTP.
    After that, it redirects to the OTP verification page.
    If there are no registration details in the cache, it redirects to the signup page.

  """
#   def get(self, request, key):
#     """
#     Handle GET requests for resending OTP.

#     """

#     signup_data = cache.get(key)
#     if signup_data:
#       email = signup_data.get('email')
#       name = signup_data.get('name')
#       otp = str(random.randint(100000, 999999))
#       print(otp)
#       send_otp_email(email, name, otp)
#       signup_data['otp'] = otp
#       existing_timeout = signup_data.get('timeout', None)
#       cache.set(key, signup_data, timeout=existing_timeout)
#       return redirect('otp', key=key)
#     return redirect('signup')
    
  # def get(self, request, key):


  def get(self, request):
    print("resend")
    # signup_data = cache.get(key)
    signup_data = request.session.get('signup_data',{})

    if signup_data:
        email = signup_data.get('email')
        name = signup_data.get('name')
        otp = str(random.randint(100000, 999999))
        account_verification_email(email, name, otp)
        signup_data['otp'] = otp
        print(signup_data,"resendotp")
      # existing_timeout = signup_data.get('timeout', None)
      # cache.set(key, signup_data, timeout=existing_timeout)
      # return redirect('user_verify_otp', key=key)            
        request.session['signup_data'] = signup_data

    
    return redirect("otp")
    # return redirect('register')
  


class ForgotPassword(View):
  
  """

    ForgotPassword view to handle password reset requests.
    This view is responsible for rendering the password reset form on GET requests.
    On POST requests, it checks if the provided email is associated with a registered user.
    If yes, it generates a password reset link, sends it to the user's email, and notifies the user.
    If no, it redirects to the registration page.
  
  
  """

  def get(self, request):

    """
     Handle GET requests for rendering the password reset form.
    
    """

    return render(request, 'password_forgot_form.html')
  
  def post(self, request):

    """
    Handle POST requests for processing password reset requests.

    """

    email=request.POST.get('email')
    try:
      user = UserProfile.objects.get(email=email)
    except:
      messages.warning(request , 'You are not registerd, Please sign up')
      return redirect('register')
    encrypt_id = urlsafe_base64_encode(str(user.pk).encode())
    reset_link = f"{request.scheme}://{request.get_host()}{reverse('reset', args=[encrypt_id])}"
    cache_key = f"reset_link_{encrypt_id}"
    cache.set(cache_key, {'reset_link':reset_link}, timeout=600) 
    reset_password_email(email, reset_link)
    messages.success(request, 'Password reset link sent to your email.')
    return redirect('login')

class UserResetPassword(View):
  

  """
    UserResetPassword view to handle resetting user passwords.
    This view is responsible for rendering the password reset form on GET requests.
    On POST requests, it checks if the reset link is valid, retrieves the user,
    updates the user's password, and notifies the user of a successful password reset.
  
  """
  
  
  
  def get(self, request, encrypt_id):

    """
    Handle GET requests for rendering the password reset form.
    """

    cache_key = f"reset_link_{encrypt_id}"
    cache_data = cache.get(cache_key)
    if not cache_data:
      raise Http404("Reset link has expired")
    reset_id = cache_data.get('reset_link')
    return render(request, 'password_reset.html',{'reset':reset_id})

  def post(self, request, encrypt_id):

    """
    Handle POST requests for processing password reset.

    """

    cache_key = f"reset_link_{encrypt_id}"
    id = str(urlsafe_base64_decode(encrypt_id), 'utf-8')
    user = UserProfile.objects.get(pk=id)
    new_password = request.POST.get('pass1')
    user.set_password(new_password)
    user.save()
    cache.delete(cache_key)
    messages.success(request, 'Password reset successful. You can now log in with your new password.')
    return redirect('login')

class LoginView(View):

    """
    LoginView class-based view for handling user login.
    This view is responsible for processing user login attempts.
    It authenticates the user using the provided credentials and logs the user in.
    On success, it redirects to the home page. On failure, it redirects back to the login page.

"""

    def post(self, request):

        """
         Handle POST requests for user login

        """

        name = request.POST.get("username")
        pass1 = request.POST.get("pass1")

        user = authenticate(request, username=name, password=pass1)
      
        if user is not None and not user.is_superuser:
            
            auth_login(request, user)
            messages.success(request, "Logged in Successfully ")
            return redirect("home")# userpassword incorrect wt to do
        else:
            return redirect("login")

    def get(self, request):

        """
        Handle GET requests for rendering the login form.

        """ 

        return render(request, "login.html")
  



class UserSignout(View):

  def get(self, request):
    logout(request)
    messages.success(request, "Logged in Successfully ")
    return redirect('login')
  
#TODO:handling 404, use cache,show original price in product detail html




class product_detail_view(View):

    """

        A class-based view for displaying details of a product.
        Instantiate this view and map it to a URL pattern in your Django project's
        urls.py file.



    """

    def get(self,request,id):

        """
           Handles HTTP GET requests to retrieve and display product details.

        """
        products=Product.objects.select_related('category').get(id=id) # i did  pre
              
      

        context= {
        "product":products,
       
        }
   
        return render(request,"product-detail.html",context)

    def post(self, request,id):

        """

        Handles HTTP POST requests to add a product to the user's shopping cart.
        Retrieves product information based on the specified ID.
        Parses the quantity and product ID from the POST data.
        If the user is authenticated:
        Retrieves or creates the user's shopping cart.
        Retrieves or creates a cart item for the specified product in the cart.
        Updates the cart item quantity based on user input.
        Displays success or error messages based on the quantity chosen.
        Redirects the user back to the previous page.  
        Integrate this method into your class-based view and map it to a URL pattern
        in your Django project's urls.py file.


        """

        product_id = request.POST.get('product_id')
        product_item = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        # Create or update the cart item with the selected product item
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, product=product_item)

            # If the cart item already exists, add the specified quantity to the existing quantity
            if not cart_item_created:
                if quantity < 5:
                    cart_item.quantity += quantity
                    messages.success(request, "Added to cart")
                else:
                    messages.error(request, 'Choose quantity less than 5')
            else:
                if quantity < 5:
                    cart_item.quantity = quantity  # Set the quantity to the desired value
                    messages.success(request, "Added to cart")
                else:
                    messages.error(request, 'Choose quantity less than 5')

            cart_item.save()

        return redirect(request.META.get('HTTP_REFERER'))







class SubmitReviewView(View):
    def post(self, request, product_id):

        """
        Handles HTTP POST requests to submit a review for a product.
        Integrate this method into your class-based view and map it to a URL pattern
        in your Django project's urls.py file.

        """

        product = get_object_or_404(Product.objects.select_related('category'), id=product_id)# i did
        user = request.user

        # Check if the user has ordered the product
        user_has_ordered_product = OrderItem.objects.filter(order__user=user, product=product).exists()


        if not user_has_ordered_product:
            messages.error(request, 'You must order this product to leave a review.')
        else:
            existing_review = Review.objects.filter(user=user, product=product).exists()
            if existing_review:
                messages.error(request, 'You can only add one review per product.')
            else:
                content = request.POST.get('review')
                rating = request.POST.get('rating')  # Get the selected rating from the form
                review = Review.objects.create(user=user,product=product, description=content, rating=rating)
                review.save()
                messages.success(request, 'Review added successfully.')

        return redirect(request.META.get('HTTP_REFERER'))




class Custom404View(View):

    """
    Integrate this view into your Django project's urls.py file to handle 404 errors
    and display a custom error page. 

    """

    def get(self, request, *args, **kwargs):

        """
        Integrate this view into your Django project's urls.py file and map it to
        a URL pattern to handle 404 errors and display a custom error page.

        """

        try:
            # Code that may raise an exception
            raise Http404("Page not found")

        except Http404 as e:
            # Handle the Http404 exception
            return render(request, '404.html', status=404)
        
# @login_required
class AddToWishlistView(View):
    """
    Integrate this view into your Django project's urls.py file to handle adding
    products to the user's wishlist.

    """

    def post(self, request, product_id):

        """
        Integrate this method into your class-based view and map it to a URL pattern
        in your Django project's urls.py file.

        """

        if request.user.is_authenticated:
            try:
                product = get_object_or_404(Product.objects.select_related('category'), pk=product_id)# i did pre
                wishlist, created = Wishlist.objects.get_or_create(user=request.user)
                wishlistitem, created = WishlistItem.objects.get_or_create(wished_item=wishlist, product=product)
              
                messages.success(request, "Added to wishlist")
                return redirect(request.META.get('HTTP_REFERER'))
            except ValueError:
                return HttpResponseBadRequest("Invalid UUID")
        else:
            return redirect('login')


class WishlistView(LoginRequiredMixin, View):

    """
    Integrate this view into your Django project's urls.py file to handle
    displaying the user's wishlist.

    """

    def get(self, request):

        """
        Integrate this method into your class-based view and map it to a URL pattern
        in your Django project's urls.py file.

        """
        
        user_wishlist,created = Wishlist.objects.get_or_create(user=request.user)
        
        
        wishlist_items = WishlistItem.objects.filter(wished_item=user_wishlist).select_related('product__category')# i did pre
        print(wishlist_items,"hy")

        
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
        





class RemoveFromWishlistView(View):

    """
        Integrate this view into your Django project's urls.py file to handle
        removing products from the user's wishlist.

    """
    def post(self, request, product_id):

        """

            Integrate this method into your class-based view and map it to a URL pattern
            in your Django project's urls.py file.
        
        """
        if request.user.is_authenticated:
            product = get_object_or_404(Product.objects.select_related('category'), pk=product_id)# i did pre
            wishlistitem = WishlistItem.objects.select_related('product__category').get(product=product,wished_item__user=request.user)# i did pre

            wishlistitem.delete()
            messages.success(request, "Item removed")
              # Remove the product from the wishlist
            return redirect('wishlist')
        else:
            # Handle the case when the user is not authenticated, e.g., redirect to a login page.
            return redirect('login')


class UserInvoice(View):
  def get(self, request, id):
    template_name = 'invoice.html'
    order = request.user.order.get(id=id)
    context = {'order':order}
    html_content = render_to_string(template_name, context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response,encoding='utf-8')
    if pisa_status:
      return response
    return None

def charts(request):
    return render(request,"charts.html")


def dashboard(request):
    return render(request,"dashboard.html")

def user_profile(request):
    return render(request,'userprofile.html')

