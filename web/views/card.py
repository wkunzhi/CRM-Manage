# -*- coding: utf-8 -*-
# __author__ = "zok"  362416272@qq.com
# Date: 2019-12-13  Python: 3.7

from stark.service.v1 import StarkHandler


class CardHandler(StarkHandler):
    """
    企业数据管理
    :return:
    """
    list_display = ['title']  # 自定义显示

