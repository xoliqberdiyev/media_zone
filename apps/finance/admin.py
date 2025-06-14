from django.contrib import admin

from apps.finance import models 


@admin.register(models.IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_price', 'income_count']

    @admin.display(description="Icome count")
    def income_count(self, obj):
        return obj.incomes.count()
    

@admin.register(models.Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'date']



@admin.register(models.ExpenceCategory)
class ExpenceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_price', 'income_count']

    @admin.display(description="Expence count")
    def income_count(self, obj):
        return obj.expences.count()
    

@admin.register(models.Expence)
class ExpenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'date']
