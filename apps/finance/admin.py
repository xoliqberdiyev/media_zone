from django.contrib import admin

from apps.finance import models

@admin.register(models.IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # 'total_price' ni olib tashlang

@admin.register(models.ExpenceCategory)
class ExpenceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # 'total_price' ni olib tashlang

@admin.register(models.Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'price', 'date', 'comment']

@admin.register(models.Expence)
class ExpenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'price', 'date', 'comment']