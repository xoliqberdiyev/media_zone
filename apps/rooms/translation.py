from modeltranslation.translator import register, TranslationOptions

from apps.rooms.models import Room


@register(Room)
class RoomTranslation(TranslationOptions):
    fields = ['name', 'description']

    