# Generated by Django 4.1.3 on 2022-12-02 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='day',
            field=models.CharField(default='2000/01/01', max_length=50, verbose_name='日付'),
        ),
    ]
