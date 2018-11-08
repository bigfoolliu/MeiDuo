# 美多商城项目

## 准备

+ 在/front_end_pc目录下通过node.js提供的**live-server**服务作为前端服务器
+ live-server运行在8080端口下，可以通过**127.0.0.1:8080**来访问静态页面

命令:

    ```text
    安装node.js的版本控制工具nvm，在终端中执行:
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
    
    nvm安装最新版本的node.js
    nvm install node
    
    安装live-server
    npm install -g live-server
    
    创建数据库
    create database meiduo_mall default charset=utf8;
     
    为本项目创建数据库用户（不再使用root账户）
    create user meiduo identified by 'meiduo';      创建用户账号 meiduo, 密码 meiduo (由identified by 指明)
    grant all on meiduo_mall.* to 'meiduo'@'%';     授权meiduo_mall数据库下的所有表的所有权限以任何ip访问数据库给用户meiduo
    flush privileges;                               刷新生效用户权限
    ```

## 项目架构

如图：

![image](https://github.com/bigfoolliu/MeiDuo/tree/linux_version/images/项目整体架构.png)

## 目录说明

> MeiDuo
>> MeiDuo
>>> apps---------->存放Django应用
>>>> areas-------->收货地址模块
>>>>
>>>> carts-------->购物车磨模块
>>>>
>>>> contents----->
>>>>
>>>> goods--------->商品模块
>>>>
>>>> oauth--------->第三方登录(qq登录)模块
>>>>
>>>> orders-------->订单模块
>>>>
>>>> users--------->用户模块
>>>>
>>>> verifications-->
>>>>
>>> logs---------->存放日志文件
>>>
>>> settings------>存放配置文件的目录，分为开发dev和线上prod
>>>
>>> utils--------->存放项目自己定义的公共函数或类等
>>>
>>> templates----->存放模板文件
>>>> search------->
>>>>
>>>
>>> docs---------->用于存放一些说明文档资料
>>>
>> celery_tasks--->用于存放使用celery执行的耗时任务代码
>>> email--------->发送email耗时代码
>>>
>>> html---------->生成静态html耗时代码
>>>
>>> sms------------>发送短信验证码耗时代码
>>>
>>
>> images--------->用于存放README文件中的图片
>>
>> scripts-------->用于存放管理脚本文件
>>
>>
>> .gitignore
>>
>> manage.py
>>
>> README.MD

## 用户模型类

### Django认证系统组成

[参考文档](https://yiyibooks.cn/xx/Django_1.11.6/topics/auth/index.html)

+ 用户
+ 权限：二元（是/否）标志指示一个用户是否可以做一个特定的任务。
+ 组：对多个用户运用标签和权限的一种通用的方式。
+ 一个可配置的密码哈希系统
+ 用户登录或内容显示的表单和视图
+ 一个可插拔的后台系统

Django默认提供的认证系统中，用户的认证机制依赖Session机制，
我们在本项目中将引入JWT认证机制，将用户的身份凭据存放在token中，然后对接Django的认证系统,实现:

+ 用户的数据模型
+ 用户密码的加密与验证
+ 用户的权限系统

## 设置域名

+ 前端: www.meiduo.site
+ 后端: api.meiduo.site

前后端访问使用不同的域名,所以当端访问前端的数据时,需要添加CORS(跨域访问)的配置.
[使用django-cors-headers扩展解决跨域问题参考文档](https://github.com/ottoyiu/django-cors-headers/)

    ```text
    编辑/etc/hosts文件，可以设置本地域名
    sudo vim /etc/hosts
    
    在文件中增加两条信息
    127.0.0.1   api.meiduo.site
    127.0.0.1   www.meiduo.site
    ```

一旦不再使用127.0.0.1访问Django后端，需要在配置文件中修改ALLOWED_HOSTS，增加可以访问后端的域名.

    ```text
    ALLOWED_HOSTS = [
        'api.meiduo.site', 
        '127.0.0.1', 
        'localhost', 
        'www.meiduo.site'
    ]
    ```


## 注册业务

实现以下几个接口:

+ 短信验证码
+ 用户名判断是否存在
+ 手机号判断是否存在
+ 注册保存用户数据

### 短信验证码

业务流程:

1. 检查是否在60s内有发送记录
2. 生成短信验证码
3. 保存短信验证码与发送记录
4. 发送短信

#### 后端接口设计

+ 访问方式:  GET /sms_code/(?P<mobile>1[3-9]\d{9})/
+ 请求参数:  路径参数与查询字符串参数

    ```text
    参数名   类型    是否必须     说明
    mobile	str	    是	        手机号
    ```

+ 返回数据: JSON

    ```text
    参数名       类型    是否必须     说明
    message	    str	    否	        OK，发送成功
    ```

### celery

等候短信验证码是一个耗时代码,在使用框架的基础上,可以使用该包来实现异步.

构成如下:

+ task: 任务-------->函数,封装了耗时代码
+ broker: 代理人---->指定队列保存位置,如redis
+ worker: 工人------>从队列中获取任务并执行
+ queue: 队列------->先进先出,维护任务的先后顺序

```text
启动celery服务
celery -A celery_tasks.main worker -l info
```

win10上运行celery4.x会出现这个问题,需要安装一个包并在执行的时候添加参数:

```text
pip install eventlet
celery -A celery_tasks.main worker -l info -P eventlet
```

### 判断账号是否存在后端接口

+ 访问方式:  GET /usernames/(?P<username>\w{5,20})/count/
+ 请求参数:  路径参数与查询字符串参数

    ```text
    参数名      类型   是否必须    说明
    username    str    是	    用户名
    ```

+ 返回数据: JSON

    ```text
    参数名      类型    是否必须   说明
    username    str     是      用户名
    count       int     是      数量
    ```

### 判断手机号是否存在后端接口

+ 访问方式:  GET /mobiles/(?P<mobile>1[3-9]\d{9})/count/
+ 请求参数:  路径参数与查询字符串参数

    ```text
    参数名      类型   是否必须    说明
    mobile     str	  是        手机号
    ```

+ 返回数据: JSON

    ```text
    参数名      类型    是否必须   说明
    mobile     str     是        手机号
    count      int     是        数量
    ```

### 注册后端接口

+ 访问方式:  POST /users/
+ 请求参数:  JSON或表单

    ```text
    参数名          类型    是否必须     说明
    username        str     是         用户名
    password        str     是         密码
    password2       str     是         确认密码
    sms_code        str     是         短信验证码
    mobile          str     是         手机号
    allow           str     是         是否同意用户协议
    ```

+ 返回数据: JSON

    ```text
    返回值      类型    是否必须      说明
    id          int     是          用户id
    username    str     是          用户名
    mobile      str     是          手机号
    ```

### JWT

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

+ 访问方式:  PUT emails/
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

实际使用时可以直接在视图集里继承一下该类即可.我们想把缓存数据保存在redis中，且设置有效期，可以通过在配置文件中定义的方式来实现.

### 用户地址管理

## 商品

我们将通过Django上传的图片保存到了FastDFS中，而保存在FastDFS中的文件名没有后缀名，
ckeditor在处理上传后的文件名按照有后缀名来处理，所以会出现bug错误.
修改django-ckeditor库的ckeditor_uploader/views.py中的代码.

### FastDFS分布式文件系统

使用 FastDFS 很容易搭建一套高性能的文件服务器集群提供文件上传、下载等服务.

FastDFS 架构包括 Tracker server 和 Storage server.

+ Tracker server 作用是负载均衡和调度, 通过 Tracker server 在文件上传时可以根据一些 策略找到 Storage server 提供文件上传服务。
可以将 tracker 称为追踪服务器或调度服务器.
+ Storage server 作用是文件存储，客户端上传的文件最终存储在 Storage 服务器上,
Storageserver 没有实现自己的文件系统而是利用操作系统 的文件系统来管理文件。可以将 storage 称为存储服务器.

### Docker

容器技术可以让多个独立的用户空间运行 在同一台宿主机上.可以为各种测试提供很好的沙盒环境.好处有：

1. 加速本地开发和构建流程，使其更加高效、更加轻量化
2. 能够让独立的服务或应用程序在不同的环境中，得到相同的运行结果.
3. 用 Docker 创建隔离的环境来进行测试
4. Docker 可以让开发者先在本机上构建一个复杂的程序或架构来进行测试，而不是 一开始就在生产环境部署、测试.

#### Docker镜像(image)

用户基于镜像来运行自己的容器.可以将镜像当作容器的“源代码”.

#### Docker容器(container)

把自己的应用程序或者服务打包放进容器.容器基于镜像启动，一旦容器启动完成后，我们就可以登录到容器中安装自己需要的软件或者服务.

#### 常用命令

1. 首次开启tracker服务 
docker run -dti --network=host --name tracker -v /var/fdfs/tracker:/var/fdfs delron/fastdfs tracker
2. 查看运行的容器
docker container ls
3. 停止tracker服务
docker container stop tracker
4. 再次开启tracker服务
docker container start tracker
5. 首次开启storage服务
docker run -dti --network=host --name storage -e TRACKER_SERVER=本机ip:22122 -v /var/fdfs/storage:/var/fdfs delron/fastdfs storage
6. 再次开启和关闭storage服务的命令和tracker相同

使用时注意每次本地的ip发生更改，则重新作为首次开启storage服务，以及修改client.conf文件中的ip！！！
数据保存目录: /var/fdfs/storage/data
如果无法重新运行，可以删除/var/fdfs/storage/data目录下的fdfs_storaged.pid 文件，然后重新运行storage.

### 富文本编辑器

使用ckeditor库来实现.

### 定时任务

使用django-crontab库实现.

常用命令：

1. 添加定时任务到系统中 python manage.py crontab add
2. 显示已经激活的定时任务 python manage.py crontab show
3. 移除定时任务 python manage.py crontab remove

### 商品搜索

使用haystack　+ Elasticsearch实现模糊搜索.

haystack:
+ 作为一个驱动包
+ Haystack为Django提供了模块化的搜索

Elasticsearch:
+ 它可以快速地储存、搜索和分析海量数据
+ Elasticsearch 不支持对中文进行分词建立索引，需要配合扩展elasticsearch-analysis-ik来实现中文分词处理


使用Docker安装Elasticsearch及其扩展
+ docker image pull delron/elasticsearch-ik:2.4.6-1.0
+ 修改elasticsearch的配置文件 elasticsearc-2.4.6/config/elasticsearch.yml第54行，更改ip地址为本机ip地址
+ docker run -dti --network=host --name=elasticsearch -v /home/python/elasticsearch-2.4.6/config:/usr/share/elasticsearch/config delron/elasticsearch-ik:2.4.6-1.0

命令：
1. 手动生成初始索引　python manage.py rebuild_index

## 购物车设计

存储结构:
1. 用户登陆使用redis存储加入购物车的商品
2. 用户未登陆使用cookie来存储加入购物车的商品
3. 登陆后合并购物车

### 添加到购物车后端接口

访问此接口，无论用户是否登录，前端请求都需携带请求头Authorization，由后端判断是否登录.

+ 访问方式:  POST　cart/
+ 请求参数:  json或表单

    ```text
    参数名       类型    是否必须     说明
    sku_id	    int	    是	        商品sku_id
    count	    int	    是	        数量
    selected	bool	否	        是否勾选，默认勾选
    ```

+ 返回数据: JSON

    ```text
    参数名       类型    是否必须     说明
    sku_id	    int	    是	        商品sku_id
    count	    int	    是	        数量
    selected	bool	是	        是否勾选，默认勾选
    ```

### 查询购物车后端接口

+ 访问方式:  GET　cart/
+ 请求参数:  无
+ 返回数据: JSON

    ```text
    参数名               类型    是否必须     说明
    id	                int	    是	        商品sku id
    count	            int	    是	        数量
    selected	        bool	是	        是否勾选，默认勾选
    name	            str	    是	        商品名称
    default_image_url	str	    是	        商品默认图片
    price	            decimal	是	        商品单价
    ```

### 修改购物车后端接口

+ 访问方式:  PUT　cart/
+ 请求参数:  json或表单

    ```text
    参数名       类型    是否必须     说明
    sku_id	    int	    是	        商品sku id
    count	    int	    是	        数量
    selected	bool	否	        是否勾选，默认勾选
    ```

+ 返回数据: JSON

    ```text
    参数名       类型    是否必须     说明
    sku_id	    int	    是	        商品sku id
    count	    int	    是	        数量
    selected	bool	是	        是否勾选，默认勾选
    ```

### 删除购物车后端接口

+ 访问方式:  DELETE　cart/
+ 请求参数:  json或表单

    ```text
    参数名       类型    是否必须     说明
    sku_id	    int	    是	        商品sku id
    ```

+ 返回数据: 无，状态码204

### 购物车全选后端接口

+ 访问方式:  PUT　cart/selection/
+ 请求参数:  json或表单

    ```text
    参数名       类型    是否必须     说明
    selected	bool	是	    是否全选，true表示全选，false表示取消全选
    ```

+ 返回数据: JSON

    ```text
    参数名       类型    是否必须     说明
    message	    str	    是	        ok
    ```

### 登录合并购物车

即将未登录时加入购物车中的cookie数据合并到登录账户中，默认由cookie会直接增加到登录的用户redis购物车数据中。

普通登录和qq登录都需要合并，故将合并的代码放到一个单独的模块。在普通登录和qq登录的视图post方法的代码中进行更改。

## 订单

### 订单结算后端接口

+ 访问方式:  GET orders/settlement/
+ 请求参数:  无
+ 返回数据: JSON

    ```text
    参数名               类型      是否必须     说明
    freight	            decimal	    是	    运费
    skus	            sku[]	    是	    结算的商品列表
    id	                int	        是	    商品id
    name	            str	        是	    商品名称
    default_image_url	str	        是	    商品默认图片
    price	            decimal	    是	    商品单价
    count	            int	        是	    商品数量
    ```

### 保存订单后端接口

+ 访问方式:  POST orders/
+ 请求参数:  json或表单

    ```text
    参数名       类型    是否必须     说明
    address	    int	    是	    收货地址id
    pay_method	int	    是	    支付方式
    ```

+ 返回数据: JSON

    ```text
    参数名       类型    是否必须     说明
    order_id	char	是	        订单编号
    ```

### 下单并发问题

解决方法:

1. 悲观锁 当查询某条记录时，即让数据库为该记录加锁，锁住记录后别人无法操作
2. 乐观锁 不是真实的锁,而是在更新的时候判断此时的库存是否是之前查询出的库存,相同表示没人修改,可更新库存,否则表示别人抢过资源,不再执行库存更新
3. 任务队列 将下单的逻辑放到任务队列中（如celery）,将并行转为串行,所有人排队下单.比如开启只有一个进程的Celery,一个订单一个订单的处理

### 修改MySQL的事务隔离级别

事务隔离级别指的是在处理同一个数据的多个事务中，一个事务修改数据后，其他事务何时能看到修改后的结果。

MySQL数据库事务隔离级别主要有四种：

+ Serializable 串行化，一个事务一个事务的执行
+ Repeatable read 可重复读，无论其他事务是否修改并提交了数据，在这个事务中看到的数据值始终不受其他事务影响
+ Read committed 读取已提交，其他事务提交了对数据的修改后，本事务就能读取到修改后的数据值
+ Read uncommitted 读取未提交，其他事务只要修改了数据，即使未提交，本事务也能看到修改后的数据值。

MySQL数据库默认使用可重复读（ Repeatable read），而使用乐观锁的时候，如果一个事务修改了库存并提交了事务，
那其他的事务应该可以读取到修改后的数据值，所以不能使用可重复读的隔离级别，应该修改为读取已提交Read committed。

```text
cd /etc/mysql/mysql.conf.d
sudo vi mysqld.cnf
在配置的末尾一行添加配置:
transaction-isolation=READ-COMMITTED
```

## 支付宝支付

对接支付宝：

参考其官方文档: [支付宝开发平台登录](https://open.alipay.com/platform/home.htm)

## 使用xadmin管理后台

命令

```text
使用django２,因此安装xadmin版本的分支
pip install git+git://github.com/sshwsfc/xadmin.git@django2
```

