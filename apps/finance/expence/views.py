from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from apps.finance.models import Expence, ExpenceCategory
from apps.finance.expence import serializers
from datetime import datetime
from rest_framework import views, permissions
from rest_framework.response import Response
from apps.finance.models import Expence
from apps.finance.expence.serializers import ExpenceStatisticsSerializer
from django.db.models import Sum
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

class ExpenceStatistsApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenceStatisticsSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: ExpenceStatisticsSerializer}
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

    def get_queryset(self):
        queryset = Expence.objects.all()
        category_id = self.kwargs.get('id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset.order_by('-date')

class ExpenceDeleteApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        expence = get_object_or_404(Expence, id=id)
        expence.delete()
        return Response({"success": True, "message": "deleted!"}, status=status.HTTP_204_NO_CONTENT)

class ExpenceUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.ExpenceUpdateSerializer
    queryset = Expence.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]