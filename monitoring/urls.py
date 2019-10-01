from django.urls import path, include
from .views import monitoring_pinduoduo_goods_by_url

urlpatterns = [
    path("sendPinduoduoUrl", monitoring_pinduoduo_goods_by_url),
]
