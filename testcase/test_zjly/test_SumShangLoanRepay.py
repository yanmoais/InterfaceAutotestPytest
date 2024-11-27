#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午2:46
"""
    此文件自动化案例为各个资金方授信-借款-还款流程
"""
from testdata.assert_data.banding_assert_data import banding_card_assert_data
from testdata.assert_data.loan_assert_data import loan_success_assert_data
from testfunctions.core_zjly_test import *
from util_tools.Loop_result import loop_result
from util_tools.Public_Assert import banding_card_success_assert, loan_success_assert
from util_tools.logger import Logger
from util_tools.Faker import *
from common.Core_Zjly_Api import core_zjly_api
from common.Encrypt_Decrypt import encrypt_decrypt
import allure


@allure.epic("苏商蒙商资方")
@allure.feature("授信模块")
@allure.story("苏商蒙商资方授信放款案例")
@allure.title("放款成功")
def test_mengshang_loan_success():
    with allure.step("数据初始化"):
        id_no, birthday = "440114197601103679", "1976-01-10"
        user_name = "陆虎"
        mobile_no = "15978291031"
        acct_no = "6217001732171164400"
        custid = "ZL173217974399"
        bank_name = "建设银行"
        loan_amt = "2000"
        reqPeriods = "12"
        bk_no = get_bank_id()
        repay_no = get_repay_no()
        apiKey = "CSSUSHANG"
        channel = "suShang"

        loan_sqe_no = get_req_seq_no()
        req_no = get_req_no()
        fk_no = get_fk_id()
        contract_no = get_contract_no()
        dbht_no = get_dbht_no()
        bink_no = get_bink_no()
        logging = Logger().init_logger()

    # 绑定支付通道
    with allure.step("绑定支付通道"):
        resp = test_zfzt_bank_apply(ACCOUNT_NAME=user_name, TEL=mobile_no, ID=id_no, CREDIT_ACCTNO=acct_no)
        resp_confirm = test_zfzt_bank_confirm(resp[0])
        signProtocolId = resp_confirm['AGRMNO']
        logging.info(f"当前绑卡状态为： {resp_confirm}")

    # 每次请求前需要进行加密，得到的返回结果需要传给下游接口时候需要解密出来，下次使用又需要加密
    with allure.step("发起授信"):
        # 1.授信申请加密
        sx_need_encry_data = {'apiKey': apiKey,'params':json_dumps_cn({"riskInfo":{"creditLimitAmt":"20000.00","loanAmount":loan_amt,"overdue":"0","current_due_money":"0.00","maxOverDueDay":"0","guaranteeRateIrr":"0.000175"},"gender":"F","birthday":birthday,"guaranteeInfo":{"guarOdIntRate":"0.00022037","guarRate":"0.079333","guarTime":"12","guarAmt":"237.96"},"nation":"汉","loanseqno":loan_sqe_no,"idNo":id_no,"merchantName":"大商户","monthlySalary":"1000","idExpireDate":"2037-11-30","merchantId":"69355551222","companyPhone":"02061959111","childrenNum":"2","custId":custid,"fromChannel":"01","regAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"liveAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"applyDt":"2024-09-04","emergencyContact":[{"relation":"01","mobileNo":"18197269653","name":"毛不易"},{"relation":"02","mobileNo":"18197269659","name":"李文忠"}],"idStartDate":"2017-11-30","signOffice":"罗定市公安局","mobileNo":mobile_no,"userName":user_name,"fileIDs":"ef4cfdde418f4aa58ddb266ba905d9871731916380657,aaee76137d934f6daf73f9256fc61c8d1731916380870,3ed601982d294380881b2f5fa45252dc1731916381114,b8d92eef19ad4293b770c1e7db3ba8e51731916381227","occupationInfo":{"companyAddInfo":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"profession":"0","companyPhone":"02035949111","companyName":"测试科技有限公司","industry":"A","position":"01"},"loanInfo":{"priceAcc":"0.2395","loanFreq":"1M","rateType":"1","loanType":"PZ","reqPeriods":reqPeriods,"reqAmount":loan_amt,"dueDayOpt":"1","custDayRate":"0.2394","reqPurpose":"1"},"maxDegree":"10","accInfoList":[{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"},{"acctKind":"02","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"}],"maritalStatus":"10"}), 'requestNo': req_no}
        # 加密数据
        sx_encry_data = encrypt_decrypt().param_encry_by_channel(sx_need_encry_data, channel)
        # 1.授信申请请求,获取返回数据
        sxsq_resp = core_zjly_api().test_order_apply(sx_encry_data)
        # 1.授信申请返回数据解密
        decry_data = encrypt_decrypt().param_decrys_by_channel(sxsq_resp, channel)
        logging.info(f"解密后的授信申请返回数据为：======{decry_data}")

    with allure.step("授信状态查询"):
        # 2.授信状态查询加密
        zt_need_ency_data = {"apiKey": apiKey,"params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的授信状态查询数据为：======{zt_need_ency_data}")
        sxzt_encry = encrypt_decrypt().param_encry_by_channel(zt_need_ency_data, channel)
        logging.info(f"加密后的授信状态查询数据为：======{sxzt_encry}")
        # 轮训读取判断查询结果，为"授信通过"则跳出
        # 2.授信状态查询请求
        loop_result().loop_sxcx_result(sxzt_encry, channel)

    # with allure.step("发起通联绑卡"):
    #     # 3.签约申请加密
    #     qybk_ency_data = {"apiKey": apiKey,"params":json_dumps_cn({"seqno":bk_no,"loanseqno":loan_sqe_no,"id_no":id_no,"user_name":user_name,"mobile_no":mobile_no,"bankCode":"0105","cardNo":acct_no,"bankName":bank_name,"registerPhone":mobile_no}),"requestNo": req_no}
    #     # 加密数据
    #     logging.info(f"需要加密的签约申请数据为：======{qybk_ency_data}")
    #     qybk_encry = encrypt_decrypt().param_encry_by_channel(qybk_ency_data, channel)
    #     logging.info(f"加密后的签约申请数据为：======{qybk_encry}")
    #     # 3.签约申请请求
    #     qysq_resp = core_zjly_api().test_binding_card_apply(qybk_encry)
    #     # 3.签约申请返回数据解密
    #     qysq_decry = encrypt_decrypt().param_decrys_by_channel(qysq_resp,channel)
    #     logging.info(f"解密后的签约申请返回数据为：======{qysq_decry}")
    #
    # with allure.step("绑卡签约确认"):
    #     # 4.签约确认加密
    #     qyqr_encry_data = {"apiKey": apiKey,"params":json_dumps_cn({"seqno":bk_no,"smscode":"111111"}),"requestNo": req_no}
    #     # 需要将数据再次格式化成带转义符并且去除空格
    #     qyqr_encry = encrypt_decrypt().param_encry_by_channel(qyqr_encry_data,channel)
    #     logging.info(f"加密后的签约确认数据为：======{qyqr_encry}")
    #     # 4.签约确认请求
    #     qyqr_resp = core_zjly_api().test_binding_card_confirm(qyqr_encry)
    #     # 4.签约确认返回数据解密
    #     qyqr_decry = encrypt_decrypt().param_decrys_by_channel(qyqr_resp,channel)
    #     logging.info(f"解密后的签约确认返回数据为：======{qyqr_decry}")

    with allure.step("发起借款"):
        # 5.放款申请加密
        fk_encry_data = {"apiKey":apiKey,"params":json_dumps_cn({"payChannel":"BF","signProtocolId":signProtocolId,"requestNo":fk_no,"loanseqno":loan_sqe_no,"bindid":bink_no,"amt":loan_amt,"guarAmt":"237.96","guarRate":"0.079333","guarTime":"12","guarOdIntRate":"0.00022037","guarSignTime":"2024-09-07","guarEndTime":"2025-09-07","guarContNo":dbht_no,"guarContAddr":"广东","contractNo":contract_no,"fileIDs":"","accInfoDto":{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","acct_no":acct_no,"acctName":user_name,"id_no":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮","bankName":bank_name},"guaranteeList":[{"perdNo":"1","guarDate":"2024-10-07","perGuarFee":"19.83"},{"perdNo":"2","guarDate":"2024-11-07","perGuarFee":"19.83"},{"perdNo":"3","guarDate":"2024-12-07","perGuarFee":"19.83"},{"perdNo":"4","guarDate":"2025-01-07","perGuarFee":"19.83"},{"perdNo":"5","guarDate":"2025-02-07","perGuarFee":"19.83"},{"perdNo":"6","guarDate":"2025-03-07","perGuarFee":"19.83"},{"perdNo":"7","guarDate":"2025-04-07","perGuarFee":"19.83"},{"perdNo":"8","guarDate":"2025-05-07","perGuarFee":"19.83"},{"perdNo":"9","guarDate":"2025-06-07","perGuarFee":"19.83"},{"perdNo":"10","guarDate":"2025-07-07","perGuarFee":"19.83"},{"perdNo":"11","guarDate":"2025-08-07","perGuarFee":"19.83"},{"perdNo":"12","guarDate":"2025-09-07","perGuarFee":"19.83"}]}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的放款申请数据为：======{fk_encry_data}")
        fksq_encry = encrypt_decrypt().param_encry_by_channel(fk_encry_data, channel)
        logging.info(f"加密后的放款申请数据为：======{fksq_encry}")
        # 5.放款申请请求
        fksq_resp = core_zjly_api().test_loan_apply_settle(fksq_encry)
        # 5.放款申请返回数据解密
        fksq_decry = encrypt_decrypt().param_decrys_by_channel(fksq_resp, channel)
        logging.info(f"解密后的放款申请返回数据为：======{fksq_decry}")

    with allure.step("借款状态查询"):
        # 6.放款状态查询加密
        fkzt_encry_data = {"apiKey": apiKey,"params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        fkzt_encry = encrypt_decrypt().param_encry_by_channel(fkzt_encry_data, channel)
        logging.info(f"加密后的放款状态数据为：======{fkzt_encry}")
        # 轮询查询放款结果，查询到结果为"放款成功"则跳出
        # 6.放款状态查询请求
        loop_result().loop_fkcx_result(fkzt_encry, channel)

    with allure.step("还款计划查询"):
        # 放款成功后需要再次调用一下还款计划接口，落库更新
        # 7.还款计划查询加密
        hkjh_encry_data = {"apiKey":apiKey,"params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的还款计划查询数据为：======{hkjh_encry_data}")
        hkjh_encry = encrypt_decrypt().param_encry_by_channel(hkjh_encry_data, channel)
        logging.info(f"加密后的还款计划查询数据为：======{hkjh_encry}")
        # 7.还款计划查询请求
        hkjh_resp = core_zjly_api().test_loan_apply_order_query(hkjh_encry)
        # 7.还款计划查询返回数据解密
        hkjh_decry = encrypt_decrypt().param_decrys_by_channel(hkjh_resp, channel)
        logging.info(f"解密后的还款计划查询数据为：======{hkjh_decry}")

    with allure.step("放款成功断言"):
        loan_success_assert(loan_sqe_no, loan_success_assert_data)
