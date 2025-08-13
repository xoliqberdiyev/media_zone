from django.db import models

from apps.shared.models import BaseModel


class IncomeCategory(BaseModel):
    name = models.CharField(max_length=50, db_index=True, unique=True)

    def __str__(self):
        return f'{self.name}'


class ExpenceCategory(BaseModel):
    name = models.CharField(max_length=50, db_index=True, unique=True)

    def __str__(self):
        return f'{self.name}'


class Income(BaseModel):
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, related_name='incomes')
    price = models.PositiveBigIntegerField()
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.price} - {self.date} income'

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def delete(self):
        return super().delete()


class Expence(BaseModel):
    category = models.ForeignKey(ExpenceCategory, on_delete=models.CASCADE, related_name='expences')
    price = models.PositiveBigIntegerField()
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.price} - {self.date} expence'

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def delete(self):
        return super().delete()