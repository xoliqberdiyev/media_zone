from django.urls import path 

from apps.client import views 

urlpatterns = [
    path('create/', views.ClientCreateApiView.as_view(), name='client_create_api'),
    path('<uuid:id>/update/', views.ClientUpdateApiView.as_view(), name='client_update_api'),

]