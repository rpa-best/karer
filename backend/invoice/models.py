from uuid import uuid4
from django.db import models


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

    def __str__(self) -> str:
        return self.number

    @property
    def number(self):
        return f"{dict(TYPES)[self.type][0]}{self.id}"
    

class InvoiceNomenclature(models.Model):
    invoice = models.ForeignKey(Invoice, models.CASCADE)
    nomenclature = models.ForeignKey('onec.Nomenclature', models.PROTECT)
    value = models.FloatField()

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
    additive = models.FloatField(help_text='Добавка')
    order = models.FloatField(help_text='Заказ')
    fact = models.FloatField(blank=True, null=True)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return  f"{self.invoice} - {self.nomenclature}"
    