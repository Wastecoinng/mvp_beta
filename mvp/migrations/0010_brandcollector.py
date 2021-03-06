# Generated by Django 2.2.13 on 2020-11-30 14:52

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0009_manufacturer'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandCollector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.TextField(max_length=500, verbose_name='Item brand')),
                ('barcode_identification', models.TextField(max_length=500, verbose_name='Item Barcode Identification')),
                ('date_added_with_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_added', models.DateField(default=datetime.date.today)),
            ],
            options={
                'db_table': 'Brand_collector_table',
            },
        ),
    ]
