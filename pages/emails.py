from django.core.mail import EmailMessage
from django.conf import settings

def send_order_emails(context, cart_items, total_cost):
    try:
        # Generate the HTML email inline
        cart_html = ""
        for item in cart_items:
            cart_html += f"<li>{item['product'].name} × {item['quantity']} — ${item['total_price']}</li>"

        email_body = f"""
            Order Summary
            Name: {context['customer_name']}
            Email: {context['customer_email']}
            Phone: {context['customer_phone']}
            Address: {context['customer_address']}, {context['customer_city']}, {context['customer_state']}, {context['customer_country']}
            Notes: {context.get('customer_notes', 'N/A')}
            Cart Items:
            {cart_html}
            Total: ${total_cost}
        """

        admin_email = settings.ADMIN_EMAIL

        # Log the email details to the console for now
        print("=== Email to Admin ===")
        print(f"Subject: New Order Received")
        print(f"Body: {email_body}")
        print(f"To: {admin_email}")

        print("\n=== Email to Customer ===")
        print(f"Subject: Your Order Confirmation")
        print(f"Body: {email_body}")
        print(f"To: {context['customer_email']}")

        # Uncomment these lines to send the emails
        # EmailMessage(
        #     subject='New Order Received',
        #     body=email_body,
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     to=[admin_email],
        #     headers={'Reply-To': context['customer_email']},
        # ).send()

        # EmailMessage(
        #     subject='Your Order Confirmation',
        #     body=email_body,
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     to=[context['customer_email']],
        # ).send()

    except Exception as e:
        print(f"Error in send_order_emails: {e}")