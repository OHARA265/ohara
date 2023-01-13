from django.db import models

from django.utils import timezone

from accounts.models import CustomUser

# Create your models here.

class Zaseki(models.Model):
    name = models.CharField('席番号',max_length=100)
    description = models.TextField('説明、概要',default="",blank=True)
    image = models.ImageField(upload_to='images',verbose_name='イメージ画像',null=True,blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, verbose_name='顧客', on_delete=models.CASCADE)
    zaseki = models.ForeignKey(Zaseki, verbose_name='個室', on_delete=models.CASCADE)
    tel = models.CharField('電話番号', max_length=100, null=True, blank=True)
    remarks = models.TextField('備考', default="", blank=True)
    start = models.DateTimeField('開始時間', default=timezone.now)
    end = models.DateTimeField('終了時間', default=timezone.now)
    today = models.DateTimeField('判定日付',default=timezone.now)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%D %H:%M')
        end = timezone.localtime(self.end).strftime('%Y/%m/%D %H:%M')
        return f'{start} ~ {end} {self.zaseki} {self.customer}'


class News(models.Model):
    day = models.DateField('日付',default=timezone.now)
    title = models.CharField('タイトル',max_length=30)
    news = models.CharField('お知らせ',max_length=1000,null=False,blank=False)
    important = models.IntegerField('重要度',default=1)