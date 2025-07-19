from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from apps.rooms.models import Room, RoomOrder, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 0

admin.site.register(RoomOrder)
admin.site.register(RoomImage)

@admin.register(Room)
class RoomAdmin(TranslationAdmin):
    inlines = [RoomImageInline]