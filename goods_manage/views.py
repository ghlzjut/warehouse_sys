# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db.models import QuerySet
from django.shortcuts import render,render_to_response,HttpResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from goods_manage.models import ClothInfo,ClothIn,ClothOut,ClothDeal,ClothPieceInfo
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

#跳转到出库管理
def manageGoodsOut(request):
    return render_to_response('news/goodsManageOut.html')

#跳转到入库管理
def manageGoodsIn(request):
    return render_to_response('news/goodsManage.html')

#跳转出厂加工
def dealGoods(request):
    return render_to_response('news/goodsDeal.html')

#跳转到加工完成入库
def dealGoodsIn(request):
    return render_to_response('news/re_goodsDeal.html')

#跳转到布匹查询
def addPieceGoods(request):
    return render_to_response('news/newsPieceGoods.html')

#跳转到布匹添加
def queryPieceGoods(request):
    return render_to_response('news/queryPieceGoods.html')

#报表数据结转
def getCustomer(request):
    customer_list=[]
    cursor=connection.cursor()
    for i in cursor.execute('SELECT CUSTOMER FROM goods_manage_clothout GROUP BY CUSTOMER '):
        dict={}
        dict["CUSTOMER"]=i[0]
        customer_list.append(dict)
    print  customer_list
    return HttpResponse(json.dumps(customer_list))

#跳转到财务报表
def Report(request):
    customer_list = []
    cursor = connection.cursor()
    for i in cursor.execute('SELECT CUSTOMER FROM goods_manage_clothout GROUP BY CUSTOMER '):
        customer_list.append(i[0])
    return render_to_response('REPORT/financialReport.html',{'customer_list':json.dumps(customer_list)})

#登陸驗證
@csrf_exempt
def loginSuccess(request):
    userName=password=code=''
    if request.method=='GET':
        userName=request.GET.get('userName')
        password=request.GET.get('password')
        code=request.GET.get('code')
    # print(userName,password)
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
        if request.GET.get('page'):
            page=request.GET.get('page')
        if request.GET.get('limit'):
            limit=request.GET.get('limit')
    begin = (int(page)-1)*int(limit)
    end = int(page)*int(limit)
    #搜索关键字
    key=''
    if request.GET.get('key'):
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

