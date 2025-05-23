# Generated by Django 4.1 on 2025-04-01 15:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('fullname', models.CharField(max_length=255)),
                ('inn', models.CharField(max_length=255)),
                ('kpp', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('delivery_address', models.CharField(max_length=255)),
                ('payment_deferment', models.IntegerField(blank=True, null=True)),
                ('amount_limit', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(default=0)),
                ('specification', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='onec.specification')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('price', models.FloatField()),
                ('nomenclature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onec.nomenclature')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onec.specification')),
            ],
            options={
                'unique_together': {('nomenclature', 'specification')},
            },
        ),
    ]
