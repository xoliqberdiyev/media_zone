from datetime import datetime, timedelta

from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, views, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.finance.income import serializers
from apps.finance.models import Income, IncomeCategory


class IncomeCreateApiView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = serializers.IncomeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class IncomeCategoryApiView(generics.ListAPIView):
    serializer_class = serializers.IncomeCategorySerializer
    queryset = IncomeCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        for category in queryset:
            category.update_total_price()
        return queryset


class IncomeStatistsApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.IncomeStatisticsSerializer

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not (start_date and end_date):
            return Response({"error": "start_date va end_date kerak (YYYY-MM-DD)"}, status=400)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Sana formati noto‘g‘ri (YYYY-MM-DD)"}, status=400)

        queryset = Income.objects.filter(date__range=[start_date, end_date])
        total_income = queryset.aggregate(Sum('price'))['price__sum'] or 0

        return Response({"total_income": total_income})


class IncomeMonthlyStatisticsApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = (
            Income.objects
            .annotate(year=ExtractYear("created_at"), month=ExtractMonth('created_at'))
            .values('year', 'month')
            .annotate(total=Sum('price'))
            .order_by('year', 'month')
        )

        result = {}
        for item in data:
            year = item['year']
            month = item['month']
            total = item['total']
            if year not in result:
                result[year] = {i: 0 for i in range(1, 13)}
            result[year][month] = total

        return Response(result)


class IncomeListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class IncomeListApiView(generics.ListAPIView):
    serializer_class = serializers.IncomeListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']
    pagination_class = IncomeListPagination

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)
        return Response({
            'page': int(request.query_params.get('page', 1)),
            'page_size': paginator.get_page_size(request),
            'total_pages': paginator.page.paginator.num_pages,
            'total_items': paginator.page.paginator.count,
            'results': serializer.data
        })

    def get_queryset(self):
        queryset = Income.objects.all()
        category_id = self.kwargs.get('id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                pass

        return queryset.order_by('-date')


class IncomeDeleteApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        income = get_object_or_404(Income, id=id)
        income.delete()
        return Response({"success": True, "message": "deleted!"}, status=204)


class IncomeUpdateApiView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    serializer_class = serializers.IncomeUpdateSerializer
    queryset = Income.objects.all()

    def perform_update(self, serializer):
        instance = serializer.instance
        super().perform_update(serializer)
        instance.category.update_total_price()


class IncomeLastPeriodApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        last = request.query_params.get('last')
        valid_periods = ['last_day', 'last_week', 'last_month', 'last_year']
        if last not in valid_periods:
            return Response({"error": "last parametri last_day, last_week, last_month yoki last_year bo‘lishi kerak"}, status=400)

        today = datetime.now().date()
        if last == 'last_day':
            start_date = today - timedelta(days=1)
        elif last == 'last_week':
            start_date = today - timedelta(days=7)
        elif last == 'last_month':
            start_date = today - timedelta(days=30)
        else:  # last_year
            start_date = today - timedelta(days=365)

        queryset = Income.objects.filter(date__gte=start_date, date__lte=today)
        total_income = queryset.aggregate(Sum('price'))['price__sum'] or 0

        return Response({last: total_income})

# Add to income/views.py
class IncomeCategoryTotalApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.IncomeCategoryTotalSerializer

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not (start_date and end_date):
            return Response({"error": "start_date va end_date kerak (YYYY-MM-DD)"}, status=400)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Sana formati noto‘g‘ri (YYYY-MM-DD)"}, status=400)

        categories = IncomeCategory.objects.all()
        result = []
        for category in categories:
            total_price = Income.objects.filter(
                category=category,
                date__range=[start_date, end_date]
            ).aggregate(total_price=Sum('price'))['total_price'] or 0
            result.append({
                'id': category.id,
                'name': category.name,
                'total_price': total_price
            })

        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data)