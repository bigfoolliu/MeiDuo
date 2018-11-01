from django.contrib import admin

# Register your models here.
from .models import *


"""
在后台管理中注册模型类
"""
admin.site.register(ContentCategory)
admin.site.register(Content)
