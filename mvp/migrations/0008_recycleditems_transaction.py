# Generated by Django 2.2.13 on 2020-11-29 23:51

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0007_auto_20201129_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0, verbose_name='Coins Earned')),
                ('transaction_type', models.TextField(default='Credit', max_length=500, verbose_name='Transaction Type')),
                ('date_added_with_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_added', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.User')),
            ],
            options={
                'db_table': 'Transaction_table',
            },
        ),
        migrations.CreateModel(
            name='RecycledItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_manufacturer', models.TextField(max_length=500, verbose_name='Item Manufacturer')),
                ('item_barcode', models.TextField(max_length=500, verbose_name='Item Barcode')),
                ('hub', models.TextField(default='WasteCoin Hub', max_length=200, verbose_name='Hub Name')),
                ('hub_address', models.TextField(default='Lugbe 1', max_length=200, verbose_name='Address')),
                ('hub_state', models.TextField(default='Abuja', max_length=200, verbose_name='State')),
                ('hub_council_area', models.TextField(default='AMAC', max_length=200, verbose_name='LGA/Council Area')),
                ('hub_country', models.TextField(default='Nigeria', max_length=200, verbose_name='Country')),
                ('date_added_with_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_added', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.User')),
            ],
            options={
                'db_table': 'Recycled_Items_table',
            },
        ),
    ]
