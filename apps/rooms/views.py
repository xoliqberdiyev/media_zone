from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.rooms import serializers, models
from apps.shared.pagination import CustomPageNumberPagination
from django.db.models import Sum

class RoomListApiView(generics.ListAPIView):
    serializer_class = serializers.RoomListSerializer
    queryset = models.Room.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class RoomOrderCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.RoomOrderCreateSerializer
    queryset = models.RoomOrder.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class RoomOrderListApiView(generics.ListAPIView):
    serializer_class = serializers.RoomOrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        queryset = models.RoomOrder.objects.filter(room_id=room_id)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        return queryset.order_by('start_time')

# Yangi view: Faqat umumiy pul
class RoomIncomeStatisticsApiView(generics.GenericAPIView):
    serializer_class = serializers.RoomIncomeStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room_id):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not (start_date and end_date):
            return Response({"error": "start_date va end_date kerak (YYYY-MM-DD)"}, status=400)

        queryset = models.RoomOrder.objects.filter(room_id=room_id, date__range=[start_date, end_date])
        total_income = queryset.aggregate(Sum('price'))['price__sum'] or 0

        return Response({"total_income": total_income})