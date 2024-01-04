from django.urls import path
from . import views







urlpatterns=[
    path('register/',views.SignupView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('verify/',views.VerifyOtpView.as_view(),name='otp'),
    path('',views.HomeView.as_view(),name='home'),
    path('resend_otp/', views.ResendOTP.as_view(), name='resend_otp'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot'),
    path('rreset_password/<str:encrypt_id>/',views.UserResetPassword.as_view(),name='reset'),
    path('signout/',views.UserSignout.as_view(),name='signout'),
    path('product/',views.ProductListView.as_view(),name='product_list'),
    path('product/<str:id>/',views.product_detail_view.as_view(),name='product_detail'),
    path('category/<str:category_title>/',views.CategoryProductListView.as_view(), name='category_product_list'),
    path('custom_404/', views.Custom404View.as_view(),name='custom_404'),
    path('submit_review/<str:product_id>/',views.SubmitReviewView.as_view(), name='submit_review'),
    path('add_to_wishlist/<uuid:product_id>/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('remove_from_wishlist/<uuid:product_id>/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    path('charts/', views.charts, name='charts'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('invoice/<str:id>/', views.UserInvoice.as_view(), name='invoice'),
    
    
]
  


    
     
 
  
    






