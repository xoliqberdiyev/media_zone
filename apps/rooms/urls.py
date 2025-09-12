from django.urls import path
from apps.rooms import views

urlpatterns = [
    path('room-list/', views.RoomListApiView.as_view()),
    path('room_order/create/', views.RoomOrderCreateApiView.as_view()),
    path('<uuid:room_id>/room_order/list/', views.RoomOrderListApiView.as_view()),
    path('room_order/<uuid:id>/delete/', views.RoomOrderDeleteApiView.as_view()),
    path('room_order/<uuid:id>/update/', views.RoomOrderUpdateApiView.as_view()),
    path('room_order/deleted/list/', views.DeletedRoomOrdersApiView.as_view()),
]