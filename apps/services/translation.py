from modeltranslation.translator import register, TranslationOptions
from apps.services.models import Service

@register(Service)
class ServiceTranslation(TranslationOptions):
    fields = ['name', 'description']