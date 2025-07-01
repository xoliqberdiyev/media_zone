from django.contrib import admin

from apps.rooms.models import Room, RoomOrder

admin.site.register(Room)
admin.site.register(RoomOrder)