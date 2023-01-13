from django.db import models

from django.contrib.auth.models import AbstractUser, PermissionsMixin

class CustomUser(AbstractUser):

        class Meta:
                verbose_name_plural = 'CustomUser'
                db_table = 'custom_user'

        nickname = models.CharField(max_length=50,default=('大原'))
        address =models.CharField(max_length=300)
        tel = models.CharField(max_length=50,null=True,blank=True)
        birth = models.CharField(max_length=50)
        booking_kazu = models.IntegerField(default=0) 
        post_code = models.IntegerField(default=('4801234'))
        raikan_kazu = models.IntegerField(default=0)
    
