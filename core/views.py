from django.shortcuts import render
from .models import Product, Order, OrderItem
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import json
import iyzipay

def pcb_service(request):
    return render(request, 'core/pcb_service.html')
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'core/product_detail.html', {'product': product})
def home(request):
    return render(request, 'core/home.html')

def services(request):
    return render(request, 'core/services.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'core/products.html', {'products': products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        product.total_price = product.price * quantity
        product.quantity = quantity

        total += product.total_price
        products.append(product)

    return render(request, 'core/cart.html', {
        'products': products,
        'total': total
    })

def increase_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] -= 1

        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')

def checkout(request):
    cart = request.session.get('cart', {})

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        total = 0
        products = []

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total += product.price * quantity
            products.append((product, quantity))

        # ORDER oluştur
        order = Order.objects.create(
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=total,
        )

        # ORDER ITEMS
        for product, quantity in products:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        # sepeti temizle
        request.session['cart'] = {}

        return redirect('payment', order_id=order.id)

    return render(request, 'core/checkout.html')

def payment(request, order_id):
    order = Order.objects.get(id=order_id)

    options = {
        'api_key': settings.IYZICO_API_KEY,
        'secret_key': settings.IYZICO_SECRET_KEY,
        'base_url': settings.IYZICO_BASE_URL
    }

    request_iyzi = {
        'locale' : 'tr',
        'conversationId': str(order.id),
        'price': str(order.total_price),
        'paidPrice': str(order.total_price),
        'currency': 'TRY',
        'basketId': str(order.id),
        'paymentGroup': 'PRODUCT',
        'callbackUrl': 'http://127.0.0.1:8000/payment-callback/',
        'buyer': {
            'id': 'BY789',
            'name': order.full_name,
            'surname': 'User',
            'gsmNumber': order.phone,
            'email': 'test@test.com',
            'identityNumber': '11111111111',
            'lastLoginDate': '2020-10-05 12:43:35',
            'registrationDate': '2020-10-05 12:43:35',
            'registrationAddress': order.address,
            'ip': '85.34.78.112',
            'city': 'Istanbul',
            'country': 'Turkey',
            'zipCode': '34732'
        },
        'shippingAddress': {
            'contactName': order.full_name,
            'city': 'Istanbul',
            'country': 'Turkey',
            'address': order.address,
            'zipCode': '34732'
        },
        'billingAddress':{
            'contactName': order.full_name,
            'city': 'Istanbul',
            'country': 'Turkey',
            'address': order.address,
            'zipCode': '34732'
        },
        'basketItems':[]
    }

    # ürünleri ekle
    for item in order.orderitem_set.all():
        request_iyzi['basketItems'].append({
            'id': str(item.product.id),
            'name': item.product.name,
            'category1': 'General',
            'itemType': 'PHYSICAL',
            'price': str(item.price)
        })

    response = iyzipay.CheckoutFormInitialize().create(request_iyzi, options)
    result = json.loads(response.read().decode('utf-8'))

    return redirect(result['paymentPageUrl'])

@csrf_exempt
def payment_callback(request):
    token = request.POST.get('token')

    options = {
        'api_key': settings.IYZICO_API_KEY,
        'secret_key': settings.IYZICO_SECRET_KEY,
        'base_url': settings.IYZICO_BASE_URL
    }

    request_iyzi = {'token': token}

    result = iyzipay.CheckoutForm().retrieve(request_iyzi, options)
    data = result.read().decode('utf-8')

    payment_result = json.loads(data)

    order_id = payment_result['conversationId']
    order = Order.objects.get(id=order_id)

    if payment_result['paymentStatus'] == 'SUCCESS':
        order.status = 'paid'
        order.save()

    return redirect('home')

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'core/product_detail.html', {'product': product})