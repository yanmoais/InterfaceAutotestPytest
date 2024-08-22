#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午6:30
import datetime

from util_tools.Database_Conn import Mysql
from dateutil.relativedelta import relativedelta
from common.Select_Database_Result import Select_Sql_Result


class Update_Sql_Result(Mysql):
    def __init__(self):
        super().__init__()

    # 查询批发侧fr_api_order_info表订单信息,根据借款流水号来查询
    def update_api_binding_bank_card_result(self, req_seq_no):
        update_sql = f"UPDATE finance_router.fr_api_binding_bank_card SET result_code='1001', result_msg = '签约成功',bind_id = '732855302144952973',messageNo = '200604000014372-17200785447440696447852' WHERE loanseqno = '{req_seq_no}';"
        result = Mysql().update_db(update_sql)
        self.logging.info(f"数据库执行完成：==={result}")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zx_credit_applicant_info表
    def update_api_flow_zx_credit_applicant_info(self, funds_code, user_id):
        update_sql = f"UPDATE zws_middleware_360.zx_credit_applicant_info as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql("api").update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zx_credit_applicant_result表
    def update_api_flow_zx_credit_applicant_result(self, funds_code, user_id):
        update_sql = f"UPDATE zws_middleware_360.zx_credit_applicant_result as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql("api").update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zx_credit_user_info表
    def update_api_flow_zx_credit_user_info(self, funds_code, user_id):
        update_sql = f"UPDATE zws_middleware_360.zx_credit_user_info as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql("api").update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zl_drms_judgements表
    def update_api_flow_zl_drms_judgements(self, funds_code, user_id):
        update_sql = f"UPDATE zws_middleware_360.zl_drms_judgements as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql("api").update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zx_credit_info表
    def update_api_flow_zx_credit_info(self, funds_code, user_id):
        update_sql = f"UPDATE zws_middleware_360.zx_credit_info as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql("api").update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api操作还款前对api侧zx_loan_plan_info放款日期与还款计划进行修改,根据loan_apply_no来模糊查询,根据对应期数来修改日期
    def update_api_flow_zx_loan_plan_info_d0(self, loan_apply_no, term):
        update_sql = f"UPDATE zws_middleware_360.zx_loan_plan_info as cai SET cai.start_date = '{(datetime.datetime.now() - relativedelta(months=1)).strftime('%Y%m%d')}', cai.due_date = '{(datetime.datetime.now().strftime('%Y%m%d'))}' WHERE cai.plan_no LIKE '{loan_apply_no}%' AND cai.term = '{term}';"
        result = Mysql("api").update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api操作还款前对api侧zx_loan_note_info放款日期与还款计划进行修改,根据loan_apply_no来模糊查询,根据对应期数来修改日期
    def update_api_flow_zx_loan_note_info_d0(self, loan_apply_no):
        update_sql = f"UPDATE zws_middleware_360.zx_loan_note_info as cai SET cai.loan_time = '{(datetime.datetime.now() - relativedelta(months=1)).strftime('%Y%m%d%H%M%S')}', cai.cash_date = '{((datetime.datetime.now() - relativedelta(months=1)).strftime('%Y%m%d'))}', cai.inst_date = '{((datetime.datetime.now() - relativedelta(months=1)).strftime('%Y%m%d'))}' WHERE cai.loan_apply_no = '{loan_apply_no}';"
        result = Mysql("api").update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api操作还款前对批发侧fr_api_repayment_plan还款计划进行修改,根据loan_apply_no来查询,根据对应期数来修改日期
    def update_api_core_fr_api_repayment_plan_d0(self, loan_apply_no, term):
        core_loan_no = Select_Sql_Result().select_fr_api_repayment_plan(loan_apply_no)[0]['loan_no']
        update_sql = f"UPDATE finance_router.fr_api_repayment_plan as fr SET fr.ps_due_dt = '{(datetime.datetime.now().strftime('%Y-%m-%d'))}' WHERE fr.loan_no = '{core_loan_no}' AND fr.period = '{term}';"
        result = Mysql().update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api操作还款前对批发侧fr_api_order_info订单表进行修改,根据loan_apply_no来查询,修改日期
    def update_api_core_fr_api_order_info_d0(self, loan_apply_no):
        req_seq_no = Select_Sql_Result().select_zx_loan_apply_record(loan_apply_no)['loan_no']
        now_date = (datetime.datetime.now() - relativedelta(months=1))
        update_sql = f"UPDATE finance_router.fr_api_order_info as fr SET fr.settle_time = '{now_date.strftime('%Y-%m-%d %H:%M:%S')}',fr.apply_dt = '{now_date.strftime('%Y-%m-%d')}', fr.repay_day = '{now_date.strftime('%Y-%m-%d')}' WHERE fr.req_seq_no = '{req_seq_no}';"
        result = Mysql().update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # 集合更新api侧绑卡前的funds_code
    def update_api_flow_all_table(self, funds_code, user_id):
        db = Update_Sql_Result()
        db.update_api_flow_zx_credit_user_info(funds_code, user_id)
        db.update_api_flow_zx_credit_applicant_result(funds_code, user_id)
        db.update_api_flow_zl_drms_judgements(funds_code, user_id)
        db.update_api_flow_zx_credit_applicant_info(funds_code, user_id)
        db.update_api_flow_zx_credit_info(funds_code, user_id)
        self.logging.info(f"全部执行完毕！")


if __name__ == '__main__':
    user_id = "NCY1723456810067"
    print(Update_Sql_Result().update_api_core_fr_api_repayment_plan_d0("NCY1723456810067", "1"))
    # print((datetime.datetime.now() - relativedelta(months=1)).strftime("%Y-%m-%d %H:%M:%S"))
