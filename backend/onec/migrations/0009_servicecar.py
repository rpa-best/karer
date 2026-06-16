from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('onec', '0008_car_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCar',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('reg_number', models.CharField(blank=True, max_length=255, null=True)),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('our_prorerty', models.BooleanField(default=False)),
                ('trailer_reg_number', models.CharField(blank=True, max_length=255, null=True)),
                ('trailer_brand', models.CharField(blank=True, max_length=255, null=True)),
                ('not_weight', models.BooleanField(default=False, help_text='Не взвешивать')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='service_car')),
            ],
        ),
    ]