#接口--布匹库存查询
def showPieceGoods(request):
    #分页参数page/limit
    page=1
    limit=15
    if request.method=='GET':
        if request.GET.get('page'):
            page=request.GET.get('page')
        if request.GET.get('limit'):
            limit=request.GET.get('limit')
    begin = (int(page)-1)*int(limit)
    end = int(page)*int(limit)
    #搜索关键字
    key=''
    if request.GET.get('key'):
        key=request.GET.get('key')
    #json拼接
    dict={"code": 0,"msg": "","count": 15}
    list=[]
    #判断关键字是否为空，来选择执行不同的sql
    if key == None:
        list_count=ClothPieceInfo.objects.all().count()
        for i in ClothPieceInfo.objects.all()[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    else:
        list_count = ClothPieceInfo.objects.all().filter(CLOTH_CODE__contains=key).count()
        for i in ClothPieceInfo.objects.all().filter(CLOTH_CODE__contains=key)[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    dict["count"]=list_count
    dict["data"] = list
    return HttpResponse(json.dumps(dict,ensure_ascii=False))

def test(request):
    return render_to_response('news/test.html')

#存储/编辑布样内容
@csrf_exempt
def addClothSuccess(request):
    curdate=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    ID=''
    CLOTH_REMAIN=CLOTH_DEAL_REMAIN=0
    #获取前端数据
    if request.method=='POST':
        ID = request.POST['ID']
        newsCode=request.POST['newsCode']
        newsName=request.POST['newsName']
        newsFactory=request.POST['newsFactory']
        content=request.POST['content']
        if request.POST['CLOTH_REMAIN']:
            CLOTH_REMAIN=request.POST['CLOTH_REMAIN']
        if request.POST['CLOTH_DEAL_REMAIN'] :
            CLOTH_DEAL_REMAIN=request.POST['CLOTH_DEAL_REMAIN']
    #通过id是否为空来判断添加/编辑布样内容
    if ID=='':
        try:
            ClothInfo.objects.create(CLOTH_CODE=newsCode,CLOTH_NAME=newsName,CLOTH_FACTORY=newsFactory,CONTENT=content,CLOTH_STATUS=1,CLOTH_IMG=1,CLOTH_TOP=1,CREATE_TIME=curdate,CLOTH_REMAIN=CLOTH_REMAIN,CLOTH_DEAL_REMAIN=CLOTH_DEAL_REMAIN)
        except ValueError as err:
            print err
    else:
        try:
            ClothInfo.objects.filter(id=ID).update(CLOTH_CODE=newsCode,CLOTH_NAME=newsName,CLOTH_FACTORY=newsFactory,CONTENT=content,CLOTH_REMAIN=CLOTH_REMAIN,CLOTH_DEAL_REMAIN=CLOTH_DEAL_REMAIN)
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
    # print  newsID,newGoodID
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
    # print(CLOTH_CODE,IN_COUNT)
    #插入入库流水
    try:
        ClothIn.objects.create(CLOTH_CODE=CLOTH_CODE,CLOTH_COUNT=IN_COUNT)
    except ValueError as err:
        print(err)
    except:
        return HttpResponse('notNull')
    #增加库存
    try:
        clothinfo=ClothInfo.objects.get(id=newsID)
        clothinfo.CLOTH_REMAIN = clothinfo.CLOTH_REMAIN + float(IN_COUNT)
        clothinfo.save()
        return HttpResponse('success')
    except ValueError as err:
        return HttpResponse('ValueError')

#出库操作
@csrf_exempt
def outWareHouse(request):
    curdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if request.method=='GET':
        newsID=request.GET.get('id')
        CLOTH_CODE=request.GET.get('CLOTH_CODE')
        CUSTOMER=request.GET.get('CUSTOMER')
        OUT_COUNT=request.GET.get('OUT_COUNT')
        AMOUNT=request.GET.get('AMOUNT')
    #插入出库流水
    print  AMOUNT
    try:
        ClothOut.objects.create(CLOTH_CODE=CLOTH_CODE,CLOTH_COUNT=OUT_COUNT,CUSTOMER=CUSTOMER,AMOUNT=AMOUNT,CREATE_TIME=curdate)
    except ValueError as err:
        print(err)
    except :
        return HttpResponse('notNull')
    #削减库存
    try:
        clothinfo = ClothInfo.objects.get(id=newsID)
    except ValueError as err:
        print(err)
    try:
        if clothinfo.CLOTH_REMAIN >= float(OUT_COUNT):
            clothinfo.CLOTH_REMAIN =round(clothinfo.CLOTH_REMAIN - float(OUT_COUNT),2)
            clothinfo.save()
            return HttpResponse('success')
        else:
            return HttpResponse('fail')
    except ValueError as err:
        return HttpResponse('ValueError')

#出库加工
def dealWareHouse(request):
    if request.method=='GET':
        newsID=request.GET.get('id')
        CLOTH_CODE=request.GET.get('CLOTH_CODE')
        DEAL_COUNT=request.GET.get('DEAL_COUNT')
    #插入出库加工流水
    try:
        ClothDeal.objects.create(CLOTH_CODE=CLOTH_CODE,CLOTH_COUNT=DEAL_COUNT)
    except ValueError as err:
        print(err)
    except:
        return HttpResponse('notNull')
    #削减库存
    clothinfo = ClothInfo.objects.get(id=newsID)
    try:
        if clothinfo.CLOTH_REMAIN >= float(DEAL_COUNT):
            clothinfo.CLOTH_REMAIN =round(clothinfo.CLOTH_REMAIN - float(DEAL_COUNT),2)
            clothinfo.save()
        else:
            return HttpResponse('fail')
    except ValueError as err:
        return HttpResponse('ValueError')
    #增加出厂加工数量
    try:
        clothinfo=ClothInfo.objects.get(id=newsID)
        clothinfo.CLOTH_DEAL_REMAIN = clothinfo.CLOTH_DEAL_REMAIN + float(DEAL_COUNT)
        clothinfo.save()
        return HttpResponse('success')
    except ValueError as err:
        print err

#加工完成入库
def dealWareHouseIn(request):
    if request.method=='GET':
        newsID=request.GET.get('id')
        CLOTH_CODE=request.GET.get('CLOTH_CODE')
        DEAL_COUNT=request.GET.get('DEAL_COUNT')
    #削減出厂加工数量
    try:
        clothinfo=ClothInfo.objects.get(id=newsID)
        # print clothinfo.CLOTH_DEAL_REMAIN,DEAL_COUNT
        if clothinfo.CLOTH_DEAL_REMAIN >= float(DEAL_COUNT):
            clothinfo.CLOTH_DEAL_REMAIN = round(clothinfo.CLOTH_DEAL_REMAIN - float(DEAL_COUNT),2)
            clothinfo.save()
        else:
            return HttpResponse('fail')
    except ValueError as err:
        return HttpResponse('ValueError')
    #增加库存
    clothinfo = ClothInfo.objects.get(id=newsID)
    try:
        clothinfo.CLOTH_REMAIN =clothinfo.CLOTH_REMAIN + float(DEAL_COUNT)
        clothinfo.save()
        return HttpResponse('success')
    except ValueError as err:
        return HttpResponse('ValueError')

#统计报表接口
def financialReport(request):
    beginDate='2018-01-01 00:00:00'
    endDate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if request.method=='GET':
        customer=request.GET.get('CUSTOMER')
        #判断时间是否为空，为空则不赋值
        if request.GET.get('BEGINDATE'):
            beginDate=request.GET.get('BEGINDATE')
        if request.GET.get('ENDDATE'):
            endDate=request.GET.get('ENDDATE')
        page = request.GET.get('page')
        limit = request.GET.get('limit')
    begin = (int(page)-1)*int(limit)
    end = int(page)*int(limit)
    #定义数据库连接
    cursor=connection.cursor()
    query='SELECT CUSTOMER,CLOTH_CODE,sum(CLOTH_COUNT) as COUNT,AMOUNT,sum(CLOTH_COUNT*AMOUNT) as ALL_AMOUNT from goods_manage_clothout WHERE CREATE_TIME BETWEEN %s AND %s AND CUSTOMER = %s GROUP BY CUSTOMER,CLOTH_CODE,AMOUNT limit %s,%s'
    dict = {"code": 0, "msg": "", "count": 15}
    list = []
    for i in cursor.execute(query,[beginDate,endDate,customer,begin,end]):
        dict1 = {}
        dict1["CUSTOMER"]=i[0]
        dict1["CLOTH_CODE"]=i[1]
        dict1["COUNT"]=i[2]
        dict1["AMOUNT"]=i[3]
        dict1["ALL_AMOUNT"]=i[4]
        list.append(dict1)
    dict["count"]=len(list)
    dict["data"]=list
    return HttpResponse(json.dumps(dict,ensure_ascii=False))

def delPeiceGoods(request):
    # 批量删除商品的id
    newsID = []
    # 删除商品的id
    newGoodID = 0
    if request.method == 'GET':
        if request.GET.getlist('id[]'):
            newsID = request.GET.getlist('id[]')
        if request.GET.get('id'):
            newGoodID = request.GET.get('id')
    # print  newsID,newGoodID
    if newGoodID != 0:
        try:
            ClothPieceInfo.objects.filter(id=newGoodID).delete()
        except ValueError as err:
            print(err)
    if len(newsID) != 0:
        for ID in newsID:
            try:
                ClothPieceInfo.objects.filter(id=ID).delete()
            except ValueError as err:
                print(err)
    return HttpResponse('success');
def addPieceGoodsAction(request):
    CLOTH_CODE=CLOTH_PIECE=CLOTH_PIECE_COUNT=0
    if request.method=='GET':
        if request.GET.get('CLOTH_CODE'):
            CLOTH_CODE=request.GET.get('CLOTH_CODE')
        if request.GET.get('CLOTH_PIECE'):
            CLOTH_PIECE=request.GET.get('CLOTH_PIECE')
        if request.GET.get('CLOTH_PIECE_COUNT'):
            CLOTH_PIECE_COUNT=request.GET.get('CLOTH_PIECE_COUNT')
    if CLOTH_PIECE==0:
        return HttpResponse('pieceFailed')
    if CLOTH_PIECE_COUNT==0:
        return HttpResponse('pieceCountFailed')
    try:
        ClothPieceInfo.objects.create(CLOTH_CODE=CLOTH_CODE,CLOTH_PIECE=CLOTH_PIECE,CLOTH_PIECE_COUNT=CLOTH_PIECE_COUNT)
    except:
        return  HttpResponse('fail')
    return HttpResponse('success')

def editPeiceGoods(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            id = request.GET.get('id')
        if request.GET.get('CLOTH_PIECE'):
            CLOTH_PIECE = request.GET.get('CLOTH_PIECE')
    try:
        ClothPieceInfo.objects.filter(id=id).update(CLOTH_PIECE=CLOTH_PIECE)
    except ValueError as err:
        return HttpResponse(err)
    return HttpResponse('success')