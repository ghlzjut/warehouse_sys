# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from goods_manage.models import ClothInfo,ClothIn,ClothOut,ClothDeal
# Admin控制
class ClothInfoAdmin(admin.ModelAdmin):
    list_display = ( 'CLOTH_CODE', 'CLOTH_NAME', 'CLOTH_FACTORY', 'CLOTH_STATUS', 'CLOTH_IMG','CLOTH_TOP','CREATE_TIME','CONTENT','CLOTH_REMAIN','CLOTH_DEAL_REMAIN')
admin.site.register(ClothInfo, ClothInfoAdmin)
# Register your models here.
class ClothInAdmin(admin.ModelAdmin):
    list_display = ('CLOTH_CODE', 'CLOTH_COUNT')
admin.site.register(ClothIn, ClothInAdmin)

class ClothOutAdmin(admin.ModelAdmin):
    list_display = ('CLOTH_CODE', 'CLOTH_COUNT')
admin.site.register(ClothOut, ClothOutAdmin)

class ClothDealAdmin(admin.ModelAdmin):
    list_display = ('CLOTH_CODE', 'CLOTH_COUNT')
admin.site.register(ClothDeal, ClothDealAdmin)