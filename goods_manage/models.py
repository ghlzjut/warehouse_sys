 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib import admin

class ClothInfo(models.Model):
    #布样ID
    # ID = models.AutoField(primary_key=True)
    #布样编码
    CLOTH_CODE = models.CharField(max_length=10,default="")
    # 布样名称
    CLOTH_NAME = models.CharField(max_length=50,default="")
    # 布样厂商
    CLOTH_FACTORY = models.CharField(max_length=100,default="")
    # 布样创建状态
    CLOTH_STATUS = models.IntegerField(default="1")
    # 布样样例图
    CLOTH_IMG = models.CharField(max_length=100,default="")
    # 布样置顶
    CLOTH_TOP = models.IntegerField(default="")
    # 布样时间
    CREATE_TIME = models.CharField(max_length=100, default="2018-05-01")
    # 布样介绍
    CONTENT = models.TextField(max_length=255,default="")
    #仓库余量
    CLOTH_REMAIN = models.FloatField(default=0.0)
    #布样加工数量
    CLOTH_DEAL_REMAIN = models.FloatField(default=0.0)

    # 返回模版信息
    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s' % (self.id,self.CLOTH_CODE, self.CLOTH_NAME, self.CLOTH_FACTORY,self.CLOTH_STATUS,self.CLOTH_IMG,self.CLOTH_TOP,self.CREATE_TIME,self.CONTENT,self.CLOTH_REMAIN,self.CLOTH_DEAL_REMAIN)

class ClothIn(models.Model):
    # 布样编码
    CLOTH_CODE = models.CharField(max_length=10, default="")
    #入库数量
    CLOTH_COUNT = models.FloatField(default=0.0)

    # 返回模版信息
    def __unicode__(self):
        return u'%s %s' % (self.CLOTH_CODE,self.CLOTH_COUNT)

class ClothOut(models.Model):
    # 布样编码
    CLOTH_CODE = models.CharField(max_length=10, default="")
    #入库数量
    CLOTH_COUNT = models.FloatField(default=0.0)

    # 返回模版信息
    def __unicode__(self):
        return u'%s %s' % (self.CLOTH_CODE, self.CLOTH_COUNT)

class ClothDeal(models.Model):
    # 布样编码
    CLOTH_CODE = models.CharField(max_length=10, default="")
    #入库数量
    CLOTH_COUNT = models.FloatField(default=0.0)

    # 返回模版信息
    def __unicode__(self):
        return u'%s %s' % (self.CLOTH_CODE, self.CLOTH_COUNT)
