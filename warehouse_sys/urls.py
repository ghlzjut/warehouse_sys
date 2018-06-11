"""warehouse_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from goods_manage.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', toIndex),
    url(r'^$', toLogin),
]
#warehouse manage urls
urlpatterns += [
    url(r'^addgoods/', addIndex),
    url(r'^addcloth/', addCloth),
    url(r'^Report/', Report),
    url(r'^showGoodsList/', show_goods_list),
    url(r'^addClothSuccess/', addClothSuccess),
    url(r'^delCloth/', delCloth),
    url(r'^manageGoodsIn/', manageGoodsIn),
    url(r'^inWareHouse/', inWareHouse),
    url(r'^outWareHouse/', outWareHouse),
    url(r'^loginSuccess/', loginSuccess),
    url(r'^dealGoods/', dealGoods),
    url(r'^dealGoodsIn/', dealGoodsIn),
    url(r'^dealWareHouse/', dealWareHouse),
    url(r'^dealWareHouseIn/', dealWareHouseIn),
    url(r'^manageGoodsOut/', manageGoodsOut),
    url(r'^financialReport/', financialReport),
    url(r'^getCustomer/', getCustomer),
    url(r'^addPieceGoods/', addPieceGoods),
    url(r'^queryPieceGoods/', queryPieceGoods),
    url(r'^showPieceGoods/', showPieceGoods),
    url(r'^delPeiceGoods/', delPeiceGoods),
    url(r'^addPieceGoodsAction/', addPieceGoodsAction),
    url(r'^editPeiceGoods/', editPeiceGoods),
    url(r'^toWhiteCloth/', toWhiteCloth),
    url(r'^showWhiteCloth/', show_white_cloth),
    url(r'^addWhiteCloth/', addWhiteCloth),
    url(r'^addWhiteClothSuccess/', addWhiteClothSuccess),
    url(r'^delWhiteCloth/', delWhiteCloth),
    url(r'^goodsManageOutInfo/', goodsManageOutInfo),
    url(r'^showGoodsOut/', showGoodsOut),
    url(r'^editGoodsOut/', editGoodsOut),
    url(r'^showOrderList/', show_order_list),
    url(r'^orderManage/', orderManage),
    url(r'^addOrder/', addOrder),
    url(r'^addOrderSuccess/', addOrderSuccess),
    url(r'^delOrder/', delOrder),
    url(r'^setOrderInfo/', setOrderInfo),
    url(r'^addToOrder/', addToOrder),
    url(r'^orderDetail/', orderDetail),
    url(r'^showOrderDetail/', showOrderDetail),
    url(r'^removePiece/', removePiece),
    url(r'^editOrderPiece/', editOrderPiece),
    url(r'^placeOrder/', placeOrder),
]

urlpatterns += [
    url(r'^test/',test),
]
