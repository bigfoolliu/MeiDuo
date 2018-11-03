#!-*-coding:utf-8-*-
# !@Date: 18-11-2 下午10:39
# !@Author: Liu Rui
# !@github: bigfoolliu


import os
import django

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'MeiDuo.settings.dev'
django.setup()

from django.conf import settings
from django.shortcuts import render

from MeiDuo.utils.goods_category import get_goods_category
from contents.models import ContentCategory


def generate_index_html():
    """
    生成首页的静态html文件
    步骤：
        1. 查询首页的列表分类数据,广告数据(主要就这两种数据)
        2. 生成html标签
    :return:
    """
    # 查询分类数据
    categories = get_goods_category()
    # 查询广告数据
    contents = {}
    content_categories = ContentCategory.objects.all()
    for category in content_categories:
        contents[category.key] = category.content_set.filter(status=True).order_by('sequence')

    # 生成html标签,写到html文件中
    response = render(None, 'index.html', {'categories': categories, 'contents': contents})
    html_str = response.content.decode()
    # 写文件
    filename = os.path.join(settings.GENERATE_STATIC_HTML_PATH, 'index.html')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_str)

    print('generate_index_html OK')


if __name__ == '__main__':
    generate_index_html()
