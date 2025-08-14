from django.utils import timezone
from django.db import models
from apps.shared.models import BaseModel
from apps.shared.regex import phone_regex

class Room(BaseModel):
    name = models.CharField(max_length=150)
    monthly_income = models.PositiveBigIntegerField(default=0)
    room_price_per_hour = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to="media_zone/rooms/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        now = timezone.now()
        total = RoomOrder.objects.filter(
            room=self,
            date__month=now.month,
            date__year=now.year
        ).aggregate(total_price=models.Sum('price'))['total_price'] or 0

        self.monthly_income = total
        super().save(*args, **kwargs)

class RoomOrder(BaseModel):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.PositiveBigIntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(choices=[('crm', 'crm'), ('web', 'web')], max_length=3, default='crm')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_orders")
    servis_type = models.CharField(max_length=50, null=True, blank=True)  # Optional field

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        now = timezone.now()
        total = RoomOrder.objects.filter(
            room=self.room,
            date__month=now.month,
            date__year=now.year
        ).aggregate(total_price=models.Sum('price'))['total_price'] or 0

        self.room.monthly_income = total
        self.room.save()
        super().save(*args, **kwargs)

class RoomImage(BaseModel):
    image = models.ImageField(upload_to="media_zone/room_images/")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_images")

    def __str__(self):
        return self.room.name