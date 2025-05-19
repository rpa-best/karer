from uuid import uuid4

from celery import shared_task
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from career.tasks import send_to_career

TYPE_PREPAYMENT = 'prepayment'
TYPE_DEFERMENT_PAYMENT = 'deferment_payment'
TYPE_LIMIT = 'limit'
TYPES = (
    (TYPE_PREPAYMENT, 'Предоплата'),
    (TYPE_DEFERMENT_PAYMENT, 'Отсрочка платежа'),
    (TYPE_LIMIT, 'Лимит')
)

STATUS_CREATED = 'created'
STATUS_PROCESS = 'process'
STATUS_DONE = 'done'
STATUS_CANCELED = 'canceled'
STATUSES = (
    (STATUS_CREATED, 'Принято'),
    (STATUS_PROCESS, 'В обработке'),
    (STATUS_DONE, 'Успешно'),
    (STATUS_CANCELED, 'Отклонено')
)


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
    car = models.ForeignKey('car.Car', models.PROTECT)
    driver = models.ForeignKey('driver.Driver', models.PROTECT)
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
    driver_comments = models.JSONField(default=list)

    def __str__(self) -> str:
        return  f"{self.invoice} - {self.nomenclature}"

    @shared_task
    def send_driver_comment(self, text):
        comment = {
            'uuid': uuid4(),
            'status': 'loading',
            'comment': text
        }
        self.driver_comments.append(comment)
        self.save()
        try:
            self.driver.send_comment(text)
            comment['status'] = 'ok'
        except ConnectionError:
            comment['status'] = 'error'
        for c in self.driver_comments:
            if c['uuid'] == comment['uuid']:
                c['status'] = comment['status']
                break
        self.save()
    

@receiver(post_save, sender=Order, dispatch_uid="update_invoice_status_process")
def update_invoice_status_process(sender, instance: Order, **kwargs):
    if instance.invoice.status == STATUS_CREATED:
        instance.invoice.status = STATUS_PROCESS
        instance.invoice.save()
    send_to_career.delay(instance.pk)
