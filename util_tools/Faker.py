#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:03
"""
    随机Mock数据工具
"""
import datetime
import json
import random
import time
import jsonpath
from faker import Faker
from util_tools.Read_Yaml import *
from common.Encrypt_Decrypt import *


# 实例化Faker对象
def get_fake():
    get_fakes = Faker("zh-CN")
    return get_fakes


# 获取随机借据号
def get_loan_no():
    return str(
        "TX" + datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d") + str(int(time.time() * 1000000)).zfill(
            7) + "SINO")


# 获取随机借据申请流水号
def get_req_seq_no(channel="ZLTEST"):
    return str(channel + str(int(time.time() * 1000)))


# 获取随机借据授信申请流水号，API全流程
def get_credit_apply_no(channel="ZLTEST_"):
    return str(channel + datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d") + str(int(time.time() * 1000)))


# 获取支付平台随机申请编号
def get_zfpt_req_no():
    return str(datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S%S") + str(
        random.randint(1000000, 9999999)))


# 获取随机绑卡订单号
def get_bank_id():
    return str("BK" + str(int(time.time() * 1000)))


# 获取随机放款订单号
def get_fk_id():
    return str("FK" + str(int(time.time() * 1000)))


# 获取随机担保合同号
def get_dbht_no():
    return str("DBHT" + str(int(time.time() * 0.01)))


# 获取随机合同编号
def get_contract_no():
    return str(str("31" + str(int(time.time() * 10000000))))


# 获取随机申请流水号
def get_req_no(channel="ZL"):
    return str(channel + str(int(time.time() * 1000)))


# 获取随机还款流水号
def get_repay_no(code="HK"):
    return str(code + str(int(time.time() * 0.01)))


# 获取绑卡ID
def get_bink_no():
    return str("48" + str(int(time.time() * 1000000)))


# 获取当前标准时间
def get_time_stand():
    return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# 获取当前标准时间
def get_time_stand_api():
    return str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))


# 生成年月日日期
def get_now_time():
    now_time = datetime.datetime.now()
    now_time_str = datetime.datetime.strftime(now_time, "%Y-%m-%d")
    return now_time_str


# 中文解码，返回中文
def json_dump_cn(data):
    return json.dumps(data).encode('utf-8').decode('unicode_escape')


# 格式化，并且返回中文解码，方法2
def json_dumps_cn(data):
    return json.dumps(data, ensure_ascii=False)


# 格式化请求参数，适配参数化
def json_dumps_format(data):
    return json.loads(json.dumps(data, ensure_ascii=False).replace(" ", ""))


# 获取上游接口动态参数传递下游接口
def get_request_data(data, key):
    return json.loads(jsonpath.jsonpath(data, "$..params")[0])[key]


# 获取随机客户姓名
def get_user_name():
    return get_fake().name()


# 获取随机身份证号码
def get_user_id_no():
    id_number = get_fake().ssn()
    return id_number


# 获取g固定日期随机身份证号码
def get_my_id_no():
    return str("62538119940617" + str(int(time.time() * 100))[-4:])


# 获取随机电话号码
def get_phone_mum():
    return get_fake().phone_number()


# 新长银手机号MOCK规则-手机号为4放款失败，随机到尾号为4则+1
def get_new_cy_phone_mum():
    data = get_fake().phone_number()
    if data.endswith("4"):
        return int(data) + 1
    else:
        return data


# 获取随机custid
def get_cust_id():
    num = str("ZL" + str(int(time.time() * 100)))
    return num


# 获取随机绑卡id
def get_api_bk_id():
    num = str("SC" + str(int(time.time() * 10)))
    return num


# 获取随机工商银行卡号
def get_icbc_num():
    timestamp_part = str(int(time.time() * 1000)).zfill(1)
    data = "622200" + timestamp_part
    return data


