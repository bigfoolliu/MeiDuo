# 美多商城项目

## 准备

+ 在/front_end_pc目录下通过node.js提供的**live-server**服务作为前端服务器
+ live-server运行在8080端口下，可以通过**127.0.0.1:8080**来访问静态页面

### 目录说明

> Meiduo
>> front_end_pc
>>
>> celery_tasks
>>
>> MeiDuo
>>> apps------>存放Dajango应用
>>>
>>> logs------>存放日志文件
>>>
>>> settings-->存放配置文件的目录，分为开发dev和线上prod
>>>
>>> utils----->存放项目自己定义的公共函数或类等
>>>
>>> docs------>用于存放一些说明文档资料
>>>
>>> scripts--->用于存放管理脚本文件
>>>
>>> libs------>存放第三方的库文件
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

前后端访问使用不同的域名,所以当端访问前端的数据时,需要添加CORS(跨域访问)的配置.

## 注册业务

实现以下几个接口:

+ 短信验证码
+ 用户名判断是否存在
+ 手机号判断是否存在
+ 注册保存用户数据

### 短信验证码

#### 业务流程

1. 检查是否在60s内有发送记录
2. 生成短信验证码
3. 保存短信验证码与发送记录
4. 发送短信
   
#### 后端接口设计

+ 访问方式:  GET /sms_code/(?P<mobile>1[3-9]\d{9})/
+ 请求参数: mobile: str,必须有,手机号
+ 返回数据: message: str,非必传,OK(发送成功),JSON

### celery

等候短信验证码是一个耗时代码,在使用框架的基础上,可以使用该包来实现异步.

#### 构成如下:

+ task: 任务-------->函数,封装了耗时代码
+ broker: 代理人---->指定队列保存位置,如redis
+ worker: 工人------>从队列中获取任务并执行
+ queue: 队列------->先进先出,维护任务的先后顺序

启动celery服务

进入到终端, 编写如下命令执行(linux):

```text
celery -A celery_tasks.main worker -l info
```

win10上运行celery4.x会出现这个问题,需要安装一个包并在执行的时候添加参数:

```text
pip install eventlet
celery -A celery_tasks.main worker -l info -P eventlet
```

### 判断账号是否存在

#### 后端接口设计

+ 访问方式:  GET usernames/(?P<username>\w{5,20})/count/
+ 请求参数: username: str,必须有,用户名
+ 返回数据: username: str,必须有,用户名; count: int,必须有,数量

```json
{
    "username": "itcast",
    "count": "1"
}
```

### 判断手机号是否存在

#### 后端接口设计

+ 访问方式:  GET mobiles/(?P<mobile>1[3-9]\d{9})/count/
+ 请求参数: mobile: str,必须有,用户名
+ 返回数据: mobile: str,必须有,手机号; count: int,必须有,数量

```json
{
    "mobile": "13112341234",
    "count": "1"
}
```

### 具体注册

#### 后端接口设计

+ 访问方式:  POST /users/
+ 请求参数:

```text
参数名          类型    是否必须     说明
username        str	是          用户名
password        str	是          密码
password2       str	是          确认密码
sms_code        str	是          短信验证码
mobile          str	是          手机号
allow           str	是          是否同意用户协议
```

+ 返回数据:

```text
返回值      类型    是否必须    说明
id          int     是      用户id
username    str     是      用户名
mobile      str     是      手机号

```

```json
{
    "mobile": "13112341234",
    "count": "1"
}
```

