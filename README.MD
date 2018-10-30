# 美多商城项目

## 准备

+ 在/front_end_pc目录下通过node.js提供的**live-server**服务作为前端服务器
+ live-server运行在8080端口下，可以通过**127.0.0.1:8080**来访问静态页面

### 目录说明

> MeiDuo
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

+ 前端: www.meiduo.site
+ 后端: api.meiduo.site

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

#### 构成如下

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
username        str     是          用户名
password        str     是          密码
password2       str     是          确认密码
sms_code        str     是          短信验证码
mobile          str     是          手机号
allow           str     是          是否同意用户协议
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

#### JWT

Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).
不再使用Session认证机制, 而使用Json Web Token认证机制.

JWT的组成:

+ 头部(header),声明类型(jwt)和声明加密的算法(通常为hmac sha256)
+ 载荷(payload),存放标准中注册的声明、公共的声明和私有的声明
+ 签证(signature),由header(base64加密后的)、payload(base64加密后的)和secret(保存在服务器)组成

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.(第一部分)
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.(第二部分)
TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ(第三部分)
```

基于token的鉴权机制流程:

+ 用户使用用户名密码来请求服务器
+ 服务器进行验证用户的信息
+ 服务器通过验证发送给用户一个token
+ 客户端存储token，并在每次请求时附送上这个token值
+ 服务端验证token值，并返回数据

## 登录业务

使用Django自带的用户认证系统(django.contrib.auth).

认证系统包含:

+ 用户
+ 权限：二元（是/否）标志指示一个用户是否可以做一个特定的任务。
+ 组：对多个用户运用标签和权限的一种通用的方式。
+ 一个可配置的密码哈希系统
+ 用户登录或内容显示的表单和视图
+ 一个可插拔的后台系统

### 后端接口设计

+ 访问方式:  POST /authorizations/
+ 请求参数:

```text
参数名          类型    是否必须     说明
username        str     是          用户名
password        str     是          密码
```

+ 返回数据: JSON

```text
参数名          类型    是否必须     说明
username        str     是          用户名
user_id         int     是          用户id
token           str     是          身份认证凭据
```

### 第三方登录--QQ登录

步骤:

1. 首先成为qq互联的开发者,需注册
2. 创建应用,获取项目的appid(应用的唯一标识)和appkey(appid对应的密钥)
3. 放置“QQ登录”按钮_OAuth2.0
4. 获取Authorization Code(GET方式请求网址:https://graph.qq.com/oauth2.0/authorize 并携带参数)
5. 通过Authorization_Code获取Access_Token(GET方式请求网址:https://graph.qq.com/oauth2.0/token 并携带参数)
6. 通过Access Token,得到对应用户身份的OpenID(网站上或应用中唯一对应用户身份的标识,网站或应用可将此ID进行存储，便于用户下次登录时辨识其身份，或将其与用户在网站上或应用中的原有账号进行绑定)

### urllib

在后端接口中，我们需要向QQ服务器发送请求，查询用户的QQ信息，Python提供了标准模块urllib可以帮助我们发送http请求。

+ urllib.parse.urlencode(query)------将query字典转换为url路径中的查询字符串
+ urllib.parse.parse_qs(qs)------将qs查询字符串格式数据转换为python的字典
+ urllib.request.urlopen(url, data=None)------发送http请求，如果data为None，发送GET请求，如果data不为None，发送POST请求返回response响应对象，可以通过read()读取响应体数据，需要注意读取出的响应体数据为bytes类型

### 返回QQ登录网址后端接口设计

+ 访问方式:  GET /oauth/qq/authorization/?next=xxx
+ 请求参数:  查询字符串

```text
参数名  类型    是否必须     说明
next    str     否        用户QQ登录成功后进入美多商城的哪个网址
```

+ 返回数据: JSON

```text
参数名          类型    是否必须     说明
login_url      str     是          qq登录网址
```

### QQ登录回调处理

本项目中,QQ登录开发资质时配置的回调地址为：
http://www.meiduo.site:8080/oauth_callback.html

+ 访问方式:  GET /oauth/qq/user/?code=xxx
+ 请求参数:  查询字符串

```text
参数名  类型    是否必须     说明
code    str     是        qq返回的授权凭证code
```

+ 返回数据: JSON

```text
参数名          类型    是否必须     说明
access_token   str     否         用户是第一次使用QQ登录时返回，其中包含openid，用于绑定身份使用，注意这个是我们自己生成的
token          str     否         用户不是第一次使用QQ登录时返回，登录成功的JWT token
username       str     否         用户不是第一次使用QQ登录时返回，用户名
user_id        int     否         用户不是第一次使用QQ登录时返回，用户id
```

### 绑定用户接口

用户是首次使用QQ登录，则需要绑定用户.

+ 访问方式:  GET /oauth/qq/user/
+ 请求参数:  查询字符串

```text
参数名           类型    是否必须     说明
mobile          str     是          手机号
password        str     是          密码
sms_code        str     是          短信验证码
access_token    str     是          凭据(包含openid)
```

+ 返回数据: JSON

```text
参数名       类型    是否必须     说明
token       str     是          JWT token
id          int     是          用户id
username    str     是          用户名
```

## 邮件验证

步骤:

1. 用户点击保存邮箱
2. 向用户的邮箱发送一封验证邮件(邮件携带激活链接, 跳转网址+token参数验证身份)
3. 用户点击激活链接,跳转至验证成功页面,同时将User模型的email_active字段状态调整为True

在django.core.mail模块提供了send_mail来发送邮件。

send_mail(subject, message, from_email, recipient_list,html_message=None)

+ subject 邮件标题
+ message 普通邮件正文， 普通字符串
+ from_email 发件人
+ recipient_list 收件人列表
+ html_message 多媒体邮件正文，可以是html字符串

### 发送邮件后端接口

+ 访问方式:  PUT /emails/
+ 请求参数:  JSON或表单

```text
参数名  类型    是否必须     说明
email   str     是        Email邮箱
```

+ 返回数据: JSON

```text
参数名  类型    是否必须     说明
id      int     是          用户id
email   str     是          Email邮箱
```

### 验证邮件后端接口

+ 访问方式:  GET /emails/verification/?token=xxx
+ 请求参数:  查询字符串

```text
参数名  类型    是否必须     说明
token   str     是        用于验证邮箱的token
```

+ 返回数据: JSON

```text
参数名      类型    是否必须     说明
message     str     是          验证处理结果
```

## 收货地址

主要的业务逻辑有：

1. 省市区地址的数据库建立与查询
2. 用户地址的增删改查处理
3. 设置默认地址
4. 设置地址标题

省市区三级联动
在Django REST framework中使用缓存

### 请求省份后端接口

+ 访问方式:  GET areas/
+ 请求参数:  无

+ 返回数据: JSON

```text
参数名  类型    是否必须     说明
id      int     是          省份id
name    str     是          省份名称
```

### 请求城市或区县后端接口

+ 访问方式:  GET areas/(?P<pk>\d+)/
+ 请求参数:  路径参数

```text
参数名  类型    是否必须     说明
pk      int     是          上级区划id（省份id用于获取城市数据，或城市id用于获取区县数据）
```

+ 返回数据: JSON

```text
参数名  类型    是否必须     说明
id      int     是          上级区划id（省份id或城市id）
name    str     是          上级区划的名称
subs    list[]  是          下属所有区划信息
```

### 缓存

通过pip安装扩展 drf-extensions来实现地址的缓存,从而不必每次都从数据库里进行数据查找.

使用方式:

1. 直接在视图的请求方法上添加装饰器 @cache_response(timeout=60*60, cache='default')
2. 使用drf-extensions提供的扩展类

        ListCacheResponseMixin
        用于缓存返回列表数据的视图，与ListModelMixin扩展类配合使用，实际是为list方法添加了cache_response装饰器

        RetrieveCacheResponseMixin
        用于缓存返回单一数据的视图，与RetrieveModelMixin扩展类配合使用，实际是为retrieve方法添加了cache_response装饰器

        CacheResponseMixin
        为视图集同时补充List和Retrieve两种缓存，与ListModelMixin和RetrieveModelMixin一起配合使用。

实际使用时可以直接在视图集里继承一下该类即可.我们想把缓存数据保存在redis中，且设置有效期，可以通过在配置文件中定义的方式来实现

