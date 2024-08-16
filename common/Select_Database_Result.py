#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午6:30

from util_tools.Database_Conn import Mysql


class Select_Sql_Result(Mysql):

    # 查询批发侧fr_api_order_info表订单信息,根据借款流水号来查询
    def select_api_order_info_result(self, req_seq_no):
        select_sql = f"SELECT ord.loan_state, ord.trans_result, ord.trans_result_msg, ord.up_appl_sts, ord.settle_status, ord.is_compensatory, ord.delete_flag, ord.notify FROM finance_router.fr_api_order_info ord WHERE ord.req_seq_no = '{req_seq_no}'"
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
    def select_zx_loan_apply_record(self, loan_apply_no):
        select_sql = f"SELECT ap.loan_no,ap.risk_status, ap.apply_status, ap.loan_status, ap.sign_status FROM zx_loan_apply_record as ap WHERE ap.loan_apply_no = '{loan_apply_no}';"
        result = Mysql("api").select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询api侧zx_credit_applicant_result表当前授信进度，根据借款流水号授信申请单号来查询(credit_apply_no)
    def select_zx_credit_applicant_result(self, loan_apply_no):
        select_sql = f"SELECT ar.sign_status, ar.risk_status FROM zx_credit_applicant_result as ar WHERE ar.credit_apply_no = '{loan_apply_no}';"
        result = Mysql("api").select_db(select_sql)[0]
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

    # 查询api侧zx_loan_plan_info表还款计划详情，根据loan_apply_no来模糊查询所有期数
    def select_api_flow_zx_loan_plan_info(self, loan_apply_no):
        select_sql = f"SELECT term,overdue_day,start_date,due_date,plan_status,CAST(prin_amt AS CHAR)AS prin_amt,CAST(int_amt AS CHAR)AS int_amt,CAST(oint_amt AS CHAR)AS oint_amt FROM zx_loan_plan_info WHERE plan_no LIKE '{loan_apply_no}%';"
        data = Mysql("api").select_db(select_sql)
        self.logging.info(f"数据库查询返回数据为：==={data}")
        result = {}
        for index, value in enumerate(data):
            result[index] = value
        return result


if __name__ == '__main__':
    bk_id = "SLN4401604407"
    db = Select_Sql_Result()
    datas = db.select_zx_loan_apply_record(bk_id)
    print(datas['loan_no'])
