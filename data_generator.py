#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午9:56
import random
import time
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('zh_CN')


def generate_random_data(last_time=None):
    """生成单条随机数据"""
    # user_id: zl开头6位数字
    user_id = f"zl{random.randint(0, 9999):04d}"

    # 7位申请编号
    credit_apply_no = f"{random.randint(0, 9999999):07d}"

    # 时间生成（首次使用当前时间）
    current_time = last_time + timedelta(seconds=1) if last_time else datetime.now()
    apply_time = current_time.strftime("%Y%m%d%H%M%S")

    # 中文姓名
    user_name = fake.name()

    # 有效身份证号
    id_no = fake.ssn()

    # 19位银行卡号（最后一位0）
    bank_card = f"{random.randint(10 ** 17, 10 ** 18 - 1)}0"

    return {
        "user_id": user_id,
        "credit_apply_no": credit_apply_no,
        "apply_time": apply_time,
        "user_name": user_name,
        "id_no": id_no,
        "bank_card_no": bank_card
    }, current_time


def write_random_data_to_file(filename, rows=100):
    """生成并写入随机数据"""
    last_time = None
    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(rows):
            data, last_time = generate_random_data(last_time)
            line = f"{data['user_id']},{data['credit_apply_no']},{data['apply_time']},{data['user_name']},{data['id_no']},{data['bank_card_no']}\n"
            f.write(line)


def read_random_line(filename):
    """随机读取一行数据"""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            return None

        random_line = random.choice(lines)
        parts = random_line.strip().split(',')
        if len(parts) == 6:
            return {
                "user_id": parts[0],
                "credit_apply_no": parts[1],
                "apply_time": parts[2],
                "user_name": parts[3],
                "id_no": parts[4],
                "bank_card_no": parts[5]
            }
    return None


# 使用示例
if __name__ == "__main__":
    # 生成测试数据
    write_random_data_to_file("test_data.txt", 10000)
    data = None
    # 随机读取
    for _ in range(1):  # 随机读取3次演示
        data = read_random_line("test_data.txt")
    print(data)
    print(data['user_id'], data['credit_apply_no'], data['apply_time'])

