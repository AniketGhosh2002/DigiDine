"""
URL configuration for menuapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home.views import DishViewSet, OrderViewSet, OrderItemViewSet, CustomerViewSet, CuisineViewSet, ChefViewSet, PaymentViewSet
from django.conf import settings
from django.conf.urls.static import static
from home import views


router = DefaultRouter()
router.register(r'dish', DishViewSet)
router.register(r'order', OrderViewSet)
router.register(r'orderitem', OrderItemViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'cuisine', CuisineViewSet)
router.register(r'chef', ChefViewSet)
router.register(r'payment', PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurent/api/', include(router.urls)),
    path('home/<int:customer_id>/', views.home, name='home'),
    path('', views.customers, name='customers'),
    path('orderitems/<int:order_id>/', views.orderitems, name='orderitems'),
    path('payments/<int:customer_id>/', views.customer_payments, name='customer_payments'),
    path('makepayment/', views.makepayment, name='make_payment'),
    path('chefs/<int:pk>/', views.chefs, name='chefs'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
