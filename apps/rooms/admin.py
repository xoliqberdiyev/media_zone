from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from apps.rooms.models import Room, RoomOrder, RoomImage


admin.site.register(Room, TranslationAdmin)
admin.site.register(RoomOrder)
admin.site.register(RoomImage)
