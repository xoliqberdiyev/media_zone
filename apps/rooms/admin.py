from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from apps.rooms.models import Room, RoomOrder, RoomImage

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 0

@admin.register(Room)
class RoomAdmin(TranslationAdmin):
    inlines = [RoomImageInline]
    list_display = ['name', 'monthly_income', 'room_price_per_hour']
    search_fields = ['name']

@admin.register(RoomOrder)
class RoomOrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date', 'start_time', 'end_time', 'price']
    list_filter = ['date', 'type']
    search_fields = ['full_name', 'phone']

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room', 'image']