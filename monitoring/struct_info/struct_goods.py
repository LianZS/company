from typing import List


class PinDuoDuoGoodsType:
    """
    商品类型基本信息
    """
    __slots__ = ["goods_name", "goods_size", "normal_price", "group_price"]

    def __init__(self, goods_name, goods_size, normal_price, group_price):
        """

        :param goods_name: 商品类型
        :param goods_size: 商品尺寸
        :param normal_price: 单独购买价格
        :param group_price: 发起拼单价格
        """
        self.goods_name = goods_name
        self.goods_size = goods_size
        self.normal_price = normal_price
        self.group_price = group_price

    def __str__(self):
        return "商品类型:{goods_name},商品尺寸:{goods_size},单独购买价格:{normal_price},发起拼单价格:{group_price}".format(
            goods_name=self.goods_name, goods_size=self.goods_size, normal_price=self.normal_price,
            group_price=self.group_price)


class PinDuoDuoGoodsTypesInfo:
    """
    商品的所有类型信息
    """
    __slots__ = ["goods_title", "goods_type_info"]

    def __init__(self, goods_title, goods_info: List[PinDuoDuoGoodsType]):
        """

        :param goods_title: 商品标题
        :param goods_info:商品类型的信息
        """
        self.goods_title = goods_title
        self.goods_type_info = goods_info

    def __str__(self):
        return "商品标题:{goods_title}".format(goods_title=self.goods_title)


class PinDuoDuoGoodsSold:
    """
    商品售卖数
    """
    __slots__ = ['goods_title', 'sold_num']

    def __init__(self, goods_title, sold_num):
        """

        :param goods_title: 商品标题
        :param sold_num:已售数量
        """
        self.goods_title = goods_title
        self.sold_num = sold_num

    def __str__(self):
        return "商品标题:{goods_title},已售数量：{sold_num}".format(goods_title=self.goods_title, sold_num=self.sold_num)


class PinDuoDuoGoodsCommentTag:
    """
    商品评价标签
    """
    __slots__ = ['tag_name', 'tag_num']

    def __init__(self, tag_name, tag_num):
        """

        :param tag_name: 标签名
        :param tag_num: 标签出现次数
        """
        self.tag_num = tag_num
        self.tag_name = tag_name

    def __str__(self):
        return "标签名：{tag_name}，标签出现次数：{tag_num}".format(tag_name=self.tag_name, tag_num=self.tag_num)


class PinDuoDuoGoodsCommentTagInfo:
    """
    商品评价标签信息
    """
    __slots__ = ["goods_title", "goods_tag"]

    def __init__(self, goods_title, goods_tag: List[PinDuoDuoGoodsCommentTag]):
        """

        :param goods_title: 商品标题
        :param goods_tag: 商品评价标签集合
        """
        self.goods_title = goods_title
        self.goods_tag = goods_tag

    def __str__(self):
        return "商品标题:{goods_title}".format(goods_title=self.goods_title)


class PinDuoDuoGoodsCharacteristic:
    """
    商品某项特征
    """
    __slots__ = ['characteristic_type', 'characteristic_content']

    def __init__(self, characteristic_type, characteristic_content):
        """

        :param characteristic_type: 特征类型
        :param characteristic_content: 特征详情
        """
        self.characteristic_type = characteristic_type
        self.characteristic_content = characteristic_content

    def __str__(self):
        return "特征类型:{characteristic_type},characteristic_content:{characteristic_content}".format(
            characteristic_type=self.characteristic_type, characteristic_content=self.characteristic_content)


class PinDuoDuoGoodsCharacteristicsInfo:
    """
     商品特征信息
    """
    __slots__ = ['goods_title', 'goods_characteristics']

    def __init__(self, goods_title, goods_characteristics: List[PinDuoDuoGoodsCharacteristic]):
        """

        :param goods_title: 商品标题
        :param goods_characteristics: 商品特征集合
        """
        self.goods_title = goods_title
        self.goods_characteristics = goods_characteristics

    def __str__(self):
        return "商品标题:{goods_title},商品特征:{goods_characteristics}".format(goods_title=self.goods_title,
                                                                        goods_characteristics=self.goods_characteristics)


class PinDuoDuoGoodsSummaryInfo:
    """
    商品信息汇总
    """
    __slots__ = ["shops", "shops_url", "goods_title", "goods_type_info", "goods_tag_info", "goods_charateristics_info",
                 "goods_sold_info"]

    def __init__(self, shops, shops_url, goods_title: str, goods_type_info: PinDuoDuoGoodsTypesInfo,
                 goods_tag_info: PinDuoDuoGoodsCommentTagInfo,
                 goods_charateristics_info: PinDuoDuoGoodsCharacteristicsInfo, goods_sold_info: PinDuoDuoGoodsSold):
        """
        :param shops:店铺名
        :param shops_url:店铺链接
        :param goods_title:商品标题
        :param goods_type_info:商品类型信息
        :param goods_tag_info:商品评价标签信息
        :param goods_charateristics_info:商品特征信息
        :param goods_sold_info:商品售卖数
        """
        self.shops = shops
        self.shops_url = shops_url
        self.goods_title = goods_title
        self.goods_type_info = goods_type_info
        self.goods_tag_info = goods_tag_info
        self.goods_charateristics_info = goods_charateristics_info
        self.goods_sold_info = goods_sold_info

    def __str__(self):
        return "店铺：{shops},商品标题：{goods_title},商品类型信息:{goods_type_info},商品评价标签信息:{goods_tag_info},商品特征信息:{goods_charateristics}," \
               "商品售卖数:{goods_sold_info}".format(shops=self.shops, goods_title=self.goods_title,
                                                goods_type_info=self.goods_type_info,
                                                goods_tag_info=self.goods_tag_info,
                                                goods_charateristics=self.goods_charateristics_info,
                                                goods_sold_info=self.goods_sold_info)


class PinDuoDuoShopsGoodsInfo:
    """
    商品链接信息
    """
    __slots__ = ["goods_title", "goods_url"]

    def __init__(self, goods_title, goods_url):
        """

        :param goods_title: 商品标题
        :param goods_url: 商品链接
        """
        self.goods_title = goods_title
        self.goods_url = goods_url

    def __str__(self):
        return "商品标题:{goods_title},商品链接:{goods_url}".format(goods_title=self.goods_title, goods_url=self.goods_url)


class PinDuoDuoShops:
    """
    店铺商品信息概况
    """
    __slots__ = ["shops", "shops_url", "shops_goods_info"]

    def __init__(self, shops: str, shops_url, shops_goods_info: List[PinDuoDuoShopsGoodsInfo]):
        """
        :param shops_url:店铺链接
        :param shops: 店铺
        :param shops_goods_info:商品信息
        """
        self.shops = shops
        self.shops_url = shops_url
        self.shops_goods_info = shops_goods_info

    def __str__(self):
        return "店铺:{shops},店铺链接:{shops_url}".format(shops=self.shops, shops_url=self.shops_url)
