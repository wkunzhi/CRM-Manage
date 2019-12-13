from django.db import models


class Menu(models.Model):
    """
    一级菜单表
    """
    title = models.CharField(verbose_name='菜单名称', max_length=32)
    # 图标http://fontawesome.dashgame.com/

    sort = models.IntegerField(verbose_name='显示顺序', default=1)

    icon = models.CharField(verbose_name='菜单图标', max_length=32)  # blank 为admin后台可以空

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    # 用来做控制，一些小权限（非菜单）么有就不显示
    name = models.CharField(verbose_name='URL别名', max_length=32, unique=True)  # unique唯一
    menu = models.ForeignKey(verbose_name='所属一级菜单', help_text='null表示不是菜单，否则为二级菜单', null=True, blank=True, to='Menu',
                             on_delete=models.CASCADE)

    # 跟自身表关联，已经是菜单的就可以不关联null=True
    # 非菜单的权限，要选一个母菜单。当选中该权限时就可以归类跳转到母菜单下
    pid = models.ForeignKey(verbose_name='关联的权限', to='Permission', null=True, blank=True, related_name='parents',
                            help_text='非菜单的权限，要选一个母菜单。当选中该权限时就可以归类跳转到母菜单下', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        # 此类可以当做父类，被其他model继承。字段自动过度给，继承的model
        abstract = True  # 【django以后做数据库迁移时， 不再为UserInfo类创建相关的表以及表结构了】
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

