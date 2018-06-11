 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib import admin

class ClothInfo(models.Model):
    #布样ID
    # ID = models.AutoField()
    #布样编码
    CLOTH_CODE =  models.CharField(max_length=10, default="")
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

class WhiteClothInfo(models.Model):
    # 布样编码
    CLOTH_CODE = models.CharField(max_length=10, default="")
    # 布样名称
    CLOTH_NAME = models.CharField(max_length=50, default="")
    # 仓库余量
    CLOTH_REMAIN = models.FloatField(default=0.0)
    # 布样加工数量
    CLOTH_DEAL_REMAIN = models.FloatField(default=0.0)

    # 返回模版信息
    def __unicode__(self):
        return u'%s %s %s %s %s' % (self.id,self.CLOTH_CODE, self.CLOTH_NAME,self.CLOTH_REMAIN,self.CLOTH_DEAL_REMAIN)

#布匹入库流水
class ClothIn(models.Model):
    # 布样编码
    CLOTH_CODE = models.CharField(max_length=10, default="")
    #入库数量
    CLOTH_COUNT = models.FloatField(default=0.0)

    # 返回模版信息
    def __unicode__(self):
        return u'%s %s' % (self.CLOTH_CODE,self.CLOTH_COUNT)

#布匹出库流水
class ClothOut(models.Model):
    # 布样编码
    CLOTH_CODE = models.CharField(max_length=10, default="")
    #出库数量
    CLOTH_COUNT = models.FloatField(default=0.0)
    #客戶姓名
    CUSTOMER = models.CharField(max_length=50,default="")
    #布匹单价（元/米）
    AMOUNT =  models.FloatField(default=0.0)
    #出库时间
    CREATE_TIME = models.DateField(auto_now=False)
    # 返回模版信息
    def __unicode__(self):
        return u'%s %s %s' % (self.CLOTH_CODE, self.CLOTH_COUNT,self.CUSTOMER)

#布匹出厂加工流水
class ClothDeal(models.Model):
    # 布样编码
    CLOTH_CODE = models.CharField(max_length=10, default="")
    #入库数量
    CLOTH_COUNT = models.FloatField(default=0.0)

    # 返回模版信息
    def __unicode__(self):
        return u'%s %s' % (self.CLOTH_CODE, self.CLOTH_COUNT)

#布匹库存信息
class ClothPieceInfo(models.Model):
    # 布样编码
    CLOTH_CODE = models.CharField(max_length=10, default="")
    #布匹数量
    CLOTH_PIECE = models.FloatField(default=0.0)
    #布匹米数
    CLOTH_PIECE_COUNT = models.FloatField(default=0.0)
    #备注
    REMARKS=models.CharField(max_length=100,default="-")
    #码单号
    ORDER_ID=models.IntegerField(default=0)
    # 返回模版信息
    def __unicode__(self):
        return u'%s %s %s %s' % (self.CLOTH_CODE, self.CLOTH_PIECE,self.CLOTH_PIECE_COUNT,self.REMARKS,self.ORDER_ID)

#码单信息
class ClothOrder(models.Model):
    #客戶姓名
    CUSTOMER = models.CharField(max_length=50,default="")
    # 布匹数量
    CLOTH_PIECE = models.IntegerField(default=0)
    # 出库米数
    CLOTH_COUNT = models.FloatField(default=0.0)
    # 布匹总价
    AMOUNT = models.FloatField(default=0.0)
    #下单时间
    ORDER_TIME = models.DateField(auto_now=False)

    # 返回模版信息
    def __unicode__(self):
        return u'%s %s %s %s %s' %(self.CUSTOMER,self.CLOTH_PIECE,self.CLOTH_COUNT,self.AMOUNT,self.ORDER_TIME)
