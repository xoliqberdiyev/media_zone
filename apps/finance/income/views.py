from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, permissions
from django_filters.rest_framework import DjangoFilterBackend
from apps.finance.models import Income, IncomeCategory
from apps.finance.income import serializers
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView

class IncomeCreateApiView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = serializers.IncomeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class IncomeCategoryApiView(generics.ListAPIView):
    serializer_class = serializers.IncomeCategorySerializer
    queryset = IncomeCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY, description="Kategoriya ID (UUID)", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=False),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_context = self.get_serializer_context()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True, context=serializer_context)
        if page is not None:
            return Response({
                "page": self.paginator.page.number,
                "page_size": self.paginator.page_size,
                "total_pages": self.paginator.page.paginator.num_pages,
                "total_items": self.paginator.page.paginator.count,
                "results": serializer.data
            })
        return Response({
            "page": 1,
            "page_size": queryset.count(),
            "total_pages": 1,
            "total_items": queryset.count(),
            "results": serializer.data
        })

    def get_serializer_context(self):
        context = super().get_serializer_context()
        category_id = self.request.query_params.get('category_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        queryset = Income.objects.all()

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

        # Pagination o'rniga to'liq QuerySet uzatamiz
        context['queryset'] = queryset[:10]  # JSONdagi 10 ta tranzaksiyaga moslashtiramiz
        return context

class IncomeStatistsApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.IncomeStatisticsSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: serializers.IncomeStatisticsSerializer}
    )
    def get(self, request):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
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

class IncomeListApiView(generics.ListAPIView):
    serializer_class = serializers.IncomeListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=False),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        total_price = queryset.aggregate(total_price=Sum('price'))['total_price'] or 0
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        if page is not None:
            return Response({
                "page": self.paginator.page.number,
                "page_size": self.paginator.page_size,
                "total_pages": self.paginator.page.paginator.num_pages,
                "total_items": self.paginator.page.paginator.count,
                "results": serializer.data,
                "total_price": total_price
            })
        return Response({
            "page": 1,
            "page_size": queryset.count(),
            "total_pages": 1,
            "total_items": queryset.count(),
            "results": serializer.data,
            "total_price": total_price
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

class IncomeLastStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('last', openapi.IN_QUERY, description="Vaqt oralig'i: last_day, last_week, last_month, last_year", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: openapi.Response('Umumiy kirim', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'last_day': openapi.Schema(type=openapi.TYPE_INTEGER),
                'last_week': openapi.Schema(type=openapi.TYPE_INTEGER),
                'last_month': openapi.Schema(type=openapi.TYPE_INTEGER),
                'last_year': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))}
    )
    def get(self, request):
        last = self.request.query_params.get('last')
        now = timezone.now().date()

        if last == 'last_day':
            start_date = now - timedelta(days=1)
            key = 'last_day'
        elif last == 'last_week':
            start_date = now - timedelta(weeks=1)
            key = 'last_week'
        elif last == 'last_month':
            start_date = now - timedelta(days=30)
            key = 'last_month'
        elif last == 'last_year':
            start_date = now - timedelta(days=365)
            key = 'last_year'
        else:
            return Response({"error": "Noto‘g‘ri 'last' parametri"}, status=400)

        total_income = Income.objects.filter(date__gte=start_date).aggregate(Sum('price'))['price__sum'] or 0

        return Response({key: total_income})