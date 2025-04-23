from django.core.mail import EmailMessage
from django.conf import settings

def send_order_emails(context, user_email):
    # Generate the HTML email inline
    cart_html = ""
    for item in context['cart_items']:
        cart_html += f"<li>{item['product'].name} × {item['quantity']} — ${item['subtotal']}</li>"

    email_body = f"""
        <h2>Order Summary</h2>
        <p><strong>Name:</strong> {context['first_name']} {context['last_name']}</p>
        <p><strong>Email:</strong> {context['email']}</p>
        <p><strong>Phone:</strong> {context['phone']}</p>
        <p><strong>Address:</strong> {context['address']}, {context['city']}</p>
        <p><strong>Notes:</strong> {context['notes']}</p>
        <p><strong>Proof of Payment:</strong> {'Provided' if context['proof_provided'] else 'Not Provided'}</p>
        <h3>Cart Items:</h3>
        <ul>{cart_html}</ul>
        <p><strong>Total:</strong> ${context['total_cost']}</p>
    """

    admin_email = settings.ADMIN_EMAIL

    # Send to admin
    EmailMessage(
        subject='New Order Received',
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[admin_email],
        headers={'Reply-To': context['email']},
    ).send()

    # Send to customer
    EmailMessage(
        subject='Your Order Confirmation',
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
    ).send()