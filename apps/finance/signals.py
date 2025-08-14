from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from apps.finance.models import Income, IncomeCategory

@receiver(pre_save, sender=Income)
def update_income_category_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Income.objects.get(pk=instance.pk)
        instance.category.total_price -= old_instance.price

@receiver(post_save, sender=Income)
def update_income_category_post_save(sender, instance, **kwargs):
    instance.category.total_price += instance.price
    instance.category.save()

@receiver(post_delete, sender=Income)
def update_income_category_delete(sender, instance, **kwargs):
    instance.category.total_price -= instance.price
    instance.category.save()