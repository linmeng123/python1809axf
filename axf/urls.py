from django.conf.urls import url

from axf import views

urlpatterns = [
    url(r'^$',views.home,name='home')
]