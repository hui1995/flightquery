# coding: utf-8
from pyutil.resource.db import DAL

db_client = None


def get_db_client():
    global db_client
    if db_client is None:
        db_client = DAL(
            host='127.0.0.1',  # 主机
            port=3306,  # 端口
            user='root',  # 用户名
            passwd='1042578865xin',  # 密码
            db='test'  # 数据库名
        )
    return db_client
