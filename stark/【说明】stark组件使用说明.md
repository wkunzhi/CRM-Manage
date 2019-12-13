> 先将stark目录组件拷贝进需要的项目中

1. 在需要stark功能的 app内，创建stark.py ，django会在启动时候自动读取其中内容（单例模式）
2. 在其中添加代码如 参考`web/stark.py`的方法，可以自定制 ,当然定制内容写到了web/views/xxx对应py文件中
3. 添加路由 `url(r'^stark', site.urls),`  参考 urls.py的添加方法


# 自定义方法
1. 显示choice的中文
```python
from stark.service.v1 import get_choice_text

get_choice_text('性别', 'gender')  # 原理：使用了闭包函数
```
2. 通过modelForm修改字段显示顺序
```python
# 用户表
class UserInfoModelForm(StarkModelForm):
    """
    修改字段显示顺序
    自定义展示顺序，因为原理用的ModelForm，所以这里直接引用修改即可
    """
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']


class UserInfoHandler(StarkHandler):
    list_display = ['nickname', get_choice_text('性别', 'gender'), 'phone', 'email', 'depart']
    model_form_class = UserInfoModelForm  # 引用

site.register(models.UserInfo, UserInfoHandler)
```

# 钩子方法,判断两次密码输入是否相同
详情参看示例`web/stark.py`


# 自定义筛选过滤
详情参看示例`web/公户.py`

# 定制chekbox方法
> list_display 中 `StarkHandler.display_checkbox` 即可

# 自定义函数
详情参看示例`web/公户.py`

# 数据库锁使用
详情参看示例`web/public_customer.py`
```python
 from django.db import transaction
     with transaction.atomic():  # 事务
     ...
```

# 自定义模板页面
> 如果默认的changelist页面太丑，想用自己的，就

`change_list_template = '自己的.html'`

详情参看示例`web/views/consult_record.py`

# 控制到粒度
`案例web/base.py`
> 单独存放base.py 在需要粒度控制时候，引入继承该类，参考公户-私户py

```python
# stark业务开发中的粒度控制类
from django.conf import settings


class PermissionHandler(object):
    # 是否显示添加按钮（控制粒度）
    def get_add_btn(self, request, *args, **kwargs):
        # 拿到当前用户所有权限信息 session总获取
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if self.get_add_url_name not in permission_dict:
            # 没有添加权限
            return None
        return super().get_add_btn(request, *args, **kwargs)

    # 添加删除按钮粒度控制
    def get_list_display(self, request, *args, **kwargs):
        # 拿到当前用户所有权限信息 session总获取
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        value = []
        # 默认展示 修改和 删除
        if self.list_display:
            value.extend(self.list_display)
            if self.get_change_url_name in permission_dict and self.get_delete_url_name in permission_dict:
                # 既有编辑权限，也有删除权限
                value.append(type(self).display_edit_del)
            elif self.get_change_url_name in permission_dict:
                # 有编辑权限
                value.append(type(self).display_edit)
            elif self.get_delete_url_name in permission_dict:
                # 如果有删除权限
                value.append(type(self).display_del)
        return value
```
