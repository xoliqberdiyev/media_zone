from django.contrib import admin

# Register your models here.
from apps.web.models import Partner, Image, Video, Team


admin.site.register(Partner)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Team)
