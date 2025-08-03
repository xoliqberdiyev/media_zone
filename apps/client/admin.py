from django.contrib import admin

from apps.client.models import Client, ClientComment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'status']
    list_filter = ['status']


@admin.register(ClientComment)
class ClientCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'date', 'comment']