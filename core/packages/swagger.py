from django.conf import settings

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')