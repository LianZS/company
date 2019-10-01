import requests
import re
import json
from typing import Union
from bs4 import BeautifulSoup
from monitoring.struct_info.struct_goods import PinDuoDuoGood, PinDuoDuoGoodsInfo, PinDuoDuoGoodsSold


class PinDuoDuo:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36',
            'cookie': 'api_uid=CiFjZV2M4NNHKgBOSSKEAg==; _nano_fp=XpdjlpdaXqEJX5XbnT_fqLjtzH6S6NeyVD6RVRC3; '
                      'msec=1800000; pdd_user_id=7535527805049; pdd_user_uin=LN35OVQXEXJDDBR6O64BVPY7R4_GEXDA; '
                      'PDDAccessToken=QMOPVA2EKE2IVAYWQZACH5G4YJL7VHG3CYA2Q465WOFCJ7FYRGYA110798f; rec_list_mall_'
                      'bottom=rec_list_mall_bottom_5bFnZV; group_rec_list=group_rec_list_a44iQA; chat_list_rec_'
                      'list=chat_list_rec_list_wZlIVR; JSESSIONID=139FC4FD1CDC6870479ACD0FAA7380E7; '
                      'ua=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_12_6)%20AppleWebKit'
                      '%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F77.0.3865.90%20Safari%2F537.36; webp=1'

        }

    def get_goods_sold_by_url(self, url) -> Union[None, PinDuoDuoGoodsSold]:
        """
        获取链接中商品标题和已买商品数
        :param url:商品链接
        :return:
        """
        response = requests.get(url=url, headers=self.headers)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'lxml')
        # 获取已售件数----获取得：已拼n件
        try:
            sold = soup.find(name='span', attrs={"class": '_3ORJYJDV'}).text  # 获取已售件数----获取得：已拼n件
            # 提取到此时售卖数
            sold_num = re.match("\w{2}(\d+)", sold).group(1)
            # 商品标题
            goods_title = soup.find(name="span", attrs={"class": "enable-select"}).text  # 商品标题
        except AttributeError as e:
            print(e)
            return None

        return PinDuoDuoGoodsSold(goods_title, sold_num)

    def get_goods_info_by_url(self, url) -> Union[None, PinDuoDuoGoodsInfo]:
        """
        获取链接商品信息，商品名称，已买商品数，商品款式，价格

        :param url: 商品链接
        :return:
        """
        response = requests.get(url=url, headers=self.headers, timeout=5)
        if response.status_code != 200:
            return None
        # 提取链接商品全部信息
        goods_info = re.search("rawData=\s(.*?);\s+</script>", response.text).group(1)  # 拥有商品所有信息
        goods_info_dict: dict = json.loads(goods_info)
        goods_info: dict = goods_info_dict['store']['initDataObj']['goods']  # 提取需要的商品信息
        goods_title = goods_info['goodsName']  # 商品标题
        goods_info_list = list()  # 存放商品类型的基本信息
        for goods in goods_info['skus']:
            goods_name, goods_size = None, None
            for goods_struct in goods['specs']:
                spec_key = goods_struct['spec_key']
                spec_value = goods_struct['spec_value']
                if spec_key == "型号":
                    goods_name = spec_value  # 商品名称

                if spec_key == "尺寸":
                    goods_size = spec_value  # 商品尺寸
            normal_price = goods['normalPrice']  # 单独购买价格
            group_price = goods['groupPrice']  # 发起拼单价格
            goods = PinDuoDuoGood(goods_name, goods_size, normal_price, group_price)
            goods_info_list.append(goods)
        return PinDuoDuoGoodsInfo(goods_title, goods_info_list)
