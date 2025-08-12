# models.py
from django.utils import timezone
from django.db import models
from apps.shared.models import BaseModel

class Service(BaseModel):
    name = models.CharField(max_length=150)
    monthly_income = models.PositiveBigIntegerField(default=0)
    service_price_per_hour = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to="media_zone/services/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def update_monthly_income(self):
        """Foydalanuvchi chaqirganda joriy oydagi daromadni hisoblaydi"""
        now = timezone.now()
        total = ServiceOrder.objects.filter(
            service=self,
            date__month=now.month,
            date__year=now.year
        ).aggregate(total_price=models.Sum('price'))['total_price'] or 0
        self.monthly_income = total
        # update faqat shu fieldni
        Service.objects.filter(pk=self.pk).update(monthly_income=total)


class ServiceOrder(BaseModel):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.PositiveBigIntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(choices=[('crm', 'crm'), ('web', 'web')], max_length=3, default='crm')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_orders")

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Avval buyurtmani saqlaymiz
        # Keyin faqat monthly_income ni yangilaymiz
        self.service.update_monthly_income()


class ServiceImage(BaseModel):
    image = models.ImageField(upload_to="media_zone/service_images/")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_images")

    def __str__(self):
        return self.service.name
