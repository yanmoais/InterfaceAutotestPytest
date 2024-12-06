# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午2:20
import logging
import time
from common.Core_Zfpt_Api import core_zfpt_api
from common.Core_Api_Flow_Api import *
from common.Update_Database_Result import Update_Sql_Result
from util_tools.logger import Logger
from util_tools.Faker import *


class core_zjly_func:

    # 资金路由加密
    def test_zjl_jiami(self, data):
        return core_zfpt_api().zfpt_param_encry(data)

    # 资金路由解密
    def test_zjly_jiemi(self, data):
        return core_zfpt_api().zfpt_param_decry(data)

    # 海峡切换成mock环境
    def test_haixia_mock(self):
        Update_Sql_Result().update_haixia_zjly_mock()

    # 已绑银行卡查询
    def test_zfzt_banked_query(self):
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
        datas = self.test_zjl_jiami(req_data)
        resp = core_zfpt_api().zfzt_bind_bank_query(reqsn, businessChannel, datas)
        decry_resp = self.test_zjly_jiemi(resp)
        Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
        return decry_resp

    # 支付中台绑卡申请
    def test_zfzt_bank_apply(self, ACCOUNT_NAME="胡斌", TEL="15932943620", ID="440106197404139496",
                             CREDIT_ACCTNO="6217001732763194480", PRODUCT_CODE="BF"):
        ACCOUNT_NAME = ACCOUNT_NAME
        TEL = TEL
        ID = ID
        CREDIT_ACCTNO = CREDIT_ACCTNO
        if PRODUCT_CODE == "BF":
            BIND_PRODUCT_CODE = "bind_mock"
        elif PRODUCT_CODE == "TL":
            BIND_PRODUCT_CODE = "bind_tonglian_09"
        else:
            return False
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
                "BIND_PRODUCT_CODE": BIND_PRODUCT_CODE
            })
        }
        datas = self.test_zjl_jiami(req_data)
        resp = core_zfpt_api().zfzt_bind_bank_apply(reqsn, businessChannel, datas)
        decry_resp = self.test_zjly_jiemi(resp)
        Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
        return reqsn, decry_resp

    # 支付中台绑卡确认
    def test_zfzt_bank_confirm(self, reqsn="APP20241128112600779009"):
        reqsn = reqsn
        businessChannel = 101
        req_data = {
            "reqSn": reqsn,
            "businessChannel": businessChannel,
            "params": json_dumps_cn({
                "VERCODE": "111111"
            })
        }
        datas = self.test_zjl_jiami(req_data)
        resp = core_zfpt_api().zfzt_bind_bank_confirm(reqsn, businessChannel, datas)
        decry_resp = self.test_zjly_jiemi(resp)
        Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
        return decry_resp

    # 支付中台渠道协议号同步
    def test_zfzt_agrm_no_sync(self):
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
        datas = self.test_zjl_jiami(req_data)
        resp = core_zfpt_api().zfzt_agrm_no_sync(reqsn, businessChannel, datas)
        decry_resp = self.test_zjly_jiemi(resp)
        Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
        return decry_resp

    # 支付中台扣款申请 ACCOUNT_NAME="胡斌", TEL="15932943620", ID="440106197404139496",
    #                          CREDIT_ACCTNO="6217001732763194480", PRODUCT_CODE="TL"
    def test_zfzt_withhold_apply(self, ccb_account="6217001732872646040", tel="15917853170", id_no="440111199912223459",
                                 product_code="BF", amount="30000"):
        reqsn = get_zfpt_req_no()
        businessChannel = 101
        ccb_account = ccb_account
        if product_code == "BF":
            REPAY_PRODUCT_CODE = "repay_mock"
        elif product_code == "TL":
            REPAY_PRODUCT_CODE = "repay_tonglian_09"
        else:
            return False
        req_data = {
            "reqSn": reqsn,
            "businessChannel": businessChannel,
            "params": json_dumps_cn({
                "ACCOUNT_NAME": "扣款测试",
                "BANK_CODE": "0105",
                "BANK_NAME": "中国建设银行",
                "CREDIT_ACCTNO": ccb_account,
                "TEL": tel,
                "ID": id_no,
                "REPAY_PRODUCT_CODE": REPAY_PRODUCT_CODE,
                "AMOUNT": amount,
                "TYPE": 3
                # "LEDGERS": {"ACCOUNT_SUBJECT": 4, "AMOUNT": "30000", "REMARK": "新浪分账测试"}
            })
        }
        datas = self.test_zjl_jiami(req_data)
        print(datas)
        resp = core_zfpt_api().zfzt_withhold_apply(reqsn, businessChannel, datas)
        decry_resp = self.test_zjly_jiemi(resp)
        Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
        return decry_resp

    # 聚合支付扣款申请
    def test_zfzt_together_withhold_apply(self):
        reqsn = get_zfpt_req_no()
        businessChannel = 101
        req_data = {
            "reqSn": reqsn,
            "businessChannel": businessChannel,
            "params": json_dumps_cn({
                "REPAY_PRODUCT_CODE": "WECHAT_REPAY",
                "AMOUNT": "1"
            })
        }
        datas = self.test_zjl_jiami(req_data)
        resp = core_zfpt_api().zfzt_together_withhold_apply(reqsn, businessChannel, datas)
        decry_resp = self.test_zjly_jiemi(resp)
        Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
        return decry_resp

    # 支付中台扣款查询
    def test_zfzt_withhold_query(self, reqsn="APP20241129173150392150"):
        reqsn = reqsn
        businessChannel = 101
        req_data = {
            "reqSn": reqsn,
            "businessChannel": businessChannel
        }
        datas = self.test_zjl_jiami(req_data)
        resp = core_zfpt_api().zfzt_withhold_query(reqsn, businessChannel, datas)
        decry_resp = self.test_zjly_jiemi(resp)
        Logger().init_logger().info(f"解密后的数据为：{decry_resp}")
        return decry_resp
