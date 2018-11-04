#!/usr/bin/env python
# 在当前环境中查找python的目录,指定当期文件执行时的解释器

# !/home/python/.virtualenvs/meiduo_env/bin/python
# 指定当前文件执行时，使用的解释器(使用which python查看),这么写不好

# !@Date: 18-11-3 下午5:53
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
本文件为一个脚本，只要运行(即在命令行里$generate_detail_html即可执行文件)就会查询所有商品，生成html
１．需要指定上方的配置
２．which python
３．更改该文件的权限，使之可以执行
    ll
    chmod +x generate_detail_html.py
"""
import os
import sys

import django

from celery_tasks.html.tasks import generate_static_sku_detail_html
from goods.models import SKU

sys.path.insert(0, '../')  # 指定python解释器查找包的路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MeiDuo.settings.dev")
django.setup()


if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        generate_static_sku_detail_html(sku.id)
    print('OK')
