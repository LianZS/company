from typing import List


class PinDuoDuoGood:
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
