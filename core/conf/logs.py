# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#
#     'formatters': {
#         'default': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#     },
#
#     'handlers': {
#         'info_file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename':  'logs/info.log',
#             'formatter': 'default',
#         },
#     },
#
#     'loggers': {
#         'django': {
#             'handlers': ['info_file', 'warning_file', 'error_file'],
#             'level': 'INFO',  # So INFO va undan yuqori darajadagilar loglanadi
#             'propagate': True,
#         },
#     }
# }