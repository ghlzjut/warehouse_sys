# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import datetime
from django.db.models import QuerySet
from django.shortcuts import render,render_to_response,HttpResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from goods_manage.models import ClothInfo,ClothIn,ClothOut,ClothDeal,ClothPieceInfo,WhiteClothInfo,ClothOrder
from django.core import serializers
from django.db import connection
import json
# Create your views here.

#时间类型json
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

#跳转到登录页面
def toLogin(request):
    return render_to_response('login.html')


#跳转到主页
@csrf_exempt
def toIndex(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
    if username=='admin'and password=='xsf345':
        return render_to_response('index.html')
    else:
        return HttpResponse('密码错误')
#跳转到布样管理模块
def addIndex(request):
    return render_to_response('news/newgoods.html')

#跳转添加布样
def addCloth(request):
    return render_to_response('news/newsAdd.html')

#跳转添加白胚布样
def addWhiteCloth(request):
    return render_to_response('news/whiteNewsAdd.html')

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

#跳转到白胚布管理
def toWhiteCloth(request):
    return render_to_response('news/whilteNewsGoods.html')

#跳转到出库详情
def goodsManageOutInfo(request):
    return render_to_response('news/goodsManagerOutInfo.html')

#跳转到码单管理
def orderManage(request):
    return render_to_response('news/newOrder.html')

#跳转到码单添加
def addOrder(request):
    return render_to_response('news/AddOrder.html')

#跳转到码单信息
def setOrderInfo(request):
    return render_to_response('news/setOrderInfo.html')

#跳转到码单详情
def orderDetail(request):
    return render_to_response('news/OrderDetail.html')

#报表数据结转
def getCustomer(request):
    customer_list=[]
    cursor=connection.cursor()
    for i in cursor.execute('SELECT CUSTOMER FROM goods_manage_clothorder GROUP BY CUSTOMER '):
        dict={}
        dict["CUSTOMER"]=i[0]
        customer_list.append(dict)
    print  customer_list
    return HttpResponse(json.dumps(customer_list))

#跳转到财务报表
def Report(request):
    customer_list = []
    cursor = connection.cursor()
    for i in cursor.execute('SELECT CUSTOMER FROM goods_manage_clothorder GROUP BY CUSTOMER '):
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
    end = int(limit)
    #搜索关键字
    key=''
    if request.GET.get('key'):
        key=request.GET.get('key')
    #json拼接
    dict={"code": 0,"msg": "","count": 15}
    list=[]
    #判断关键字是否为空，来选择执行不同的sql
    if key == '':
        list_count = ClothInfo.objects.filter(CLOTH_STATUS=1).count()
        cursor = connection.cursor()
        query='SELECT i.id,i.CLOTH_CODE,i.CLOTH_NAME,i.CLOTH_FACTORY,sum(p.CLOTH_PIECE_COUNT) AS CLOTH_REMAIN,i.CREATE_TIME,i.CONTENT,i.CLOTH_DEAL_REMAIN FROM goods_manage_clothinfo i LEFT JOIN goods_manage_clothpieceinfo p ON i.CLOTH_CODE = p.CLOTH_CODE WHERE CLOTH_STATUS = 1 GROUP BY i.CLOTH_CODE LIMIT %s,%s'
        for i in cursor.execute(query,[begin,end]):
            dict1={}
            dict1["id"]=i[0]
            dict1["CLOTH_CODE"]=i[1]
            dict1["CLOTH_NAME"]=i[2]
            dict1["CLOTH_FACTORY"]=i[3]
            if i[4]==None:
                dict1["CLOTH_REMAIN"]=0
            else:
                dict1["CLOTH_REMAIN"] = round(i[4],2)
            dict1["CREATE_TIME"]=i[5]
            dict1["CONTENT"] = i[6]
            dict1["CLOTH_DEAL_REMAIN"] = i[7]
            list.append(dict1)
    else:
        print type(key)
        list_count = ClothInfo.objects.filter(CLOTH_STATUS=1).filter(CLOTH_CODE__contains=key).count()
        key=key+'%'
        cursor = connection.cursor()
        query='SELECT i.id,i.CLOTH_CODE,i.CLOTH_NAME,i.CLOTH_FACTORY,sum(p.CLOTH_PIECE_COUNT) AS CLOTH_REMAIN,i.CREATE_TIME,i.CONTENT,i.CLOTH_DEAL_REMAIN FROM goods_manage_clothinfo i LEFT JOIN goods_manage_clothpieceinfo p ON i.CLOTH_CODE = p.CLOTH_CODE WHERE CLOTH_STATUS = 1 AND i.CLOTH_CODE LIKE %s GROUP BY i.CLOTH_CODE LIMIT %s,%s'
        for i in cursor.execute(query,[key,begin,end]):
            dict1 = {}
            dict1["id"]=i[0]
            dict1["CLOTH_CODE"] = i[1]
            dict1["CLOTH_NAME"] = i[2]
            dict1["CLOTH_FACTORY"] = i[3]
            if i[4]==None:
                dict1["CLOTH_REMAIN"]=0
            else:
                dict1["CLOTH_REMAIN"] = round(i[4],2)
            dict1["CREATE_TIME"] = i[5]
            dict1["CONTENT"] = i[6]
            dict1["CLOTH_DEAL_REMAIN"] = i[7]
            list.append(dict1)
    dict["count"]=list_count
    dict["data"] = list
    # raw=serializers.serialize('json', ClothInfo.objects.all())
    # print dict
    return HttpResponse(json.dumps(dict,ensure_ascii=False))

#接口-返回所有已经添加的白胚布样
def show_white_cloth(request):
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
        list_count=WhiteClothInfo.objects.all().count()
        for i in WhiteClothInfo.objects.all()[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    else:
        list_count = WhiteClothInfo.objects.all().filter(CLOTH_CODE__contains=key).count()
        for i in WhiteClothInfo.objects.all().filter(CLOTH_CODE__contains=key)[begin:end]:
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
        list_count=ClothPieceInfo.objects.all().filter(ORDER_ID=0).count()
        for i in ClothPieceInfo.objects.all().filter(ORDER_ID=0)[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    else:
        list_count = ClothPieceInfo.objects.all().filter(ORDER_ID=0).filter(CLOTH_CODE__contains=key).count()
        for i in ClothPieceInfo.objects.all().filter(ORDER_ID=0).filter(CLOTH_CODE__contains=key)[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    dict["count"]=list_count
    dict["data"] = list
    return HttpResponse(json.dumps(dict,ensure_ascii=False))

#接口--出库详情查询
def showGoodsOut(request):
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
        list_count=ClothOut.objects.all().count()
        for i in ClothOut.objects.all()[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    else:
        list_count = ClothOut.objects.all().filter(CLOTH_CODE__contains=key).count()
        for i in ClothOut.objects.all().filter(CLOTH_CODE__contains=key)[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    dict["count"]=list_count
    dict["data"] = list
    return HttpResponse(json.dumps(dict,ensure_ascii=False,cls=CJsonEncoder))

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

#添加白胚布布样
@csrf_exempt
def addWhiteClothSuccess(request):
    ID=''
    CLOTH_REMAIN=CLOTH_DEAL_REMAIN=0
    #获取前端数据
    if request.method=='POST':
        ID = request.POST['ID']
        newsCode=request.POST['newsCode']
        newsName=request.POST['newsName']
        if request.POST['CLOTH_REMAIN']:
            CLOTH_REMAIN=request.POST['CLOTH_REMAIN']
        if request.POST['CLOTH_DEAL_REMAIN'] :
            CLOTH_DEAL_REMAIN=request.POST['CLOTH_DEAL_REMAIN']
    #通过id是否为空来判断添加/编辑布样内容
    if ID=='':
        try:
            WhiteClothInfo.objects.create(CLOTH_CODE=newsCode,CLOTH_NAME=newsName,CLOTH_REMAIN=CLOTH_REMAIN,CLOTH_DEAL_REMAIN=CLOTH_DEAL_REMAIN)
        except ValueError as err:
            print err
    else:
        try:
            WhiteClothInfo.objects.filter(id=ID).update(CLOTH_CODE=newsCode,CLOTH_NAME=newsName,CLOTH_REMAIN=CLOTH_REMAIN,CLOTH_DEAL_REMAIN=CLOTH_DEAL_REMAIN)
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

#删除白胚布样接口
@csrf_exempt
def delWhiteCloth(request):
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
            WhiteClothInfo.objects.filter(id=newGoodID).delete()
        except ValueError as err:
            print(err)
    if  len(newsID) != 0:
        for ID in newsID:
            try:
                WhiteClothInfo.objects.filter(id=ID).delete()
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
    curdate = time.strftime("%Y-%m-%d", time.localtime())
    if request.method=='GET':
        newsID=request.GET.get('id')
        CLOTH_CODE=request.GET.get('CLOTH_CODE')
        CUSTOMER=request.GET.get('CUSTOMER')
        OUT_COUNT=request.GET.get('OUT_COUNT')
        AMOUNT=request.GET.get('AMOUNT')
        if request.GET.get('CREATE_DATE'):
            curdate = request.GET.get('CREATE_DATE')
    print curdate
    #插入出库流水
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

#白胚出库加工
def dealWareHouse(request):
    if request.method=='GET':
        newsID=request.GET.get('id')
        CLOTH_CODE=request.GET.get('CLOTH_CODE')
        if request.GET.get('DEAL_COUNT'):
            DEAL_COUNT=request.GET.get('DEAL_COUNT')
    print DEAL_COUNT,CLOTH_CODE
    #插入出库加工流水
    try:
        ClothDeal.objects.create(CLOTH_CODE=CLOTH_CODE,CLOTH_COUNT=DEAL_COUNT)
    except ValueError as err:
        print(err)
    except:
        return HttpResponse('notNull')
    #削减库存
    whiteclothinfo = WhiteClothInfo.objects.get(id=newsID)
    try:
        if whiteclothinfo.CLOTH_REMAIN >= float(DEAL_COUNT):
            whiteclothinfo.CLOTH_REMAIN =round(whiteclothinfo.CLOTH_REMAIN - float(DEAL_COUNT),2)
            whiteclothinfo.save()
        else:
            return HttpResponse('fail')
    except ValueError as err:
        return HttpResponse('ValueError')
    #增加出厂加工数量
    try:
        clothinfo=WhiteClothInfo.objects.get(id=newsID)
        clothinfo.CLOTH_DEAL_REMAIN = clothinfo.CLOTH_DEAL_REMAIN + float(DEAL_COUNT)
        clothinfo.save()
        return HttpResponse('success')
    except ValueError as err:
        print err

#白胚加工完成入库
def dealWareHouseIn(request):
    if request.method=='GET':
        newsID=request.GET.get('id')
        CLOTH_CODE=request.GET.get('CLOTH_CODE')
        DEAL_COUNT=request.GET.get('DEAL_COUNT')
    #削減出厂加工数量
    try:
        clothinfo=WhiteClothInfo.objects.get(id=newsID)
        # print clothinfo.CLOTH_DEAL_REMAIN,DEAL_COUNT
        if clothinfo.CLOTH_DEAL_REMAIN >= float(DEAL_COUNT):
            clothinfo.CLOTH_DEAL_REMAIN = round(clothinfo.CLOTH_DEAL_REMAIN - float(DEAL_COUNT),2)
            clothinfo.save()
        else:
            return HttpResponse('fail')
    except ValueError as err:
        return HttpResponse('ValueError')
    #增加库存
    clothinfo = WhiteClothInfo.objects.get(id=newsID)
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
    query='SELECT o.CUSTOMER,o.ORDER_TIME,p.CLOTH_CODE,sum(p.CLOTH_PIECE) AS CLOTH_PIECE,sum(EDIT_CLOTH_COUNT) AS EDIT_CLOTH_COUNT,sum(p.EDIT_CLOTH_COUNT*p.AMOUNT) AS AMOUNT from goods_manage_clothorder o LEFT JOIN goods_manage_clothpieceinfo p on o.id=p.ORDER_ID WHERE ORDER_TIME BETWEEN %s AND %s AND CUSTOMER = %s  GROUP BY o.CUSTOMER,o.ORDER_TIME,p.CLOTH_CODE limit %s,%s'
    dict = {"code": 0, "msg": "", "count": 15}
    list = []
    for i in cursor.execute(query,[beginDate,endDate,customer,begin,end]):
        dict1 = {}
        dict1["CUSTOMER"]=i[0]
        dict1["ORDER_TIME"]=i[1]
        dict1["CLOTH_CODE"]=i[2]
        dict1["CLOTH_PIECE"]=i[3]
        dict1["EDIT_CLOTH_COUNT"]=i[4]
        if i[5]==None:
            dict1["AMOUNT"]=0
        else:
            dict1["AMOUNT"]=round(i[5],2)
        list.append(dict1)
    dict["count"]=len(list)
    dict["data"]=list
    return HttpResponse(json.dumps(dict,ensure_ascii=False,cls=CJsonEncoder))

#布匹删除接口
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

#布匹数量添加
def addPieceGoodsAction(request):
    REMARKS='-'
    CLOTH_PIECE=1
    CLOTH_PIECE_COUNT=0.0
    if request.method=='GET':
        if request.GET.get('CLOTH_CODE'):
            CLOTH_CODE=request.GET.get('CLOTH_CODE')
        if request.GET.get('CLOTH_PIECE_COUNT'):
            CLOTH_PIECE_COUNT=request.GET.get('CLOTH_PIECE_COUNT')
        if request.GET.get('REMARKS'):
            REMARKS=request.GET.get('REMARKS')
    if CLOTH_PIECE_COUNT==0:
        return HttpResponse('pieceCountFailed')
    #布匹添加后库存随之增加
    clothinfo=ClothInfo.objects.filter(CLOTH_STATUS='1').get(CLOTH_CODE=CLOTH_CODE)
    clothinfo.CLOTH_REMAIN= round((clothinfo.CLOTH_REMAIN+float(CLOTH_PIECE)*float(CLOTH_PIECE_COUNT)),2)
    clothinfo.save()
    try:
        ClothPieceInfo.objects.create(CLOTH_CODE=CLOTH_CODE,CLOTH_PIECE=CLOTH_PIECE,CLOTH_PIECE_COUNT=CLOTH_PIECE_COUNT,REMARKS=REMARKS)
    except:
        return  HttpResponse('fail')
    return HttpResponse('success')

#布匹编辑
def editPeiceGoods(request):
    REMARKS='-'
    if request.method == 'GET':
        if request.GET.get('id'):
            id = request.GET.get('id')
        if request.GET.get('CLOTH_PIECE'):
            CLOTH_PIECE = request.GET.get('CLOTH_PIECE')
        if request.GET.get('REMARKS'):
            REMARKS = request.GET.get('REMARKS')
    try:
        ClothPieceInfo.objects.filter(id=id).update(CLOTH_PIECE=CLOTH_PIECE,REMARKS=REMARKS)
    except ValueError as err:
        return HttpResponse(err)
    return HttpResponse('success')

#出库详情修改
def editGoodsOut(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            id = request.GET.get('id')
        if request.GET.get('CUSTOMER'):
            CUSTOMER = request.GET.get('CUSTOMER')
        if request.GET.get('CLOTH_COUNT'):
            CLOTH_COUNT = request.GET.get('CLOTH_COUNT')
        if request.GET.get('AMOUNT'):
            AMOUNT = request.GET.get('AMOUNT')
        if request.GET.get('CLOTH_COUNT'):
            CREATE_TIME = request.GET.get('CREATE_TIME')
    try:
        ClothOut.objects.filter(id=id).update(CUSTOMER=CUSTOMER,CLOTH_COUNT=CLOTH_COUNT,AMOUNT=AMOUNT,CREATE_TIME=CREATE_TIME)
    except ValueError as err:
        return HttpResponse(err)
    return HttpResponse('success')

#码单管理
def show_order_list(request):
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
        list_count=ClothOrder.objects.count()
        for i in ClothOrder.objects[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    else:
        list_count = ClothOrder.objects.filter(CUSTOMER__contains=key).count()
        for i in ClothOrder.objects.filter(CUSTOMER__contains=key)[begin:end]:
            dict1=model_to_dict(i)
            list.append(dict1)
    dict["count"]=list_count
    dict["data"] = list
    return HttpResponse(json.dumps(dict,ensure_ascii=False,cls=CJsonEncoder))

@csrf_exempt
#添加码单
def addOrderSuccess(request):
    ORDER_TIME=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    ID=''
    CLOTH_PIECE=CLOTH_COUNT=AMOUNT=0
    #获取前端数据
    if request.method=='POST':
        ID = request.POST['ID']
        CUSTOMER=request.POST['CUSTOMER']
        if request.POST['CLOTH_PIECE']:
            CLOTH_PIECE=request.POST['CLOTH_PIECE']
        if request.POST['CLOTH_COUNT']:
            CLOTH_COUNT=request.POST['CLOTH_COUNT']
        if request.POST['AMOUNT']:
            AMOUNT=request.POST['AMOUNT']
        if request.POST['ORDER_TIME']:
            ORDER_TIME=request.POST['ORDER_TIME']
    #通过id是否为空来判断添加/编辑码单内容
    if ID=='':
        try:
            ClothOrder.objects.create(CUSTOMER=CUSTOMER,CLOTH_PIECE=CLOTH_PIECE,CLOTH_COUNT=CLOTH_COUNT,AMOUNT=AMOUNT,ORDER_TIME=ORDER_TIME)
        except ValueError as err:
            print err
    else:
        try:
            ClothOrder.objects.filter(id=ID).update(CUSTOMER=CUSTOMER,CLOTH_PIECE=CLOTH_PIECE,CLOTH_COUNT=CLOTH_COUNT,AMOUNT=AMOUNT,ORDER_TIME=ORDER_TIME)
        except ValueError as err:
            print err
    return HttpResponse('success');

#删除码单
def delOrder(request):
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
            ClothOrder.objects.filter(id=newGoodID).delete()
        except ValueError as err:
            print(err)
    if  len(newsID) != 0:
        for ID in newsID:
            try:
                ClothOrder.objects.filter(id=ID).delete()
            except ValueError as err:
                print(err)
    return HttpResponse('success')

#添加布匹至码单
def addToOrder(request):
    if request.method=='GET':
        id=int(request.GET.get('id'))
        PieceId=int(request.GET.get('PieceId'))
    try:
        #将布匹添加到码单
        ClothPieceInfo.objects.filter(id=PieceId).update(ORDER_ID=id)
    except ValueError as err:
        print err
    return HttpResponse('success')

#码单详情接口
def showOrderDetail(request):
    if request.method=='GET':
        orderNo=int(request.GET.get('orderNo'))
    dict = {"code": 0, "msg": "", "count": 15}
    list = []
    # 判断关键字是否为空，来选择执行不同的sql
    list_count = ClothPieceInfo.objects.all().filter(ORDER_ID=orderNo).count()
    for i in ClothPieceInfo.objects.all().filter(ORDER_ID=orderNo):
        dict1 = model_to_dict(i)
        list.append(dict1)
    dict["count"] = list_count
    dict["data"] = list
    return HttpResponse(json.dumps(dict,ensure_ascii=False))

#将布匹移出码单
def removePiece(request):
    if request.method=='GET':
        PIECE_ID=request.GET.get('id')
    try:
        ClothPieceInfo.objects.filter(id=PIECE_ID).update(ORDER_ID=0,EDIT_CLOTH_COUNT=0,AMOUNT=0)
    except ValueError as err:
        print err
    return HttpResponse('success')

#修改码单布匹
def editOrderPiece(request):
    if request.method=='GET':
        PIECE_ID=request.GET.get('id')
        EDIT_CLOTH_COUNT=float(request.GET.get('EDIT_CLOTH_COUNT'))
        AMOUNT=float(request.GET.get('AMOUNT'))
        REMARKS=request.GET.get('REMARKS')
    try:
        ClothPieceInfo.objects.filter(id=PIECE_ID).update(EDIT_CLOTH_COUNT=EDIT_CLOTH_COUNT,REMARKS=REMARKS,AMOUNT=AMOUNT)
    except ValueError as err:
        print err
    return HttpResponse('success')

#下单
def placeOrder(request):
    if request.method=='GET':
        ORDER_ID=int(request.GET.get('id'))
    cursor = connection.cursor()
    query='SELECT count(id) AS CLOTH_PIECE,sum(EDIT_CLOTH_COUNT) AS CLOTH_COUNT ,sum(EDIT_CLOTH_COUNT*AMOUNT) AS AMOUNT from goods_manage_clothpieceinfo WHERE ORDER_ID= %s'
    for i in cursor.execute(query,[ORDER_ID]):
        if i[0]==None:
            CLOTH_PIECE=0
        else:
            CLOTH_PIECE=i[0]
        if i[1]==None:
            CLOTH_COUNT=0
        else:
            CLOTH_COUNT=i[1]
        if i[2]==None:
            AMOUNT=0
        else:
            AMOUNT=i[2]
    try:
        ClothOrder.objects.filter(id=ORDER_ID).update(CLOTH_PIECE=CLOTH_PIECE,CLOTH_COUNT=CLOTH_COUNT,AMOUNT=AMOUNT)
    except ValueError as err:
        print err
    return HttpResponse('success')


