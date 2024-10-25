#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午2:39
from util_tools.logger import Logger
from util_tools.Read_Yaml import read_db_yaml
import redis as re


class Redis:
    # 设置数据库的初始设置等等，后续可优化切换环境
    def __init__(self, test_db_name="zjly"):
        self.logging = Logger().init_logger()
        # 设置最大重试次数
        self._max_retry_connect = 3
        # 设置连接时间
        self._connect_timeout = 600
        self.test_db_name = test_db_name
        self.db_host, self.password, self.port, self.db = self._get_db_config()
        try:
            self._connect_db()
        except re.RedisError as e:
            self.logging.info(f"mysql数据库连接失败-----{self.test_db_name}")
            self.logging.info(f"错误信息为：{e}")

    # 关闭数据库
    def close_db(self):
        self.redb.close()
        self.logging.info(f"Redis数据库{self.test_db_name}，关闭成功！")

    def _get_db_config(self):
        config = read_db_yaml()
        if self.test_db_name == "zjly":
            db_config = config['redis']['zjly']
        elif self.test_db_name == "api" or self.test_db_name == "tyh":
            db_config = config['redis']['api']
        else:
            raise ValueError("未知的数据库名称")
        return db_config['host'], db_config['password'], db_config['port'], db_config['db']

    # 删除指定key
    def delete_redis_key(self, key):
        result = self.redb.delete(key)
        if result:
            self.logging.info(f"该key {key} 值已被删除！")
        else:
            self.logging.info(f"该key {key} 值删除失败！")
        return result

    def _connect_db(self):
        self.redb = re.StrictRedis(host=self.db_host, port=self.port, db=self.db, password=self.password,
                                   decode_responses=True)
        self.logging.info(f"Redis数据库连接成功-----{self.test_db_name}")


if __name__ == '__main__':
    redis_client = Redis('api')
    print(redis_client.redb.get('zl_cashloan:zl_api_user:::' + 'ICE_ZLSK_36'))
    redis_client.close_db()
