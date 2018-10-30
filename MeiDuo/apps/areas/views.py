from django.shortcuts import render

# Create your views here.


# 查多个list：返回所有的省信息
# 查一个retrieve：返回pk对应的地区，并包含它的子级地区
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from areas.models import Area
from areas.serializers import AreaSerializer, AreaSubSerializer


# class AreaListView(ListAPIView):
#     """
#     查询省份列表视图接口
#     """
#     queryset = Area.objects.filter(parent__isnull=True)  # 省份的父级id为空
#     serializer_class = AreaSerializer
#     # get方法
#
#
# class AreaRetrieveView(RetrieveAPIView):
#     """
#     查询下辖区域列表视图接口
#     """
#     queryset = Area.objects.all()
#     serializer_class = AreaSubSerializer
#     # get方法


class AreaViewSet(ReadOnlyModelViewSet):
    """
    视图集来合并上面的两个View
    这里不能直接指定queryset和serializer_class,因为上述查询的方式和序列化器均不一样
    利用action来解决,即指定请求方式与处理函数的对应关系
    """

    def get_queryset(self):
        """
        指定查询集
        :return:
        """
        # 如果查询的是省份,返回父类id为空的所有对象
        if self.action == 'list':
            return Area.objects.filter(parent__isnull=True)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        """
        指定序列化器
        :return:
        """
        if self.action == 'list':
            return AreaSerializer
        else:
            return AreaSubSerializer


