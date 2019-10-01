from typing import List


class PinDuoDuoGood:
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


class PinDuoDuoGoodsInfo:
    """
    商品的所有类型信息
    """
    __slots__ = ["goods_title", "goods_info"]

    def __init__(self, goods_title, goods_info: List[PinDuoDuoGood]):
        """

        :param goods_title: 商品标题
        :param goods_info:商品类型的信息
        """
        self.goods_title = goods_title
        self.goods_info = goods_info

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
        :param sold_num:
        """
        self.goods_title = goods_title
        self.sold_num = sold_num


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
