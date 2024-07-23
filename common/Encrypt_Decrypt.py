"""
    加解密
"""
import logging
from common.Base_API import Base_Api
from util_tools.Faker import *
from util_tools.logger import Logger


class encrypt_decrypt(Base_Api):
    def __init__(self, ENV=None):
        super().__init__(ENV)
        self.dubbo_api = Base_Api(ENV)
        self.now_time = get_time_stand()
        self.logging = Logger().init_logger()

    # 加密请求数据
    def param_encry(self, request_data):
        apis = "/paramsEncryption"
        try:
            # 需要将数据再次格式化成带转义符并且去除空格
            data = json_dumps_format(request_data)
            logging.info(f"需要加密的代偿后还款计划同步数据为：======{data}")
            self.logging.info(f"开始加密请求数据==========,{data}")
            encry_data = self.dubbo_api.post(apis, data)
            return encry_data
        except Exception as e:
            self.logging.info(f"请求数据加密异常=======，异常信息：{e}")

    # 解密返回数据
    def param_decry(self, response_data):
        apis = "/paramsDecryption"
        try:
            self.logging.info(f"开始解密返回数据==========,{response_data}")
            encry_data = self.dubbo_api.post(apis, response_data)
            return encry_data
        except Exception as e:
            self.logging.info(f"返回数据解密异常=======，异常信息：{e}")

    # 加密请求数据,根据资方code来选择加密套
    def param_encry_by_channel(self, request_data, channel):
        apis = f"/paramsEncrypt/{channel}"
        try:
            # 需要将数据再次格式化成带转义符并且去除空格
            data = json_dumps_format(request_data)
            logging.info(f"需要加密的代偿后还款计划同步数据为：======{data}")
            self.logging.info(f"开始加密请求数据==========,{data}")
            encry_data = self.dubbo_api.post(apis, data)
            return encry_data
        except Exception as e:
            self.logging.info(f"请求数据加密异常=======，异常信息：{e}")

    # 解密返回数据,根据资方code来选择解密套
    def param_decrys_by_channel(self, response_data, channel):
        apis = f"/paramsDecrypt/{channel}"
        try:
            self.logging.info(f"开始解密返回数据==========,{response_data}")
            encry_data = self.dubbo_api.post(apis, response_data)
            return encry_data
        except Exception as e:
            self.logging.info(f"返回数据解密异常=======，异常信息：{e}")


if __name__ == '__main__':
    ss = encrypt_decrypt("encry")
    print(ss.dubbo_api.uri)
