from django.contrib import admin

from apps.rooms.models import Room, RoomOrder, RoomImage

admin.site.register(Room)
admin.site.register(RoomOrder)
admin.site.register(RoomImage)
