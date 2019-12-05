# -*- coding: utf-8 -*-
# __author__ = "zok"  362416272@qq.com
# Date: 2019-12-05  Python: 3.7

import requests
import re

response = requests.get('http://www.fontawesome.com.cn/faicons/')

ret = re.findall(r'<i class="fa fa-(.*?)" aria-hidden="true">', response.text)
# 去重
ret = list(set(ret))
item = []
for i in ret:
    # 空格
    if i.find(' ') < 0:
        ret.pop(ret.index(i))
        t = ['fa fa-check-square', mark_safe('<i class="fa fa-check-square" aria-hidden="true"></i>')],

"""
['fa fa-check-square', mark_safe('<i class="fa fa-check-square" aria-hidden="true"></i>')],
"""