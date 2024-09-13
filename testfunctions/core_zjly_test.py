#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午2:20
from common.Core_Zfpt_Api import core_zfpt_api
from common.Core_Api_Flow_Api import *
from util_tools.logger import Logger
from util_tools.Faker import *


# 资金路由加密
def test_zjl_jiami(data):
    return core_zfpt_api().zfpt_param_encry(data)


# 资金路由解密
def test_zjly_jiemi(data):
    return core_zfpt_api().zfpt_param_decry(data)


# 已绑银行卡查询
def test_zfzt_banked_query():
    reqsn = get_zfpt_req_no()
    businessChannel = 101
    req_data = {
        "reqSn": reqsn,
        "businessChannel": businessChannel,
        "params": json_dumps_cn({
            "ID": "440402199402101216",
            "BIND_PRODUCT_CODE": "bind_sian_03"
        })
    }
    datas = test_zjl_jiami(req_data)
    resp = core_zfpt_api().zfzt_bind_bank_query(reqsn, businessChannel, datas)
    decry_resp = test_zjly_jiemi(resp)
    Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
    return decry_resp


# 支付中台绑卡申请
def test_zfzt_bank_apply():
    ACCOUNT_NAME = "吴霞"
    CREDIT_ACCTNO = "6217000544979326825"
    TEL = "15915480565"
    ID = "610522200007287100"
    reqsn = get_zfpt_req_no()
    businessChannel = 101
    req_data = {
        "reqSn": reqsn,
        "businessChannel": businessChannel,
        "params": json_dumps_cn({
            "ACCOUNT_NAME": ACCOUNT_NAME,
            "BANK_CODE": "0105",
            "BANK_NAME": "建设银行",
            "CREDIT_ACCTNO": CREDIT_ACCTNO,
            "TEL": TEL,
            "ID": ID,
            "BIND_PRODUCT_CODE": "bind_baofu_8"
        })
    }
    datas = test_zjl_jiami(req_data)
    resp = core_zfpt_api().zfzt_bind_bank_apply(reqsn, businessChannel, datas)
    decry_resp = test_zjly_jiemi(resp)
    Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
    return decry_resp


# 支付中台绑卡确认
def test_zfzt_bank_confirm():
    reqsn = "APP20240906175738193787"
    businessChannel = 101
    req_data = {
        "reqSn": reqsn,
        "businessChannel": businessChannel,
        "params": json_dumps_cn({
            "VERCODE": "111111"
        })
    }
    datas = test_zjl_jiami(req_data)
    resp = core_zfpt_api().zfzt_bind_bank_confirm(reqsn, businessChannel, datas)
    decry_resp = test_zjly_jiemi(resp)
    Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
    return decry_resp


# 支付中台渠道协议号同步
def test_zfzt_agrm_no_sync():
    reqsn = get_zfpt_req_no()
    businessChannel = 101
    ccb_account = "6217007320102015947"
    req_data = {
        "reqSn": reqsn,
        "businessChannel": businessChannel,
        "params": json_dumps_cn({
            "ACCOUNT_NAME": "新浪绑卡",
            "BANK_CODE": "0105",
            "BANK_NAME": "中国建设银行",
            "CREDIT_ACCTNO": ccb_account,
            "TEL": "13312920936",
            "ID": "440402199402101216",
            "BIND_PRODUCT_CODE": "bind_sian_03",
            "AGRMNO": "1202408231146562850000369487"
        })
    }
    datas = test_zjl_jiami(req_data)
    resp = core_zfpt_api().zfzt_agrm_no_sync(reqsn, businessChannel, datas)
    decry_resp = test_zjly_jiemi(resp)
    Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
    return decry_resp


# 支付中台扣款申请
def test_zfzt_withhold_apply():
    reqsn = get_zfpt_req_no()
    businessChannel = 101
    ccb_account = "6217005449206215178"
    req_data = {
        "reqSn": reqsn,
        "businessChannel": businessChannel,
        "params": json_dumps_cn({
            "ACCOUNT_NAME": "新浪扣款测试",
            "BANK_CODE": "0105",
            "BANK_NAME": "中国建设银行",
            "CREDIT_ACCTNO": ccb_account,
            "TEL": "13312920936",
            "ID": "440607197702107218",
            "REPAY_PRODUCT_CODE": "repay_sina_01",
            "AMOUNT": "30000",
            "TYPE": 3
            # "LEDGERS": {"ACCOUNT_SUBJECT": 4, "AMOUNT": "30000", "REMARK": "新浪分账测试"}
        })
    }
    datas = test_zjl_jiami(req_data)
    resp = core_zfpt_api().zfzt_withhold_apply(reqsn, businessChannel, datas)
    decry_resp = test_zjly_jiemi(resp)
    Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
    return decry_resp


# 聚合支付扣款申请
def test_zfzt_together_withhold_apply():
    reqsn = get_zfpt_req_no()
    businessChannel = 101
    req_data = {
        "reqSn": reqsn,
        "businessChannel": businessChannel,
        "params": json_dumps_cn({
            "REPAY_PRODUCT_CODE": "ALI_REPAY",
            "AMOUNT": "1"
        })
    }
    datas = test_zjl_jiami(req_data)
    resp = core_zfpt_api().zfzt_together_withhold_apply(reqsn, businessChannel, datas)
    decry_resp = test_zjly_jiemi(resp)
    Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
    return decry_resp


# 支付中台扣款查询
def test_zfzt_withhold_query():
    reqsn = "APP20240910152406750667"
    businessChannel = 101
    req_data = {
        "reqSn": reqsn,
        "businessChannel": businessChannel
    }
    datas = test_zjl_jiami(req_data)
    resp = core_zfpt_api().zfzt_withhold_query(reqsn, businessChannel, datas)
    decry_resp = test_zjly_jiemi(resp)
    Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
    return decry_resp
