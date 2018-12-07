# 验证模块包含
* User    用户数据表包含:username,password,email,is_active
* Group 用户组
* Permission 存放用户和组的权限


# 一个登录的视图
* 通过用户提交的表单获取用户名和密码
* 将用户名和密码与数据库中的数据进行匹配
* 检查用户是否处于活跃状态
* 通过在http请求上附加session,让用户进入登录状态



# 使用消息框架
* django.contrib.messagses 和 MessageMiddleware 共同构成了消息系统


# sorl-thumbnail
* 这个模块采用两种方式缩略图
* 提供了一个新的标签模板{% thumbnail %}
* 二是基于ImageField自定义的图片字段


# 使用jquery发送ajax请求
* AJAX Asynchronous javascript and XML
* xml不是必须采用的格式, 还可以是json和html或者纯文本



