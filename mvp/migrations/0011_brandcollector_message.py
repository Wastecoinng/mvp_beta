# Generated by Django 3.1.2 on 2020-12-25 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0010_brandcollector'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandcollector',
            name='message',
            field=models.TextField(default='hello admin!', max_length=500, verbose_name='Feedback Message'),
        ),
    ]
