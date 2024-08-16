"""
    读取Yaml文件
"""
import random
import warnings
import yaml
from config.Base_Env import *

# 忽略警告
warnings.filterwarnings("ignore")


# 读取Config目录下的数据库配置文件，后续可以根据测试环境切换（待优化）
def read_db_yaml():
    path = DB_YAML_PATH
    with open(path, "r", encoding="utf-8") as file:
        db_data = yaml.safe_load(file)
        return db_data


def read_risk_phone():
    path = RISK_PHONE_PATH
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if lines:
            random_line = random.choice(lines)
            return random_line.strip()
        else:
            print("文件为空")


if __name__ == '__main__':
    print(read_risk_phone())