# 获取随机农业银行卡号
def get_abc_num():
    timestamp_part = str(int(time.time() * 100)).zfill(1)
    data = "6232" + timestamp_part
    return data


# 获取随机中国银行卡号
def get_boc_num():
    timestamp_part = str(int(time.time() * 100)).zfill(1)
    data = "6216" + timestamp_part
    return data


# 获取随机建设银行卡号
def get_ccb_num():
    while True:
        timestamp_part = str(int(time.time() * 1000)).zfill(1)
        data = "621700" + timestamp_part
        if data.endswith(('0', '1', '9')):
            return data  # 返回找到的数据


# 获取随机建设银行卡号,新长银MOCK规则-银行卡，尾号2、3、5、6失败
def get_new_cy_ccb_num():
    while True:
        timestamp_part = str(int(time.time() * 1000)).zfill(1)
        data = "621720" + timestamp_part
        if data.endswith(('0', '4', '8', '9')):
            return data


# 获取随机建设银行卡号,金美信MOCK规则-银行卡，尾号3、6、8失败
def get_jmx_ccb_num():
    while True:
        timestamp_part = str(int(time.time() * 1000)).zfill(1)
        data = "621720" + timestamp_part
        if data.endswith(('1', '2', '4', '5', '7', '9', '0')):
            return data


# 获取随机建设银行卡号,中原MOCK规则-银行卡，尾号3、8失败
def get_zy_ccb_num():
    while True:
        timestamp_part = str(int(time.time() * 1000)).zfill(1)
        data = "621720" + timestamp_part
        if data.endswith(('1', '2', '4', '5', '6', '7', '9', '0')):
            return data


# 获取随机建设银行卡号,海峡MOCK规则-银行卡，尾号1、2失败
def get_haixia_ccb_num():
    while True:
        timestamp_part = str(int(time.time() * 1000)).zfill(1)
        data = "621720" + timestamp_part
        if data.endswith(('3', '4', '5', '6', '7', '8', '9', '0')):
            return data


# 获取随机建设银行卡号,宝付MOCK规则-银行卡
def get_baofu_ccb_num(rule=('0')):
    while True:
        timestamp_part = str(int(time.time() * 1000)).zfill(1)
        data = "621720" + timestamp_part
        if data.endswith((rule)):
            return data


# 获取随机建设银行卡号,通联绑卡以0,1,9结尾
def get_tl_bank_ccb_num():
    while True:
        timestamp_part = str(int(time.time() * 1000)).zfill(1)
        data = "621720" + timestamp_part
        if data.endswith(('0')):
            return data  # 返回找到的数据


def get_user_idNo(sex='girl'):  # 1. 生成身份证号码的前17位
    # 区域码：假设我们使用一个常见的区域码，例如“440101” (广州)
    area_code = random.choice([
        '440103', '440104', '440105', '440106', '440111',
        '440112', '440113', '440114', '440115'
    ])

    # 随机生成出生日期，假设出生日期范围在1980年到2000年之间
    start_date = datetime.date(1980, 1, 1)
    end_date = datetime.date(2000, 12, 31)
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    birth_date = random_date.strftime('%Y%m%d')

    # 随机生成序列号，通常为3位数字，性别不同会影响序列号最后一位
    serial_number = f"{random.randint(0, 999):03d}"

    # 拼接前17位
    id_front = area_code + birth_date + serial_number

    # 2. 计算校验码
    # 系数
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]

    # 校验码对应表
    check_digits = '10X98765432'

    # 计算加权和
    weighted_sum = sum(int(id_front[i]) * weights[i] for i in range(17))

    # 计算余数并确定校验码
    remainder = weighted_sum % 11
    check_code = check_digits[remainder]

    # 生成完整身份证号码
    id_card_number = id_front + check_code
    # 提取生日信息
    birthday = f"{id_card_number[6:10]}-{id_card_number[10:12]}-{id_card_number[12:14]}"

    return id_card_number, birthday


