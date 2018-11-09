import hashlib
import os
import random
import time
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from Python1809AXF import settings
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
    token = request.session.get('token')
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)
        return render(request,'cart/cart.html',context={'carts':carts})
    else:
        return redirect('axf:login')
    


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

def genarate_password(param):
    sha = hashlib.sha256()
    sha.update(param.encode('utf-8'))
    return sha.hexdigest()


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)
            if user.password == password:    # 登录成功

                # 更新token
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                request.session['token'] = user.token
                return redirect('axf:mine')
            else:   # 登录失败
                return render(request, 'mine/login.html', context={'passwdErr': '密码错误!'})
        except:
            return render(request, 'mine/login.html', context={'acountErr':'账号不存在!'})
def registe(request):
    if request.method == 'GET':
        return render(request,'mine/registe.html')
    elif request.method =='POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = request.POST.get('password')
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.addr = request.POST.get('addr')
        user.token = str(uuid.uuid5(uuid.uuid4(),'register'))

        #头像操作
        imgName = user.account + '.png'
        imgPath = os.path.join(settings.MEDIA_ROOT,imgName)
        file = request.FILES.get('icon')
        with open(imgPath,'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName
        user.save()
        #状体保持
        request.session['token'] = user.token

        #重定向回去
        return redirect('axf:mine')




    return None

def logout(request):
    request.session.flush()
    return redirect('axf:mine')
def mine(request):
    token = request.session.get('token')
    responseData = {

    }
    if token:
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['islogin'] = 1

    else:
        responseData['name'] = '未登录'
        responseData['rank'] = '无等级'
        responseData['img'] = '/static/uploads/axf.png'


    return render(request,'mine/mine.html',context=responseData)


def checkaccount(request):
    account = request.GET.get('account')
    responseData = {
        'msg': '账号可用',
        'status': 1,
    }
    try:
        user = User.objects.get(account=account)
        responseData['msg']='账号已被占用'
        responseData['status']=-1
        return JsonResponse(responseData)
    except:

        return JsonResponse(responseData)


def addcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg':'添加购物车成功',
        'status': 1
    }

    if token:
        # 获取用户
        user = User.objects.get(token=token)
        # 获取商品
        goods = Goods.objects.get(pk=goodsid)

        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()
            responseData['number'] = cart.number
        else:
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()

            responseData['number'] = cart.number

        return JsonResponse(responseData)
    else:
        responseData['msg'] = '未登录，请登录后操作'
        responseData['status'] = -1
        return JsonResponse(responseData)


def subcart(request):
    # 获取数据
    token = request.session.get('token')
    goodsid = request.GET.get('goodsid')

    responseData = {
        'msg': '添加购物车成功',
        'status': 1
    }
    user = User.objects.get(token=token)
    goods = Goods.objects.get(pk=goodsid)
    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number - 1
    cart.save()
    responseData['number'] = cart.number



    return JsonResponse(responseData)


def changecartstatus(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()
    responseData = {
        'msg':'选中状态改变',
        'status':1,
        'isselect':cart.isselect
    }
    return JsonResponse(responseData)


def changeallselect(request):
    isselect = request.GET.get('isselect')
    if isselect == 'true':
        isselect = True
    else:
        isselect = False
    user = User.objects.filter(token=request.session.get('token'))
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        cart.isselect = isselect
        cart.save()
    return JsonResponse({'status':1})


def generateorder(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)

    #生成订单
    order = Order()
    order.user = user
    order.status = 1
    order.identifier = str(int(time.time())) + str(random.randrange(1000,10000))
    order.save()

    #对应订单商品
    carts = Cart.objects.filter(user=user).filter(isselect=True)
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.order = order
        orderGoods.goods = cart.goods
        orderGoods.number = cart.number
        orderGoods.number = cart.number
        orderGoods.save()

        cart.delete()
    responseData = {
            'msg': '订单生成成功',
            'status': 1,
            'identifier': order.identifier
    }

    return JsonResponse(responseData)


def orderinfo(request,identifier):
    order = Order.objects.get(identifier=identifier)
    order_list = order.ordergoods_set.all()
    return render(request,'order/orderinfo.html',context={'order':order,'order_list':order_list})