from uuid import uuid4
from django.db import models


class Nomenclature(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Organization(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    inn = models.CharField(max_length=255)
    kpp = models.CharField(max_length=255)
    do_not_display_volume = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Specification(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    payment_deferment = models.IntegerField(blank=True, null=True)
    amount_limit = models.FloatField(blank=True, null=True)
    organization = models.ForeignKey(Organization, models.CASCADE, null=True, blank=True)
    nomenclatures = models.ManyToManyField(Nomenclature, blank=True)

    def __str__(self):
        return self.name
    

class Price(models.Model):
    nomenclature = models.ForeignKey(Nomenclature, models.CASCADE)
    specification = models.ForeignKey(Specification, models.CASCADE)
    date = models.DateTimeField()
    price = models.FloatField()

    def __str__(self) -> str:
        return f"{self.nomenclature} ({self.specification})"
    
    class Meta:
        unique_together = (('nomenclature', 'specification'),)


class Balance(models.Model):
    specification = models.OneToOneField(Specification, models.CASCADE)
    balance = models.FloatField(default=0)

    def __str__(self):
        return f"{self.specification}-----{self.balance}"


class Car(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    reg_number = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    our_prorerty = models.BooleanField(default=False)
    trailer_reg_number = models.CharField(max_length=255, blank=True, null=True)
    trailer_brand = models.CharField(max_length=255, blank=True, null=True)
    
    not_weight = models.BooleanField(default=False, help_text='Не взвешивать')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to='car')

    def __str__(self):
        return self.name
    

class Driver(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    inn = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    drivers_license_series = models.CharField(max_length=255, blank=True, null=True)
    drivers_license_number = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to='driver')
    telegram_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
