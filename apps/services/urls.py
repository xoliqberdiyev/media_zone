from django.urls import path, include
from apps.services import views

urlpatterns = [
    path('services-list/', views.ServiceListApiView.as_view(), name='service_list'),
    path('services_order/create/', views.ServiceOrderCreateApiView.as_view(), name='service_order_create'),
    path('<uuid:services_id>/services_order/list/', views.ServiceOrderListApiView.as_view(), name='service_order_list'),
]