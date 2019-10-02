from django.urls import path, include
from .views import request_pinduoduo_goods_by_url,get_monitoring_pinduoduo_goods_info

urlpatterns = [
    path("sendPinduoduoGoodsUrl", request_pinduoduo_goods_by_url),
    path("getPinduoduoGoodsInfo", get_monitoring_pinduoduo_goods_info),

]
