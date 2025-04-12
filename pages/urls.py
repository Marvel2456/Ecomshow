from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('products/', views.productView, name='products'),
    path('contact/', views.contactView, name='contact'),
    path('product_detail/<uuid:pk>/', views.productDetailView, name='product_detail'),
    # path('add-to-cart/<uuid:pk>/', views.addToCartView, name='add_to_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cartView, name='cart'),
    path('checkout/', views.checkoutView, name='checkout'),
]