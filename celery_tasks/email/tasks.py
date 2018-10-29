#!-*-coding:utf-8-*-
# !@Date: 2018/10/29 15:41
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
执行发送邮件的耗时代码
"""

from celery_tasks.main import app
from django.core.mail import send_mail  # django自带发送邮件的功能


@app.task(name='send_verify_email')
def send_verify_mail(to_email, verify_url):
    """
    发送验证邮件
    :param to_email: 目的邮箱
    :param verify_url: 邮件中的验证url
    :return:
    """
    pass

