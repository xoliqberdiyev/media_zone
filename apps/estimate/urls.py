from django.urls import path, include

from apps.estimate import views


urlpatterns = [
    path('income/create/', views.EstimateIncomeCreateApiView.as_view()),
    path('income/list/', views.EstimateIncomeListApiView.as_view()),
    path('expence/create/', views.EstimateExpenceCreateApiView.as_view()),
    path('expence/list/', views.EstimateExpenceListApiView.as_view()),
    path('<uuid:id>/delete/', views.EstimateDeleteApiView.as_view()),
    path('<uuid:id>/update/', views.EstimateUpdateApiView.as_view()),
]