# by 362416272@qq.com
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



