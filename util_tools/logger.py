"""
    日志处理对象,对logging的封装
"""
import logging
import logging.config
from util_tools.Faker import get_now_time
from config.testconfig import BASE_DIR


class Logger(object):
    def __init__(self, log_name=f"{BASE_DIR}/logs/{get_now_time()}_log.log", log_level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(filename=log_name, encoding="utf-8")
        fh.setLevel(log_level)
        # 判断当前日志对象中是否有处理器，如果没有，则添加处理器
        # 否则会重复打印日志
        if not self.logger.handlers:
            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            # 定义handler的输出格式
            formatter = logging.Formatter(
                '\n%(asctime)s [pid:%(process)d] %(levelname)s [FILE:%(filename)s:%(lineno)d FUN:%(funcName)s]: %(message)s'
            )
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 给logger添加handler
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def init_logger(self):
        return self.logger
