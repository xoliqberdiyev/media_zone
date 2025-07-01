from django.urls import path 

from apps.rooms import views

urlpatterns = [
    path('room-list/', views.RoomListApiView.as_view()),
    path('room_order/create/', views.RoomOrderCreateApiView.as_view()),
    path('<uuid:room_id>/room_order/list/', views.RoomOrderListSerializer.as_view()),
]