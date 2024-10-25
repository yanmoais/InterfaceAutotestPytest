#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午3:54
from testdata.assert_data.banding_assert_data import *
from testdata.assert_data.loan_assert_data import *
from testdata.assert_data.loan_credit_amt_assert_data import credit_amt_query_success_data
from util_tools.Loop_result import loop_result
from util_tools.Public_Assert import loan_success_assert, banding_card_success_assert, loan_credit_amt_success_assert
from util_tools.logger import Logger
from util_tools.Faker import *
from common.Core_Zjly_Api import core_zjly_api
from common.Encrypt_Decrypt import encrypt_decrypt
import allure


@allure.epic("同程资方")
@allure.feature("授信模块")
@allure.story("同程资方授信放款案例")
@allure.title("放款成功")
def test_zx_loan_success():
    with allure.step("数据初始化"):
        id_no, birthday = get_zx_user_id_no()
        user_name = get_user_name()
        mobile_no = get_phone_mum()
        acct_no = get_ccb_num()
        custid = get_cust_id()
        bank_name = "中国建设银行"
        loan_amt = "2000"
        reqPeriods = "12"
        current_date = get_now_time()

        loan_sqe_no = get_req_seq_no()
        req_no = get_req_no()
        bk_no = get_bank_id()
        fk_no = get_fk_id()
        logging = Logger().init_logger()

    with allure.step("发起授信/客户信息同步"):
        # 1.授信申请加密
        sx_need_encry_data = {'apiKey': 'CSTC', 'params':json_dumps_cn({"birthday":birthday,"applyDt":current_date,"maxDegree":"10","maritalStatus":"10","idStartDate":"2024-07-18","signOffice":"罗定市公安局","mobileNo":mobile_no,"gender":"F","userName":user_name,"loanseqno":loan_sqe_no,"idNo":id_no,"monthlySalary":"1000","idExpireDate":"9999-12-31","custId":custid,"fromChannel":"01","fileIDs":"e6e60b02818642118986b9be415ad0f71688616059531,bc5cfb353801470d9ce96eaff7f9e9581688621835451,562d6907777740f48511cc21977ffe811688621899067,6851d584430f46699fa5d5cde7da53b61688708647828,5781179a81d34dd69a5dbb8034a41ed71689059737521,11143efc9ca84fd7ba2cc768c05dfde71689059737681,1b9d43f6dee840dcbb2f7358c87ff6f11689059737364,a318af748ff54269ab8a8463134ccd501689059737448","regAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"liveAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"emergencyContact":[{"relation":"01","mobileNo":"18197269653","name":"毛不易"},{"relation":"02","mobileNo":"18197269659","name":"李文忠"}],"occupationInfo":{"companyAddInfo":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"profession":"0","companyPhone":"02035949111","companyName":"测试科技有限公司","industry":"A","position":"01"},"loanInfo":{"priceAcc":"0.2395","loanFreq":"1M","rateType":"1","loanType":"PZ","reqPeriods":reqPeriods,"reqAmount":loan_amt,"dueDayOpt":"1","custDayRate":"0.2395","reqPurpose":"1"},"accInfoList":[{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"},{"acctKind":"02","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"}]}), 'requestNo': req_no}
        # 加密数据
        sx_encry_data = encrypt_decrypt().param_encry_by_channel(sx_need_encry_data, 'tongCheng')
        # 1.授信申请请求,获取返回数据
        sxsq_resp = core_zjly_api().test_order_apply(sx_encry_data)
        # 1.授信申请返回数据解密
        decry_data = encrypt_decrypt().param_decrys_by_channel(sxsq_resp, 'tongCheng')
        logging.info(f"解密后的授信申请返回数据为：======{decry_data}")

    with allure.step("授信状态查询"):
        # 2.授信状态查询加密
        zt_need_ency_data = {"apiKey": "CSTC","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的授信状态查询数据为：======{zt_need_ency_data}")
        sxzt_encry = encrypt_decrypt().param_encry_by_channel(zt_need_ency_data,'tongCheng')
        logging.info(f"加密后的授信状态查询数据为：======{sxzt_encry}")
        # 轮训读取判断查询结果，为"授信通过"则跳出
        # 2.授信状态查询请求
        loop_result().loop_sxcx_result(sxzt_encry,'tongCheng')

    with allure.step("发起通联绑卡"):
        # 3.签约申请加密
        qybk_ency_data = {"apiKey": "CSTC","params":json_dumps_cn({"seqno":bk_no,"loanseqno":loan_sqe_no,"id_no":id_no,"user_name":user_name,"mobile_no":mobile_no,"bankCode":"0105","cardNo":acct_no,"bankName":bank_name,"registerPhone":mobile_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的签约申请数据为：======{qybk_ency_data}")
        qybk_encry = encrypt_decrypt().param_encry_by_channel(qybk_ency_data, 'tongCheng')
        logging.info(f"加密后的签约申请数据为：======{qybk_encry}")
        # 3.签约申请请求
        qysq_resp = core_zjly_api().test_binding_card_apply(qybk_encry)
        # 3.签约申请返回数据解密
        qysq_decry = encrypt_decrypt().param_decrys_by_channel(qysq_resp,'tongCheng')
        logging.info(f"解密后的签约申请返回数据为：======{qysq_decry}")

    with allure.step("绑卡签约确认"):
        # 4.签约确认加密
        qyqr_encry_data = {"apiKey": "CSTC","params":json_dumps_cn({"seqno":bk_no,"smscode":"111111"}),"requestNo": req_no}
        # 需要将数据再次格式化成带转义符并且去除空格
        qyqr_encry = encrypt_decrypt().param_encry_by_channel(qyqr_encry_data,'tongCheng')
        logging.info(f"加密后的签约确认数据为：======{qyqr_encry}")
        # 4.签约确认请求
        qyqr_resp = core_zjly_api().test_binding_card_confirm(qyqr_encry)
        # 4.签约确认返回数据解密
        qyqr_decry = encrypt_decrypt().param_decrys_by_channel(qyqr_resp,'tongCheng')
        logging.info(f"解密后的签约确认返回数据为：======{qyqr_decry}")

    with allure.step("发起借款"):
        # 5.放款申请加密
        fk_encry_data = {"apiKey":"CSTC","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no,"amt":loan_amt,"fileIDs":"1780487717038329856,6b2a97dc90794fe2b78fa5412c82be581713337050255","accInfoDto":{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","acct_no":acct_no,"acctName":user_name,"id_no":id_no,"acctPhone":mobile_no,"bankName":bank_name}}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的放款申请数据为：======{fk_encry_data}")
        fksq_encry = encrypt_decrypt().param_encry_by_channel(fk_encry_data, 'tongCheng')
        logging.info(f"加密后的放款申请数据为：======{fksq_encry}")
        # 5.放款申请请求
        fksq_resp = core_zjly_api().test_loan_apply_settle(fksq_encry)
        # 5.放款申请返回数据解密
        fksq_decry = encrypt_decrypt().param_decrys_by_channel(fksq_resp, 'tongCheng')
        logging.info(f"解密后的放款申请返回数据为：======{fksq_decry}")

    with allure.step("借款状态查询"):
        # 6.放款状态查询加密
        fkzt_encry_data = {"apiKey": "CSTC","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        fkzt_encry = encrypt_decrypt().param_encry_by_channel(fkzt_encry_data, 'tongCheng')
        logging.info(f"加密后的放款状态数据为：======{fkzt_encry}")
        # 轮询查询放款结果，查询到结果为"放款成功"则跳出
        # 6.放款状态查询请求
        loop_result().loop_fkcx_result(fkzt_encry, 'tongCheng')

    with allure.step("还款计划查询"):
        # 放款成功后需要再次调用一下还款计划接口，落库更新
        # 7.还款计划查询加密
        hkjh_encry_data = {"apiKey":"CSTC","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的还款计划查询数据为：======{hkjh_encry_data}")
        hkjh_encry = encrypt_decrypt().param_encry_by_channel(hkjh_encry_data, 'tongCheng')
        logging.info(f"加密后的还款计划查询数据为：======{hkjh_encry}")
        # 7.还款计划查询请求
        hkjh_resp = core_zjly_api().test_loan_apply_order_query(hkjh_encry)
        # 7.还款计划查询返回数据解密
        hkjh_decry = encrypt_decrypt().param_decrys_by_channel(hkjh_resp, 'tongCheng')
        logging.info(f"解密后的还款计划查询数据为：======{hkjh_decry}")

    with allure.step("断言绑卡信息表"):
        banding_card_success_assert(bk_no, banding_card_assert_data)

    with allure.step("断言授信订单表"):
        loan_success_assert(loan_sqe_no, loan_success_assert_data)
