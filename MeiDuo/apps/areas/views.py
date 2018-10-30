from django.shortcuts import render

# Create your views here.


# 查多个list：返回所有的省信息
# 查一个retrieve：返回pk对应的地区，并包含它的子级地区
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from areas.models import Area
from areas.serializers import AreaSerializer, AreaSubSerializer


class AreaListView(ListAPIView):
    """
    查询省份列表视图接口
    """
    queryset = Area.objects.filter(parent__isnull=True)  # 省份的父级id为空
    serializer_class = AreaSerializer
    # get方法


class AreaRetrieveView(RetrieveAPIView):
    """
    查询下辖区域列表视图接口
    """
    queryset = Area.objects.all()
    serializer_class = AreaSubSerializer
    # get方法


