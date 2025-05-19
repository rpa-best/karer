from django.db import models


class Driver(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to='driver')

    def __str__(self) -> str:
        return str(self.name)

    def send_comment(self, text):
        # If error return: ConnectionError
        pass