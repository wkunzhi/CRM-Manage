# -*- coding: utf-8 -*-
# __author__ = "zok"  362416272@qq.com
# Date: 2019-12-09  Python: 3.7

from .base import PermissionHandler  # 粒度控制
from stark.service.v1 import StarkHandler, get_choice_text, StarkModelForm, StarkForm, Option


class CompanyHandler(PermissionHandler, StarkHandler):
    """
    企业数据管理
    :return:
    """
    list_display = ['title', 'money', 'flag_date', 'state', 'code', 'register_code', 'user_number', 'company_type', 'people']  # 自定义显示

    # 加上模糊搜索
    search_list = ['title__contains', 'once_name__contains', 'english_name__contains']
