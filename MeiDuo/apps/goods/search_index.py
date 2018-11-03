#!-*-coding:utf-8-*-
# !@Date: 18-11-3 下午4:41
# !@Author: Liu Rui
# !@github: bigfoolliu
from haystack import indexes

from goods.models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    SKU索引数据模型类
    通过创建索引类，来指明让搜索引擎对哪些字段建立索引，也就是可以通过哪些字段的关键字来检索数据。
    注意这里的数据大部分不能修改
    """
    # 在模板中指定搜索的列，可修改
    # templates/search/indexes/应用名称/模型类小写_text.txt
    # 在模板文件中定义查询属性：{{object.属性名称}}
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """
        获取模型，即建立搜索索引的模型
        :return:
        """
        return SKU

    def index_queryset(self, using=None):
        """
        定义查询集，也就是建立搜索索引的集合
        :param using:
        :return:
        """
        return self.get_model().objects.filter(is_launched=True)  # 只搜索上架的

