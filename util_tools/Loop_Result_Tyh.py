#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午10:11
from common.Core_Tyh_Api import core_tyh_api
from util_tools.logger import Logger
from common.Encrypt_Decrypt import encrypt_decrypt
from util_tools.Xxl_Job_Executor import *
from common.Select_Database_Result import Select_Sql_Result
from util_tools.Loop_result import loop_result
import time


class loop_result_tyh:
    def __init__(self):
        self.logging = Logger().init_logger()
        self.db = Select_Sql_Result()
        self.api = core_tyh_api()

    # 天源花授信结果轮询查询
    def loop_tyh_sx_result(self, data, credit_applyNo):
        """
        轮询查询授信结果
        :param data: 查询参数
        :param credit_applyNo: 授信申请编号
        :return: bool 是否查询成功
        """
        MAX_RETRIES = 10  # 最大重试次数
        SLEEP_INTERVAL = 5  # 轮询间隔时间(秒)
        count = 0
        while True:
            count += 1
            if count >= MAX_RETRIES:
                self.logging.info(f"已达到最大查询次数{MAX_RETRIES}次，请稍后重试！")
                return False
            try:
                time.sleep(SLEEP_INTERVAL)
                self.logging.info(f"第{count}次查询授信结果")
                # 加密并发送查询请求
                encry_data = self.api.api_param_encry(data)
                resp = self.api.test_query_credit_result(encry_data)
                if not resp:
                    self.logging.error("请求返回为空，无法继续处理！")
                    return False
                # 查询API侧的授信申请单号
                credit_applyNo_for_api = Select_Sql_Result().select_credit_apply_no_by_tyh(credit_applyNo)
                # 解密返回结果
                resp_decry = self.api.api_param_decry(resp)
                self.logging.info(f"当前解密后的返回数据为：{resp_decry}")
                if not resp_decry.get("status"):
                    self.logging.info(f"系统发生错误！请检查返回数据：{resp_decry}")
                    return False
                # 根据状态处理
                status = resp_decry["status"]
                if status == "S":
                    self.logging.info("授信成功！")
                    break  # 使用 break 而不是 return，确保完全跳出循环
                elif status == "F":
                    self.logging.info("申请失败，请检查落库原因！")
                    return False
                elif status in ["P", "W", "U"]:
                    self.logging.info("授信处理中，继续轮询...")
                    # 调用API侧轮询任务
                    api_result = loop_result().loop_tyh_api_sx_result(credit_applyNo_for_api)
                    if api_result:  # 如果API侧处理成功，也跳出循环
                        break
                    continue
                else:
                    self.logging.info("系统错误,请重新尝试！")
                    return False
            except Exception as e:
                self.logging.error(f"请求发生错误：{e}")
                return False
        return True  # 循环正常结束（通过break跳出）时返回True

    # 天源花借款结果轮询查询
    def loop_tyh_jk_result(self, data, loan_applyNo):
        # 轮训判断 授信查询结果，为"成功"则跳出
        count = 0
        while True:
            count += 1
            # 等待15秒后发起授信查询请求
            resp = None
            if count < 10:
                try:
                    time.sleep(15)
                    # 加密借款查询数据
                    encry_data = self.api.api_param_encry(data)
                    # 查询借款结果
                    resp = self.api.test_query_loan_result(encry_data)
                    # 查询出对应API侧的借款申请单号
                    loan_apply_no = Select_Sql_Result().select_loan_apply_no_by_tyh(loan_applyNo)
                    if resp:
                        try:
                            # 解密返回结果
                            resp_decry = self.api.api_param_decry(resp)
                            self.logging.info(f"当前解密后的返回数据为：{resp_decry}")
                            if resp_decry["loanStatus"] is not None:
                                if resp_decry["loanStatus"] == "P" or resp_decry["loanStatus"] == "W":
                                    self.logging.info("借款处理中，请稍等！！")
                                    # 调用API侧轮询任务
                                    loop_result().loop_tyh_api_loan_result(loan_apply_no)
                                elif resp_decry["loanStatus"] == "F":
                                    self.logging.info("借款申请失败，请检查落库原因！")
                                    break
                                elif resp_decry["loanStatus"] == "S":
                                    self.logging.info(f"借款成功！")
                                    return resp_decry
                                else:
                                    self.logging.info("系统错误,掉单,请重新尝试！！")
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
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    break
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                return False

    # api全流程绑卡轮询
    def loop_tyh_bk_result(self, bk_data, channel_code):
        # 轮训判断 绑卡结果
        count = 0
        while True:
            count += 1
            # 等待2秒后发起绑卡请求
            time.sleep(5)
            resp = None
            if count < 10:
                try:
                    # 加密绑卡鉴权数据
                    encry_data = self.api.api_param_encry(bk_data, channel_code)
                    # 发起鉴权绑卡请求
                    resp = self.api.test_apply_certification(encry_data)
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    continue
                if resp:
                    try:
                        # 解密返回结果
                        resp_decry = self.api.api_param_decry(resp)
                        self.logging.info(f"当前解密后的返回数据为：{resp_decry}")
                        if resp_decry["result"] is not None:
                            if resp_decry["result"] == "S":
                                verify_need_encry_data = {"userId": resp_decry["userId"],
                                                          "certificationApplyNo": resp_decry["certificationApplyNo"],
                                                          "cdKey": resp_decry["cdKey"], "verificationCode": "111111",
                                                          "bindType": "fundsChannel"}
                                self.logging.info("鉴权成功！！")
                                # 加密验证数据
                                verify_encry_data = self.api.api_param_encry(verify_need_encry_data, channel_code)
                                # 发起验证请求
                                bk_resp = self.api.test_verify_code(verify_encry_data)
                                # 解密验证返回数据
                                bk_resp_decry_data = self.api.api_param_decry(bk_resp)
                                if bk_resp_decry_data:
                                    if bk_resp_decry_data["verifyResult"] is not None:
                                        if bk_resp_decry_data["verifyResult"] == "S":
                                            self.logging.info("绑卡成功！！")
                                            return bk_resp_decry_data
                                        else:
                                            self.logging.info(f"绑卡失败！{bk_resp_decry_data['reasonMsg']}")
                                            break
                            elif resp_decry["result"] == "F":
                                self.logging.info(f"绑卡失败，{resp['reasonCode']}！")
                                break
                            else:
                                self.logging.info("系统错误,请重新尝试！！")
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
                return False


if __name__ == '__main__':
    data = {"userId": "ZL172916805172", "loanApplyNo": "JMX1729168051731"}
    api = loop_result_tyh()
    api.loop_tyh_jk_result(data, "JMX1729168051731")
