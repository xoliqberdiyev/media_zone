LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename':  'logs/info.log',
            'formatter': 'default',
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename':  'logs/warning.log',
            'formatter': 'default',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
            'formatter': 'default',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['info_file', 'warning_file', 'error_file'],
            'level': 'INFO',  # So INFO va undan yuqori darajadagilar loglanadi
            'propagate': True,
        },
        'django.request': {
            'handlers': ['info_file', 'warning_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['warning_file', 'error_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}