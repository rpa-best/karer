from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0009_alter_order_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicenomenclature',
            name='volume_coefficient',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='order',
            name='volume_coefficient',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
