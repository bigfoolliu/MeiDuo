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
    ret = client.upload_by_file('1.jpg')
    print(ret)

"""
正确结果:
{
    'Group name': 'group1',
    'Remote file_id': 'group1/M00/00/00/wKhAg1vcRYuAU2wDACkhPO9qQ1o192.jpg',
    'Status': 'Upload successed.',
    'Local file name': '1.jpg',
    'Uploaded size': '2.00MB',
    'Storage IP': '192.168.64.131'
}

数据保存目录: /var/fdfs/storage/data
"""
