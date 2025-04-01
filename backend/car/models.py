from django.db import models


class Car(models.Model):
    number = models.CharField(max_length=255, unique=True)
    marka = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    vin = models.CharField(max_length=255)
    not_weight = models.BooleanField(default=False, help_text='Не взвешивать')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to='car')

    def __str__(self) -> str:
        return self.number