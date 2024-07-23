#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午10:20
from util_tools.Faker import *
from util_tools.logger import Logger


# 抽离初始化数据
def init_datas():
    id_no, birthday = get_user_idNo()
    user_name = get_user_name()
    mobile_no = get_phone_mum()
    acct_no = get_ccb_num()
    custid = get_cust_id()
    bank_name = "建设银行"
    loan_amt = "2000"
    reqPeriods = "12"
    loan_sqe_no = get_req_seq_no()
    req_no = get_req_no()
    fk_no = get_fk_id()
    contract_no = get_contract_no()
    dbht_no = get_dbht_no()
    bink_no = get_bink_no()
    logging = Logger().init_logger()
    return id_no, birthday, user_name, mobile_no, acct_no, custid, bank_name, loan_amt, reqPeriods, loan_sqe_no, req_no, fk_no, contract_no, dbht_no, bink_no, logging
