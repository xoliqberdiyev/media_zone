from django.urls import path
from apps.rooms import views

urlpatterns = [
    path('room-list/', views.RoomListApiView.as_view(), name='room_list'),
    path('room_order/create/', views.RoomOrderCreateApiView.as_view(), name='room_order_create'),
    path('<uuid:room_id>/room_order/list/', views.RoomOrderListApiView.as_view(), name='room_order_list'),
]