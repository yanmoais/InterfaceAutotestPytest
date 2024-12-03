# # -*- coding: utf-8 -*-
import csv
import random
import socket
import pytest
from locust import task, TaskSet, HttpUser, tag
from testfunctions.core_zjly_test import *
from random import randint
import json

from util_tools.Faker import json_dumps_cn, json_dumps_format


class UserTasks(TaskSet):
    def on_start(self):
        print("-----------on_start----------------")

    # 声明下面是一个任务
    @task(1)
    def repay_zfzt(self):
        # 发送请求并响应
        # response = self.client.post("/path",data = self.loginData[ranIndex],catch_response=True)
        # response = self.client.get(url="http://59.110.220.173:8082")

        # 读取 CSV 文件并加载到内存中
        with open("user_data.csv", mode="r") as file:
            reader = csv.DictReader(file)
            users = [row for row in reader]  # 将每行数据存储为字典
        user_data = random.choice(users)

        reqSn = get_zfpt_req_no()
        apply_data = {
            "reqSn": reqSn,
            "businessChannel": 101,
            "params": json_dumps_cn({
                "ACCOUNT_NAME": "扣款测试",
                "BANK_CODE": "0105",
                "BANK_NAME": "中国建设银行",
                "CREDIT_ACCTNO": user_data['acct'],
                "TEL": user_data['mobile'],
                "ID": user_data['id_no'],
                "REPAY_PRODUCT_CODE": "repay_mock",
                "AMOUNT": "30000",
                "TYPE": 3
            })
        }
        request_data = test_zjl_jiami(apply_data)
        headers = {"Content-Type": "application/json"}
        apply_request_data = {"reqSn": request_data['reqSn'], "timeStamp": request_data['timeStamp'],
                              "businessChannel": 101,
                              "sign": request_data['sign'],
                              "key": request_data['key'],
                              "requestData": request_data['requestData']}
        # 发送扣款申请
        # print("发送扣款申请的流水号", reqSn)
        rep = self.client.post(url="http://192.168.1.187:8199/v1/withholdApply", json=apply_request_data,
                               headers=headers)
        # 发送扣款结果查询
        query_data = {
            "reqSn": reqSn,
            "businessChannel": 101
        }
        # print("发送扣款查询的流水号", reqSn)
        query_request_data = test_zjl_jiami(query_data)
        print("加密后的数据为：", query_request_data)
        query_apply_data = {"reqSn": query_request_data['reqSn'], "timeStamp": query_request_data['timeStamp'],
                            "businessChannel": 101,
                            "sign": query_request_data['sign'],
                            "key": query_request_data['key']}
        reps = self.client.post(url="http://192.168.1.187:8199/v1/withholdQuery", json=query_apply_data,
                                headers=headers)

    # @task(2)
    # def band_card(self):
    #     # 读取 CSV 文件并加载到内存中
    #     with open("band_card_data.csv", mode="r") as file:
    #         reader = csv.DictReader(file)
    #         users = [row for row in reader]  # 将每行数据存储为字典
    #     user_data = random.choice(users)
    #
    #     reqSn = get_zfpt_req_no()
    #     apply_data = {
    #         "reqSn": reqSn,
    #         "businessChannel": 101,
    #         "params": json_dumps_cn({
    #             "ACCOUNT_NAME": user_data['user_name'],
    #             "BANK_CODE": "0105",
    #             "BANK_NAME": "建设银行",
    #             "CREDIT_ACCTNO": user_data['acct'],
    #             "TEL": user_data['phone'],
    #             "ID": user_data['id_no'],
    #             "BIND_PRODUCT_CODE": "bind_mock"
    #         })
    #     }
    #     request_data = test_zjl_jiami(apply_data)
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
    #     # print("发送扣款查询的流水号", reqSn)
    #     query_request_data = test_zjl_jiami(query_data)
    #     query_apply_data = {"reqSn": query_request_data['reqSn'], "timeStamp": query_request_data['timeStamp'],
    #                           "businessChannel": 101,
    #                           "sign": query_request_data['sign'],
    #                           "key": query_request_data['key'],
    #                           "requestData": query_request_data['requestData']}
    #     reps = self.client.post(url="http://192.168.1.187:8199/v1/bindBankConfirm", json=query_apply_data,
    #                             headers=headers)


class WebUser(HttpUser):
    tasks = [UserTasks]
    # 最小等待时间和最大等待时间   请求间的间隔时间
    min_wait = 2000
    max_wait = 4000
# locust -f performance_test.py --host=http://localhost:8082
# Number of total users to simulate   模拟的用户数
# Spawn rate (users spawned/second)   每秒产生的用户数
# locust -f  performance_test.py --web-host=127.0.0.1  --web-port=8083
