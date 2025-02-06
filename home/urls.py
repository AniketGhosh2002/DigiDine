from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.CustomerView.as_view(), name='customerview'),
    path('order/', views.OrderView.as_view(), name='orderview'),
    path('orderitem/', views.OrderItemView.as_view(), name='orderitemview'),
    path('orderitems/<int:pk>', views.OrderItemDetailView.as_view(), name='orderitemdetailview'),
    path('payment/', views.PaymentView.as_view(), name='paymentview')
]