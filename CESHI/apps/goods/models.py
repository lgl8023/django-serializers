# 因为版本之间的不兼容性, 所以 导入 unicode_literals 可以兼容下一个版本
from __future__ import unicode_literals

from django.db import models


# 品牌
class Brand(models.Model):
    name = models.CharField(max_length=20, verbose_name='名称')
    '''...其他字段省略....'''

    class Meta:
        db_table = 'tb_brand'

    def __str__(self):
        return self.name


# 分类
class Cate(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_cate', null=True, blank=True, verbose_name='外键关联')
    cate_name = models.CharField(max_length=100, verbose_name='分类名称')
    '''...其他字段省略....'''

    class Meta:
        db_table = 'tb_cate'


# 商品
class Goods(models.Model):
    cate = models.ForeignKey ( Cate, on_delete=models.CASCADE, related_name='cate_goods', null=True, blank=True,
                                verbose_name='外键关联' )
    goods_name = models.CharField(max_length=50, verbose_name='商品名称')
    goods_size = models.CharField(max_length=50, verbose_name='商品规格')
    goods_count = models.CharField(max_length=100, verbose_name='商品数量')
    '''...其他字段省略....'''

    class Meta:
        db_table = 'tb_goods'

    def __str__(self):
        return self.goods_name


