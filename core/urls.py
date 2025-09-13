from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/', include(   
      [
         path('auth/', include('apps.authentication.urls')),
         path('finance/', include('apps.finance.urls')),    
         path('client/', include('apps.client.urls')), 
         path('estimate/', include('apps.estimate.urls')),
         path('rooms/', include('apps.rooms.urls')),
         path('web/', include('apps.web.urls')),
          path("services/", include('apps.services.urls')),
      ]
   ))
]

urlpatterns += [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
