from django.conf.urls import url

from axf import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^market/(\d+)/(\d+)/(\d+)/$',views.market,name='market'),
    url(r'^mine/$',views.mine,name='mine'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^registe/$',views.registe,name='registe'),
    url(r'^checkaccount/$',views.checkaccount,name='checkaccount'),
    url(r'^addcart/$',views.addcart,name='addcart'),
    url(r'^subcart/$', views.subcart, name='subcart'),
    url(r'^changecartstatus/$',views.changecartstatus,name='changecartstatus'),
    url(r'changeallselect/$',views.changeallselect,name='changeallselect'),
    url(r'^generateorder/$',views.generateorder,name='generateorder'),
    url(r'^orderinfo/(\d+)/$',views.orderinfo,name='orderinfo')

]