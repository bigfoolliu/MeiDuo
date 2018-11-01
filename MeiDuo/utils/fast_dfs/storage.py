#!-*-coding:utf-8-*-
# !@Date: 2018/11/1 20:45
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
保存文件的代码
"""
from fdfs_client.client import Fdfs_client

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible  # 加该装饰器,则它在迁移中的一个字段上使用的时候可以被序列化
class FdfsStorage(Storage):
    """
    上传文件到fastdfs的类
    下面的方法都是重写django的文件存储Storage类中的方法
    """

    def open(self, name, mode='rb'):
        """
        重写django中的打开文档方法
        文件保存在fastdfs中，读取由fastdfs做，不需要django操作，此方法无用
        :param name:
        :param mode:
        :return:
        """
        pass

    def save(self, name, content, max_length=None):
        """
        重写django中的保存文档方法, 将文档存储到fastdfs
        :param name: 传入的文件名
        :param content: 文件内容
        :param max_length:
        :return: 保存到数据库中的FastDFS的文件名
        """
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        ret = client.upload_by_buffer(content.read())  # 读取request中的文件用content

        # 判断是否上传成功
        if ret['Status'] != 'Upload successed.':
            raise Exception('文件保存失败')

        # 返回上传成功到FastDFS的文件名
        return ret['Remote file_id']

    def exists(self, name):
        """
        判断文件是否存在，FastDFS可以自行解决文件的重名问题
        所以此处返回False，告诉Django上传的都是新文件
        :param name:
        :return:
        """
        return False

    def url(self, name):
        """
        返回文件的完整URL路径
        :param name: 数据库中保存的文件名
        :return: 完整的URL
        """
        return settings.FDFS_URL + name

