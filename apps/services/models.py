from django.utils import timezone
from django.db import models
from apps.shared.models import BaseModel
from apps.shared.regex import phone_regex

class Service(BaseModel):
    name = models.CharField(max_length=150)
    monthly_income = models.PositiveBigIntegerField(default=0)
    service_price_per_hour = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to="media_zone/services/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        now = timezone.now()
        total = ServiceOrder.objects.filter(
            service=self,
            date__month=now.month,
            date__year=now.year
        ).aggregate(total_price=models.Sum('price'))['total_price'] or 0

        self.monthly_income = total
        super().save(*args, **kwargs)

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
        now = timezone.now()
        total = ServiceOrder.objects.filter(
            service=self.service,
            date__month=now.month,
            date__year=now.year
        ).aggregate(total_price=models.Sum('price'))['total_price'] or 0

        self.service.monthly_income = total
        self.service.save()
        super().save(*args, **kwargs)

class ServiceImage(BaseModel):
    image = models.ImageField(upload_to="media_zone/service_images/")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="service_images")

    def __str__(self):
        return self.service.name