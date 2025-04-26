# # -*- coding: utf-8 -*-
import csv
import json
import random
import socket
from datetime import datetime
from locust import task, TaskSet, HttpUser, tag

from data_generator import read_random_line
from testfunctions.core_zjly_test import core_zjly_func
from util_tools.Faker import *
from util_tools.Faker import json_dumps_cn, json_dumps_format
from util_tools.Read_photo import get_positive_photo, get_negative_photo, get_best_photo


class UserTasks(TaskSet):
    def on_start(self):
        print("-----------on_start----------------")

    # 声明下面是一个任务
    # @task(1)
    # def repay_zfzt(self):
    #     # 发送请求并响应
    #     # response = self.client.post("/path",data = self.loginData[ranIndex],catch_response=True)
    #     # response = self.client.get(url="http://59.110.220.173:8082")
    #
    #     # 读取 CSV 文件并加载到内存中
    #     with open("user_data.csv", mode="r") as file:
    #         reader = csv.DictReader(file)
    #         users = [row for row in reader]  # 将每行数据存储为字典
    #     user_data = random.choice(users)
    #
    #     reqSn = get_zfpt_req_no()
    #     apply_data = {
    #         "reqSn": reqSn,
    #         "businessChannel": 101,
    #         "params": json_dumps_cn({
    #             "ACCOUNT_NAME": "扣款测试",
    #             "BANK_CODE": "0105",
    #             "BANK_NAME": "中国建设银行",
    #             "CREDIT_ACCTNO": user_data['acct'],
    #             "TEL": user_data['mobile'],
    #             "ID": user_data['id_no'],
    #             "REPAY_PRODUCT_CODE": "repay_mock",
    #             "AMOUNT": "30000",
    #             "TYPE": 3
    #         })
    #     }
    #     request_data = core_zjly_func().test_zjl_jiami(apply_data)
    #     headers = {"Content-Type": "application/json"}
    #     apply_request_data = {"reqSn": request_data['reqSn'], "timeStamp": request_data['timeStamp'],
    #                           "businessChannel": 101,
    #                           "sign": request_data['sign'],
    #                           "key": request_data['key'],
    #                           "requestData": request_data['requestData']}
    #     # 发送扣款申请
    #     # print("发送扣款申请的流水号", reqSn)
    #     rep = self.client.post(url="http://192.168.1.187:8199/v1/withholdApply", json=apply_request_data,
    #                            headers=headers)
    #     # 发送扣款结果查询
    #     query_data = {
    #         "reqSn": reqSn,
    #         "businessChannel": 101
    #     }
    #     # print("发送扣款查询的流水号", reqSn)
    #     query_request_data = core_zjly_func().test_zjl_jiami(query_data)
    #     print("加密后的数据为：", query_request_data)
    #     query_apply_data = {"reqSn": query_request_data['reqSn'], "timeStamp": query_request_data['timeStamp'],
    #                         "businessChannel": 101,
    #                         "sign": query_request_data['sign'],
    #                         "key": query_request_data['key']}
    #     reps = self.client.post(url="http://192.168.1.187:8199/v1/withholdQuery", json=query_apply_data,
    #                             headers=headers)

    # @task(1)
    # def band_card(self):
    #     # start_time = datetime.datetime.now()
    #     # print("开始的时间", start_time)
    #     # # 读取 CSV 文件并加载到内存中
    #     # with open("user_data.csv", mode="r", encoding='utf-8') as file:
    #     #     reader = csv.DictReader(file)
    #     #     users = [row for row in reader]  # 将每行数据存储为字典
    #     # user_data = random.choice(users)
    #
    #     # 使用Faker工具类库生成数据
    #     # user_name = get_user_name()
    #     # acct = get_baofu_ccb_num()
    #     # phone = get_phone_mum()
    #     # id_no, birthday = get_zx_user_id_no()
    #
    #     reqSn = get_zfpt_req_no()
    #     apply_data = {
    #         "reqSn": reqSn,
    #         "businessChannel": 101,
    #         "params": json_dumps_cn({
    #             "ACCOUNT_NAME": "王婷",
    #             "BANK_CODE": "0105",
    #             "BANK_NAME": "建设银行",
    #             "CREDIT_ACCTNO": "6217201733797738840",
    #             "TEL": "15955348291",
    #             "ID": "440113197708128669",
    #             "BIND_PRODUCT_CODE": "bind_mock"
    #         })
    #     }
    #     request_data = core_zjly_func().test_zjl_jiami(apply_data)
    #     headers = {"Content-Type": "application/json"}
    #     apply_request_data = {"reqSn": request_data['reqSn'], "timeStamp": request_data['timeStamp'],
    #                           "businessChannel": 101,
    #                           "sign": request_data['sign'],
    #                           "key": request_data['key'],
    #                           "requestData": request_data['requestData']}
    #     # 发送绑卡申请
    #     # print("发送绑卡申请的流水号", reqSn)
    #     rep = self.client.post(url="http://192.168.1.187:8199/v1/bindBankApply", json=apply_request_data,
    #                            headers=headers)
    #     # 发送绑卡结果查询
    #     query_data = {
    #         "reqSn": reqSn,
    #         "businessChannel": 101,
    #         "params": json_dumps_cn({
    #             "VERCODE": "111111"
    #         })
    #     }
    #     # print("发送绑卡查询的流水号", reqSn)
    #     query_request_data = core_zjly_func().test_zjl_jiami(query_data)
    #     print("绑卡查询数据加密：", query_request_data)
    #     query_apply_data = {"reqSn": query_request_data['reqSn'], "timeStamp": query_request_data['timeStamp'],
    #                         "businessChannel": 101,
    #                         "sign": query_request_data['sign'],
    #                         "key": query_request_data['key'],
    #                         "requestData": query_request_data['requestData']}
    #     reps = self.client.post(url="http://192.168.1.187:8199/v1/bindBankConfirm", json=query_apply_data,
    #                             headers=headers)
    #     # end_time = datetime.datetime.now()
    #     # print("结束的时间", end_time)
    #     # # 计算时间差
    #     # time_difference = start_time - end_time
    #     # print("相差的时间", time_difference)

    # @task(1)
    # def short_link(self):
    #     # # 读取 CSV 文件并加载到内存中
    #     # with open("user_data.csv", mode="r", encoding='utf-8') as file:
    #     #     reader = csv.DictReader(file)
    #     #     users = [row for row in reader]  # 将每行数据存储为字典
    #     # user_data = random.choice(users)
    #
    #     # 使用Faker工具类库生成数据
    #     # user_name = get_user_name()
    #     # acct = get_baofu_ccb_num()
    #     # phone = get_phone_mum()
    #     # id_no, birthday = get_zx_user_id_no()
    #     numbs = random.randint(0, 999)
    #     numb = random.randint(0, 100)
    #     payload = {
    #         "action": "shorturl",
    #         "url": f"http://{numbs}.{numb}.com",
    #         "format":"json"
    #     }
    #     headers = {
    #         "Content-Type": "multipart/form-data; charset=utf-8"
    #     }
    #     # 发送创建短链请求
    #     # print("发送绑卡申请的流水号", reqSn)
    #     rep = self.client.post(url=f"http://183.6.104.148:1008/api.php?username=test&password=test", data=payload)
    #     print(rep.text)

    # @task(1)
    # def sit_check_user(self):
    #     # 读取 txt 文件并加载到内存中
    #     mobile_data = read_risk_phone(RISK_PHONE_MD5_PATH)
    #     # 初始化环境参数
    #     host = "http://gzdev.ffyla.com:26801"
    #     channelId = "LLH_XY"
    #     payload = {
    #         "partner": channelId
    #     }
    #     headers = {"Content-Type": "application/json;charset=UTF-8"}
    #     payload["data"] = {"md5": mobile_data, "mode": "M"}
    #     print(payload)
    #     # 发送撞库请求
    #     rep = self.client.post(url=host + "/checkUser", json=payload, headers=headers)
    #     print(rep)

    # @task(1)
    # def sit_tiny_id(self):
    #     host = "http://tinyid-sit.zhonglishuke.com/tinyid/id/nextSegmentIdSimple?token=0f673adf80504e2eaa552f5d791b644c&bizType=test_refresh"
    #     headers = {"Content-Type": "application/json;charset=UTF-8"}
    #     # 发送请求
    #     rep = self.client.get(url=host, headers=headers)
    #     print(rep.text)


    @task(1)
    def sit_apply_credit(self):
        data = None
        # 初始化环境参数
        host = "http://gzdev.ffyla.com:26801"
        channelId = "LLH_XY"
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        payload = {
            "partner": channelId
        }
        for _ in range(1):  # 随机读取1次
            data = read_random_line("test_data.txt")

        credit_apply_no = data['credit_apply_no']
        apply_time = data['apply_time']
        id_no = data['id_no']
        user_name = data['user_name']
        user_id = data['user_id']
        bank_card_no = data['bank_card_no']

        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()
        # 产品信息
        product_code = "LLH"
        # 授信申请数据
        sx_need_encry_data = {"userId": user_id, "creditApplyNo": credit_apply_no, "applyTime": apply_time,
                              "productCode": product_code, "applyAmount": "20000.00",
                              "userInfo": {"mobile": mobile_no, "name": user_name, "idCardNo": id_no, "marriage": "20",
                                           "monthlyIncome": "4", "education": "20", "job": "1", "province": "广东省",
                                           "city": "广州市", "district": "番禺区",
                                           "addrDetail": "广东省广州市番禺区成钧街道豪承小区190号楼501"},
                              "idCardOcrInfo": {"positive": get_positive_photo(), "negative": get_negative_photo(),
                                                "nameOCR": user_name, "idCardNoOCR": id_no, "beginTimeOCR": "20230829",
                                                "duetimeOCR": "20991231",
                                                "addressOCR": "广东省广州市番禺区成钧街道豪承小区190号楼501",
                                                "sexOCR": "M", "ethnicOCR": "汉族", "issueOrgOCR": "广州市公安局"},
                              "faceInfo": {"assayTime": apply_time, "assayType": "SENSETIME", "best": get_best_photo()},
                              "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455377",
                                              "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209187"},
                              "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                               "userName": user_name, "bankCardNo": bank_card_no},
                              "geoInfo": {"latitude": "43.57687931900941", "longitude": "112.55172012515888"},
                              "companyInfo": {
                                  "companyName": "中国建筑集团有限公司",
                                  "province": "440000",
                                  "city": "440100", "district": "440114",
                                  "companyAddr": "广东省广州市番禺区三里河路15号"},
                              "agreementTime": apply_time,
                              "extendInfo": {
                                  "UTag": "C",
                                  "mobileMode": "21091116AC",
                                  "networkType": "",
                                  "system": "android",
                                  "systemVersion": "13"}}
        payload["data"] = sx_need_encry_data
        print("授信请求数据：", payload)
        # 发送授信请求
        rep = self.client.post(url=host + "/applyCredit", json=payload, headers=headers)
        print(rep.text)


class WebUser(HttpUser):
    tasks = [UserTasks]
    # 最小等待时间和最大等待时间   请求间的间隔时间
    min_wait = 2000
    max_wait = 4000
# locust -f performance_test.py --host=http://localhost:8089
# Number of total users to simulate   模拟的用户数
# Spawn rate (users spawned/second)   每秒产生的用户数
# locust -f  performance_test.py --web-host=127.0.0.1  --web-port=8083
