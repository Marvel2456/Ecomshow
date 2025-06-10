# import pprint
# from pages.models import Product

# def cart_count(request):
#     cart = request.session.get('cart', {})
#     pprint.pprint(cart)
#     count = sum(cart.values())  
#     return {'cart_count': count}



# def cart_items(request):
#     cart = request.session.get('cart', {})
#     items = []

#     for product_id, quantity in cart.items():
#         try:
#             product = Product.objects.get(id=product_id)
#             items.append({
#                 'product': product,
#                 'quantity': quantity,
#                 'total_price': product.price * quantity
#             })
#         except Product.DoesNotExist:
#             continue

#     total = sum(item['total_price'] for item in items)

#     return {
#         'cart_items': items,
#         'cart_total': total,
#         'cart_count': sum(cart.values()),
#     }


# import pprint
# from pages.models import Product

# def cart_processor(request):
#     """
#     Single context processor to handle all cart-related data
#     """
#     cart = request.session.get('cart', {})
#     items = []
    
#     # Debug print initial cart data
#     pprint.pprint({
#         'function': 'cart_processor',
#         'initial_cart_data': cart
#     })
    
#     # Get cart items and calculate totals
#     for product_id, quantity in cart.items():
#         try:
#             product = Product.objects.get(id=product_id)
#             items.append({
#                 'product': product,
#                 'quantity': quantity,
#                 'total_price': product.price * quantity
#             })
#         except Product.DoesNotExist:
#             continue

#     # Calculate totals
#     total = sum(item['total_price'] for item in items)
#     count = sum(cart.values())

#     # Debug print processed cart data
#     pprint.pprint({
#         'function': 'cart_processor',
#         'processed_items': [
#             {
#                 'product_name': item['product'].name,
#                 'quantity': item['quantity'],
#                 'total_price': item['total_price']
#             } for item in items
#         ],
#         'cart_total': total,
#         'cart_count': count
#     })

#     return {
#         'cart_items': items,
#         'cart_total': total,
#         'cart_count': count,
#     }

import pprint
from pages.models import Product
import uuid
from django.core.exceptions import ValidationError

def cart_processor(request):
    """
    Single context processor to handle all cart-related data
    """
    cart = request.session.get('cart', {})
    items = []
    valid_cart = {}
    
    # Debug print initial cart data
    pprint.pprint({
        'function': 'cart_processor',
        'initial_cart_data': cart
    })
    
    # Clean and validate cart items
    for product_id, quantity in cart.items():
        # Skip invalid entries
        if product_id == 'null' or not product_id:
            continue
            
        try:
            # Validate UUID
            uuid_obj = uuid.UUID(str(product_id))
            product = Product.objects.get(id=uuid_obj)
            
            items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            })
            valid_cart[str(product_id)] = quantity
            
        except (ValueError, ValidationError, Product.DoesNotExist):
            # Skip invalid UUIDs or non-existent products
            continue

    # Update session if cart was cleaned
    if valid_cart != cart:
        request.session['cart'] = valid_cart
        request.session.modified = True

    # Calculate totals
    total = sum(item['total_price'] for item in items)
    count = sum(valid_cart.values())

    # Debug print processed cart data
    pprint.pprint({
        'function': 'cart_processor',
        'cleaned_cart': valid_cart,
        'processed_items': [
            {
                'product_name': item['product'].name,
                'quantity': item['quantity'],
                'total_price': item['total_price']
            } for item in items
        ],
        'cart_total': total,
        'cart_count': count
    })

    return {
        'cart_items': items,
        'cart_total': total,
        'cart_count': count,
    }