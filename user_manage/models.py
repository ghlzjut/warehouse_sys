# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class user_info(models.Model):
    #用户名
    USER_NAME=models.CharField(max_length=50)
    #密码
    PASSWORD=models.CharField(max_length=50)
    #商户名
    SUPPLIER_NAME=models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s %s %s' % (self.USER_NAME,self.PASSWORD,self.SUPPLIER_NAME)