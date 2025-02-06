from django.shortcuts import render
from home.models import Dish, Order, OrderItem, Customer, Cuisine, Chef, Payment
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import DishSerializer, OrderSerializer, OrderItemSerializer, CustomerSerializer, CuisineSerializer, ChefSerializer, PaymentSerializer
import qrcode
import base64
from io import BytesIO
from rest_framework.response import Response

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer

class ChefViewSet(viewsets.ModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

def customers(request):
    return render(request, 'customer.html')

def home(request, customer_id):
    customers = Customer.objects.all()
    orders = Order.objects.filter(customer_id=customer_id).order_by('-order_time')
    category_order = ["starter", "main course", "side dish", "dessert", "drinks"]
    def get_category_index(cuisine_name):
        name_lower = cuisine_name.lower()
        for index, category in enumerate(category_order):
            if category in name_lower:
                return index
        return len(category_order) 

    cuisines = sorted(Cuisine.objects.all(), key=lambda c: get_category_index(c.name))
    return render(request, "home.html", {'customer_id': customer_id, 'cuisines': cuisines, 'orders': orders, 'customers': customers})

def orderitems(request, order_id):
    order = Order.objects.all().get(pk=order_id)
    category_order = ["starter", "main course", "side dish", "dessert", "drinks"]
    def get_category_index(cuisine_name):
        name_lower = cuisine_name.lower()
        for index, category in enumerate(category_order):
            if category in name_lower:
                return index
        return len(category_order) 
    
    cuisines = sorted(Cuisine.objects.all(), key=lambda c: get_category_index(c.name))
    return render(request, 'orderitem.html', {'order_id': order_id, 'cuisines': cuisines, 'order': order})

def chefs(request, pk):
    chef = Chef.objects.get(pk=pk)
    cuisines = Cuisine.objects.filter(chefs=chef)
    order_items = OrderItem.objects.filter(dish__cuisine__chefs=chef).order_by('is_done')
    customers = Customer.objects.all()  

    return render(request, 'chef.html', {
        'chefs': chef,
        'cuisines': cuisines,
        'orders': order_items,
        'customers': customers  
    })

def customer_payments(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    orders = Order.objects.filter(customer_id=customer).order_by('-order_time')
    payments = Payment.objects.filter(order__customer_id=customer)

    paid_order_ids = list(payments.values_list('order_id', flat=True))
    paid_orders = orders.filter(id__in=paid_order_ids)  
    unpaid_orders = orders.exclude(id__in=paid_order_ids)  

    order_items = OrderItem.objects.filter(order__in=orders)

    order_totals = {}
    for order in orders:
        total_price = sum(item.quantity * item.dish.price for item in order_items if item.order.id == order.id)
        order_totals[order.id] = total_price  

    final_amount = sum(order_totals.values())   

    upi_data = f"upi://pay?pa=8902038188@apl&am={final_amount}"

    qr = qrcode.QRCode()
    qr.add_data(upi_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#513430", back_color="#f0ca75")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    payment_qr = base64.b64encode(buffer.getvalue()).decode('utf-8') 

    return render(request, 'payment.html', {
        'customer': customer,
        'customer_id': customer_id,
        'orders': orders,
        'paid_orders': paid_orders,
        'paid_order_ids': paid_order_ids,
        'unpaid_orders': unpaid_orders,
        'order_items': order_items,
        'payments': payments,
        'order_totals': order_totals,
        "final_amount": final_amount,  
        "qr_code_url": payment_qr,    
    })


def makepayment(request):
    orders = Order.objects.all().order_by('-order_time')
    return render(request, 'managepayment.html', {'orders': orders})