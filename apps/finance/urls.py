from django.urls import path
from apps.finance.income import views as income_views
from apps.finance.expence import views as expence_views

urlpatterns = [
    # Income URLs
    path('income/create/', income_views.IncomeCreateApiView.as_view(), name='income_create_api'),
    path('income/category/list/', income_views.IncomeCategoryApiView.as_view(), name='income_category_list_api'),
    path('income/statistics/', income_views.IncomeStatistsApiView.as_view(), name='income_statistics_api'),
    path('income/monthly/statistics/', income_views.IncomeMonthlyStatisticsApiView.as_view(),
         name='income_monthly_statistics_api'),
    path('income/category/<uuid:id>/income/list/', income_views.IncomeListApiView.as_view(), name='income_list_api'),
    path('income/delete/<uuid:id>/', income_views.IncomeDeleteApiView.as_view(), name='income_delete_api'),
    path('income/update/<uuid:id>/', income_views.IncomeUpdateApiView.as_view(), name='income_update_api'),
    path('income/last-period/', income_views.IncomeLastPeriodApiView.as_view(), name='income_last_period_api'),

    # Expence URLs
    path('expence/create/', expence_views.ExpenceCreateApiView.as_view(), name='expence_create_api'),
    path('expence/category/list/', expence_views.ExpenceCategoryApiView.as_view(), name='expence_category_list_api'),
    path('expence/statistics/', expence_views.ExpenceStatistsApiView.as_view(), name='expence_statistics_api'),
    path('expence/monthly-statistics/', expence_views.ExpenceMonthlyStatisticsApiView.as_view(),
         name='expence_monthly_statistics_api'),
    path('expence/category/<uuid:id>/list/', expence_views.ExpenceListApiView.as_view(), name='expence_list_api'),
    path('expence/delete/<uuid:id>/', expence_views.ExpenceDeleteApiView.as_view(), name='expence_delete_api'),
    path('expence/update/<uuid:id>/', expence_views.ExpenceUpdateApiView.as_view(), name='expence_update_api'),
    path('expence/last-period/', expence_views.ExpenceLastPeriodApiView.as_view(), name='expence_last_period_api'),
]