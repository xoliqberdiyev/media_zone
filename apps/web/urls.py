from django.urls import path 

from . import views

urlpatterns = [
    path('rooms/list/', views.RoomListApiView.as_view()),
    path('rooms/<uuid:id>/', views.RoomDetailApiView.as_view()),

    path('partners/', views.PartnerListApiView.as_view()),
    path('images/', views.ImageListApiView.as_view()),
    path('videos/', views.VideoListApiView.as_view()),

    path('rooms/order/create/', views.RoomOrderCreateApiView.as_view()),
]