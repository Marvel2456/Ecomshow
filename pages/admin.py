from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['name']
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_popular', 'is_most_profitable', 'is_top_rated', 'is_featured']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'is_popular', 'is_most_profitable', 'is_top_rated', 'is_featured']
    ordering = ['name']
    list_per_page = 10
    list_editable = ['is_popular', 'is_most_profitable', 'is_top_rated', 'is_featured']

@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'message', 'created_at']
    search_fields = ['full_name', 'email', 'subject']
    list_filter = ['created_at']
    ordering = ['created_at']
    list_per_page = 10

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['session_id', 'customer_name', 'customer_email', 'customer_address', 'total_cost', 'status', 'created_at']
    search_fields = ['session_id', 'customer_name', 'customer_email']
    list_filter = ['status', 'created_at']
    ordering = ['created_at']
    list_per_page = 10
    
@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'total_price']
    search_fields = ['order__session_id', 'product__name']
    list_filter = ['order__status']
    ordering = ['order__created_at']
    list_per_page = 10


@admin.register(WalletAdress)
class WalletAdressAdmin(ModelAdmin):
    list_display = ['address', 'name', 'created_at']
    search_fields = ['address', 'name']
    list_filter = ['created_at']
    ordering = ['created_at']
    list_per_page = 10