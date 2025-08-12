from django.urls import path
from apps.rooms import views

urlpatterns = [
    path('room-list/', views.RoomListApiView.as_view(), name='room-list'),
    path('room_order/create/', views.RoomOrderCreateApiView.as_view(), name='room-order-create'),
    path('<uuid:room_id>/room_order/list/', views.RoomOrderListApiView.as_view(), name='room-order-list'),
    path('room_order/<uuid:id>/delete/', views.RoomOrderDeleteApiView.as_view(), name='room-order-delete'),
    path('room_order/<uuid:id>/update/', views.RoomOrderUpdateApiView.as_view(), name='room-order-update'),
]