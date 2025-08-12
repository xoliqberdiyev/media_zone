from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from apps.services.models import Service, ServiceOrder, ServiceImage

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 0

@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    inlines = [ServiceImageInline]
    list_display = ['name', 'monthly_income', 'service_price_per_hour']
    search_fields = ['name']

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date', 'start_time', 'end_time', 'price']
    list_filter = ['date', 'type']
    search_fields = ['full_name', 'phone']

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['service', 'image']