> 这是对之前一个项目的升级 [旧版项目地址](https://github.com/wkunzhi/rbac-stark-crm)
包含可拆卸 权限组件rbac 与 stark插件 可以单独取出代码并运用到任意后端开发项目中。 该套CRM系统就是用rbac组件+stark组件开发的实例项目

# 开发环境
- Django 2.2.1
- Python 3.6
- Mysql 5.7

# 目录
- rbac **权限与菜单组件**
- stark **路由组件**
- web **业务逻辑**
- static **静态文件**
- Company.sql **数据库文件**
- GetFont.py **获取图标爬虫(不须使用)**

# 截图
**菜单分配**
![](https://github.com/wkunzhi/CRM-Manage/blob/master/static/img/img5.png)
**用户管理**
![](https://github.com/wkunzhi/CRM-Manage/blob/master/static/img/img4.png)
**权限分配**
![](https://github.com/wkunzhi/CRM-Manage/blob/master/static/img/img3.png)
**菜单路由**
![](https://github.com/wkunzhi/CRM-Manage/blob/master/static/img/img2.png)
**信息管理**
![](https://github.com/wkunzhi/CRM-Manage/blob/master/static/img/img1.png)

# 使用说明
1. 根目录下 `Company.sql` 为数据库， 需要先导入到自己数据库中！！！（数据库是我已经准备好的 ，需要导入一下）
2. 在 CompanyQuiry -> setting.py 中该部分设置导入后的数据库连接
    
    ```python
    DATABASES = {
        'default': {
            # 连接数据库类型 在末尾写入mysql即可
            'ENGINE': 'django.db.backends.mysql',
            # 数据库地址
            'HOST': '127.0.0.1',
            # 端口
            'PORT': 3306,
            # 数据库名
            'NAME': 'Company',
            # 用户
            'USER': 'root',
            # 密码
            'PASSWORD': ''
        }
    }
    ```
3. 启动Django项目


# rbac 组件使用
[**rbac 说明文档**](https://blog.zhangkunzhi.com/2019/12/13/crm%E7%BB%84%E4%BB%B6%E4%BD%BF%E7%94%A8/index.html)

# stark 组件使用说明

[**stark 说明文档**](https://blog.zhangkunzhi.com/2019/12/13/stark%E7%BB%84%E4%BB%B6%E4%BD%BF%E7%94%A8/index.html)

# 常见问题
- [添加菜单后页面访问失败] 
   ![](https://zok-blog.oss-cn-hangzhou.aliyuncs.com/images/20191226/WX20191226-110123%402x.png)
    原因：菜单设置的路径名与model中不匹配导致无法自动寻找到路由
    ![](https://zok-blog.oss-cn-hangzhou.aliyuncs.com/images/20191226/WX20191226-110354%402x.png)
    ![](https://zok-blog.oss-cn-hangzhou.aliyuncs.com/images/20191226/WX20191226-110423%402x.png)
    



# QQ讨论群

群号： 497377504

![](https://zok-blog.oss-cn-hangzhou.aliyuncs.com/2019/11/18/wx201911181627012x.png)
