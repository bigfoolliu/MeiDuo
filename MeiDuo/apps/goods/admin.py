from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(GoodsCategory)
admin.site.register(GoodsChannel)
admin.site.register(Goods)
admin.site.register(Brand)
admin.site.register(GoodsSpecification)
admin.site.register(SpecificationOption)
admin.site.register(SKU)
admin.site.register(SKUSpecification)
admin.site.register(SKUImage)
