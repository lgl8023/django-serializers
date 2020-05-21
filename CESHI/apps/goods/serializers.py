from goods.models import *
from rest_framework import serializers

'''
序列化多表查询嵌套添加修改, 前提必须有外键关联.....
'''


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ('id', 'goods_name', 'goods_count', 'goods_size')


class CateSerializer(serializers.ModelSerializer):

    cate_goods = GoodsSerializer ( many=True )

    class Meta:
        model = Cate
        fields = ('id', 'cate_name', 'cate_goods')


class BrandSerializer(serializers.ModelSerializer):

    brand_cate = CateSerializer ( many=True )

    class Meta:
        model = Brand
        fields = ('id', 'name', 'brand_cate')

    def create(self, validated_data):
        # pop 弹出data 中的 数据并保存
        brand_cates = validated_data.pop('brand_cate')
        # 并进行第一张表的添加
        brand = Brand.objects.create(**validated_data)
        # 遍历 弹出的第二张表的数据并添加第二章表, 且 主键信息为单独添加
        for cate_data in brand_cates:
            cate_goods = cate_data.pop ( 'cate_goods' )
            cate = Cate.objects.create(brand=brand, **cate_data)
            # 第三张表数据添加
            for goods in cate_goods:
                Goods.objects.create (cate=cate, **goods)
        return brand

    def update(self, instance, validated_data):
        # 获取当前json 数据中 外键表的数据
        brand_cate = validated_data.pop('brand_cate')
        # 通过 instance 实例 去获取它外键表的实例
        brand_cate_data = (instance.brand_cate).all()
        brand_cate_data = list(brand_cate_data)
        # 修改 当前实例表的数据
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        # 遍历 pop弹出的 外键表要修改的数据
        for cate_data in brand_cate:
            # 继续弹出第三张表外键的数据
            goods_data = cate_data.pop ( 'cate_goods' )
            # 获取第一张外键的 实例
            cate_instance = brand_cate_data.pop(0)
            # 获取第三张表的实例
            cate_goods = list((cate_instance.cate_goods).all())
            # 更新 第一张外键表数据
            cate_instance.name = cate_data.get('cate_name', cate_instance.cate_name)
            cate_instance.save()
            # 遍历继续更新第三张表的数据
            for goods in goods_data:
                goods_instance = cate_goods.pop(0)
                goods_instance.goods_name = goods.get("goods_name",goods_instance.goods_name)
                goods_instance.goods_count = goods.get("goods_count",goods_instance.goods_count)
                goods_instance.goods_size = goods.get("goods_size",goods_instance.goods_size)
                goods_instance.save()
        return instance


class GoodsSerializersModel(serializers.ModelSerializer):
    # 通过 source 去指向源地址, 也就是cate外键 数据中的 name 值
    cate_name = serializers.CharField ( source="cate.cate_name" )
    class Meta:
        model = Goods
        fields = '__all__'


class CatesSerializers(serializers.ModelSerializer):
    '''
    通过这种方法也可以进行数据嵌套返回
    '''
    # SerializerMethodField () 父类序列化容器, 通过它可以去查询并并返回相关的数据
    goodsList = serializers.SerializerMethodField ()

    # get__ 必须跟 前面定义的变量, row 值表示父类容器的当前这一条数
    def get_goodsList ( self, row ):
        try:
            # 通过当前row 的 id 去查询外键数据
            goodsQuery = Goods.objects.filter ( cate=row.id ).all ()
            # 查询到的QuerySet 通过 自定义的序列化容器 返回响应的数据
            goodsList = GoodsSerializersModel ( goodsQuery, many=True )
            return goodsList.data
        except:
            return [ ]

    class Meta:
        model = Cate
        fields = '__all__'

