from django.forms import ModelForm
from .models import Product, Category, Contact, Order



class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'subject', 'message']


        # widgets = {
        #     'full_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'message': forms.Textarea(attrs={'class': 'form-control'}),
        # }


class CheckoutForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_address', 'customer_city', 
                  'customer_state', 'customer_zip', 'customer_country', 'customer_phone', 
                  'customer_notes', 'payment_method']