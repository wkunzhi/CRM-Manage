from django.db import models
from rbac.models import UserInfo as RbacUserInfo


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(RbacUserInfo):  # 继承rbac的UserInfo基类
    """
    用户表
    """
    nickname = models.CharField(verbose_name='真实姓名', max_length=16)
    phone = models.CharField(verbose_name='手机号', max_length=32)

    gender_choices = ((1, '男'), (2, '女'))
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, default=1)
    depart = models.ForeignKey(verbose_name='部门', to='Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
