from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from apps.finance.models import Expence, ExpenceCategory
from apps.finance.expence import serializers
from rest_framework import views, permissions
from rest_framework.response import Response
from apps.finance.models import Expence
from apps.finance.expence.serializers import ExpenceStatisticsSerializer
from django.db.models import Sum
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.finance import models
from apps.shared.pagination import CustomPageNumberPagination
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView


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




# class ExpenceListApiView(generics.ListAPIView):
#     serializer_class = serializers.ExpenceListSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['date']
#
#     def get_queryset(self):
#         queryset = Expence.objects.all()
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


class ExpenceLastStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'last',
                openapi.IN_QUERY,
                description="Vaqt oralig'i: last_day, last_week, last_month, last_year",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={200: openapi.Response('Umumiy chiqim', schema=openapi.Schema(
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
        last = request.query_params.get('last')
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

        total_expense = Expence.objects.filter(date__gte=start_date).aggregate(Sum('price'))['price__sum'] or 0

        return Response({key: total_expense})