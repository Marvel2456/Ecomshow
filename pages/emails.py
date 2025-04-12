from django.core.mail import send_mail
from django.conf import settings

def send_order_email(form_data, cart_items, total_cost):
    body = f"New Order:\n\n"
    for item in cart_items:
        body += f"{item['product'].name} x {item['quantity']} = {item['total_price']}\n"
    body += f"\nTotal: {total_cost}\n\n"
    body += f"Customer Info:\n{form_data['name']}\n{form_data['email']}\n{form_data['address']}"

    send_mail(
        subject='New Order Received',
        message=body,
        from_email=form_data['email'],
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )
