from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^$',home,name="home"),
		url(r'^store/$',store,name="store"),
		url(r'^product/(\d+)/$',product,name="product"),
		url(r'^checkout/$',checkout,name="checkout"),
		url(r'^cart_remove/$',cart_remove,name="cart_remove"),
		url(r'^invoice/$',invoice,name="invoice"),

	]