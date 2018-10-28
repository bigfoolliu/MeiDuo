from django.db import models

# Create your models here.
from MeiDuo.utils.models import BaseModel


class QQUser(BaseModel):
    """
    新建一张表,用于维护以qq账号登录的用户,将其与手机号注册的用户关联
    如果是其他的第三方登录方式,则再次新建一张表进行维护,以尽量不更改原始的表和代码为主
    """
    # openid是用户的qq账号在qq网站的唯一标识
    openid = models.CharField(max_length=64)
    # 关联本网站的用户
    user = models.ForeignKey('users.User', on_delete=None)

    class Meta:
        db_table = 'tb_oauth_qq'

