from django.urls import path 

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authentication import views


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login_api'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_api'),
    path('user/create/', views.CreateUserApiView.as_view()),
    path('user/<uuid:id>/', views.UserApiView.as_view()),
    path('user/list/', views.UserListApiView.as_view()),
]