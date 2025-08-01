from django.urls import path, include 

from apps.finance.expence import views
from apps.finance.income import views as income_views

urlpatterns = [
    path('expence/', include(
        [
            path('create/', views.ExpenceCreateApiView.as_view(), name='expence_create_api'),
            path('statistics/', views.ExpenceStatistsApiView.as_view(), name='expence_statatistics_api'),
            path('monthly-statistics/', views.ExpenceMonthlyStatisticsApiView.as_view(), name='expence_statistics_api'),
            path('category/list/', views.ExpenceCategoryApiView.as_view()),
            path('category/<uuid:id>/expence/list/', views.ExpenceListApiView.as_view()),
            path('<uuid:id>/delete/', views.ExpenceDeleteApiView.as_view()),
            path('<uuid:id>/update/', views.ExpenceUpdateApiView.as_view()),
        ]
    )),
    path('income/', include(
        [
            path('create/', income_views.IncomeCreateApiView.as_view()),
            path('statistics/', income_views.IncomeStatistsApiView.as_view()),
            path('monthly-statistics/', income_views.IncomeMonthlyStatisticsApiView.as_view()),
            path('category/list/', income_views.IncomeCategoryApiView.as_view()),
            path('category/<uuid:id>/income/list/', income_views.IncomeListApiView.as_view()),
            path('<uuid:id>/delete/', income_views.IncomeDeleteApiView.as_view()),
            path('<uuid:id>/update/', income_views.IncomeUpdateApiView.as_view()),
        ]
    ))
]