from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
# content types
# django.contrib.conttenttypes
# ContentType
# app_label 数据模型所属的应用名称
class Action(models.Model):
    user = models.ForeignKey('auth.User',related_name='action',db_index=True,on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='target_obj',on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,blank=True,db_index=True)
    target = GenericForeignKey('target_ct','target_id')
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        db_table='action'
        ordering = ('-created',)










