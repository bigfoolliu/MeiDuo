#!-*-coding:utf-8-*-
# !@Date: 2018/10/29 15:41
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
执行发送邮件的耗时代码
"""
from django.conf import settings

from celery_tasks.main import app
from django.core.mail import send_mail  # django自带发送邮件的功能


@app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    """
    发送验证邮件
    :param to_email: 目的邮箱
    :param verify_url: 邮件中的验证url
    :return:
    """
    print(verify_url)  # TODO: 测试

    # 配发送的邮件的内容
    subject = '美多商城验证'  # 邮件主题
    # 发送的html邮件内容
    html_message = '<p>你好!</p>' \
                   '<p>感谢使用美多商城.</p>' \
                   '<p>您的邮箱为: %s</p>' \
                   '<p>点此链接激活您的邮箱:</p>' \
                   '<p><a href="%s">%s</a></p>' % (to_email, verify_url, verify_url)

    # 使用django自带的email功能发送邮件,此句为耗时代码
    send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)
