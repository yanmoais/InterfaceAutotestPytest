#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午10:37
import json
import logging

import requests
from util_tools.logger import Logger
from config.Base_Env import *

requests.packages.urllib3.disable_warnings()


class xxlJob(object):
    def __init__(self):
        self.cookies = ''
        self.proxies = ''
        self.xxl_job_username = XXL_JOB_USERNMAE
        self.xxl_job_password = XXL_JOB_PASSWORD
        self.logging = Logger().init_logger()

    # 登录XXL-JOB
    def login_xxl_job(self, ENV="flow_api"):
        global uri
        if ENV == "core_api":
            uri = f'{XXL_JOB_HOST_CORE_API}xxl-job-admin/login'
        elif ENV == "flow_api":
            uri = f'{XXL_JOB_HOST_FLOW_API}xxl-job-admin/login'
        elif ENV == "sit_llh":
            uri = f'{XXL_JBO_HOST_SIT_LLH}xxl-job-admin/login'
            self.xxl_job_username = XXL_JOB_SIT_LLH_USERNMAE
            self.xxl_job_password = XXL_JOB_SIT_LLH_PASSWORD
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        cookies = ''
        proxies = self.proxies
        params = {
            'userName': self.xxl_job_username,
            'password': self.xxl_job_password,
            'ifRemember': 'on',
        }
        data = requests.post(url=uri, data=params, cookies=cookies, headers=headers, proxies=proxies, verify=False,
                             timeout=3000, allow_redirects=False)
        self.logging.info('接口返回数据：\n\t' + str(data.content))
        respone_data = json.loads(data.content)
        if respone_data['code'] == 500 and '账号或密码错误' in respone_data['msg']:
            self.logging.info('账号或密码错误\n\t')
            assert False
        if respone_data['code'] == 200:
            self.cookies = data.cookies
            self.logging.info('登录成功\n\t')
        self.logging.info('\n\t\n\t')

    # 执行对应的JOB任务
    def trigger_xxl_job(self, id, executorParam=None, ENV="flow_api"):
        # 登录XXL-JOB
        # global uri
        # if ENV == "core_api":
        #     uri = f'{XXL_JOB_HOST_CORE_API}xxl-job-admin/login'
        # elif ENV == "flow_api":
        #     uri = f'{XXL_JOB_HOST_FLOW_API}xxl-job-admin/login'
        # elif ENV == "sit_llh":
        #     uri = f'{XXL_JBO_HOST_SIT_LLH}xxl-job-admin/login'
        #     self.xxl_job_username = XXL_JOB_SIT_LLH_USERNMAE
        #     self.xxl_job_password = XXL_JOB_SIT_LLH_PASSWORD
        # headers = {
        #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        #     "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        # cookies = ''
        # proxies = self.proxies
        # params = {
        #     'userName': self.xxl_job_username,
        #     'password': self.xxl_job_password,
        #     'ifRemember': 'on',
        # }
        # data = requests.post(url=uri, data=params, cookies=cookies, headers=headers, proxies=proxies, verify=False,
        #                      timeout=3000, allow_redirects=False)
        # self.logging.info('接口返回数据：\n\t' + str(data.content))
        # respone_data = json.loads(data.content)
        # if respone_data['code'] == 500 and '账号或密码错误' in respone_data['msg']:
        #     self.logging.info('账号或密码错误\n\t')
        #     assert False
        # if respone_data['code'] == 200:
        #     self.cookies = data.cookies
        #     self.logging.info('登录成功\n\t')
        # self.logging.info('\n\t\n\t')

        self.login_xxl_job(ENV)
        logging.info("登录成功")
        global uris
        if ENV == "core_api":
            uris = f'{XXL_JOB_HOST_CORE_API}xxl-job-admin/jobinfo/trigger'
        elif ENV == "flow_api":
            uris = f'{XXL_JOB_HOST_FLOW_API}xxl-job-admin/jobinfo/trigger'
        elif ENV == "sit_llh":
            uris = f'{XXL_JBO_HOST_SIT_LLH}xxl-job-admin/jobinfo/trigger'
        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x1800142b) NetType/WIFI Language/zh_CN",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
        cookies = self.cookies
        proxies = self.proxies
        params = {
            "id": id,
            "executorParam": executorParam,
            "addressList": '',
            'chainParamType': 0
        }
        data = requests.post(uris, data=params, cookies=cookies, headers=headers, proxies=proxies, verify=False,
                             timeout=3000, allow_redirects=False)
        self.logging.info('接口返回数据：\n\t' + str(data.json()))
        respone_data = json.loads(data.content)
        if respone_data['code'] == 200:
            self.logging.info('只触发一次job任务成功\n\t')


if __name__ == '__main__':
    xxlJob().login_xxl_job("sit_llh")
