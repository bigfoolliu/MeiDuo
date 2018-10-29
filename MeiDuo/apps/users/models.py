from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from users import constants


class User(AbstractUser):
    """
    用户模型类
    继承于AbstractUser,其中就已经定义了很多的字段
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')  # 邮箱是否激活字段

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
        return 'http://site.meiduo.site:8000/success_verify_email.html?token=' + token

