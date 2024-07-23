#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:03

"""
    轮询查询结果
"""

from common.Core_Zjly_Api import core_zjly_api
from util_tools.Faker import get_now_time
from util_tools.logger import Logger
from common.Encrypt_Decrypt import encrypt_decrypt
import time


class loop_result:
    def __init__(self):
        self.logging = Logger().init_logger()

    # 授信结果查询轮询
    def loop_sxcx_result(self, data, channel=None):
        # 轮训判断授信查询结果，为"授信成功"则跳出
        count = 0
        while True:
            # 等待2秒后发起授信状态查询请求
            count += 1
            time.sleep(10)
            resp = None
            if count < 20:
                try:
                    resp = core_zjly_api().test_order_apply_query(data)
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    continue
                if resp:
                    try:
                        resp_decry = encrypt_decrypt().param_decrys_by_channel(resp, channel)
                        self.logging.info(f"当前解密后的返回数据为：{resp_decry}")
                        if resp_decry["outSts"] is not None:
                            if resp_decry["outSts"] == "01":
                                self.logging.info("还未授信成功，请等待！")
                            elif resp_decry["outSts"] == "02":
                                self.logging.info("授信失败！请检查落库信息！")
                                break
                            elif resp_decry["outSts"] == "04":
                                self.logging.info(f"授信返回数据为：{resp_decry}")
                                self.logging.info("授信成功！")
                                return resp_decry
                            else:
                                self.logging.info("授信失败！记录不存在！")
                                break
                        else:
                            self.logging.info(f"系统发生错误！请检查返回数据：{resp_decry}")
                            break
                    except Exception as e:
                        self.logging.error(f"解密过程中发生错误：{e}不存在或预期错误")
                        break
                else:
                    self.logging.error("请求返回为空，无法继续处理！")
                    break
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                break

    # 放款结果轮询查询
    def loop_fkcx_result(self, data, channel=None):
        # 轮训判断放款查询结果，为"放款成功"则跳出
        count = 0
        while True:
            # 等待2秒后发起放款查询请求
            count += 1
            time.sleep(30)
            resp = None
            if count < 10:
                try:
                    resp = core_zjly_api().test_loan_apply_settle_query(data)
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    continue
                if resp:
                    try:
                        resp_decry = encrypt_decrypt().param_decrys_by_channel(resp, channel)
                        self.logging.info(f"当前解密后的返回数据为：{resp_decry}")
                        if resp_decry["dnSts"] is not None:
                            if resp_decry["dnSts"] == "2":
                                self.logging.info("还未放款成功，请等待！")
                            elif resp_decry["dnSts"] == "3":
                                self.logging.info("放款失败！请检查落库信息！")
                                break
                            elif resp_decry["dnSts"] == "1":
                                self.logging.info(f"放款返回数据为：{resp_decry}")
                                self.logging.info("放款成功！")
                                return resp_decry
                            else:
                                self.logging.info("放款失败！记录不存在！")
                                break
                        else:
                            self.logging.info(f"系统发生错误！请检查返回数据：{resp_decry}")
                            break
                    except Exception as e:
                        self.logging.error(f"解密过程中发生错误：{e}不存在或预期错误")
                        break
                else:
                    self.logging.error("请求返回为空，无法继续处理！")
                    break
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                break

    # 还款结果轮询查询
    def loop_hkcx_result(self, data, channel=None):
        # 轮训判断 还款查询结果，为"还款成功"则跳出
        count = 0
        while True:
            count += 1
            # 等待2秒后发起还款查询请求
            time.sleep(10)
            resp = None
            if count < 10:
                try:
                    resp = core_zjly_api().test_apply_repayment_query(data)
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    continue
                if resp:
                    try:
                        resp_decry = encrypt_decrypt().param_decrys_by_channel(resp, channel)
                        self.logging.info(f"当前解密后的返回数据为：{resp_decry}")
                        if resp_decry["setlSts"] is not None:
                            if resp_decry["setlSts"] == "2":
                                self.logging.info("还未还款成功，请等待！")
                            elif resp_decry["setlSts"] == "3":
                                self.logging.info("还款失败！请检查落库信息！")
                                break
                            elif resp_decry["setlSts"] == "1":
                                self.logging.info(f"还款返回数据为：{resp_decry}")
                                self.logging.info(f"还款成功！总还款：{resp_decry['totalAmt']}")
                                return resp_decry
                            else:
                                self.logging.info("还款失败！记录不存在！")
                        else:
                            self.logging.info(f"系统发生错误！请检查返回数据：{resp_decry}")
                            break
                    except Exception as e:
                        self.logging.error(f"解密过程中发生错误：{e}不存在或预期错误")
                        break
                else:
                    self.logging.error("请求返回为空，无法继续处理！")
                    break
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                break

    # 绑卡申请结果轮询查询
    def loop_bkcx_result(self, data, channel=None):
        # 轮训判断 绑卡申请查询结果，为"成功"则跳出
        count = 0
        while True:
            count += 1
            # 等待2秒后发起还款查询请求
            time.sleep(5)
            resp = None
            if count < 10:
                try:
                    resp = core_zjly_api().test_binding_card_query(data)
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    continue
                if resp:
                    try:
                        resp_decry = encrypt_decrypt().param_decrys_by_channel(resp, channel)
                        self.logging.info(f"当前解密后的返回数据为：{resp_decry}")
                        if resp_decry["resultCode"] is not None:
                            if resp_decry["resultCode"] == "9999":
                                self.logging.info("系统错误！！")
                                break
                            elif resp_decry["resultCode"] == "3000":
                                self.logging.info("卡bin不存在！卡号错误，请检查卡号！")
                                break
                            elif resp_decry["resultCode"] == "1001":
                                self.logging.info(f"绑卡返回数据为：{resp_decry}")
                                self.logging.info(f"绑卡成功！")
                                return resp_decry
                            else:
                                self.logging.info("绑卡发生错误！请重新尝试！")
                                break
                        else:
                            self.logging.info(f"系统发生错误！请检查返回数据：{resp_decry}")
                            break
                    except Exception as e:
                        self.logging.error(f"解密过程中发生错误：{e}不存在或预期错误")
                        break
                else:
                    self.logging.error("请求返回为空，无法继续处理！")
                    break
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                break
