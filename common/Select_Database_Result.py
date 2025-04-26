#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午6:30
import time

from util_tools.Database_Conn import Mysql


class Select_Sql_Result(Mysql):

    # 查询批发侧fr_api_order_info表订单信息,根据借款流水号来查询
    def select_api_order_info_result(self, req_seq_no):
        select_sql = f"SELECT ord.loan_state, ord.trans_result_msg, ord.up_appl_sts, ord.settle_status, ord.is_compensatory, ord.delete_flag, ord.notify FROM finance_router.fr_api_order_info ord WHERE ord.req_seq_no = '{req_seq_no}'"
        result = Mysql().select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询批发侧fr_api_order_info表上游借据号,根据下游借款流水号来查询
    def select_api_order_info_up_order_no(self, req_seq_no):
        select_sql = f"SELECT ord.up_order_no FROM finance_router.fr_api_order_info ord WHERE ord.req_seq_no = '{req_seq_no}'"
        result = Mysql().select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询批发侧fr_api_binding_bank_card表绑卡信息,根据签约单号来查询
    def select_api_binding_bank_card_result(self, bk_id):
        select_sql = f"SELECT bin.result_code, bin.result_msg FROM finance_router.fr_api_binding_bank_card bin WHERE bin.seqno = '{bk_id}'"
        result = Mysql().select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询批发侧fr_api_loan_amt_log表放款额度信息，根据借款流水号查询
    def select_api_loan_amt_log_result(self, loanseqno):
        select_sql = f"SELECT CAST(log.loan_amt AS CHAR)AS loan_amt,log.dn_sts, log.pay_msg,log.notify FROM finance_router.fr_api_loan_amt_log as log WHERE log.loanseqno = '{loanseqno}';"
        result = Mysql().select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询api侧zx_loan_apply_record表当前放款进度，根据借款流水号来查询(loan_apply_no)
    def select_zx_loan_apply_record(self, loan_apply_no, test_db="api"):
        select_sql = f"SELECT ap.loan_no,ap.risk_status, ap.apply_status, ap.loan_status, ap.sign_status, ap.reason_msg FROM zx_loan_apply_record as ap WHERE ap.loan_apply_no = '{loan_apply_no}';"
        result = Mysql(test_db).select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询api侧zx_credit_applicant_result表当前授信进度，根据借款流水号授信申请单号来查询(credit_apply_no)
    def select_zx_credit_applicant_result(self, loan_apply_no, test_db="api"):
        select_sql = f"SELECT ar.status, ar.sign_status, ar.risk_status FROM zx_credit_applicant_result as ar WHERE ar.credit_apply_no = '{loan_apply_no}';"
        result = Mysql(test_db).select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询api侧zl_batch_deduction_apply表当前还款进度，根据借款流水号授信申请单号来查询(zx_loan_apply_no)
    def select_zl_batch_deduction_apply(self, loan_apply_no, test_db="api"):
        select_sql = f"SELECT ar.repay_status, ar.jxym_repay_status FROM zl_batch_deduction_apply as ar WHERE ar.zx_loan_apply_no = '{loan_apply_no}';"
        result = Mysql(test_db).select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询批发侧fr_api_repayment_plan表还款计划详情，根据上游借据号来查询
    def select_fr_api_repayment_plan(self, loan_apply_no):
        api_loan_no = Select_Sql_Result().select_zx_loan_apply_record(loan_apply_no)['loan_no']
        core_up_order_no = Select_Sql_Result().select_api_order_info_up_order_no(api_loan_no)['up_order_no']
        select_sql = f"SELECT loan_no,period,ps_due_dt,pay_dt,ps_sts,setl_ind,last_setl_dt,ps_od_ind,grace_period_flag,grace_days,CAST(perd_amt AS CHAR)AS perd_amt,CAST(instm_amt AS CHAR)AS instm_amt,CAST(prcp_amt AS CHAR)AS prcp_amt,CAST(norm_int_amt AS CHAR)AS norm_int_amt,CAST(setl_prcp_amt AS CHAR)AS setl_prcp_amt,CAST(setl_norm_int_amt AS CHAR)AS setl_norm_int_amt,CAST(setl_od_int_amt AS CHAR)AS setl_od_int_amt FROM fr_api_repayment_plan WHERE loan_no = '{core_up_order_no}';"
        data = Mysql().select_db(select_sql)
        self.logging.info(f"数据库查询返回数据为：==={data}")
        result = {}
        for index, value in enumerate(data):
            result[index] = value
        return result

    # 查询批发侧fr_api_repayment_log表当前还款进度，根据下游借款流水号来查询(req_seq_no)
    def select_fr_api_repayment_log(self, req_seq_no):
        select_sql = f"SELECT pay_type,repay_type,period,setl_sts,pay_msg,pay_mind FROM fr_api_repayment_log WHERE loanseqno = '{req_seq_no}';"
        result = Mysql().select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询批发侧fr_channel_config表当前为何环境，根据name来查询(name)
    def select_fr_channel_config(self, name):
        select_sql = f"SELECT * FROM finance_router.fr_channel_config WHERE name = '{name}';"
        result = Mysql().select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：===,{result}")
        return result

    # 查询api侧zl_api_user表当前渠道为何模式，根据channel_code来查询(channel_code)
    def select_zl_api_user(self, channel_code, test_db="api"):
        select_sql = f"SELECT * FROM zws_middleware_360.zl_api_user WHERE channel_code = '{channel_code}';"
        result = Mysql(test_db).select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：===,{result}")
        return result

    # 查询api侧zx_loan_plan_info表还款计划详情，根据loan_apply_no来模糊查询所有期数
    def select_api_flow_zx_loan_plan_info(self, loan_apply_no, test_db="api"):
        select_sql = f"SELECT term,overdue_day,start_date,due_date,plan_status,CAST(prin_amt AS CHAR)AS prin_amt,CAST(int_amt AS CHAR)AS int_amt,CAST(oint_amt AS CHAR)AS oint_amt FROM zx_loan_plan_info WHERE plan_no LIKE '{loan_apply_no}%';"
        data = Mysql(test_db).select_db(select_sql)
        self.logging.info(f"数据库查询返回数据为：==={data}")
        result = {}
        for index, value in enumerate(data):
            result[index] = value
        return result

    # 查询api侧的放款订单表是否存在数据
    def select_api_zx_loan_apply_record_tools(self, loan_apply_no, test_db="api"):
        loan_apply_sql = f"SELECT term,loan_status,funds_code,loan_no FROM zx_loan_apply_record WHERE loan_apply_no = '{loan_apply_no}';"
        loan_apply_result = Mysql(test_db).select_db(loan_apply_sql)
        self.logging.info(f"数据库查询返回数据为：==={loan_apply_result}")
        if loan_apply_result:
            return loan_apply_result
        else:
            self.logging.info(f"没有找到数据，该笔数据可能掉单，请检查数据库！")
            return False

    # 查询api侧zx_loan_plan_info表还款计划详情，根据loan_apply_no来模糊查询所有期数(仅对测试平台)
    def select_api_flow_zx_loan_plan_info_for_test_tools(self, loan_apply_no, test_db="api"):
        result = None
        loan_apply_result = Select_Sql_Result().select_api_zx_loan_apply_record_tools(loan_apply_no)
        self.logging.info(f"数据库查询返回数据为：==={loan_apply_result}")
        if loan_apply_result:
            select_sql = f"SELECT term,start_date,due_date,plan_status,CAST(prin_amt AS CHAR)AS prin_amt,CAST(int_amt AS CHAR)AS int_amt,CAST(guarantee_amt AS CHAR)AS guarantee_amt,CAST(advice_amt AS CHAR)AS advice_amt FROM zx_loan_plan_info WHERE plan_no LIKE '{loan_apply_no}%' ORDER BY term;"
            result = Mysql(test_db).select_db(select_sql)
            self.logging.info(f"还款计划查询结果为：==={result}")
            return result
        else:
            self.logging.info(f"没有找到数据，该笔数据可能掉单，请检查数据库！")
            return False

    # 查询api侧zx_loan_apply_record表放款成功后的partner_loan_no，根据loan_apply_no来查询(loan_apply_no)
    def select_partner_loan_no_apply_record(self, loan_apply_no, test_db="api"):
        select_sql = f"SELECT partner_loan_no FROM zws_middleware_360.zx_loan_apply_record WHERE loan_apply_no = '{loan_apply_no}';"
        result = Mysql(test_db).select_db(select_sql)[0]['partner_loan_no']
        self.logging.info(f"数据库查询返回数据为：===,{result}")
        return result

    # 查询api侧tlt_bind_card_info表绑卡资方成功后的协议号、支付通道，根据user_id来查询(user_id)
    def select_greement_id_pay_channel(self, user_id, test_db="api"):
        select_sql = f"SELECT pay_channel_code,agrmno FROM zws_middleware_360.tlt_bind_confirm_info WHERE user_id = '{user_id}' AND pay_channel_code IS NOT NULL;"
        result = Mysql(test_db).select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：===,{result}")
        return result['pay_channel_code'], result['agrmno']

    # 查询api侧zx_credit_applicant_result表的credit_apply_no，根据天源花的credit_apply_no来查找apply表在api侧的数据
    def select_credit_apply_no_by_tyh(self, tyh_credit_apply_no, test_db="tyh", max_retries=5, wait_time=20):
        select_sql = f"SELECT credit_apply_no FROM jxym_credit_apply WHERE zx_credit_apply_no = '{tyh_credit_apply_no}';"
        retries = 0
        while retries < max_retries:
            try:
                # 执行查询
                result = Mysql(test_db).select_db(select_sql)
                if result:  # 如果有数据返回
                    self.logging.info(f"数据库查询返回数据为：{result}")
                    # 假设查询结果是列表且有数据
                    return result[0]['credit_apply_no']
                self.logging.info(f"未找到对应的授信申请号：{tyh_credit_apply_no}")
            except Exception as e:
                # 捕获异常并记录日志
                self.logging.error(f"查询数据库出错：{str(e)}")
            retries += 1
            # 如果查询结果为空，表示没有找到数据
            self.logging.info(f"没有找到数据，等待 {wait_time} 秒后重试...（重试次数：{retries}/{max_retries}）")
            time.sleep(wait_time)  # 等待指定时间后重试
        # 达到最大重试次数后返回 None
        self.logging.error(f"查询失败，达到最大重试次数：{max_retries}次，该笔数据可能掉单，请检查数据库！")
        return None

    # 查询api侧zx_credit_applicant_result表的user_id，根据天源花的credit_apply_no来查找apply表在api侧的数据
    def select_user_id_by_tyh(self, tyh_credit_apply_no, test_db="api", max_retries=5, wait_time=20):
        select_sql = f"SELECT user_id FROM zx_credit_applicant_result WHERE credit_apply_no = '{tyh_credit_apply_no}';"
        retries = 0
        while retries < max_retries:
            try:
                # 执行查询
                result = Mysql(test_db).select_db(select_sql)
                if result:  # 如果有数据返回
                    self.logging.info(f"数据库查询返回数据为：{result}")
                    # 假设查询结果是列表且有数据
                    return result[0]['user_id']
                self.logging.info(f"未找到对应的授信申请号：{tyh_credit_apply_no}")
            except Exception as e:
                # 捕获异常并记录日志
                self.logging.error(f"查询数据库出错：{str(e)}")
            retries += 1
            # 如果查询结果为空，表示没有找到数据
            self.logging.info(f"没有找到数据，等待 {wait_time} 秒后重试...（重试次数：{retries}/{max_retries}）")
            time.sleep(wait_time)  # 等待指定时间后重试
        # 达到最大重试次数后返回 None
        self.logging.error(f"查询失败，达到最大重试次数：{max_retries}次，该笔数据可能掉单，请检查数据库！")
        return None

    # 查询天源花侧zx_credit_applicant_result表的partner_credit_no，根据天源花的credit_apply_no来查找
    def select_partner_credit_no_by_tyh(self, credit_apply_no, test_db="tyh", max_retries=5, wait_time=20):
        select_sql = f"SELECT partner_credit_no FROM zx_credit_applicant_result WHERE credit_apply_no = '{credit_apply_no}';"
        retries = 0
        while retries < max_retries:
            try:
                # 执行查询
                result = Mysql(test_db).select_db(select_sql)
                if result:  # 如果有数据返回
                    self.logging.info(f"数据库查询返回数据为：{result}")
                    # 假设查询结果是列表且有数据
                    return result[0]['partner_credit_no']
                # 如果查询结果为空，表示没有找到数据
                self.logging.info(f"未找到对应的授信申请号：{credit_apply_no}")
            except Exception as e:
                # 捕获异常并记录日志
                self.logging.error(f"查询数据库出错：{str(e)}")
            retries += 1
            self.logging.info(f"没有找到数据，等待 {wait_time} 秒后重试...（重试次数：{retries}/{max_retries}）")
            time.sleep(wait_time)  # 等待指定时间后重试
        # 达到最大重试次数后返回 None
        self.logging.error(f"查询失败，达到最大重试次数：{max_retries}次，该笔数据可能掉单，请检查数据库！")
        return None

    # 查询天源花侧zx_credit_applicant_result表的partner_credit_no，根据天源花的credit_apply_no来查找
    def select_loan_apply_no_by_tyh(self, zx_loan_apply_no, test_db="tyh", max_retries=5, wait_time=20):
        # 准备查询 SQL
        select_sql = f"SELECT loan_apply_no FROM jxym_loan_apply WHERE zx_loan_apply_no = '{zx_loan_apply_no}';"
        retries = 0
        while retries < max_retries:
            try:
                # 执行查询
                result = Mysql(test_db).select_db(select_sql)
                if result:  # 如果有数据返回
                    self.logging.info(f"数据库查询返回数据为：{result}")
                    # 假设查询结果是列表且有数据
                    return result[0]['loan_apply_no']
                # 如果查询结果为空，表示没有找到数据
                self.logging.info(f"未找到对应的贷款申请号：{zx_loan_apply_no}")
            except Exception as e:
                # 捕获异常并记录日志
                self.logging.error(f"查询数据库出错：{str(e)}")
            retries += 1
            self.logging.info(f"没有找到数据，等待 {wait_time} 秒后重试...（重试次数：{retries}/{max_retries}）")
            time.sleep(wait_time)  # 等待指定时间后重试
        # 达到最大重试次数后返回 None
        self.logging.error(f"查询失败，达到最大重试次数：{max_retries}次，该笔数据可能掉单，请检查数据库！")
        return None

    # 查询测试报告数据库的数据
    def select_test_report(self, test_db="auto"):
        select_sql = f"SELECT * FROM automation_test_result.test_report_result ORDER BY id;"
        result = Mysql(test_db).select_db(select_sql)
        return result


if __name__ == '__main__':
    loan_apply_no = 'ZL_ZA1910617843309879296'
    db = Select_Sql_Result()
    reap = db.select_api_zx_loan_apply_record_tools(loan_apply_no)
    print(reap)
