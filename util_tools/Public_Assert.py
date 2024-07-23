#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午6:52
from common.Select_Database_Result import Select_Sql_Result


# 授信断言
def loan_success_assert(req_seq_no, actual_data):
    expected_data = Select_Sql_Result().select_api_order_info_result(req_seq_no)
    assert expected_data == actual_data


# 绑卡断言
def banding_card_success_assert(bk_id, actual_data):
    expected_data = Select_Sql_Result().select_api_binding_bank_card_result(bk_id)
    assert expected_data == actual_data


# 授信额度断言
def loan_credit_amt_success_assert(loanseqno, actual_data):
    expected_data = Select_Sql_Result().select_api_loan_amt_log_result(loanseqno)
    assert expected_data == actual_data


if __name__ == '__main__':
    bk_id = "BK1721035797151"
    data = {'result_code': '1001', 'result_msg': '已签约'}
    banding_card_success_assert(bk_id, data)
