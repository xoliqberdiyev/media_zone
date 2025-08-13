from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from apps.finance.models import Income, IncomeCategory
from apps.finance.income import serializers
from datetime import datetime
from rest_framework import views, permissions
from rest_framework.response import Response
from apps.finance.models import Income
from apps.finance.income.serializers import IncomeStatisticsSerializer
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class IncomeCreateApiView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = serializers.IncomeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class IncomeCategoryApiView(generics.ListAPIView):
    serializer_class = serializers.IncomeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncomeCategory.objects.all()

class IncomeStatistsApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IncomeStatisticsSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: IncomeStatisticsSerializer}
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

# class IncomeListApiView(generics.ListAPIView):
#     serializer_class = serializers.IncomeListSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['date']
#
#     def get_queryset(self):
#         queryset = Income.objects.all()
#         category_id = self.kwargs.get('id')
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')
#
#         if category_id:
#             queryset = queryset.filter(category__id=category_id)
#         if start_date and end_date:
#             queryset = queryset.filter(date__range=[start_date, end_date])
#
#         return queryset.order_by('-date')

class IncomeListApiView(generics.ListAPIView):
    serializer_class = serializers.IncomeListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Boshlanish sanasi (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Tugash sanasi (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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