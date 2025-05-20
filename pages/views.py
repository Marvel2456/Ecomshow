from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Order, OrderItem, WalletAdress
from .forms import ContactForm, CheckoutForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest
from .utils import get_bitcoin_conversion_rate, get_ethereum_conversion_rate
from django.core.paginator import Paginator
from django.db.models import Count, Min, Max
# from .emails import send_order_emails
# Create your views here.



def indexView(request):
    popular_product = Product.objects.filter(is_popular=True).order_by('-created_at')[:5]
    featured_product = Product.objects.filter(is_featured=True).order_by('-created_at')[:5]
    all_product = Product.objects.all().order_by('-created_at')[:5]

    context = {
        'popular_product':popular_product,
        'featured_product':featured_product,
        'all_product':all_product,

    }
    return render(request, 'pages/index.html', context)

def productView(request):
    category_id = request.GET.get('category')
    sortby = request.GET.get('sortby', '')
    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)

    if sortby == 'popularity':
        products = products.filter(is_popular=True)
    elif sortby == 'featured':
        products = products.filter(is_featured=True)
    elif sortby == 'rating':
        products = products.filter(is_top_rated=True)
    elif sortby == 'date':
        products = products.order_by('-created_at')
    elif sortby == 'all':
        products = products.all()

    paginator = Paginator(products, 6)

    page_number = request.GET.get('page') 
    product = paginator.get_page(page_number)

    categories = Category.objects.annotate(product_count=Count('product'))

    price_range = products.aggregate(min_price=Min('price'), max_price=Max('price'))

    context = {
        'product': product,
        'categories': categories,
        'min_price': price_range['min_price'],
        'max_price': price_range['max_price'],
        'selected_category': category_id,
        'selected_sortby': sortby,
    }
    return render(request, 'pages/products.html', context)

def productDetailView(request, pk):
    product = Product.objects.get(id=pk)
    category = Category.objects.all()
    context = {
        'product': product,
        'category': category,
    }
    return render(request, 'pages/product_detail.html', context)

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session['cart'] = cart

        cart_count = sum(cart.values())

        html = render_to_string("partials/cart_count.html", {'cart_count': cart_count})
        return HttpResponse(html)
        # response['HX-Redirect'] = request.path
        # return response


def cartView(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    subtotal = 0

    for product in products:
        quantity = int(cart.get(str(product.id), 0))
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    total_cost = sum(item['subtotal'] for item in cart_items)

    return render(request, 'pages/cart.html', {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'subtotal': subtotal
    })


def update_cart_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            quantity = 1

        cart = request.session.get('cart', {})
        if quantity < 1:
            cart.pop(product_id, None)
        else:
            cart[product_id] = quantity
        request.session['cart'] = cart

        return redirect('cart')  # Redirect to cart page after update

    return redirect('cart')

def remove_from_cart(request):
    if request.method == 'POST' and request.headers.get('Hx-Request') == 'true':
        product_id = request.POST.get('product_id')

        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart

        # Send empty row or removal signal
        return HttpResponse(status=204)  # triggers row removal in HTMX
    return HttpResponseBadRequest("Invalid request")


def check_payment_method(request):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        wallet_address = WalletAdress.objects.first()
        if not wallet_address:
            return HttpResponseBadRequest("No wallet address found.")

        if payment_method == "bitcoin":
            crypto_address = wallet_address.btc_address
            conversion_rate = get_bitcoin_conversion_rate()
            crypto_name = "Bitcoin"
        elif payment_method == "ethereum":
            crypto_address = wallet_address.eth_address
            conversion_rate = get_ethereum_conversion_rate()
            crypto_name = "Ethereum"
        else:
            return HttpResponseBadRequest("Invalid payment method.")

        if not conversion_rate:
            return HttpResponseBadRequest(f"Unable to fetch {crypto_name} conversion rate.")

        # Calculate total price in the selected cryptocurrency
        total_cost = request.POST.get("total_cost", 0)
        total_cost_in_crypto = float(total_cost) / conversion_rate

        # Render the modal with the cryptocurrency price
        html = render_to_string("pages/bitcoin_modal.html", {
            "crypto_name": crypto_name,
            "crypto_address": crypto_address,
            "total_cost_in_crypto": round(total_cost_in_crypto, 8),
        })
        return HttpResponse(html)
    return HttpResponse("<script>document.querySelector('form').submit();</script>")




def checkoutView(request):
    # Get cart from session
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    for product in products:
        quantity = cart[str(product.id)]
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity,
        })

    total_cost = sum(item['total_price'] for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create an Order in DB using session_id
            order = Order.objects.create(
                session_id=request.session.session_key,
                customer_name=form.cleaned_data['customer_name'],
                customer_email=form.cleaned_data['customer_email'],
                customer_address=form.cleaned_data['customer_address'],
                customer_city=form.cleaned_data['customer_city'],
                customer_state=form.cleaned_data['customer_state'],
                customer_zip=form.cleaned_data['customer_zip'],
                customer_country=form.cleaned_data['customer_country'],
                customer_phone=form.cleaned_data['customer_phone'],
                customer_notes=form.cleaned_data['customer_notes'],
                payment_method=form.cleaned_data['payment_method'],
                total_cost=total_cost,
            )

            # Create OrderItems for each product in the cart
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    total_price=item['total_price'],
                )

            # Send email to admin with the order details
            # send_order_emails form.cleaned_data, cart_items, total_cost

            # Clear the cart from session
            request.session['cart'] = {}
            request.session.modified = True


            response = HttpResponse(status=200)
            response['HX-Redirect'] = '/products'
            return response
    else:
        form = CheckoutForm()

    return render(request, 'pages/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_cost': total_cost
    })


def contactView(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    return render(request, 'pages/contact.html')


def deliveryReturnView(request):
    return render(request, 'pages/delivery.html')