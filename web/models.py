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


class Food(models.Model):
    """
    餐馆 管理
    """
    title = models.CharField(verbose_name='餐馆名', max_length=32)
    money = models.CharField(verbose_name='平均消费', max_length=32)
    addr = models.CharField(verbose_name='地址', max_length=32)
    food_type = models.CharField(verbose_name='类型', max_length=32)


class Company(models.Model):
    """
    企业信息表
    """
    title = models.CharField(verbose_name='企业名', max_length=32)
    money = models.CharField(verbose_name='注册资本', max_length=32)
    money_true = models.CharField(verbose_name='实缴资本', max_length=32)
    flag_date = models.CharField(verbose_name='成立日期', max_length=32)
    state = models.CharField(verbose_name='经营状态', max_length=32)
    code = models.CharField(verbose_name='统一社会信用代码', max_length=64)
    register_code = models.CharField(verbose_name='工商注册号', max_length=64)
    user_number = models.CharField(verbose_name='纳税人识别号', max_length=64)
    company_code = models.CharField(verbose_name='组织机构代码', max_length=64)
    company_type = models.CharField(verbose_name='公司类型', max_length=64)
    industry = models.CharField(verbose_name='行业', max_length=64)
    check_date = models.CharField(verbose_name='核准日期', max_length=64)
    registration_authority = models.CharField(verbose_name='登记机关', max_length=64)
    business_term = models.CharField(verbose_name='营业期限', max_length=64)
    taxpayer_qualification = models.CharField(verbose_name='纳税人资质', max_length=64)
    people = models.CharField(verbose_name='人员规模', max_length=64)
    registrations_people = models.CharField(verbose_name='参保人数', max_length=64)
    once_name = models.CharField(verbose_name='曾用名', max_length=64)
    english_name = models.CharField(verbose_name='英文名称', max_length=64)
    address = models.CharField(verbose_name='注册地址', max_length=64)
    text = models.TextField(verbose_name='经营范围')

    def __str__(self):
        return self.title


class Card(models.Model):
    """资质"""
    title = models.CharField(verbose_name='资质', max_length=32)

    def __str__(self):
        return self.title
