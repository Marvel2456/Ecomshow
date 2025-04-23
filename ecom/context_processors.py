import pprint
from pages.models import Product

def cart_count(request):
    cart = request.session.get('cart', {})
    pprint.pprint(cart)
    count = sum(cart.values())  
    return {'cart_count': count}



def cart_items(request):
    cart = request.session.get('cart', {})
    items = []

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            })
        except Product.DoesNotExist:
            continue

    total = sum(item['total_price'] for item in items)

    return {
        'cart_items': items,
        'cart_total': total,
        'cart_count': sum(cart.values()),
    }
