#!-*-coding:utf-8-*-
# !@Date: 2018/10/23 22:13
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
用于指定特定的任务(耗时代码)
该文件tasks.py文件名不能更改
"""
from MeiDuo.utils.ytx_sdk.sendSMS import CCP
from celery_tasks.main import app


@app.task(name='send_sms_code')  # 通过加装饰器来使该函数成为任务
def send_sms_code(mobile, code, expires, template_id):
    """
    发送短信的耗时代码
    :param mobile: 目的手机号
    :param code: 短信验证码
    :param expires: 过期时间
    :param template_id: 短信模板id
    :return:
    """
    # CCP.sendTemplateSMS(mobile, code, expires, template_id)
    print(code)  # TODO: 临时创建，需修改为上式


@app.task(name='test_func')
def test_func():
    """
    测试函数
    :return:
    """
    print('test_func processing...')  # TODO: 测试任务

