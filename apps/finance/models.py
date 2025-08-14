from django.db import models
from django.db.models import Sum
from apps.shared.models import BaseModel

class IncomeCategory(BaseModel):
    name = models.CharField(max_length=50, db_index=True, unique=True)
    total_price = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.total_price}'

    def update_total_price(self):
        """Recalculate total_price by summing all related incomes."""
        total = self.incomes.aggregate(total_price=Sum('price'))['total_price'] or 0
        self.total_price = total
        self.save()

class ExpenceCategory(BaseModel):
    name = models.CharField(max_length=50, db_index=True, unique=True)
    total_price = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.total_price}'

    def update_total_price(self):
        """Recalculate total_price by summing all related expences."""
        total = self.expences.aggregate(total_price=Sum('price'))['total_price'] or 0
        self.total_price = total
        self.save()

class Income(BaseModel):
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, related_name='incomes')
    price = models.PositiveBigIntegerField()
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.price} - {self.date} income'

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_price = None
        if not is_new:
            old_price = Income.objects.get(id=self.id).price
        super().save(*args, **kwargs)
        self.category.update_total_price()

    def delete(self, *args, **kwargs):
        category = self.category
        super().delete(*args, **kwargs)
        category.update_total_price()

class Expence(BaseModel):
    category = models.ForeignKey(ExpenceCategory, on_delete=models.CASCADE, related_name='expences')
    price = models.PositiveBigIntegerField()
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.price} - {self.date} expence'

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_price = None
        if not is_new:
            old_price = Expence.objects.get(id=self.id).price
        super().save(*args, **kwargs)
        self.category.update_total_price()

    def delete(self, *args, **kwargs):
        category = self.category
        super().delete(*args, **kwargs)
        category.update_total_price()