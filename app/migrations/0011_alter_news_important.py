# Generated by Django 4.1.3 on 2022-12-07 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_news_img_news_important'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='important',
            field=models.IntegerField(default=1, verbose_name='重要度'),
        ),
    ]
