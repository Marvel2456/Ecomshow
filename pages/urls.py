from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('products/', views.productView, name='products'),
    path('contact/', views.contactView, name='contact'),
    path('product_detail/<uuid:pk>/', views.productDetailView, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cartView, name='cart'),
    path('update-cart/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('check-payment-method/', views.check_payment_method, name='check_payment_method'),
    path('checkout/', views.checkoutView, name='checkout'),
]