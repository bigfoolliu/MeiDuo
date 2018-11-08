#!-*-coding:utf-8-*-
# !@Date: 18-11-8 上午11:13
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
xadmin后台对goods模块中模型的管理

站点Model管理
xadmin可以使用的页面样式控制基本与Django原生的admin一样。

list_display 控制列表展示的字段
search_fields 控制可以通过搜索框搜索的字段名称，xadmin使用的是模糊查询
list_filter 可以进行过滤操作的列
ordering 默认排序的字段
readonly_fields 在编辑页面的只读字段
exclude 在编辑页面隐藏的字段
list_editable 在列表页可以快速直接编辑的字段
show_detail_fields 在列表页提供快速显示详情信息
refresh_times 指定列表页的定时刷新
list_export 控制列表页导出数据的可选格式
show_bookmarks 控制是否显示书签功能
data_charts 控制显示图标的样式
model_icon 控制菜单的图标
"""
import xadmin
from xadmin import views
from .models import *


class BaseSetting(object):
    """
    xadmin的基本配置
    """
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """
    xadmin的全局配置
    """
    site_title = "美多商城运营管理系统"  # 设置站点标题
    site_footer = "美多商城集团有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)


class SKUAdmin(object):
    """
    对sku模型的管理
    """
    model_icon = 'fa fa-rocket'  # 模型前的图标(http://fontawesome.dashgame.com/)
    list_display = ['id', 'name', 'price', 'stock', 'sales']  # 列展示
    search_fields = ['name']
    list_filter = ['is_launched', 'stock', 'sales']
    list_editable = ['price', 'stock']
    show_detail_fields = ['name']
    refresh_times = [10, 60]
    show_bookmarks = True
    readonly_fields = ['sales']
    data_charts = {  # 图表echarts,参考(http://www.echartsjs.com/index.html)
        "sku_stock": {
            'title': '库存量',
            "x-field": "id",
            "y-field": ('stock',),
            "order": ('id',)
        },
        "sku_sales": {
            'title': '销量',
            "x-field": "id",
            "y-field": ('sales',),
            "order": ('id',)
        },
    }


xadmin.site.register(GoodsCategory)
xadmin.site.register(GoodsChannel)
xadmin.site.register(Goods)
xadmin.site.register(Brand)
xadmin.site.register(GoodsSpecification)
xadmin.site.register(SpecificationOption)
xadmin.site.register(SKU, SKUAdmin)
xadmin.site.register(SKUSpecification)
xadmin.site.register(SKUImage)
