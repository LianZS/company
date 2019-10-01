from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .monitoring_goods import PinDuoDuo


# Create your views here.
@csrf_exempt
def monitoring_pinduoduo_goods_by_url(request):
    """
    监控拼多多某个商品链接
    方法：POST，参数
    url：监控链接
    monitoring_state:是否长期监控，1时0不是
    :param request:
    :return:
    """
    if request.method == "POST":
        url = request.POST.get("url")  # 监控链接
        monitoring_state = request.POST.get("monitoring_state")  # 是否长期监控
        pin_duo_duo =PinDuoDuo()
        pin_duo_duo.get_goods_sold_by_url.delay(pin_duo_duo,url)
    return HttpResponse("ok")
