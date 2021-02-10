# Generated by Django 3.1.2 on 2021-02-09 12:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0016_notification_ratings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hub_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hub_id', models.CharField(max_length=500, unique=True)),
                ('firstname', models.CharField(blank=True, max_length=30, verbose_name='Firstname')),
                ('lastname', models.CharField(blank=True, max_length=30, verbose_name='Lastname')),
                ('hub_phone', models.TextField(max_length=15, null=True, unique=True, verbose_name='Telephone number')),
                ('email', models.EmailField(max_length=90, unique=True, verbose_name='Email')),
                ('hub_password', models.TextField(max_length=200, verbose_name='Password')),
                ('hub_address', models.TextField(max_length=200, verbose_name='Address')),
                ('hub_state', models.TextField(max_length=200, verbose_name='State')),
                ('hub_council_area', models.TextField(max_length=200, verbose_name='LGA/Council Area')),
                ('hub_country', models.TextField(max_length=200, verbose_name='Country')),
                ('total_items_collected', models.FloatField(default=0, verbose_name='Total Plastics collected')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'hub_user_table',
            },
        ),
        migrations.AddField(
            model_name='recycleditems',
            name='collected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recycleditems',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]