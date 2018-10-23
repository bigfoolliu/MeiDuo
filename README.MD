# 美多商城项目

## 准备

+ 在/front_end_pc目录下通过node.js提供的**live-server**服务作为前端服务器
+ live-server运行在8080端口下，可以通过**127.0.0.1:8080**来访问静态页面

### 目录说明

> Meiduo
>> front_end_pc
>>
>> MeiDuo
>>> apps 存放Dajango应用
>>>
>>> logs 存放日志文件
>>>
>>> settings 存放配置文件的目录，分为开发dev和线上prod
>>>
>>> utils 存放项目自己定义的公共函数或类等
>>>
>>> docs 用于存放一些说明文档资料
>>>
>>> scripts 用于存放管理脚本文件
>>>
>>> libs 存放第三方的库文件
>>>
>> templates
>>
>> .gitignore
>>
>> manage.py
>>
>> README.MD
>>

## 用户模型类

### Django认证系统组成

+ 用户
+ 权限：二元（是/否）标志指示一个用户是否可以做一个特定的任务。
+ 组：对多个用户运用标签和权限的一种通用的方式。
+ 一个可配置的密码哈希系统
+ 用户登录或内容显示的表单和视图
+ 一个可插拔的后台系统

Django默认提供的认证系统中，用户的认证机制依赖Session机制，我们在本项目中将引入JWT认证机制，将用户的身份凭据存放在Token中，然后对接Django的认证系统,实现:

+ 用户的数据模型
+ 用户密码的加密与验证
+ 用户的权限系统

## 设置域名

+ 前端	www.meiduo.site
+ 后端	api.meiduo.site