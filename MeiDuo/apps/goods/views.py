from django.shortcuts import render

# Create your views here.
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from goods.models import SKU
from goods.serializers import SKUSerializer, SKUIndexSerializer
from pagination import SKUListPagination


class SKUListView(ListAPIView):
    """
    查询sku
    """

    def get_queryset(self):
        """
        查询多个时，获取路径中的参数: self.kwargs表明字典
        :return:
        """
        return SKU.objects.all(category_id=self.kwargs)

    serializer_class = SKUSerializer
    # 分页功能
    pagination_class = SKUListPagination

    # 排序功能
    filter_backends = [OrderingFilter]  # 指定排序过滤器
    ordering_fields = ['create_time', 'price', 'sales']  # 指定排序的字段


class SKUSearchViewsSet(HaystackViewSet):
    """
    sku搜索的视图集
    """
    index_models = [SKU]  # 搜索模型类
    serializer_class = SKUIndexSerializer  # 指定序列化器
    pagination_class = SKUListPagination  # 分页

