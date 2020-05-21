from __future__ import unicode_literals         # 兼容版本
from .serializers import *                      # 在导包的过程中尽量不要使用 * ,我这里是因为都用到了
from rest_framework.views import APIView        # 前后端分离API[ 它的底层是dispatch()] 其实最好用的还是viewSet
from rest_framework.response import Response    #返回前端响应
from CESHI.utils.paginators import Paginators   #自定义分页类


class GoodsListView(APIView):
    '''
    :param current_page 当前页
    :param data_list 查询数据集
    :param page_count 总页数
    :param data 获取前端传递数据集
    '''
    def get(self, request):
        '''查询数据集'''
        # 获取当前页值, 没有默认为第一页
        current_page = request.GET.get('page',1)
        print(current_page)
        # 自定义分页类, 第一值: current_page, 第二值: orm模型实例 返回serializer序列化数据并且分页总页数
        data_list,page_count = Paginators(current_page=current_page,instance_objects=Brand).show_page()
        print(data_list)
        return Response({"mes":data_list,"page_count":page_count})

    def post( self, request):
        '''添加数据集'''
        data = request.data
        print(data)
        brand = BrandSerializer(data=data)
        if brand.is_valid():
            brand.save()
            return Response ( {'code': 200,"message":'SUCCESS'} )
        else:
            print(brand.errors)
            return Response ( {'code': 400, "message":'ERROR'} )

    def put( self, request):
        '''修改数据集'''
        data = request.data
        brand_instance = Brand.objects.get(id=data['id'])
        brand = BrandSerializer(brand_instance,data)
        if brand.is_valid():
            brand.save()
            return Response ( {'code': 200,"message":'SUCCESS'} )
        else:
            print(brand.errors)
            return Response ( {'code': 400, "message":'ERROR'} )


class CateListAPI(APIView):
    def get( self, request):
        data = Cate.objects.filter()
        cate_goods_list =CatesSerializers(data, many=True)
        return Response(cate_goods_list.data)
'''
{
    "name": "贵人鸟",
    "brand_cate": [
        {
            "cate_name": "鞋子",
            "cate_goods":[
                {
                "goods_name":'透气鞋子-GRN-2020-31',
                "goods_count":'200',
                "goods_size":'39,40,41',
                }
            ]
        },
        {
            "cate_name": "服装",
            "cate_goods":[
                {
                "goods_name":'运动服饰-GRN-2020-23',
                "goods_count":'12',
                "goods_size":'XL,L,M',
                }
            ]
        }
    ]
}

# PUT data to the MusicianListView to update data.
{
     'id': 1,
    "name": "贵人鸟",
    "brand_cate": [
        {
            'id': 1,
            'brand': 1,
            "cate_name": "鞋子-跑步鞋",
            "cate_goods":[
                {
                'id': 1,
                'cate': 1,
                "goods_name":'透气鞋子-GRN-2020-31-02',
                "goods_count":'210',
                "goods_size":'39,40,41',
                }
            ]
        },
        {
            'id': 2,
            'brand': 1,
            "cate_name": "服装-运动版",
            "cate_goods":[
                {
                'id': 2,
                'cate': 2,
                "goods_name":'运动服饰-GRN-2020-23',
                "goods_count":'121',
                "goods_size":'XL,L,M',
                }
            ]
        }
    ]
}'''


'''
对分页后的数据进行序列化..... 实现呢

'''
