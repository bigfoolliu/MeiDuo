# from django.contrib import admin
#
# # Register your models here.
# from .models import *
# from celery_tasks.html.tasks import generate_static_sku_detail_html
#
#
# class SKUAdmin(admin.ModelAdmin):
#     """
#     专门来对sku进行管理
#     当后台管理人员对sku进行增删改查的时候重新生成静态html文件
#     """
#     # 定义列表页的属性
#     list_display = ['id', 'name', 'price']
#
#     # 定义编辑页的属性
#     # 重写保存和删除方法
#     def save_model(self, request, obj, form, change):
#         """
#         新增或者修改sku对象的时候执行
#         :param request:
#         :param obj:
#         :param form:
#         :param change:
#         :return:
#         """
#         super().save_model(request, obj, form, change)  # 首先执行父类的方法
#         # 生成对应对象的静态文件
#         generate_static_sku_detail_html.delay(obj.id)
#
#     def delete_model(self, request, obj):
#         """
#         删除
#         :param request:
#         :param obj:
#         :return:
#         """
#         super().delete_model(request, obj)
#
#
# admin.site.register(GoodsCategory)
# admin.site.register(GoodsChannel)
# admin.site.register(Goods)
# admin.site.register(Brand)
# admin.site.register(GoodsSpecification)
# admin.site.register(SpecificationOption)
# admin.site.register(SKU)
# admin.site.register(SKUSpecification)
# admin.site.register(SKUImage)

"""
admin和adminx不能同时存在
"""