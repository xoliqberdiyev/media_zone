from django.urls import path, include 
from apps.finance.income import views as income_views
from apps.finance.expence import views as expence_views

urlpatterns = [
    path('expence/', include(
        [
            path('create/', expence_views.ExpenceCreateApiView.as_view(), name='expence_create_api'),
            path('statistics/', expence_views.ExpenceStatistsApiView.as_view(), name='expence_statistics_api'),
            path('monthly-statistics/', expence_views.ExpenceMonthlyStatisticsApiView.as_view(), name='expence_monthly_statistics_api'),
            path('category/list/', expence_views.ExpenceCategoryApiView.as_view(), name='expence_category_list'),
            path('category/<uuid:id>/expence/list/', expence_views.ExpenceListApiView.as_view(), name='expence_list'),
            path('<uuid:id>/delete/', expence_views.ExpenceDeleteApiView.as_view(), name='expence_delete'),
            path('<uuid:id>/update/', expence_views.ExpenceUpdateApiView.as_view(), name='expence_update'),
            path('last-statistics/', expence_views.ExpenceLastStatisticsView.as_view(), name='expence_last_statistics'),
        ]
    )),
    path('income/', include(
        [
            path('create/', income_views.IncomeCreateApiView.as_view(), name='income_create_api'),
            path('statistics/', income_views.IncomeStatistsApiView.as_view(), name='income_statistics_api'),
            path('monthly-statistics/', income_views.IncomeMonthlyStatisticsApiView.as_view(), name='income_monthly_statistics_api'),
            path('category/list/', income_views.IncomeCategoryApiView.as_view(), name='income_category_list'),
            path('category/<uuid:id>/income/list/', income_views.IncomeListApiView.as_view(), name='income_list'),
            path('<uuid:id>/delete/', income_views.IncomeDeleteApiView.as_view(), name='income_delete'),
            path('<uuid:id>/update/', income_views.IncomeUpdateApiView.as_view(), name='income_update'),
            path('last-statistics/', income_views.IncomeLastStatisticsView.as_view(), name='income_last_statistics'),
        ]
    ))
]