from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from .monitoring_goods import PinDuoDuo
from company.celeryconfig import app
from .struct_info.struct_goods import PinDuoDuoGoodsSummaryInfo


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
        pin_duo_duo = PinDuoDuo()
        task_id = pin_duo_duo.get_goods_all_info_by_url.apply_async(args=(pin_duo_duo, url))

    return HttpResponse(task_id)


def get_monitoring_pinduoduo_goods_info(request):
    """

    :param request:
    :return:
    """
    if request.method == "GET":
        task_id = request.GET.get("task_id")
        summary_info: PinDuoDuoGoodsSummaryInfo = app.AsyncResult(task_id)

    return HttpResponse("ok")
