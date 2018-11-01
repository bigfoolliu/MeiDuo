#!-*-coding:utf-8-*-
# !@Date: 2018/11/1 20:00
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
示例程序,来展示如何上传文件
"""
from fdfs_client.client import Fdfs_client


if __name__ == '__main__':
    # 指定一个Fdfs客户端对象,并指定配置文件
    client = Fdfs_client('client.conf')
    # 上传文件(会返回文件名)
    ret = client.upload_by_file('1.PNG')
    print(ret)

"""
正确结果:
{
    'Uploaded size': '12.00KB',
    'Status': 'Upload successed.',
    'Storage IP': '192.168.247.128',
    'Group name': 'group1',
    'Local file name': '/home/python/Desktop/pic/avatar/1.jpg',
    'Remote file_id': 'group1/M00/00/02/wKj3gFvaou-ACZ2EAAAwL_xHUtE202.jpg'
}
"""