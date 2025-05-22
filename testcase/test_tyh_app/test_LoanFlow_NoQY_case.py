import pytest
import requests
import pymysql
import json
import time
from datetime import datetime


class TestLoanAutomation:
    @pytest.fixture(autouse=True)
    def setup(self):
        # 数据库配置
        self.db_config = {
            'host': 'localhost',
            'user': 'your_username',
            'password': 'your_password',
            'database': 'your_database',
            'port': 3306,
            'charset': 'utf8mb4'
        }

        # 请求头
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # 初始化变量
        self.token = None
        self.bank_card_no = None
        self.user_id = None
        self.phone = None
        self.username = None

    def execute_sql(self, sql):
        """执行SQL查询并返回结果"""
        try:
            conn = pymysql.connect(**self.db_config)
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            return result
        except Exception as e:
            pytest.fail(f"SQL执行错误: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def test_get_available_user(self):
        """获取有额度的用户手机号"""
        sql = """
        SELECT * FROM tb_loan_user_info where user_name='宋军强' ;
        """
        result = self.execute_sql(sql)
        assert result and len(result) > 0, "未找到符合条件的用户"
        self.phone = result[0][0]
        print(f"获取到有额度的用户手机号: {self.phone}")

    def test_send_verify_code(self):
        """发送验证码"""
        if not self.phone:
            pytest.skip("用户手机号未设置，跳过发送验证码")

        url = "http://192.168.33.254:28018/api/register/verify"
        data = {
            "clientIp": "192.168.2.80",
            "appUserId": "",
            "description": "短信验证码发送",
            "startTime": int(time.time() * 1000),
            "spendTime": 10,
            "uri": "/api/register/verify",
            "url": "http://192.168.33.254:28018/api/register/verify",
            "method": "POST",
            "ip": "02-42-F9-F9-F7-07",
            "parameter": {"phone": self.phone, "type": "registerAndLogin"}
        }

        response = requests.post(url, headers=self.headers, json=data)
        assert response.status_code == 200, f"验证码发送失败: {response.text}"
        print("验证码发送成功")

    def test_login(self):
        """用户登录并获取token"""
        if not self.phone:
            pytest.skip("用户手机号未设置，跳过登录")

        url = "http://192.168.33.254:28018/api/loan/user/registerAndLogin"
        data = {
            "account": self.phone,
            "captcha": "888888",
            "device": "123EA05C3444F78DABA23A2F77E9B826",
            "loginType": "android",
            "pageResource": ""
        }

        response = requests.post(url, headers=self.headers, json=data)
        assert response.status_code == 200, f"登录失败: {response.text}"

        result = response.json()
        # 假设token在返回结果的result.data.token字段中
        assert 'result' in result and 'data' in result['result'] and 'token' in result['result']['data'], \
            f"登录成功，但未找到token字段: {result}"

        self.token = result['result']['data']['token']
        self.headers['Authorization'] = f"Bearer {self.token}"
        print(f"登录成功，获取到token: {self.token[:20]}...")

    def test_get_user_info(self):
        """获取用户信息"""
        if not self.token:
            pytest.skip("token未设置，跳过获取用户信息")

        url = "http://192.168.33.254:28018/api/common/getYxUser"
        data = {
            "clientIp": "192.168.2.80",
            "appUserId": self.phone,
            "description": "获取商城用户",
            "startTime": int(time.time() * 1000),
            "spendTime": 2,
            "uri": "/api/common/getYxUser",
            "url": "http://192.168.33.254:28018/api/common/getYxUser",
            "method": "GET",
            "ip": "02-42-F9-F9-F7-07",
            "parameter": {"baseDTO": {"userId": self.user_id}} if self.user_id else {}
        }

        response = requests.get(url, headers=self.headers, json=data)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()
        assert 'result' in result and 'data' in result['result'], f"获取用户信息失败: {result}"

        if not self.user_id and 'uid' in result['result']['data']:
            self.user_id = result['result']['data']['uid']
            print(f"获取到用户ID: {self.user_id}")
        print("获取用户信息成功")

    def test_get_credit_info(self):
        """查询用户授信信息"""
        if not self.token:
            pytest.skip("token未设置，跳过查询用户授信信息")

        url = "http://192.168.33.254:28018/api/loan/credit/getLoanUserInfo"

        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200, f"请求失败: {response.text}"

        result = response.json()
        assert 'result' in result and 'data' in result['result'], f"查询用户授信信息失败: {result}"
        print("查询用户授信信息成功")

    def test_query_amount_center(self):
        """查额度中心数据"""
        if not self.token:
            pytest.skip("token未设置，跳过查额度中心数据")

        url = "http://192.168.2.38:28080/amt/query/customerProductAmt"

        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200, f"查额度中心数据失败: {response.text}"
        print("查额度中心数据成功")

    def test_pre_loan_risk_check(self):
        """调风控前筛"""
        if not self.user_id:
            pytest.skip("用户ID未设置，无法进行风控前筛")

        url = f"http://192.168.33.254:28018/api/loan/preLoanLimitCheck?userId={self.user_id}"

        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200, f"调风控前筛失败: {response.text}"
        print("调风控前筛成功")

    def test_get_bank_card_info(self):
        """查核心绑卡信息"""
        if not self.token:
            pytest.skip("token未设置，跳过查核心绑卡信息")

        url = "http://192.168.1.167:8801/bindCardInfo"
        data = {"idCardNo": "420101199502111212"}

        response = requests.post(url, headers=self.headers, json=data)
        assert response.status_code == 200, f"查核心绑卡信息失败: {response.text}"

        result = response.json()
        # 假设返回结果中有bankCardNo字段，可能是列表或单个值
        assert 'bankCardNo' in result, "查核心绑卡信息失败: 未找到bankCardNo字段"

        if isinstance(result['bankCardNo'], list) and len(result['bankCardNo']) > 0:
            self.bank_card_no = result['bankCardNo'][0]
        else:
            self.bank_card_no = result['bankCardNo']
        print(f"查核心绑卡信息成功，获取到银行卡号: {self.bank_card_no[:4]}...{self.bank_card_no[-4:]}")

    def test_get_available_amount(self):
        """查可用额度"""
        if not self.user_id:
            pytest.skip("用户ID未设置，无法查询可用额度")

        url = f"http://192.168.33.254:28018/api/loan/credit/getAvailableAmt?userId={self.user_id}"

        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200, f"查可用额度失败: {response.text}"
        print("查可用额度成功")

    def test_get_fee_rate(self):
        """查费率"""
        if not self.user_id:
            pytest.skip("用户ID未设置，无法查询费率")

        url = "http://192.168.33.254:28018/api/loan/decision/termPrice"
        data = {"userId": str(self.user_id)}

        response = requests.post(url, headers=self.headers, json=data)
        assert response.status_code == 200, f"查费率失败: {response.text}"
        print("查费率成功")

    def test_loan_calculation(self):
        """调试算接口"""
        if not self.token:
            pytest.skip("token未设置，跳过调试算接口")

        url = "http://192.168.1.167:8801/loanTrialCommon"
        data = {
            "irrRate": "36",
            "loanAmt": "1000",
            "repayMethod": "annuity",
            "term": "12"
        }

        response = requests.post(url, headers=self.headers, json=data)
        assert response.status_code == 200, f"调试算接口失败: {response.text}"
        print("调试算接口成功")

    def test_apply_certification(self):
        """申请鉴权"""
        if not all([self.user_id, self.bank_card_no, self.phone]):
            pytest.skip("必要参数缺失，无法进行申请鉴权")

        url = "http://192.168.1.167:8801/applyCertification"
        agreement_time = datetime.now().strftime("%Y%m%d%H%M%S")
        data = {
            "agreementTime": agreement_time,
            "bankCardNo": self.bank_card_no,
            "bankCode": "0004",
            "bindType": "fundsChannel",
            "certificationApplyNo": f"ZYZX_B{agreement_time}90052",
            "idCardNo": "420101197408226217",
            "loanAmt": 1600,
            "registerMobile": self.phone,
            "routerFunds": "FR_ZHEN_XING",
            "scene": "LOAN",
            "userId": f"ZQF{self.user_id}",
            "userMobile": self.phone,
            "userName": username
        }

        response = requests.post(url, headers=self.headers, json=data)
        assert response.status_code == 200, f"申请鉴权失败: {response.text}"
        print("申请鉴权成功")