from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from apps.finance.models import Expence, ExpenceCategory
from apps.finance.expence import serializers
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ExpenceCreateApiView(generics.CreateAPIView):
    queryset = Expence.objects.all()
    serializer_class = serializers.ExpenceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpenceCategoryApiView(generics.ListAPIView):
    serializer_class = serializers.ExpenceCategorySerializer
    queryset = ExpenceCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        for category in queryset:
            category.update_total_price()
        return queryset

class ExpenceStatistsApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ExpenceStatisticsSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: serializers.ExpenceStatisticsSerializer}
    )
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

        queryset = Expence.objects.filter(date__range=[start_date, end_date])
        total_expence = queryset.aggregate(Sum('price'))['price__sum'] or 0

        return Response({"total_expence": total_expence})

class ExpenceMonthlyStatisticsApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = (
            Expence.objects
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

class ExpenceListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ExpenceListApiView(generics.ListAPIView):
    serializer_class = serializers.ExpenceListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']
    pagination_class = ExpenceListPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('page', openapi.IN_QUERY, description="Sahifa raqami", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Sahifadagi elementlar soni", type=openapi.TYPE_INTEGER, required=False),
        ]
    )
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
        queryset = Expence.objects.all()
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

class ExpenceDeleteApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        expence = get_object_or_404(Expence, id=id)
        expence.delete()
        return Response({"success": True, "message": "deleted!"}, status=204)

class ExpenceUpdateApiView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    serializer_class = serializers.ExpenceUpdateSerializer
    queryset = Expence.objects.all()

    def perform_update(self, serializer):
        instance = serializer.instance
        super().perform_update(serializer)
        instance.category.update_total_price()

class ExpenceLastPeriodApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('last', openapi.IN_QUERY, description="Period: last_day, last_week, last_month, or last_year", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: openapi.Response('Total expense for the period', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'last': openapi.Schema(type=openapi.TYPE_INTEGER)}))}
    )
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

        queryset = Expence.objects.filter(date__gte=start_date, date__lte=today)
        total_expence = queryset.aggregate(Sum('price'))['price__sum'] or 0

        return Response({last: total_expence})

# Add to expence/views.py
class ExpenceCategoryTotalApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ExpenceCategoryTotalSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: serializers.ExpenceCategoryTotalSerializer(many=True)}
    )
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

        queryset = Expence.objects.filter(date__range=[start_date, end_date]) \
            .values('category__name') \
            .annotate(total_price=Sum('price')) \
            .order_by('category__name')

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)