# Generated by Django 4.1.3 on 2022-12-06 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_news_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='day',
            field=models.DateTimeField(default='2000/01/01', max_length=50, verbose_name='日付'),
        ),
    ]
