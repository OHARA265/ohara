# Generated by Django 4.1.3 on 2022-11-22 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Zaseki',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='席番号')),
                ('description', models.TextField(blank=True, default='', verbose_name='説明、概要')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='イメージ画像')),
            ],
        ),
    ]