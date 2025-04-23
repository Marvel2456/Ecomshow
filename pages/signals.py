from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .emails import send_order_emails

@receiver(post_save, sender=Order)
def send_order_email_after_order_creation(sender, instance, created, **kwargs):
    if created:
        # Prepare the email context
        cart_items = instance.items.all()
        context = {
            'customer_name': instance.customer_name,
            'customer_email': instance.customer_email,
            'customer_phone': instance.customer_phone,
            'customer_address': instance.customer_address,
            'customer_city': instance.customer_city,
            'customer_state': instance.customer_state,
            'customer_country': instance.customer_country,
            'customer_notes': instance.customer_notes,
        }
        total_cost = instance.total_cost

        # Send the email
        send_order_emails(context, cart_items, total_cost)