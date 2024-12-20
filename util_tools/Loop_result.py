#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:03

"""
    轮询查询结果
"""

from common.Core_Zjly_Api import core_zjly_api
from common.Core_Api_Flow_Api import core_api_flow_api
from util_tools.logger import Logger
from common.Encrypt_Decrypt import encrypt_decrypt
from util_tools.Xxl_Job_Executor import *
from common.Select_Database_Result import Select_Sql_Result
import time


class loop_result:
    def __init__(self, test_db="api"):
        self.logging = Logger().init_logger()
        self.db = Select_Sql_Result()
        if test_db == "api":
            self.api = core_api_flow_api()

    # 调度任务
    def __perform_task(self, loanApplyNo, task_type):
        """执行任务的辅助函数"""
        if task_type == "loan":
            execute_xxl_job().apply_loan_xxljob(loanApplyNo)
        elif task_type == "loan_sign":
            execute_xxl_job().apply_loan_sign_xxljob()

    # 资金路由授信结果查询轮询
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

    # 资金路由放款结果轮询查询
    def loop_fkcx_result(self, data, channel=None):
        # 轮训判断放款查询结果，为"放款成功"则跳出
        count = 0
        while True:
            # 等待2秒后发起放款查询请求
            count += 1
            time.sleep(10)
            resp = None
            if count < 20:
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

    # 资金路由还款结果轮询查询
    def loop_hkcx_result(self, data, channel=None):
        # 轮训判断 还款查询结果，为"还款成功"则跳出
        count = 0
        while True:
            count += 1
            # 等待2秒后发起还款查询请求
            time.sleep(30)
            resp = None
            if count < 30:
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

    # 资金路由绑卡申请结果轮询查询
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

    # api全流程授信轮询查询
    def loop_api_flow_sx_result(self, data, credit_applyNo, channel_code):
        # 轮训判断 授信查询结果，为"成功"则跳出
        count = 0
        while True:
            count += 1
            # 等待15秒后发起授信查询请求
            resp = None
            if count < 10:
                try:
                    time.sleep(10)
                    # 加密授信查询数据
                    encry_data = self.api.api_param_encry(data, channel_code)
                    # 查询授信结果
                    resp = self.api.test_query_credit_result(encry_data)
                    if resp:
                        try:
                            # 解密返回结果
                            resp_decry = self.api.api_param_decry(resp)
                            self.logging.info(f"当前解密后的返回数据为：{resp_decry}")
                            if resp_decry["status"] is not None:
                                if resp_decry["status"] == "P" or resp_decry["status"] == "U":
                                    self.logging.info("授信处理中，请稍等！！")
                                    # 查询数据库借款单处于什么状态，来对应跑对应的任务
                                    sql_result = self.db.select_zx_credit_applicant_result(credit_applyNo)
                                    if sql_result['risk_status'] == "" or sql_result['risk_status'] == "W" or \
                                            sql_result['risk_status'] == "P":
                                        # 执行授信处理任务
                                        self.__perform_task(credit_applyNo, "loan")
                                        time.sleep(6)
                                    else:
                                        if sql_result['sign_status'] == '' or sql_result['sign_status'] == "W" or \
                                                sql_result['sign_status'] == "P":
                                            # 执行签章任务
                                            self.__perform_task(credit_applyNo, "loan_sign")
                                            time.sleep(20)
                                elif resp_decry["status"] == "F":
                                    self.logging.info("申请失败，请检查落库原因！")
                                    break
                                elif resp_decry["status"] == "S":
                                    self.logging.info(f"授信成功！")
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
                    continue
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                return False

    # api全流程绑卡轮询
    def loop_api_flow_bk_result(self, bk_data, channel_code):
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

    # api全流程借款轮询查询
    def loop_api_flow_loan_result(self, data, loanApplyNo, channel_code):
        # 轮训判断 借款查询结果，为"成功"则跳出
        count = 0
        while True:
            count += 1
            resp = None
            # 等待10秒控制查询
            time.sleep(10)
            if count < 30:
                self.logging.info(f"当前是第{count}次借款状态查询！")
                try:
                    # 加密借款查询数据
                    encry_data = self.api.api_param_encry(data, channel_code)
                    # 查询借款结果
                    resp = self.api.test_query_loan_result(encry_data)
                    if resp:
                        try:
                            # 解密返回结果
                            resp_decry = self.api.api_param_decry(resp)
                            self.logging.info(f"当前解密后的返回数据为：{resp_decry}")
                            if resp_decry["loanStatus"] is not None:
                                if resp_decry["loanStatus"] == "P":
                                    self.logging.info("借款申请处理中，请稍等！！")
                                    # 查询数据库借款单处于什么状态，来对应跑对应的任务
                                    sql_result = self.db.select_zx_loan_apply_record(loanApplyNo)
                                    if sql_result["risk_status"] == "" or sql_result["risk_status"] == "W" or \
                                            sql_result["risk_status"] == "P":
                                        # 执行放款处理任务，调取风控系统
                                        self.__perform_task(loanApplyNo, "loan")
                                        self.logging.info("开始暂停60S。。。。。")
                                        time.sleep(30)
                                        self.logging.info("暂停结束。。。。。")
                                    else:
                                        if sql_result["sign_status"]:
                                            if sql_result["sign_status"] == "P" or sql_result["sign_status"] == "W" or \
                                                    sql_result["sign_status"] == "P1":
                                                # 执行放款签章任务
                                                self.__perform_task(loanApplyNo, "loan_sign")
                                                time.sleep(15)
                                            elif sql_result["sign_status"] == "PSC" or sql_result[
                                                "sign_status"] == "PSL":
                                                # 执行放款处理任务
                                                self.__perform_task(loanApplyNo, "loan")
                                                time.sleep(15)
                                elif resp_decry["loanStatus"] == "F":
                                    self.logging.info(
                                        f"借款申请失败，请检查数据是否存在问题！错误原因：{resp_decry['reasonMsg']}")
                                    break
                                elif resp_decry["loanStatus"] == "S":
                                    self.logging.info(f"借款成功！")
                                    # 执行放款处理任务
                                    self.__perform_task(loanApplyNo, "loan")
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
                    continue
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                return False

    # api全流程还款结果轮询查询
    def loop_api_flow_repay_result(self, loanApplyNo):
        # 轮训判断 还款结果查询，为"S"则跳出
        count = 0
        while True:
            count += 1
            # 等待10秒控制查询
            time.sleep(5)
            if count < 30:
                self.logging.info(f"当前是第{count}次还款状态查询！")
                try:
                    # 查询数据库还款结果
                    repay_result = Select_Sql_Result().select_zl_batch_deduction_apply(loanApplyNo)
                    if repay_result:
                        try:
                            if repay_result["repay_status"] is not None:
                                if repay_result["repay_status"] == "P" or repay_result["jxym_repay_status"] == "P":
                                    self.logging.info("还款申请处理中，请稍等！！")
                                    # 执行api侧D0批扣查询
                                    time.sleep(5)
                                    execute_xxl_job().new_cy_d0_batch_repayment_query(loanApplyNo)
                                    self.logging.info(f"执行D0批扣结果查询成功！请稍等！")
                                elif repay_result["repay_status"] == "F" or repay_result["jxym_repay_status"] == "F":
                                    self.logging.info(
                                        f"还款申请失败，请检查数据是否存在问题！错误原因：{repay_result['reasonMsg']}")
                                    break
                                elif repay_result["repay_status"] == "S":
                                    self.logging.info(f"还款成功！")
                                    break
                                else:
                                    self.logging.info("系统错误,掉单,请重新尝试！！")
                                    break
                            else:
                                self.logging.info(f"系统发生错误！请检查返回数据：{repay_result}")
                                break
                        except Exception as e:
                            self.logging.error(f"执行过程中发生错误：{e}不存在或预期错误")
                            break
                    else:
                        self.logging.error("请求返回为空，无法继续处理！")
                        break
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    continue
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                return False

    # 仅供天源花侧查询API授信数据使用
    def loop_tyh_api_sx_result(self, credit_applyNo):
        # 轮训判断 授信表查询，为"S"则跳出
        count = 0
        while True:
            count += 1
            if count < 10:
                try:
                    # 查询API侧的表单数据
                    # 查询数据库授信单处于什么状态，来对应跑对应的任务
                    sql_result = self.db.select_zx_credit_applicant_result(credit_applyNo)
                    time.sleep(3)
                    if sql_result:
                        if sql_result["status"] is not None:
                            if sql_result["status"] == "P" or sql_result["status"] == "W":
                                self.logging.info("授信处理中，请稍等！！")
                                if sql_result['risk_status'] == "" or sql_result['risk_status'] == "W" or \
                                        sql_result['risk_status'] == "P":
                                    # 执行授信处理任务
                                    execute_xxl_job().apply_credit_xxljob(credit_applyNo)
                                    time.sleep(6)
                                else:
                                    if sql_result['sign_status'] == '' or sql_result['sign_status'] == "W" or \
                                            sql_result['sign_status'] == "P":
                                        # 执行签章任务
                                        execute_xxl_job().apply_credit_sign_xxljob()
                                        time.sleep(20)
                            elif sql_result["status"] == "F":
                                self.logging.info("申请失败，请检查落库原因！")
                                break
                            elif sql_result["status"] == "S":
                                self.logging.info(f"授信成功！")
                                return sql_result
                            else:
                                self.logging.info("系统错误,掉单,请重新尝试！！")
                                break
                        else:
                            self.logging.info(f"系统发生错误！请检查返回数据：{sql_result}")
                            break
                    else:
                        self.logging.error("请求返回为空，无法继续处理！")
                        break
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    continue
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                return False

    # 仅供天源花侧查询API借款数据使用
    def loop_tyh_api_loan_result(self, loanApplyNo):
        # 轮训判断 借款查询结果，为"成功"则跳出
        count = 0
        while True:
            count += 1
            resp = None
            # 等待10秒控制查询
            time.sleep(10)
            if count < 30:
                self.logging.info(f"当前是第{count}次借款状态查询！")
                try:
                    # 查询API侧的表单数据
                    # 查询数据库借款单处于什么状态，来对应跑对应的任务
                    sql_result = self.db.select_zx_loan_apply_record(loanApplyNo)
                    time.sleep(3)
                    if sql_result:
                        if sql_result["loan_status"] is not None:
                            if sql_result["loan_status"] == "P":
                                self.logging.info("借款申请处理中，请稍等！！")
                                if sql_result["risk_status"] == "" or sql_result["risk_status"] == "W" or \
                                        sql_result["risk_status"] == "P":
                                    # 执行放款处理任务，调取风控系统
                                    self.__perform_task(loanApplyNo, "loan")
                                    self.logging.info("开始暂停60S。。。。。")
                                    time.sleep(60)
                                    self.logging.info("暂停结束。。。。。")
                                else:
                                    if sql_result["sign_status"]:
                                        if sql_result["sign_status"] == "P" or sql_result["sign_status"] == "W" or \
                                                sql_result["sign_status"] == "P1" or sql_result["sign_status"] == "":
                                            # 执行放款签章任务
                                            self.__perform_task(loanApplyNo, "loan_sign")
                                            time.sleep(15)
                                        elif sql_result["sign_status"] == "PSC" or sql_result[
                                            "sign_status"] == "PSL":
                                            # 执行放款处理任务
                                            self.__perform_task(loanApplyNo, "loan")
                                            time.sleep(15)
                            elif sql_result["loan_status"] == "F":
                                self.logging.info(
                                    f"借款申请失败，请检查数据是否存在问题！错误原因：{sql_result['reason_msg']}")
                                break
                            elif sql_result["loan_status"] == "S":
                                self.logging.info(f"借款成功！")
                                # 执行放款签章任务
                                self.__perform_task(loanApplyNo, "loan_sign")
                                return sql_result
                            else:
                                self.logging.info("系统错误,掉单,请重新尝试！！")
                                break
                        else:
                            self.logging.info(f"系统发生错误！请检查返回数据：{sql_result}")
                            break
                    else:
                        self.logging.error("请求返回为空，无法继续处理！")
                        break
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    continue
            else:
                self.logging.info(f"当前系统查询次数过多，请稍后重试！")
                return False


if __name__ == '__main__':
    # api = core_api_flow_api()
    # enc = encrypt_decrypt()
    # apply_time = get_time_stand_api()
    # certificationApplyNo = get_api_bk_id()
    # bank_name = "中国建设银行"
    # loan_amt = "2000"
    # reqPeriods = "12"
    # current_date = get_now_time()
    # logging = Logger().init_logger()
    data = {}
    # loanApplyNo = "1846850735699148800"
    # print(loop_result().loop_tyh_api_loan_result(loanApplyNo))
