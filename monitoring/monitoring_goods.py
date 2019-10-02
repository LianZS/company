import requests
import re
import json
from typing import Union
from bs4 import BeautifulSoup
from monitoring.struct_info.struct_goods import PinDuoDuoGoodsType, PinDuoDuoGoodsTypesInfo, PinDuoDuoGoodsSold, \
    PinDuoDuoGoodsCommentTag, PinDuoDuoGoodsCommentTagInfo, PinDuoDuoGoodsCharacteristic, \
    PinDuoDuoGoodsCharacteristicsInfo, PinDuoDuoGoodsSummaryInfo
from company.celeryconfig import app


class PinDuoDuo:
    instance_flag = False
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if not PinDuoDuo.instance_flag:
            self.headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36',
                'cookie': 'api_uid=CiFjZV2M4NNHKgBOSSKEAg==; _nano_fp=XpdjlpdaXqEJX5XbnT_fqLjtzH6S6NeyVD6RVRC3; msec=1800000; rec_list_mall_bottom=rec_list_mall_bottom_5bFnZV; group_rec_list=group_rec_list_a44iQA; chat_list_rec_list=chat_list_rec_list_wZlIVR; JSESSIONID=139FC4FD1CDC6870479ACD0FAA7380E7; rec_list_index=rec_list_index_tKLrfv; rec_list_personal=rec_list_personal_bvwjjk; rec_list_footprint=rec_list_footprint_r4ql3m; pdd_user_id=7535527805049; pdd_user_uin=LN35OVQXEXJDDBR6O64BVPY7R4_GEXDA; PDDAccessToken=VCZTQ4A3423C52UTRKTJA5K2HTORQDX6V3AGSDVFW7FERQ3WCUOA110798f; ua=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_12_6)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F77.0.3865.90%20Safari%2F537.36; webp=1'
            }
            PinDuoDuo.instance_flag = True

    @app.task(queue="PinDuoDuo")
    def get_goods_sold_by_url(self, goods_url) -> Union[None, PinDuoDuoGoodsSold]:
        """
        获取链接中商品标题和已买商品数
        :param goods_url:商品链接
        :return:
        """
        response = requests.get(url=goods_url, headers=self.headers)
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

    @app.task(queue="PinDuoDuo")
    def get_goods_type_info_by_url(self, goods_url) -> Union[None, PinDuoDuoGoodsTypesInfo]:
        """
        获取链接商品信息---商品款式与价格

        :param goods_url: 商品链接
        :return:
        """
        response = requests.get(url=goods_url, headers=self.headers, timeout=10)
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
            goods = PinDuoDuoGoodsType(goods_name, goods_size, normal_price, group_price)
            goods_info_list.append(goods)
        return PinDuoDuoGoodsTypesInfo(goods_title, goods_info_list)

    @app.task(queue="PinDuoDuo")
    def get_goods_comments_tag_by_url(self, goods_url) -> Union[None, PinDuoDuoGoodsCommentTagInfo]:
        """
        获取商品评价关键词及频率
        :param goods_url:商品链接
        :return:
        """
        response = requests.get(url=goods_url, headers=self.headers, timeout=5)
        if response.status_code != 200:
            return None
        # 提取链接商品全部信息
        goods_info = re.search("rawData=\s(.*?);\s+</script>", response.text).group(1)  # 拥有商品所有信息
        goods_info_dict: dict = json.loads(goods_info)
        goods_title = goods_info_dict['store']['initDataObj']['goods']['goodsName']  # 商品标题
        tag_list = goods_info_dict['store']['initDataObj']['goods']['review']['tagList']
        goods_tag_list = list()
        for item in tag_list:
            tag_text = item['text']  # 标签文本,包含了关键词和次数
            tag_name = re.match("(\w+)", tag_text).group(1)  # 关键词
            tag_num = re.match("\w+\((\d+)\)", tag_text).group(1)  # 出现次数
            goods_tag_list.append(PinDuoDuoGoodsCommentTag(tag_name, tag_num))
        return PinDuoDuoGoodsCommentTagInfo(goods_title, goods_tag_list)

    @app.task(queue="PinDuoDuo")
    def get_goods_baseinfo_by_url(self, goods_url) -> Union[None, PinDuoDuoGoodsCharacteristicsInfo]:
        """
        商品特征信息提取
        :param goods_url: 商品链接
        :return:
        """
        response = requests.get(url=goods_url, headers=self.headers, timeout=5)
        if response.status_code != 200:
            return None
        # 提取链接商品全部信息
        goods_info = re.search("rawData=\s(.*?);\s+</script>", response.text).group(1)  # 拥有商品所有信息
        goods_info_dict: dict = json.loads(goods_info)
        goods_title = goods_info_dict['store']['initDataObj']['goods']['goodsName']  # 商品标题
        goods_characteristics_list = list()
        for item in goods_info_dict['store']['initDataObj']['goods']['goodsProperty']:
            characteristics_type = item['key']
            characteristics_content = item['values']
            goods_characteristics_list.append(
                PinDuoDuoGoodsCharacteristic(characteristics_type, characteristics_content))
        return PinDuoDuoGoodsCharacteristicsInfo(goods_title, goods_characteristics_list)

    @app.task(queue="PinDuoDuo")
    def get_goods_all_info_by_url(self, goods_url) -> Union[None, PinDuoDuoGoodsSummaryInfo]:
        """
        获取商品所有信息
        :param goods_url: 商品链接
        :return:
        """
        response = requests.get(url=goods_url, headers=self.headers, timeout=5)
        if response.status_code != 200:
            return None
        # 提取链接商品全部信息
        goods_info = re.search("rawData=\s(.*?);\s+</script>", response.text).group(1)  # 拥有商品所有信息
        goods_info_dict: dict = json.loads(goods_info)
        goods_base_info = goods_info_dict['store']['initDataObj']['goods']  # 提取需要的商品信息
        shops_url = goods_info_dict['store']['initDataObj']['mall']['pddRoute']  # 店铺链接
        complete_shops_url = "https://mobile.yangkeduo.com/" + shops_url  # 完整店铺链接
        goods_title = goods_base_info['goodsName']  # 商品标题
        soup = BeautifulSoup(response.text, 'lxml')
        # 获取已售件数----获取得：已拼n件
        try:
            sold = soup.find(name='span', attrs={"class": '_3ORJYJDV'}).text  # 获取已售件数----获取得：已拼n件
            # 提取到此时售卖数
            sold_num = re.match("\w{2}(\d+)", sold).group(1)
        except AttributeError as e:
            print(e)
            return None
        shops = soup.find(name='div', attrs={"class": "XDgqxbX_"}).text  # 商铺名
        goods_sold_info = PinDuoDuoGoodsSold(goods_title, sold_num)
        goods_info_list = list()  # 存放商品类型的基本信息
        for goods in goods_base_info['skus']:
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
            goods = PinDuoDuoGoodsType(goods_name, goods_size, normal_price, group_price)
            goods_info_list.append(goods)
        goods_type_info = PinDuoDuoGoodsTypesInfo(goods_title, goods_info_list)
        tag_list = goods_base_info['review']['tagList']
        goods_tag_list = list()
        for item in tag_list:
            tag_text = item['text']  # 标签文本,包含了关键词和次数
            tag_name = re.match("(\w+)", tag_text).group(1)  # 关键词
            tag_num = re.match("\w+\((\d+)\)", tag_text).group(1)  # 出现次数
            goods_tag_list.append(PinDuoDuoGoodsCommentTag(tag_name, tag_num))
        goods_tag_info = PinDuoDuoGoodsCommentTagInfo(goods_title, goods_tag_list)
        goods_characteristics_list = list()
        for item in goods_base_info['goodsProperty']:
            characteristics_type = item['key']
            characteristics_content = item['values']
            goods_characteristics_list.append(
                PinDuoDuoGoodsCharacteristic(characteristics_type, characteristics_content))
        goods_characteristic_info = PinDuoDuoGoodsCharacteristicsInfo(goods_title, goods_characteristics_list)
        return PinDuoDuoGoodsSummaryInfo(shops, complete_shops_url, goods_title, goods_type_info, goods_tag_info,
                                         goods_characteristic_info,
                                         goods_sold_info)

    def monitoring_goods_all_info(self, url):
        """
        长期监控商品信息
        :param url: 商品链接
        :return:
        """
        # 任务信息先写入数据库

