"""
    读取Yaml文件
"""
import random
import warnings
import yaml
import csv
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


def write_user_data(path, data):
    with open(path, mode='a', newline='', encoding="UTF-8") as file:
        # 定义 CSV 写入器，指定列名（表头）
        writer = csv.DictWriter(file, fieldnames=["id_no", "acct", "phone", "user_name"])
        # 如果文件是空的，先写入表头（列名），否则不写入
        if file.tell() == 0:
            writer.writeheader()
        # 写入一行数据
        writer.writerow(data)
        print("已写入数据", data)


if __name__ == '__main__':
    print(read_risk_phone())
