from django.shortcuts import render

# Create your views here.
from axf.models import *


def home(request):
    wheels = Wheel.objects.all()
    navs = Nav.objects.all()
    mustbuys = Mustbuy.objects.all()

    shopList = Shop.objects.all()
    shophead = shopList[0]
    shoptab = shopList[1:3]
    shopclass = shopList[3:7]
    shopcommend = shopList[7:11]

    mainshows = MainShow.objects.all()

    date = {
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shophead': shophead,
        'shoptab': shoptab,
        'shopclass': shopclass,
        'shopcommend': shopcommend,
        'mainshows': mainshows
    }
    return render(request,'home/home.html',context=date)
def cart(request):
    return render(request,'cart/cart.html')
def market(request,categoryid,childid,sortid):
    foodtypes = Foodtypes.objects.all()
    # 找到点击者的下标
    typeIndex = int(request.COOKIES.get('typeIndex',0))
    #通过找到的下标来获取对应的分类ID
    categoryid = foodtypes[typeIndex].typeid
    #所找到的信息
    childtypenames=  foodtypes.get(typeid=categoryid).childtypenames
    childTypleList = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        dir = {
            'childname':arr[0],
            'childid':arr[1]
        }
        childTypleList.append(dir)



    if childid == '0':  # 全部分类
        goodsList = Goods.objects.filter(categoryid=categoryid)
    else:  # 分类 下 子类
        goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childid)



    # 排序
    if sortid == '1':  # 销量排序
        goodsList = goodsList.order_by('-productnum')
    elif sortid == '2':  # 价格最低
        goodsList = goodsList.order_by('price')
    elif sortid == '3':  # 价格最高
        goodsList = goodsList.order_by(('-price'))

    data = {
        'foodtypes':foodtypes,
        'childTypleList': childTypleList,   # 子类信息
        'categoryid':categoryid,    # 分类ID
        'childid': childid,
        'goodsList': goodsList,  # 商品信息

    }


    return render(request,'market/market.html',context=data)
def mine(request):
    return render(request,'mine/mine.html')