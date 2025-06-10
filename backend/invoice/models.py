from uuid import uuid4

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from career.tasks import send_to_career
from .constants import *
from .tasks import send_driver_comment


class Invoice(models.Model):
    type = models.CharField(max_length=255, choices=TYPES)
    status = models.CharField(max_length=255, choices=STATUSES, default=STATUS_CREATED)
    org = models.ForeignKey('onec.Organization', models.PROTECT)
    specification = models.ForeignKey('onec.Specification', models.PROTECT)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.number

    @property
    def number(self):
        return f"{dict(TYPES)[str(self.type)][0]}{self.pk}"
    

class InvoiceNomenclature(models.Model):
    invoice = models.ForeignKey(Invoice, models.CASCADE)
    nomenclature = models.ForeignKey('onec.Nomenclature', models.PROTECT)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.invoice} - {self.nomenclature}'
    
    class Meta:
        unique_together = (('nomenclature', 'invoice'),)

    
class Order(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    invoice = models.ForeignKey(Invoice, models.CASCADE)
    car = models.ForeignKey('onec.Car', models.PROTECT, null=True)
    driver = models.ForeignKey('onec.Driver', models.PROTECT, null=True)
    address = models.CharField(max_length=255)
    nomenclature = models.ForeignKey('onec.Nomenclature', models.PROTECT)
    per_price = models.FloatField()
    price = models.FloatField()
    additive = models.FloatField(help_text='Добавка', blank=True, null=True)
    order = models.FloatField(help_text='Заказ')
    fact = models.FloatField(blank=True, null=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return  f"{self.invoice} - {self.nomenclature}"


class DriverComment(models.Model):
    order = models.ForeignKey(Order, models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=COMMENT_STATUSES, default=COMMENT_STATUS_LOADING)

    def __str__(self) -> str:
        return f"{self.order} - {self.text}"
    
    def send_driver_comment(self, user_id):
        return send_driver_comment.delay(self.pk, user_id)


@receiver(post_save, sender=Order, dispatch_uid="update_invoice_status_process")
def update_invoice_status_process(sender, instance: Order, **kwargs):
    if instance.invoice.status == STATUS_CREATED:
        instance.invoice.status = STATUS_PROCESS
        instance.invoice.save()
    send_to_career.delay(instance.pk)


receiver(post_delete, sender=Order, dispatch_uid="delete_order")
def delete_order(sender, instance: Order, **kwargs):
    send_to_career.delay(instance.pk, delete=True)
