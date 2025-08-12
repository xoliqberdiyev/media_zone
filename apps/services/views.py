from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.services import serializers, models
from apps.shared.pagination import CustomPageNumberPagination
from django.db.models import Sum, Count

class ServiceListApiView(generics.ListAPIView):
    serializer_class = serializers.ServiceListSerializer
    queryset = models.Service.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class ServiceOrderCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.ServiceOrderCreateSerializer
    queryset = models.ServiceOrder.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class ServiceOrderListApiView(generics.ListAPIView):
    serializer_class = serializers.ServiceOrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

    SERVICE_PRICES = {
        "2b6a229a-618b-4fbd-8231-8a56a2898415": 99000,
        "91cc328f-57d3-41d7-bac0-27cc0f269a46": 150000,
        "4d302e7b-9b97-435d-a431-b772d537044b": 300000,
        "d873017b-793c-4ec9-9764-a349afc94c8f": 99000
    }

    def get_queryset(self):
        # MUAMMO HAL QILINDI: 'service_id' o'rniga 'services_id' dan foydalanildi
        services_id = self.kwargs.get('services_id')
        queryset = models.ServiceOrder.objects.filter(service_id=services_id)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        return queryset.order_by('start_time')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        paginated_response = self.get_paginated_response(serializer.data).data

        total_income = queryset.aggregate(Sum('price'))['price__sum'] or 0
        total_visitors = queryset.count()
        total_hours = 0
        for order in queryset:
            start = order.start_time
            end = order.end_time
            hours = (end.hour * 60 + end.minute - start.hour * 60 - start.minute) / 60
            total_hours += max(hours, 0)

        # MUAMMO HAL QILINDI: 'service_id' o'rniga 'services_id' dan foydalanildi
        services_id = self.kwargs.get('services_id')
        service_price = self.SERVICE_PRICES.get(str(services_id))

        return Response({
            'page': paginated_response.get('page', 1),
            'page_size': paginated_response.get('page_size', self.pagination_class.page_size),
            'total_pages': paginated_response.get('total_pages', 1),
            'total_items': paginated_response.get('total_items', queryset.count()),
            'total_income': total_income,
            'total_hours_booked': int(total_hours),
            'total_visitors': total_visitors,
            'service_price': service_price,
            'results': paginated_response.get('results', serializer.data)
        })

class ServiceOrderDeleteApiView(generics.DestroyAPIView):
    queryset = models.ServiceOrder.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "ServiceOrder deleted successfully"})

class ServiceOrderUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.ServiceOrderUpdateSerializer
    queryset = models.ServiceOrder.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)