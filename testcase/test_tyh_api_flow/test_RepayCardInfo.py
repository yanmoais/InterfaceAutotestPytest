#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:03

"""
    此文件自动化案例为API全流程流程，带{channelId}，授信-借款-还款流程
"""
import json

from sqlalchemy import null

from util_tools.logger import Logger
import time
from common.Core_Tyh_App import Core_tyh_app

import allure


#还款卡⽚信息
@allure.epic("还款卡⽚信息")
@allure.feature("还款卡⽚信息")
@allure.title("还款卡⽚信息")
@allure.story("还款卡⽚信息")
@allure.severity(allure.severity_level.NORMAL)
def test_loan_card_info_success():
    with allure.step("数据初始化"):
        logging = Logger().init_logger()

    with allure.step("获取验证码"):
        request_data1 = {'phone': '13812317169',
                         'type': 'login',
                         'ticket': '123456',
                         "nonstr": '123456'
                         }
        sms_resp = Core_tyh_app().test_sms_send(request_data1)
        logging.info(f"登录数据为：======{sms_resp}")
        time.sleep(2)

    with allure.step("登录"):
        request_data2 = {
            'device': '17327587667912371212',
            'captcha': '888888',
            'account': '13812317169',
            'deviceModel': 'PC',
            'loginType': 'ios',
            'osVersion': 'Windows 10 x64'
        }
        response_data = Core_tyh_app().test_login_param(request_data2)
        logging.info(f"登录数据为：======{response_data}")
        Authorization = response_data
        #1.登录成功,获取返回数据
        token = {"Authorization": Authorization}
        logging.info(f"登录token为：======{token}")
        logging.info(f"登录返回的token数据为：======{response_data}")
        time.sleep(1)
        #2.查询用户放款信息
        response_data2 = Core_tyh_app().test_repaycard_info(headers=token)
        assert response_data2['data'] != null
        logging.info(f"用户还款卡⽚信息的数据为：======{response_data2}")




