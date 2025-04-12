import pprint

def cart_count(request):
    cart = request.session.get('cart', {})
    pprint.pprint(cart)
    count = sum(cart.values())  
    return {'cart_count': count}
