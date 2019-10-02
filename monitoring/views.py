from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    task_id = None
    if request.method == "POST":
        url = request.POST.get("url")  # 监控链接
        monitoring_state = request.POST.get("monitoring_state")  # 是否长期监控
        pin_duo_duo = PinDuoDuo()
        task_id = pin_duo_duo.get_goods_all_info_by_url.apply_async(args=(pin_duo_duo, url))
    return HttpResponse(str(task_id))


def get_monitoring_pinduoduo_goods_info(request):
    """
    获取拼多多商品监控信息
    方法：GET，参数
    task_id：任务id
    :param request:
    :return:
    """
    task_result = {}
    if request.method == "GET":
        task_id = request.GET.get("task_id")
        task_over = app.AsyncResult(task_id).ready()
        if not task_over:
            pass
        else:
            summary_info: PinDuoDuoGoodsSummaryInfo = app.AsyncResult(task_id).result
            goods_title = summary_info.goods_title  # 商品标题
            goods_sold = summary_info.goods_sold_info.sold_num  # 售卖数量

            goods_characteristics_list = list()  # 存放特征
            for characteristics in summary_info.goods_charateristics_info.goods_characteristics:
                goods_characteristic_dict = dict()

                goods_characteristic_dict['key'] = characteristics.characteristic_type
                goods_characteristic_dict['value'] = characteristics.characteristic_content
                goods_characteristics_list.append(goods_characteristic_dict)

            goods_tags_list = list()  # 存放标签
            for tag in summary_info.goods_tag_info.goods_tag:
                goods_tag_dict = dict()
                goods_tag_dict['key'] = tag.tag_name  # 标签名
                goods_tag_dict['value'] = tag.tag_num  # 标签出现次数
                goods_tags_list.append(goods_tag_dict)

            goods_types_list = list()  # 存放商量类型
            for goods_type in summary_info.goods_type_info.goods_type_info:
                goods_type_dict = dict()
                goods_type_dict['name'] = goods_type.goods_name  # 商品类型
                goods_type_dict['size'] = goods_type.goods_size  # 商品尺寸
                goods_type_dict['group_price'] = goods_type.group_price  # 单独购买价格
                goods_type_dict['normal_price'] = goods_type.normal_price  # 发起拼单价格
                goods_types_list.append(goods_type_dict)
            task_result = {
                "title": goods_title,
                "sold": goods_sold,
                "tags": goods_tags_list,
                "types": goods_types_list,
                "characteristics": goods_characteristics_list
            }
    return JsonResponse(task_result)
