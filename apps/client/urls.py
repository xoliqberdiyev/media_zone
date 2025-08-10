from django.urls import path 
from apps.client import views

urlpatterns = [
    path('create/', views.ClientCreateApiView.as_view(), name='client_create_api'),
    path('<uuid:id>/update/', views.ClientUpdateApiView.as_view(), name='client_update_api'),
    path('list/', views.ClientListApiView.as_view()),
    path('<uuid:id>/delete/', views.ClientDeleteApiView.as_view(), name='client_delete_api'),
]