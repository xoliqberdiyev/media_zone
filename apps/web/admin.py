from django.contrib import admin

# Register your models here.
from apps.web.models import Partner, Image


admin.site.register(Partner)
admin.site.register(Image)
