from django.contrib import admin
from django.contrib.auth.models import Group
admin.site.unregister(Group)

from apps.authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']