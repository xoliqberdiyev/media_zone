from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqami quyidagi formatda bo'lishi kerak: +998XXXXXXXXX"
)