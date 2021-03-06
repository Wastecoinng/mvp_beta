# Generated by Django 2.2.13 on 2020-11-26 23:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=500, unique=True)),
                ('firstname', models.CharField(blank=True, max_length=30, verbose_name='Firstname')),
                ('lastname', models.CharField(blank=True, max_length=30, verbose_name='Lastname')),
                ('user_phone', models.TextField(max_length=15, null=True, unique=True, verbose_name='Telephone number')),
                ('email', models.EmailField(max_length=90, unique=True, verbose_name='Email')),
                ('user_password', models.TextField(max_length=200, verbose_name='Password')),
                ('user_address', models.TextField(max_length=200, verbose_name='Address')),
                ('user_state', models.TextField(max_length=200, verbose_name='State')),
                ('user_council_area', models.TextField(max_length=200, verbose_name='LGA/Council Area')),
                ('user_country', models.TextField(max_length=200, verbose_name='Country')),
                ('minedCoins', models.FloatField(default=0, verbose_name='minedCoins')),
                ('account_name', models.TextField(default='Null', max_length=150, unique=True, verbose_name='Account Name')),
                ('account_number', models.TextField(default='Null', max_length=150, unique=True, verbose_name='Account Number')),
                ('bank_name', models.TextField(default='Null', max_length=150, verbose_name='Bank Name')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'user_table',
            },
        ),
        migrations.CreateModel(
            name='otp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.TextField(max_length=20, verbose_name='OTP CODE')),
                ('validated', models.BooleanField(default=False)),
                ('password_reset_code', models.TextField(default='', max_length=20, verbose_name='Reset Code')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.User')),
            ],
            options={
                'db_table': 'OTP_Code',
            },
        ),
    ]
