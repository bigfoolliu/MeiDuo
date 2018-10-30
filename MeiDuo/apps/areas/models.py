from django.db import models

# Create your models here.


class Area(models.Model):
    """
    地区模型,自关联,有省,市,区
    area: 深圳市
    area.parent_id: 广东省的id,这个是自动生成的
    area.area_set: 深圳市的区县,这个是自动生成的,此处改名为area.subs
    """
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subs', on_delete=None)

    class Meta:
        db_table = 'tb_areas'

    def __str__(self):
        return self.name
