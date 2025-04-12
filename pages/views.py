from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Order, OrderItem
from .forms import ContactForm, CheckoutForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.



def indexView(request):
    popular_product = Product.objects.filter(is_popular=True).order_by('-created_at')[:4]
    featured_product = Product.objects.filter(is_featured=True).order_by('-created_at')[:4]
    all_product = Product.objects.all().order_by('-created_at')[:4]

    context = {
        'popular_product':popular_product,
        'featured_product':featured_product,
        'all_product':all_product,

    }
    return render(request, 'pages/index.html', context)

def productView(request):
    product = Product.objects.all()

    context = {
        'product': product,
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

def cartView(request):
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

    return render(request, 'pages/cart.html', {
        'cart_items': cart_items,
        'total_cost': total_cost
    })


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
                session_id=request.session.session_key,  # Save the current session ID
                customer_name=form.cleaned_data['name'],
                customer_email=form.cleaned_data['email'],
                customer_address=form.cleaned_data['address'],
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
            send_order_email(form.cleaned_data, cart_items, total_cost)

            # Clear the cart from session
            request.session['cart'] = {}

            # Optionally, clear the entire session data if you want to remove the session ID as well
            request.session.flush()  # This deletes the session, including the session ID

            return redirect('product_list')  # Redirect to product list or a success page
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