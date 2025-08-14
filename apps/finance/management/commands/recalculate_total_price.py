from django.core.management.base import BaseCommand
from django.db.models import Sum
from apps.finance.models import IncomeCategory, ExpenceCategory

class Command(BaseCommand):
    help = 'Recalculate total_price for all IncomeCategory and ExpenceCategory'

    def handle(self, *args, **kwargs):
        for category in IncomeCategory.objects.all():
            total = category.incomes.aggregate(total_price=Sum('price'))['total_price'] or 0
            category.total_price = total
            category.save()
            self.stdout.write(self.style.SUCCESS(f'Updated IncomeCategory {category.name}: {total}'))

        for category in ExpenceCategory.objects.all():
            total = category.expences.aggregate(total_price=Sum('price'))['total_price'] or 0
            category.total_price = total
            category.save()
            self.stdout.write(self.style.SUCCESS(f'Updated ExpenceCategory {category.name}: {total}'))