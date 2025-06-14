from django.db import models

from apps.shared.models import BaseModel


class IncomeCategory(BaseModel):
    name = models.CharField(max_length=50, db_index=True, unique=True)
    total_price = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.total_price}'


class ExpenceCategory(BaseModel):
    name = models.CharField(max_length=50, db_index=True, unique=True)
    total_price = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.total_price}'


class Income(BaseModel):
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, related_name='incomes')
    price = models.PositiveBigIntegerField()
    date = models.DateField()
    comment = models.TextField()

    def __str__(self):
        return f'{self.price} - {self.date} income'

    def save(self, *args, **kwargs):
        self.category.total_price += self.price
        self.category.save()    
        return super().save(args, kwargs)


class Expence(BaseModel):
    category = models.ForeignKey(ExpenceCategory, on_delete=models.CASCADE, related_name='expences')
    price = models.PositiveBigIntegerField()
    date = models.DateField()
    comment = models.TextField()

    def __str__(self):
        return f'{self.price} - {self.date} expence'

    def save(self, *args, **kwargs):
        self.category.total_price += self.price
        self.category.save()    
        return super().save(args, kwargs)
