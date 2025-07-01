from rest_framework import views, generics, permissions

from apps.estimate.serializers import (
    EstimateExpenceCreateSerializer,
    EstimateIncomeCreateSerializer,
    EstimateListSerializer
)
from apps.estimate.models import Estimate


class EstimateIncomeCreateApiView(generics.CreateAPIView):
    serializer_class = EstimateIncomeCreateSerializer
    queryset = Estimate.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class EstimateExpenceCreateApiView(generics.CreateAPIView):
    serializer_class = EstimateExpenceCreateSerializer
    queryset = Estimate.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class EstimateIncomeListApiView(generics.ListAPIView):
    serializer_class = EstimateListSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Estimate.objects.filter(type='INCOME')


class EstimateExpenceListApiView(generics.ListAPIView):
    serializer_class = EstimateListSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Estimate.objects.filter(type='EXPENCE')


class EstimateDeleteApiView(generics.DestroyAPIView):
    lookup_field = 'id'
    queryset = Estimate.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class EstimateUpdateApiView(generics.UpdateAPIView):    
    lookup_field = 'id'
    queryset = Estimate.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EstimateListSerializer