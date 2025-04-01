from uuid import uuid4
from django.db import models


class Organization(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    inn = models.CharField(max_length=255)
    kpp = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Specification(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    payment_deferment = models.IntegerField(blank=True, null=True)
    amount_limit = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    

class Nomenclature(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    

class Price(models.Model):
    nomenclature = models.ForeignKey(Nomenclature, models.CASCADE)
    specification = models.ForeignKey(Specification, models.CASCADE)
    date = models.DateField()
    price = models.FloatField()

    def __str__(self) -> str:
        return f"{self.nomenclature} ({self.specification})"
    
    class Meta:
        unique_together = (('nomenclature', 'specification'),)


class Balance(models.Model):
    specification = models.OneToOneField(Specification, models.CASCADE)
    balance = models.FloatField(default=0)
