# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.shortcuts import render,render_to_response,HttpResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from goods_manage.models import ClothInfo,ClothIn,ClothOut
from django.core import serializers
from django.db import connection
import json
# Create your views here.
#跳转到登录页面
def toLogin(request):
    return render_to_response('login.html')
#跳转到主页
def toIndex(request):
    return render_to_response('index.html')
#跳转到布样管理模块
def addIndex(request):
    return render_to_response('news/newgoods.html')

#跳转添加布样
def addCloth(request):
    return render_to_response('news/newsAdd.html')

#跳转到出入库管理
def manageGoods(request):
    return render_to_response('news/goodsManage.html')

#登陸驗證
@csrf_exempt
def loginSuccess(request):
    userName=password=code=''
    if request.method=='GET':
        userName=request.GET.get('userName')
        password=request.GET.get('password')
        code=request.GET.get('code')
    print(userName,password)
    if userName=='admin' and password=='xsf345':
        return HttpResponse('success')
        # return toIndex(request)
    else:
        return HttpResponse('fail')

#接口-返回所有已经添加的布样
def show_goods_list(request):
    #分页参数page/limit
    page=1
    limit=15
    if request.method=='GET':
        page=request.GET.get('page')
        limit=request.GET.get('limit')
    begin = (int(page)-1)*int(limit)
    end = int(page)*int(limit)
    #搜索关键字
    key=''
    key=request.GET.get('key')
    #json拼接
    dict={"code": 0,"msg": "","count": 15}
    list=[]
    #判断关键字是否为空，来选择执行不同的sql
    if key == None:
        list_count=ClothInfo.objects.filter(CLOTH_STATUS=1).count()
        for i in ClothInfo.objects.filter(CLOTH_STATUS=1)[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    else:
        list_count = ClothInfo.objects.filter(CLOTH_STATUS=1).filter(CLOTH_CODE__contains=key).count()
        for i in ClothInfo.objects.filter(CLOTH_STATUS=1).filter(CLOTH_CODE__contains=key)[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    dict["count"]=list_count
    dict["data"] = list
    # raw=serializers.serialize('json', ClothInfo.objects.all())
    # print dict
    return HttpResponse(json.dumps(dict,ensure_ascii=False))

def test(request):
    return render_to_response('news/test.html')

#存储/编辑布样内容
@csrf_exempt
def addClothSuccess(request):
    curdate=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    ID=''
    #获取前端数据
    if request.method=='POST':
        ID = request.POST['ID']
        newsCode=request.POST['newsCode']
        newsName=request.POST['newsName']
        newsFactory=request.POST['newsFactory']
        content=request.POST['content']
    #通过id是否为空来判断添加/编辑布样内容
    if ID=='':
        try:
            ClothInfo.objects.create(CLOTH_CODE=newsCode,CLOTH_NAME=newsName,CLOTH_FACTORY=newsFactory,CONTENT=content,CLOTH_STATUS=1,CLOTH_IMG=1,CLOTH_TOP=1,CREATE_TIME=curdate)
        except ValueError as err:
            print err
    else:
        try:
            ClothInfo.objects.filter(id=ID).update(CLOTH_CODE=newsCode,CLOTH_NAME=newsName,CLOTH_FACTORY=newsFactory,CONTENT=content)
        except ValueError as err:
            print err
    return HttpResponse('success');

#删除布样接口
@csrf_exempt
def delCloth(request):
    #批量删除商品的id
    newsID=[]
   # 删除商品的id
    newGoodID=0
    if request.method=='GET':
        newsID=request.GET.getlist('id[]')
        newGoodID=request.GET.get('id')
    print  newsID,newGoodID
    if newGoodID !=0 :
        try:
            ClothInfo.objects.filter(id=newGoodID).update(CLOTH_STATUS=0)
        except ValueError as err:
            print(err)
    if  len(newsID) != 0:
        for ID in newsID:
            try:
                ClothInfo.objects.filter(id=ID).update(CLOTH_STATUS=0)
            except ValueError as err:
                print(err)
    return HttpResponse('success');

#入库操作
@csrf_exempt
def inWareHouse(request):
    newsID=CLOTH_CODE=IN_COUNT=0
    if request.method=='GET':
        newsID=request.GET.get('id')
        CLOTH_CODE=request.GET.get('CLOTH_CODE')
        IN_COUNT=request.GET.get('IN_COUNT')
    print(CLOTH_CODE,IN_COUNT)
    #插入入库流水
    try:
        ClothIn.objects.create(CLOTH_CODE=CLOTH_CODE,CLOTH_COUNT=IN_COUNT)
    except ValueError as err:
        print(err)
    #增加库存
    try:
        clothinfo=ClothInfo.objects.get(id=newsID)
    except ValueError as err:
        print(err)
    clothinfo.CLOTH_REMAIN=clothinfo.CLOTH_REMAIN+float(IN_COUNT)
    clothinfo.save()
    return HttpResponse('success')

#出库操作
@csrf_exempt
def outWareHouse(request):
    if request.method=='GET':
        newsID=request.GET.get('id')
        CLOTH_CODE=request.GET.get('CLOTH_CODE')
        OUT_COUNT=request.GET.get('OUT_COUNT')
    #插入出库流水
    try:
        ClothOut.objects.create(CLOTH_CODE=CLOTH_CODE,CLOTH_COUNT=OUT_COUNT)
    except ValueError as err:
        print(err)
    #削减库存
    try:
        clothinfo = ClothInfo.objects.get(id=newsID)
    except ValueError as err:
        print(err)
    if clothinfo.CLOTH_REMAIN >= float(OUT_COUNT):
        clothinfo.CLOTH_REMAIN = clothinfo.CLOTH_REMAIN - float(OUT_COUNT)
        clothinfo.save()
        return HttpResponse('success')
    else:
        return HttpResponse('fail')


