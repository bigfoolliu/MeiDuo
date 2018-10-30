from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from MeiDuo.utils.models import BaseModel
from users import constants


class User(AbstractUser):
    """
    用户模型类
    继承于AbstractUser,其中就已经定义了很多的字段
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')  # 邮箱是否激活字段

    # 默认收货地址
    default_address = models.OneToOneField('users.Address', related_name='user_addr', null=True,
                                           blank=True, on_delete=None)

    class Meta:
        db_table = 'tb_users'  # 表名
        verbose_name = '用户'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 单复数格式相同

    def generate_verify_url(self):
        """
        生成用户验证邮箱的url
        :return:
        """
        # 需要加密的信息
        data = {'user_id': self.id}
        # 生成token
        import tjws
        token = tjws.dumps(data, constants.VERIFY_EMAIL_EXPIRES)

        # 返回验证用的url
        return 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token


class Address(BaseModel):
    """
    用户收藏的地址
    """
    user = models.ForeignKey(User, related_name='addresses', on_delete=None, verbose_name='用户')  # 地址所属的用户
    title = models.CharField(max_length=20, verbose_name='地址名称')  # 地址标题: '学校', '家'等
    receiver = models.CharField(max_length=10)  # 收件人
    province = models.ForeignKey('areas.Area', related_name='province_addr', on_delete=None, verbose_name='省')  # 所属省
    city = models.ForeignKey('areas.Area', related_name='city_addr', on_delete=None, verbose_name='市')  # 所属市
    district = models.ForeignKey('areas.Area', related_name='district_addr', on_delete=None, verbose_name='区')  # 所属区县
    place = models.CharField(max_length=100, verbose_name='地址')  # 详细地址
    mobile = models.CharField(max_length=11, verbose_name='手机号')  # 手机号
    tel = models.CharField(max_length=20, null=True, blank=True, verbose_name='固定电话')  # 固定电话
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='邮箱')  # 邮箱
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')  # 逻辑删除

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
