# Generated by Django 3.1.2 on 2021-02-09 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0017_auto_20210209_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recycleditems',
            name='collected',
        ),
        migrations.RemoveField(
            model_name='recycleditems',
            name='paid',
        ),
        migrations.AddField(
            model_name='user',
            name='totalDelivered',
            field=models.IntegerField(default=0, verbose_name='Total plastics Delivered'),
        ),
        migrations.AddField(
            model_name='user',
            name='totalNotDelivered',
            field=models.IntegerField(default=0, verbose_name='Total plastics not Delivered'),
        ),
        migrations.AddField(
            model_name='user',
            name='totalRecyled',
            field=models.IntegerField(default=100, verbose_name='Total plastics recycled'),
        ),
    ]