# 振兴、金美信、中原、海峡身份证MOCK规则，尾号为X放款失败,所以排除了尾号X的身份证号码
def get_zx_user_id_no(year_s=1982, year_e=2000):
    id_card_number = generate_valid_id_card_number(year_s, year_e)

    # 提取生日信息
    birthday = f"{id_card_number[6:10]}-{id_card_number[10:12]}-{id_card_number[12:14]}"

    return id_card_number, birthday


def calculate_check_code(id_front):
    # 系数
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码对应表
    check_digits = '10X98765432'

    # 计算加权和
    weighted_sum = sum(int(id_front[i]) * weights[i] for i in range(17))

    # 计算余数并确定校验码
    remainder = weighted_sum % 11
    return check_digits[remainder]


def generate_valid_id_card_number(year_s=1970, year_e=1976):
    while True:
        # 1. 生成身份证号码的前17位
        area_code = random.choice([
            '440103', '440104', '440105', '440106', '440111',
            '440112', '440113', '440114', '440115'
        ])

        # 随机生成出生日期，假设出生日期范围在1975年到1977年之间
        start_date = datetime.date(year_s, 1, 1)
        end_date = datetime.date(year_e, 12, 31)
        random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        birth_date = random_date.strftime('%Y%m%d')

        # 随机生成序列号，通常为3位数字
        serial_number = f"{random.randint(0, 999):03d}"

        # 拼接前17位
        id_front = area_code + birth_date + serial_number

        # 计算校验码
        check_code = calculate_check_code(id_front)

        # 生成完整身份证号码
        id_card_number = id_front + check_code

        # 如果尾号不是'X'，则返回结果
        if check_code != 'X' and check_code != '0' and check_code != '1':
            return id_card_number


# 拼接天源花的H5链接
def tyh_h5_loan_repay(credit_apply_no, user_id, loan_apply_no):
    loan_h5 = f"\nhttp://gzdev.zhonglishuke.com:15008/pages/loan/loan?creditApplyNo={credit_apply_no}&returnUrl=http%3A%2F%2Flocalhost%3A3000%2Fmicro-loans%2F&loanApplyNo={get_req_seq_no('JMX')}&userId={user_id}&channelCode=TYH_HY\n"
    repay_h5 = f"\nhttp://gzdev.zhonglishuke.com:15008/pages/repayList/index?returnUrl=https%3A%2F%2Fnxdrd-dbg-new.vfuturetec.com%2Fmicro-loans%2Fbills%2Fstatus%2Fdcc4a5a546404d018ef550e921c03f68%3Fresult%3Dpending%26loanGid%3Ddcc4a5a546404d018ef550e921c03f68%26apiChannel%3D50048&loanApplyNo={loan_apply_no}&userId={user_id}&repayApplyNo={get_repay_no('repay')}&channelCode=TYH_HY\n"
    return loan_h5, repay_h5


if __name__ == '__main__':
    # certificationApplyNo = get_api_bk_id()
    enc = encrypt_decrypt()
    for i in range(1):
        id_no, birthday = get_zx_user_id_no(year_s=1990, year_e=1996)
        ccb = get_baofu_ccb_num()
        phone = read_risk_phone()
        # print(id_no, birthday)
        # loan, repay = tyh_h5_loan_repay("TYH_202411041730710546726", "ZL173071054678","JMX1730710546789")
        print(id_no, birthday, ccb, phone)
        print(f"{enc.param_encry_by_md5(id_no)}_{enc.param_encry_by_md5(phone)}")
    # print(get_credit_apply_no("")XM)
    # 请求鉴权数据
    # bk_jq_need_encry_data = { "certificationApplyNo": "SC00565656","SFAF":"SFASFAF"}
    # print(bk_jq_need_encry_data)
    # bk_jq_need_encry_data["certificationApplyNo"] = "SC0077844"
    # print(bk_jq_need_encry_data)
