from goods.serializers import BrandSerializer


class Paginators(object):
    '''
    :param self.current_page 当前页
    :param self.modelObjects 传入模型实例
    :param self.page_count 总页数
    :param self.start_data 起始位置
    :param self.end_data 结束位置
    :return data.data 序列化返回的JSON数据
    '''
    def __init__(self, current_page, instance_objects):
        '''静态初始化'''
        self.current_page = current_page
        self.modelObjects =instance_objects
        self.page_count = 0
        self.start_data = 0
        self.end_data = 0

    def page_dispose (self):
            current_page = int ( self.current_page )
            show_num = 10  # 显示条数
            """
            1-10条  [0:10]     1  [(1-1)*10:1*10]
            11-20条 [10:20]    2  [(2-1)*10:2*10]
            21-30条[20:30]   3  [(3-1)*10:3*10]
            m-n条  [m-1:n]   h  [(m-1)*10:n*10]
            """
            self.start_data = (current_page - 1) * show_num  # 从第几条数据显示
            self.end_data = current_page * show_num  # 显示到第几条结束
            count = self.modelObjects.objects.count ()  # 数据的总数量
            # divmod() 得余数 cunt 除 show_num 整数位m 余数为n
            m, n = divmod ( count, show_num )
            # 有余数多一页,没有就取 m 为总页数
            if n == 0:
                num_pages = m
            else:
                num_pages = m + 1
            # 切片操作获取分页数据
            datalist = self.modelObjects.objects.all ()[ self.start_data:self.end_data ]
            # 数据序列化
            data = BrandSerializer(datalist, many=True)
            return data.data,num_pages

