#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:03
import json
from util_tools.logger import Logger
import time
from util_tools.Read_Yaml import read_db_yaml
import pymysql as my
from util_tools.Faker import *


class Mysql():
    # 设置数据库的初始设置等等，后续可优化切换环境
    def __init__(self, test_db_name="zjly"):
        self.logging = Logger().init_logger()
        # 设置最大重试次数
        self._max_retry_connect = 3
        # 设置连接时间
        self._connect_timeout = 600
        self.test_db_name = test_db_name
        if self.test_db_name == "zjly":
            self.db_host = read_db_yaml()['mysql']['zjly']['host']
            self.username = read_db_yaml()['mysql']['zjly']['username']
            self.password = read_db_yaml()['mysql']['zjly']['password']
            self.port = read_db_yaml()['mysql']['zjly']['port']
            self.db_name = read_db_yaml()['mysql']['zjly']['db_name']
            try:
                # 建立数据库连接
                self.db = my.connect(
                    host=self.db_host,
                    user=self.username,
                    password=self.password,
                    db=self.db_name,
                    port=self.port,
                    charset='utf8',
                    connect_timeout=self._connect_timeout,
                    cursorclass=my.cursors.DictCursor)
                # 创建游标
                self.cursor = self.db.cursor()
                self.logging.info(f"mysql数据库连接成功-----{self.test_db_name}")
            except my.err.ProgrammingError as e:
                self.logging.info(f"mysql数据库连接失败-----{self.test_db_name}")
                self.logging.info(f"错误信息为：{e}")
            time.sleep(2)

    # 查询数据库,单条数据
    def select_db(self, sql):
        try:
            self.logging.info(f"开始执行SQL语句：==={sql}")
            self.cursor.execute(sql)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            self.logging.info(f"当前SQL语句执行失败，请检查具体信息：==={e}")
        self.close_db()

    # 更新数据库
    def update_db(self, sql):
            try:
                self.cursor.execute(sql)
                self.db.commit()
                # print("更新数据库，操作{}表数据-成功".format(dbname))
                self.logging.info("执行sql成功:\n\t{}".format(sql))
            except Exception as e:
                # 发生错误时回滚
                self.db.rollback()
                # 异常捕获
                raise e

    # 插入数据库
    def insert_db(self, sql):
        pass

    # 关闭数据库
    def close_db(self):
        self.cursor.close()
        self.db.close()
        self.logging.info(f"数据库{self.test_db_name}，关闭成功！")


if __name__ == '__main__':
    sql = "SELECT * FROM finance_router.fr_api_order_info ord WHERE ord.req_seq_no = 'ZLCHY1719459260194'"
    core_my_db = Mysql()
    datas = core_my_db.select_db(sql)[0]
    print(datas)
