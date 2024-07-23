#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午6:30

from util_tools.Database_Conn import Mysql


class Select_Sql_Result(Mysql):
    # 查询fr_api_order_info表订单信息,根据借款流水号来查询
    def select_api_order_info_result(self, req_seq_no):
        select_sql = f"SELECT ord.loan_state, ord.trans_result, ord.trans_result_msg, ord.up_appl_sts, ord.settle_status, ord.is_compensatory, ord.delete_flag, ord.notify FROM finance_router.fr_api_order_info ord WHERE ord.req_seq_no = '{req_seq_no}'"
        result = Mysql().select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询fr_api_binding_bank_card表绑卡信息,根据签约单号来查询
    def select_api_binding_bank_card_result(self, bk_id):
        select_sql = f"SELECT bin.result_code, bin.result_msg FROM finance_router.fr_api_binding_bank_card bin WHERE bin.seqno = '{bk_id}'"
        result = Mysql().select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result

    # 查询fr_api_loan_amt_log表放款额度信息，根据借款流水号查询
    def select_api_loan_amt_log_result(self, loanseqno):
        select_sql = f"SELECT CAST(log.loan_amt AS CHAR)AS loan_amt,log.dn_sts, log.pay_msg,log.notify FROM finance_router.fr_api_loan_amt_log as log WHERE log.loanseqno = '{loanseqno}';"
        result = Mysql().select_db(select_sql)[0]
        self.logging.info(f"数据库查询返回数据为：==={result}")
        return result




if __name__ == '__main__':
    bk_id = "ZLTEST1721377980959"
    db = Select_Sql_Result()
    datas = db.select_api_loan_amt_log_result(bk_id)
    print(datas)
