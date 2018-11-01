from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from MeiDuo.utils.models import BaseModel

"""
商品类别结构参考京东首页的商品结构
"""


class GoodsCategory(BaseModel):
    """
    商品类别
    """
    name = models.CharField(max_length=20, verbose_name='商品类别名称')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父类别')

    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsChannel(BaseModel):
    """
    商品频道,有就是几个类似的商品的类别的组合
    """
    group_id = models.IntegerField(verbose_name='组号')
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='顶级商品类别')
    url = models.CharField(max_length=50, verbose_name='频道页面链接')
    sequence = models.IntegerField(verbose_name='组内顺序')

    class Meta:
        db_table = 'tb_goods_channel'
        verbose_name = '商品频道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name


class Brand(BaseModel):
    """
    品牌
    """
    name = models.CharField(max_length=20, verbose_name='品牌名称')
    Logo = models.ImageField(verbose_name='商品Logo图片')
    first_letter = models.CharField(max_length=1, verbose_name='品牌首字母')

    class Meta:
        db_table = 'tb_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """
    商品SPU
    SPU = Standard Product Unit （标准产品单位）
    SPU是商品信息聚合的最小单位，是一组可服用、易检索的标准化信息的集合，该集合描述了一个产品的特性。
    通俗的讲，属性值、特性相同的商品就可以称为一个SPU。
    """
    name = models.CharField(max_length=50, verbose_name='商品名称')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='商品品牌')
    category1 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT,
                                  related_name='cat1_goods', verbose_name='一级类别')
    category2 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT,
                                  related_name='cat2_goods', verbose_name='二级类别')
    category3 = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT,
                                  related_name='cat3_goods', verbose_name='三级类别')
    sales = models.IntegerField(default=0, verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评论量')

    desc_detail = RichTextUploadingField(default='', verbose_name='详细介绍')  # 支持富文本编辑以及文件上传
    desc_pack = RichTextField(default='', verbose_name='包装信息')  # 支持富文本编辑,但不支持文件上传
    desc_service = RichTextUploadingField(default='', verbose_name='售后服务')

    class Meta:
        db_table = 'tb_goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSpecification(BaseModel):
    """
    商品规格
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    name = models.CharField(max_length=20, verbose_name='规格名称')

    class Meta:
        db_table = 'tb_goods_specification'
        verbose_name = '商品规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.goods.name, self.name)  # 商品名: 商品规格


class SpecificationOption(BaseModel):
    """
    规格选项
    """
    spec = models.ForeignKey(GoodsSpecification, on_delete=models.CASCADE, verbose_name='规格')
    value = models.CharField(max_length=20, verbose_name='选项值')

    class Meta:
        db_table = 'tb_specification_option'
        verbose_name = '规格选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s - %s' % (self.spec, self.value)  # 规格: 规格的具体数值


class SKU(BaseModel):
    """
    商品SKU
    SKU = Stock Keeping Unit （库存量单位）
    SKU即库存进出计量的单位，可以是以件、盒、托盘等为单位，是物理上不可分割的最小存货单元。在使用时要根据不同业态，不同管理模式来处理。
    例如：iPhone X 全网通黑色256G 就是一个SKU，表示了具体的规格、颜色等信息。
    """
    name = models.CharField(max_length=50, verbose_name='名称')
    caption = models.CharField(max_length=100, verbose_name='副标题')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, verbose_name='商品类别')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='进价')
    market_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='市场价')
    stock = models.IntegerField(default=0, verbose_name='库存')
    sales = models.IntegerField(default=0, verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评价量')
    is_launched = models.BooleanField(default=True, verbose_name='是否上架销售')
    default_image_url = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name='默认图片')

    class Meta:
        db_table = 'tb_sku'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)  # 具体商品id: 具体商品名称


class SKUImage(BaseModel):
    """
    SKU图片
    """
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='sku')
    image = models.ImageField(verbose_name='图片')

    class Meta:
        db_table = 'tb_sku_image'
        verbose_name = 'SKU图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.sku.name, self.id)  # sku名称: 对应图片id


class SKUSpecification(BaseModel):
    """
    SKU具体规格
    """
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='sku')
    spec = models.ForeignKey(GoodsSpecification, on_delete=models.PROTECT, verbose_name='规格名称')
    option = models.ForeignKey(SpecificationOption, on_delete=models.PROTECT, verbose_name='商品规格值')

    class Meta:
        db_table = 'tb_sku_specification'
        verbose_name = 'SKU规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s - %s' % (self.sku, self.spec.name, self.option.value)  # sku名称: 规格名-规格值

