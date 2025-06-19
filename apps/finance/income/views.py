from datetime import timedelta

from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth
from django.shortcuts import get_object_or_404

from rest_framework import generics, views, permissions
from rest_framework.response import Response

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


class IncomeStatistsApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        queryset = Income.objects.all()

        prediot = request.query_params.get('filter', 'current_year')

        if prediot == 'last_week':
            queryset = queryset.filter(date__gte=now - timedelta(days=7), date__lte=now)

        elif prediot == 'last_month':
            if now.month == 1:
                year = now.year - 1
            else:
                month = now.month - 1
            queryset = queryset.filter(date__year=year, date__month=month)

        elif prediot == 'last_year':
            queryset = queryset.filter(date__year=now.year-1)

        elif prediot == "current_month":
            queryset = queryset.filter(date__month=now.month)

        elif prediot == "current_year":
            queryset = queryset.filter(date__year=now.year)

        elif prediot == "current_week":
            queryset = queryset.filter(date__range=(now-timedelta(days=7), now))

        expence = queryset.aggregate(
            expence=Sum('price')
        )['expence']      

        return Response(
            {"expence": expence, "date_range": prediot}
        )  


class IncomeMonthlyStatisticsApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = (
            Income.objects
            .annotate(year=ExtractYear("date"), month=ExtractMonth('date'))
            .values('year', 'month')
            .annotate(total=Sum('price'))
            .order_by('year', 'month')
        )

        result = {}

        for item in data:
            print(item)
            year = item['year'] # 2025
            month = item['month'] # 01
            total = item['total'] # 1212

            if year not in result: # 2025 yoq bosa
                result[year] = {i: 0 for i in range(1,13)} # 2025: [1,2,3,4,5,6,7,8,9,10,11,12]

            result[year][month] = total # 2025: [1: 1000, 2: 1223]
        
        return Response(result)


class IncomeListApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        income_category = get_object_or_404(IncomeCategory, id=id)
        income = Income.objects.filter(category=income_category)
        serializer = serializers.IncomeListSerializer(income, many=True)
        return Response(serializer.data)