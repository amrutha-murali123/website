
from django.shortcuts import get_object_or_404, redirect,render
from .models import Cart, CartItem,Address,Order, OrderItem
from product.models import Product
from django.contrib import messages
from .forms import AddressForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views import View
from django.conf import settings
import razorpay
from decimal import Decimal
from .tasks import send_order_confirmation_email
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from shoppingcart import models






def update_cart_item_quantity(request, item_id):
    """
    Update the quantity of a specific item in the user's shopping cart.
    This typically called when a user modifies the quantity of an item in their shopping cart.
    It retrieves the CartItem using the provided item_id, updates the quantity with the new value from the POST request,
    and then redirects the user to the 'view_cart' page to see the updated cart.

    """
    cart_item = get_object_or_404(CartItem, id=item_id)
    new_quantity = request.POST.get('quantity')
    cart_item.quantity = new_quantity
    cart_item.save()
    return redirect('view_cart')

def cart_view(request):


    """
        Display the contents of the user's shopping cart.

    Retrieves the user's cart and associated cart items from the database,
    then renders the 'cart.html' template with the cart items and cart object.
    
    """
    if request.method == 'POST':
        # Iterate through the form data to update quantities
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
               
                item_id = int(key.split('_')[1])
                print(item_id)
                quantity = int(value)
                cart_item = CartItem.objects.get(id=item_id)
                cart_item.quantity = quantity
                cart_item.save()

        messages.success(request, 'Cart updated successfully')
        return redirect('shoppingcart:cart')

    
    user_cart = Cart.objects.filter(user=request.user).first()
   
    cart_items = CartItem.objects.filter(cart=user_cart)
    
    return render(request, 'cart.html', {'cartitem': cart_items,'cart':user_cart})




def remove_cart(request, product_id):

    """
     Remove a product from the user's shopping cart.

    If the user is authenticated, the function retrieves the specified product
    from the database and attempts to remove its corresponding cart item from
    the user's cart. If successful, a success message is displayed, and the user
    is redirected to the previous page.
    
    """

    if request.user.is_authenticated:
        product_item = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product=product_item).first()

        if cart_item:
            messages.success(request, "Removed from cart")
            cart_item.delete()

    return redirect(request.META.get('HTTP_REFERER'))
    


 
class CheckoutView(View):

    """

        View for handling the checkout process.

    This class-based view handles both the GET and POST requests for the checkout process.
    In the GET request, it retrieves the user's cart, cart items, addresses, and generates
    a Razorpay payment order for the transaction. In the POST request, it processes the
    submitted payment information, creates an order, and sends an order confirmation email.

    """

    template_name = 'checkout.html'

    def get(self, request, *args, **kwargs):

        """
            Handle the GET request for rendering the checkout page.

    If the user is not authenticated, redirect them to the login page.
    Retrieve the user's cart, cart items, and addresses for display on the checkout page.
    Update the cart total and generate a Razorpay payment order for the transaction.
    Render the 'checkout.html' template with the necessary context.

        
        """

        user = request.user

        if not user.is_authenticated:
            return redirect('login.html')

        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        addresses = Address.objects.filter(user=user).order_by('-created_at')[:4]
        cart.update_total()
        cart_total_float = float(cart.total)
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET))
        payment_order = client.order.create(dict(amount = cart_total_float*100, currency = "INR", payment_capture = 1))
        payment_order_id = payment_order['id']
      
        context = {
            "cart": cart,
            "cart_items": cart_items,
            "addresses": addresses,
            "payment_api_key":settings.RAZORPAY_API_KEY,
            "order_id":payment_order_id,
        }
      
        return render(request, self.template_name, context)
    

    def post(self,request):


        """
        
            Handle the POST request for processing payment and creating an order.

    Process the submitted payment information, create an order, and send an order
    confirmation email to the user. Display a success message and render the 'order.html'
    template with the order details.
        
        """


        

        selected_address_id = request.POST.get('selectedAddress')
        selected_payment_method = request.POST.get('payment_method')
       

        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = cart.total 
        selected_address=Address.objects.get(id=selected_address_id)
        
        if selected_address_id and cart and cart_items and selected_payment_method:

            order = Order.objects.create(
                        user=user,
                        total_price=total_amount,
                        shipping_address=selected_address,
                        payment_mode=selected_payment_method,


            )
            messages.success(request, 'Order placed successfully!')
            
        
            for items in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=items.product,
                    quantity=items.quantity,
                    price=items.product.price,
                    # status='processing'

                )
            

            send_order_confirmation_email(order.id, user.email)

            print("faypay",user.email,order.id)
            context= {
                    "order":order,
                    "address":selected_address,
                     
                }

            return render(request,"order.html",context)
            
        

class AddAddressView(FormView):
    
    """
        View for adding a new address during the checkout process.

    This class-based view extends the FormView class to handle the rendering
    of the 'add_address.html' template and the form submission for adding a new address.
    
    """

    template_name = 'add_address.html'
    form_class = AddressForm  
    success_url = reverse_lazy('shoppingcart:checkout')

    def form_valid(self, form):
        
        """
         Process the form submission when the form is valid.

         Associate the address with the authenticated user and save the address to the database.
        
        """
        
        user = self.request.user
        address = form.save(commit=False)
        address.user = user
        address.save()
        return super().form_valid(form)

@login_required
def order_history(request):
    
    """

       Display the order history for the authenticated user.

    Retrieves the orders associated with the authenticated user from the database,
    ordered by their creation timestamp, and renders the 'order_history.html' template
    with the user's order history.


    """

    user_orders = Order.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'order_history.html', {'user_orders': user_orders})

def order_detail(request, order_id):
    
    """

       Display the details of a specific order for the authenticated user.

    Retrieves the specified order from the database based on the provided order ID
    and the authenticated user. If the order is not found, a 404 response is returned.
    Renders the 'order_detail.html' template with the details of the selected order.
    
    """

    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

def add_address(request):
    return render(request,"add_address.html")
     





