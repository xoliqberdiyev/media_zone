from django.urls import path, include
from apps.services import views

urlpatterns = [
    path('services-list/', views.ServiceListApiView.as_view(), name='service_list'),
    path('services_order/create/', views.ServiceOrderCreateApiView.as_view(), name='service_order_create'),
    path('<uuid:service_id>/services_order/list/', views.ServiceOrderListApiView.as_view(), name='service_order_list'),
    path('services_order/<uuid:id>/delete/', views.ServiceOrderDeleteApiView.as_view(), name='service-order-delete'),
    path('services_order/<uuid:id>/update/', views.ServiceOrderUpdateApiView.as_view(), name='service-order-update'),
]