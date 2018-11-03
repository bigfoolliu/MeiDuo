#!-*-coding:utf-8-*-
# !@Date: 18-11-3 下午4:19
# !@Author: Liu Rui
# !@github: bigfoolliu
from rest_framework.pagination import PageNumberPagination


class SKUListPagination(PageNumberPagination):
    """
    重写分页类
    """
    page_size = 2  # 单页的数量
    page_size_query_description = 'page_size'
    max_page_size = 20  # 单页最大数量

