from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from apps.finance.models import Expence, ExpenceCategory
from apps.finance.expence import serializers
from rest_framework import views, permissions
from rest_framework.response import Response
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.shared.pagination import CustomPageNumberPagination

class ExpenceCreateApiView(generics.CreateAPIView):
    queryset = Expence.objects.all()
    serializer_class = serializers.ExpenceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpenceCategoryApiView(generics.ListAPIView):
    serializer_class = serializers.ExpenceCategorySerializer
    queryset = ExpenceCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated]

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

class ExpenceListApiView(generics.ListAPIView):
    serializer_class = serializers.ExpenceListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']
    pagination_class = CustomPageNumberPagination

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
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        response_data = {'results': serializer.data}

        category_id = self.kwargs.get('id')
        if category_id:
            category = get_object_or_404(ExpenceCategory, id=category_id)
            category_serializer = serializers.ExpenceCategorySerializer(category)
            response_data['category'] = category_serializer.data

        if page is not None:
            return self.get_paginated_response(response_data)
        return Response(response_data)

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

    @swagger_auto_schema(
        operation_description="ID bo‘yicha Expence yozuvini o‘chirish. Agar category_id berilsa, yozuv shu kategoriyada ekanligi tekshiriladi.",
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY, description="Kategoriya ID (ixtiyoriy)", type=openapi.TYPE_STRING, required=False),
        ],
        responses={204: 'No Content', 404: 'Not Found', 400: 'Bad Request'}
    )
    def delete(self, request, id):
        # Expence yozuvini topish
        expence = get_object_or_404(Expence, id=id)
        category = expence.category

        # Agar category_id berilgan bo‘lsa, tekshirish
        category_id = request.query_params.get('category_id')
        if category_id and str(category.id) != category_id:
            return Response({
                "success": False,
                "message": "Yozuv bu kategoriyada emas"
            }, status=400)

        # Yozuvni o‘chirish (total_price modelda avtomatik yangilanadi)
        expence.delete()

        # Yangilangan kategoriya ma’lumotlarini qaytarish
        category_serializer = serializers.ExpenceCategorySerializer(category)
        return Response({
            "success": True,
            "message": "Yozuv muvaffaqiyatli o‘chirildi",
            "category": category_serializer.data
        }, status=204)

class ExpenceUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.ExpenceUpdateSerializer
    queryset = Expence.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]