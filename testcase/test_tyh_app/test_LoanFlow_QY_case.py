import pytest
import requests
import random
import pymysql
from datetime import datetime
import time
import logging


# ========== 测试数据生成工具 ==========
@pytest.mark.order(10)
def generate_bank_card():
    """生成符合规则的银行卡号"""
    logging.info("开始生成符合规则的银行卡号")
    # 这里只是简单生成19位数字作为示例，实际应用中可能需要更复杂的算法
    bank_card = '621700' + ''.join(str(random.randint(0, 9)) for _ in range(13))
    logging.info(f"生成的银行卡号为: {bank_card}")
    return bank_card


def generate_loan_amount(min_amt=1000, max_amt=2000):
    """生成符合规则的借款金额"""
    logging.info(f"开始生成符合规则的借款金额（{min_amt}-{max_amt}）")
    # 生成1000-2000之间的整数，步长为100
    amount = random.randint(min_amt // 100, max_amt // 100) * 100
    logging.info(f"生成的借款金额为: {amount}")
    return amount


def generate_loan_term():
    """生成符合规则的借款期限"""
    logging.info("开始生成符合规则的借款期限")
    # 生成3-12个月之间的借款期限
    term = random.randint(12, 12)
    logging.info(f"生成的借款期限为: {term}个月")
    return term


# ========== 接口测试基础类 ==========
class LoanWithdrawTestSuite:
    def __init__(self):
        logging.info("初始化额度申请和提现测试套件")
        self.base_url = "http://192.168.33.254:28018"
        self.loan_url = "http://192.168.1.167:8801"
        self.db_config = {
            'host': '192.168.1.192',
            'user': 'tyh_app',
            'password': '03fwnEk8AFcm%PyaPE*k',
            'database': 'tyh_app'
        }
        self.token = None
        self.user_id = None
        self.phone = None
        self.id_card = None
        self.name = None
        self.bank_card = generate_bank_card()
        self.loan_amount = generate_loan_amount()
        self.loan_term = generate_loan_term()
        self.year_rate = None
        self.credit_apply_no = None
        self.headers = {"Content-Type": "application/json"}  # 初始化headers
        self.bank_card_no = None

    def _execute_sql(self, sql):
        """执行数据库操作"""
        logging.info("开始执行数据库操作")
        try:
            conn = pymysql.connect(**self.db_config)
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
            logging.info("数据库操作执行成功")
        except pymysql.Error as e:
            logging.error(f"数据库操作出错: {e}")
        finally:
            if conn:
                conn.close()

    def get_user_info_from_db(self):
        """从数据库获取用户信息"""
        logging.info("开始从数据库获取用户信息")
        try:
            conn = pymysql.connect(**self.db_config)
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM tb_loan_user_info where user_name='宋军强'"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    self.name = result.get('user_name')
                    self.id_card = result.get('id_card_no')
                    self.phone = result.get('mobile')
                    self.user_id = result.get('user_id')

                    logging.info(f"获取到用户信息: 姓名={self.name}, 身份证={self.id_card}, 手机号={self.phone}, 用户ID={self.user_id}")
                    return True
                else:
                    logging.error("未找到用户信息")
                    return False
        except pymysql.Error as e:
            logging.error(f"查询用户信息出错: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def _get_headers(self):
        """获取请求头"""
        if self.token:
            return {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
        return {"Content-Type": "application/json"}

    def step1_send_verify_code(self):
        """发送验证码"""
        logging.info("开始执行发送验证码步骤")
        url = f"{self.base_url}/api/register/verify"
        payload = {
            "phone": self.phone,
            "type": "registerAndLogin"
        }
        try:
            resp = requests.post(url, json=payload, headers=self._get_headers())
            resp.raise_for_status()
            assert resp.json().get('success') is True
            logging.info("发送验证码请求成功")
        except requests.RequestException as e:
            logging.error(f"发送验证码请求出错: {e}")
        except AssertionError:
            logging.error("发送验证码请求失败")

    def step2_login(self):
        """登录获取token"""
        logging.info("开始执行登录获取token步骤")
        url = f"{self.base_url}/api/loan/user/registerAndLogin"
        payload = {
            "account": self.phone,
            "captcha": "888888",
            "device": "123EA05C3444F78DABA23A2F77E9B826",
            "loginType": "android"
        }
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            resp_data = resp.json()
            data = resp_data.get('data', {})
            self.token = data.get('token')
            self.user_id = resp_data.get('userId')
            if not self.token:
                logging.error("未获取到token")
            else:
                logging.info("登录成功，获取到token")
        except requests.RequestException as e:
            logging.error(f"登录请求出错: {e}")

    # def test_get_credit_info(self):
    #     """查询用户信息"""
    #     url = f"{self.base_url}/api/loan/credit/getLoanUserInfo"
    #     response = requests.get(url, headers=self._get_headers())
    #     assert response.status_code == 200, f"查询用户信息失败: {response.text}"
    #
    #     result = response.json()
    #     assert result.get('success') is True, f"查询用户信息失败: {result.get('msg')}"
    #     assert 'data' in result, f"查询用户信息失败: 未找到data字段"
    #
    #     data = result.get('data', {})
    #     # 保存授信额度信息
    #     self.credit_amt = data.get('creditAmt')
    #     self.available_amt = data.get('availableAmt')
    #     self.year_rate = data.get('yearRate')
    #
    #     logging.info(f"查询用户信息成功: 授信额度={self.credit_amt}, 可用额度={self.available_amt}, 年化利率={self.year_rate}")
    #     print("查询用户信息成功")

    def test_query_amount_center(self):
        """查额度中心数据"""

        url = "http://192.168.2.38:28080/amt/query/customerProductAmt"
        response = requests.get(url, headers=self._get_headers())
        assert response.status_code == 200, f"查额度中心数据失败: {response.text}"
        print("查额度中心数据成功")

    def test_pre_loan_risk_check(self):
        """调风控前筛"""
        headers = {"Authorization": f"Bearer {self.token}"}
        
        url = f"{self.base_url}/api/loan/preLoanLimitCheck"
        params = {
            "userId": self.user_id
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            result = response.json()
            
            if not result.get('success'):
                logging.error(f"风控前筛失败: {result.get('msg', '未知错误')}")
                pytest.fail(f"风控前筛失败: {result.get('msg', '未知错误')}")
            
            logging.info("风控前筛成功")
            print("调风控前筛成功")
            
        except requests.RequestException as e:
            logging.error(f"风控前筛请求出错: {str(e)}")
            pytest.fail(f"风控前筛请求失败: {str(e)}")

    def test_get_bank_card_info(self):
        """查核心绑卡信息"""

        headers = {"Authorization": f"Bearer {self.token}"}

        url = "http://192.168.1.167:8801/bindCardInfo"
        data = {"idCardNo": self.id_card}

        response = requests.post(url, headers=headers, json=data)
        assert response.status_code == 200, f"查核心绑卡信息失败: {response.text}"

        result = response.json()
        assert 'bankCardNo' in result, "查核心绑卡信息失败: 未找到bankCardNo字段"

        if isinstance(result['bankCardNo'], list) and len(result['bankCardNo']) > 0:
            self.bank_card_no = result['bankCardNo'][0]
        else:
            self.bank_card_no = result['bankCardNo']
        print(f"查核心绑卡信息成功，获取到银行卡号: {self.bank_card_no[:4]}...{self.bank_card_no[-4:]}")

    def test_get_available_amount(self):
        """查可用额度"""
        url = f"{self.base_url}/api/loan/credit/getAvailableAmt?userId={self.user_id}"
        response = requests.get(url, headers=self._get_headers())
        assert response.status_code == 200, f"查可用额度失败: {response.text}"
        print("查可用额度成功")

    def test_get_fee_rate(self):
        """查费率"""
        headers = {"Authorization": f"Bearer {self.token}"}

        url = f"{self.base_url}/api/loan/decision/termPrice"
        data = {"userId": str(self.user_id)}

        response = requests.post(url, headers=headers, json=data)
        assert response.status_code == 200, f"查费率失败: {response.text}"
        
        result = response.json()
        if result.get('success'):
            self.year_rate = result.get('data', {}).get('yearRate')
            if self.year_rate:
                logging.info(f"获取到年化利率: {self.year_rate}")
            else:
                logging.error("未获取到年化利率")
        print("查费率成功")

    def test_loan_calculation(self):
        """调试算接口"""
        headers = {"Authorization": f"Bearer {self.token}"}
        url = "http://192.168.1.167:8801/loanTrialCommon"
        data = {
            "irrRate": self.year_rate if self.year_rate else "24",
            "loanAmt": str(self.loan_amount),
            "repayMethod": "annuity",
            "term": str(self.loan_term)
        }

        response = requests.post(url, headers=headers, json=data)
        assert response.status_code == 200, f"调试算接口失败: {response.text}"
        print("调试算接口成功")

    def test_apply_certification(self):
        """申请鉴权"""
        headers = {"Authorization": f"Bearer {self.token}"}
        url = "http://192.168.1.167:8801/applyCertification"
        agreement_time = datetime.now().strftime("%Y%m%d%H%M%S")
        data = {
            "agreementTime": agreement_time,
            "bankCardNo": self.bank_card_no,
            "bankCode": "0004",
            "bindType": "fundsChannel",
            "certificationApplyNo": f"ZYZX_B{agreement_time}90052",
            "idCardNo": self.id_card,
            "loanAmt": self.loan_amount,
            "registerMobile": self.phone,
            "routerFunds": "FR_ZHEN_XING",
            "scene": "LOAN",
            "userId": f"ZQF{self.user_id}",
            "userMobile": self.phone,
            "userName": self.name
        }

        response = requests.post(url, headers=headers, json=data)
        assert response.status_code == 200, f"申请鉴权失败: {response.text}"
        print("申请鉴权成功")

    def test_verify_code(self):
        """验证码校验"""
        if not self.user_id:
            pytest.skip("用户ID未设置，无法进行验证码校验")

        url = "http://192.168.1.167:8801/verifyCode"
        data = {
            "bindType": "fundsChannel",
            "cdKey": "BIND1925031081044750336",
            "certificationApplyNo": f"ZYZX_B{datetime.now().strftime('%Y%m%d%H%M%S')}9051409",
            "userId": f"ZQF{self.user_id}",
            "verificationCode": "111111"
        }

        response = requests.post(url, headers=self._get_headers(), json=data)
        assert response.status_code == 200, f"验证码校验失败: {response.text}"
        print("验证码校验成功")

    def test_apply_loan(self):
        """借款申请"""
        headers = {"Authorization": f"Bearer {self.token}"}
        url = "http://192.168.33.254:28018/api/loan/applyLoanNew"
        current_time = int(time.time() * 1000)
        data = {
            "clientIp": "192.168.2.61",
            "appUserId": "",
            "description": "借款申请(新)",
            "startTime": current_time,
            "spendTime": 657,
            "uri": "/api/loan/applyLoanNew",
            "url": "http://tyh-app-h5-sit.ziduom.com/api/loan/applyLoanNew",
            "method": "POST",
            "ip": "02-42-CD-79-99-D4",
            "parameter": {
                "bankCardNo": self.bank_card_no,
                "channelCode": "ZX",
                "ip": "192.168.2.61",
                "loanAmt": self.loan_amount,
                "loanApplyNo": f"ZYZX{datetime.now().strftime('%Y%m%d%H%M%S')}655500",
                "loanChannel": "TYH_APPZY",
                "loanPurpose": "07",
                "loanVipType": 0,
                "periods": self.loan_term,
                "qyCheckFlag": 0,
                "qyFlag": False,
                "qyOrder": "",
                "qyOrderNew": "Pludvo52v/Sx285phG+NPOjUqyQsotfRqbNxh8ZlOwE/smoA/z8ksg7SKYNvNPQ11GOc5QzutIrhZ+8MLtgSqssxXKt0sYYiJNYcRUFSPmngWFsDuKeMBJxZdDpY1WkHy4shwneVNM4Oi+r6KOFR+ftaJE1HUpwVLtwe56WU+wFKFAYjkdN1ceWXvbx39uVqjAsUW0DGhuDp1un4Mi0g/U8ZDht8BtvL2TGssAvaUdo=",
                "qyShowFlag": 1,
                "qyVersion": 1,
                "repayMethod": "01",
                "userId": self.user_id,
                "yearRate": self.year_rate if self.year_rate else "24"  # 使用查询到的年化利率，如果没有则使用默认值
            }
        }

        response = requests.post(url, headers=headers, json=data)
        assert response.status_code == 200, f"借款申请失败: {response.text}"
        print("借款申请成功")



# ========== pytest测试用例 ==========
@pytest.mark.order(2)
def test_loan_withdraw_flow():
    """测试完整的借款提现流程"""
    logging.info("开始执行完整借款流程测试用例")
    
    try:
        # 初始化测试套件
        test_suite = LoanWithdrawTestSuite()
        
        # 0. 获取用户信息
        logging.info("步骤0: 获取用户信息")
        if not test_suite.get_user_info_from_db():
            pytest.skip("获取用户信息失败，跳过测试")
        
        # 1. 发送验证码
        logging.info("步骤1: 发送验证码")
        test_suite.step1_send_verify_code()
        
        # 2. 登录获取token
        logging.info("步骤2: 登录获取token")
        test_suite.step2_login()
        
        # 3. 查询用户授信信息
        # logging.info("步骤3: 查询用户授信信息")
        # test_suite.test_get_credit_info()
        
        # 4. 查询额度中心数据
        logging.info("步骤4: 查询额度中心数据")
        test_suite.test_query_amount_center()
        
        # 5. 风控前筛
        logging.info("步骤5: 执行风控前筛")
        test_suite.test_pre_loan_risk_check()
        
        # 6. 查询核心绑卡信息
        logging.info("步骤6: 查询核心绑卡信息")
        test_suite.test_get_bank_card_info()
        
        # 7. 查询可用额度
        logging.info("步骤7: 查询可用额度")
        test_suite.test_get_available_amount()
        
        # 8. 查询费率
        logging.info("步骤8: 查询费率")
        test_suite.test_get_fee_rate()
        
        # 9. 调试算接口
        logging.info("步骤9: 调试算接口")
        test_suite.test_loan_calculation()
        
        # 10. 申请鉴权
        logging.info("步骤10: 申请鉴权")
        test_suite.test_apply_certification()
        
        # 11. 验证码校验
        logging.info("步骤11: 验证码校验")
        test_suite.test_verify_code()
        
        # 12. 借款申请
        logging.info("步骤12: 借款申请")
        test_suite.test_apply_loan()

        logging.info("完整借款流程测试完成")
        
    except Exception as e:
        logging.error(f"借款流程测试过程中发生错误: {str(e)}")
        pytest.fail(f"借款流程测试失败: {str(e)}")
        raise


# 执行测试并生成报告：pytest --html=report.html
if __name__ == "__main__":
    pytest.main()