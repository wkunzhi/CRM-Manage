# by 362416272@qq.com
import hashlib


def gen_md5(origin):
    """
    md5加密
    :param origin:
    :return:
    """
    ha = hashlib.md5(b'fasdfsdf')
    ha.update(origin.encode('utf-8'))
    return ha.hexdigest()
