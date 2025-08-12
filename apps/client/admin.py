from django.contrib import admin
from apps.client.models import Client, ClientComment

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'status', 'back_color']
    list_filter = ['status']
    search_fields = ['name', 'phone']

@admin.register(ClientComment)
class ClientCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'date', 'comment']
    search_fields = ['client__name', 'comment']