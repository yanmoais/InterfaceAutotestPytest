import pytest
import requests
import random
import pymysql
from datetime import datetime
import time
import logging


# from util_tools.logger import Logger

# 配置日志

# ========== 测试数据生成工具 ==========
@pytest.mark.order(10)
def generate_phone():
    """生成符合规则的手机号"""
    logging.info("开始生成符合规则的手机号")
    prefixes = ['138', '139', '136', '188']
    phone = random.choice(prefixes) + ''.join(str(random.randint(0, 9)) for _ in range(8))
    #
    logging.info(f"生成的手机号为: {phone}")
    return phone


def generate_id_number():
    """生成符合校验规则的身份证号（1980-1995出生）[6,7,8](@ref)"""
    logging.info("开始生成符合校验规则的身份证号（1980 - 1995出生）")
    # 前6位行政区划码（示例使用河南省焦作市沁阳市）
    area_code = '410882'
    # 生成1980-1995年的出生日期
    birth_date = f"19{random.randint(80, 95)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}"
    # 顺序码（3位）
    sequence = f"{random.randint(0, 999):03d}"
    # 前17位组合
    base_number = area_code + birth_date + sequence

    # 计算校验码[6](@ref)
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_code_map = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}

    total = sum(int(n) * w for n, w in zip(base_number, weight))
    check_code = check_code_map[total % 11]
    id_number = base_number + check_code
    #
    logging.info(f"生成的身份证号为: {id_number}")
    return id_number


# ========== 接口测试基础类 ==========
class CreditTestSuite:
    def __init__(self):
        logging.info("初始化测试套件")
        self.base_url = "http://192.168.33.254:28018"
        self.encrypt_url = "http://192.168.1.101:8290/test/encrypt"
        self.db_config = {
            'host': '192.168.1.192',
            'user': 'tyh_app',
            'password': '03fwnEk8AFcm%PyaPE*k',
            'database': 'tyh_app'
        }
        self.token = None
        self.user_id = None
        self.phone = generate_phone()
        self.id_card = generate_id_number()
        self.name = "龚勋"

    def _request_encrypt(self, data):
        """处理加密接口调用[8](@ref)"""

        logging.info("开始处理加密接口调用")
        try:
            resp = requests.post(self.encrypt_url, json=data)
            resp.raise_for_status()
            result = resp.json().get('data')
            logging.info("加密接口调用成功")
            return result
        except requests.RequestException as e:
            logging.error(f"加密接口调用出错: {e}")
            return None

    def _execute_sql(self, sql):
        """执行数据库操作[5](@ref)"""

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

    def _query_credit_status(self):
        """查询授信结果"""
        logging.info("开始查询授信结果")
        try:
            conn = pymysql.connect(**self.db_config)
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = f"SELECT * FROM tb_loan_apply_credit WHERE user_id = {self.user_id}"
                cursor.execute(sql)
                result = cursor.fetchone()
                status = result.get('status') if result else None
                logging.info(f"查询到的授信状态为: {status}")
                return status
        except pymysql.Error as e:
            logging.error(f"查询授信结果出错: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def _wait_for_credit_result(self):
        """等待授信结果"""
        logging.info("开始等待授信结果")
        max_wait_time = 5 * 60
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > max_wait_time:
                logging.warning("5分钟后无结果，请人工查询。")
                break
            status = self._query_credit_status()
            if status == 'S':
                logging.info("授信通过")
                break
            elif status == 'F':
                logging.info("授信拒绝")
                break
            elif status == 'U':
                logging.info("掉单")
                break
            elif status in ['P', 'PP']:
                logging.info("等待中，1分钟后继续查询...")
                time.sleep(60)
            else:
                logging.info("未知状态，等待中...")
                time.sleep(60)

    # ========== 测试步骤实现 ==========

    def step1_send_verify_code(self):
        """发送验证码"""

        logging.info("开始执行发送验证码步骤")
        url = f"{self.base_url}/api/register/verify"
        payload = {
            "phone": self.phone,
            "type": "registerAndLogin"
        }
        try:
            resp = requests.post(url, json=payload)
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

    def step7_credit_flow(self):

        """授信流程主逻辑"""
        logging.info("开始执行授信流程主逻辑")
        if not self.token:
            logging.error("未获取到token，无法执行授信流程")
            return

        # 新增：获取用户个人信息
        get_user_url = f"{self.base_url}/api/common/getYxUser"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            user_resp = requests.get(get_user_url, headers=headers)
            user_resp.raise_for_status()
            user_resp_data = user_resp.json()
            if user_resp_data.get('result', {}).get('success'):
                logging.info("获取用户个人信息成功")
                self.user_id = user_resp_data.get('result', {}).get('data', {}).get('uid')
            else:
                logging.error("获取用户个人信息失败")
        except requests.RequestException as e:
            logging.error(f"获取用户个人信息请求出错: {e}")



        # 调用 /api/loan/credit/idCard/OCR 接口（正面）
        ocr_front_url = f"{self.base_url}/api/loan/credit/idCard/OCR"
        headers = {"Authorization": f"Bearer {self.token}"}
        ocr_front_payload = {
            "cardType": "front",
            "url": "https://tyhshopb2c.oss-cn-shenzhen.aliyuncs.com/null20250317/vd3drvuttw2li9eubt04yjw8zpmlbe2o.jpg"
        }
        try:
            logging.info(f"身份证正面OCR识别请求体: {ocr_front_payload}")
            ocr_front_resp = requests.post(ocr_front_url, headers=headers, json=ocr_front_payload)
            ocr_front_resp.raise_for_status()
            ocr_front_data = ocr_front_resp.json().get('data', {})
            self.id_card = ocr_front_data.get('idCardNo', self.id_card)
            self.name = ocr_front_data.get('userName', self.name)
            logging.info("身份证正面OCR识别成功")
        except requests.RequestException as e:
            logging.error(f"身份证正面OCR识别请求出错: {e}")
            return

        # 调用 /api/loan/credit/idCard/OCR 接口（背面）
        ocr_back_url = f"{self.base_url}/api/loan/credit/idCard/OCR"
        headers = {"Authorization": f"Bearer {self.token}"}
        ocr_back_payload = {
            "cardType": "back",
            "url": "https://tyhshopb2c.oss-cn-shenzhen.aliyuncs.com/null20250317/cw8jbvg16l30wbej9dcty69urjhu5ikw.png"
        }
        try:
            logging.info(f"身份证背面OCR识别请求体: {ocr_back_payload}")
            ocr_back_resp = requests.post(ocr_back_url, headers=headers, json=ocr_back_payload)
            ocr_back_resp.raise_for_status()
            logging.info("身份证背面OCR识别成功")
        except requests.RequestException as e:
            logging.error(f"身份证背面OCR识别请求出错: {e}")
            return

        # 执行后续接口调用（示例）
        save_idcard_url = f"{self.base_url}/api/loan/credit/saveIdCardInfo"
        headers = {"Authorization": f"Bearer {self.token}"}
        idcard_payload = {"userName": self.name, "idCardNo": self.id_card,
                          "address": "广东省广州市越秀区东风东路858号", "beginTime": "20141201", "dueTime": "20341201",
                          "ethnic": "汉", "gender": "M", "issueOrg": "广州市越秀区公安局",
                          "frontUrl": "https://tyhshopb2c.oss-cn-shenzhen.aliyuncs.com/null20250317/vd3drvuttw2li9eubt04yjw8zpmlbe2o.jpg",
                          "backUrl": "https://tyhshopb2c.oss-cn-shenzhen.aliyuncs.com/null20250317/cw8jbvg16l30wbej9dcty69urjhu5ikw.png"}
        try:
            logging.info(f"保存身份证信息请求体: {idcard_payload}")
            resp = requests.post(save_idcard_url, headers=headers, json=idcard_payload)
            resp.raise_for_status()
            logging.info("保存身份证信息请求成功")
        except requests.RequestException as e:
            logging.error(f"保存身份证信息请求出错: {e}")

        # 执行数据库跳过人脸验证
        self._execute_sql(
            f"UPDATE tb_loan_user_info SET state = CONCAT(state, ',5'),assay_type='TENCENT',assay_time='2025-02-23 14:03:44',face_url='https://tyhshopb2c.oss-cn-shenzhen.aliyuncs.com/app/face_auth/430923199512122015_1740386543524.jpg' WHERE mobile = '{self.phone}'")

        # 7.4.2 保存用户基本信息
        save_base_url = f"{self.base_url}/api/loan/credit/saveBaseUserInfo"
        base_info_payload = {"addrDetail": "北京市东城区1号", "alipay": "", "applyAmount": 10000, "city": "110100",
                             "cityName": "北京市", "companyName": "", "companyPhone": "", "district": "110101",
                             "districtName": "东城区", "education": "20", "job": "3", "marriage": "20",
                             "monthlyIncome": 0, "province": "110000", "provinceName": "北京", "wechatId": "",
                             "companyAddressDetail": ""}
        try:
            logging.info(f"保存用户基本信息请求体: {base_info_payload}")
            requests.post(save_base_url, headers=headers, json=base_info_payload)
            logging.info("保存用户基本信息请求发送成功")
        except requests.RequestException as e:
            logging.error(f"保存用户基本信息请求出错: {e}")

        # 7.4.3 保存联系人信息
        save_linkman_url = f"{self.base_url}/api/loan/credit/saveLinkmanInfo"
        linkman_payload = {
            "clientIp": "192.168.2.80",
            "linkmanInfos": [
                {"name": "黄正", "phone": "15611395281", "relationship": "60"},
                {"name": "张添柱", "phone": "13017295446", "relationship": "50"}
            ],
            "userId": self.user_id

        }
        try:
            logging.info(f"保存联系人信息请求体: {linkman_payload}")
            requests.post(save_linkman_url, headers=headers, json=linkman_payload)
            logging.info("保存联系人信息请求发送成功")
        except requests.RequestException as e:
            logging.error(f"保存联系人信息请求出错: {e}")

        # 7.4.4 手机号风控加白
        risk_white_url = "http://120.77.248.212:9090/drms/risk_management/white/add"
        white_payload = {
            "data": [self.phone]
        }
        try:
            logging.info(f"手机号风控加白请求体: {white_payload}")
            requests.post(risk_white_url, headers=headers, json=white_payload)
            logging.info("手机号风控加白请求发送成功")
        except requests.RequestException as e:
            logging.error(f"手机号风控加白请求出错: {e}")

        # 7.4.5 发起授信请求
        credit_url = f"{self.base_url}/api/loan/applyCredit"
        credit_payload = {
            "clientIp": "192.168.2.80",
            "osDetail": "android天源花test",
            "tdBlackBox": f"KGPHb{int(datetime.now().timestamp() * 1000)}LJuuECZp9v5",
            "userId": self.user_id

        }
        try:
            logging.info(f"发起授信请求请求体: {credit_payload}")
            credit_resp = requests.post(credit_url, headers=headers, json=credit_payload)
            credit_resp.raise_for_status()
            resp_data = credit_resp.json()
            assert resp_data.get('success') is True
            assert 'creditApplyNo' in resp_data.get('data', {})
            logging.info("发起授信请求成功")
            # 发起授信请求成功后，查询授信结果
            self._wait_for_credit_result()
        except requests.RequestException as e:
            logging.error(f"发起授信请求出错: {e}")
        except AssertionError:
            logging.error("发起授信请求失败")

    def _query_credit_status(self):
        """查询授信结果"""
        logging.info("开始查询授信结果")
        if not self.user_id or not self.credit_apply_no:
            logging.error("用户ID或授信申请号未设置，无法查询授信结果")
            return None

        url = f"{self.base_url}/api/loan/query/applyCreditResult"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        payload = {
            "userId": self.user_id,
            "creditApplyNo": self.credit_apply_no
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            if result.get('success'):
                status = result.get('data', {}).get('applyCreditStatus')
                logging.info(f"查询到的授信状态为: {status}")
                return status
            else:
                logging.error(f"查询授信结果失败: {result.get('message')}")
                return None
        except requests.RequestException as e:
            logging.error(f"查询授信结果请求出错: {e}")
            return None

    def _wait_for_credit_result(self):
        """等待授信结果"""
        logging.info("开始等待授信结果")
        max_wait_time = 5 * 60  # 5分钟超时
        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > max_wait_time:
                logging.warning("5分钟后无结果，请人工查询")
                break

            status = self._query_credit_status()
            if status == 'S':
                logging.info("授信成功")
                return True
            elif status == 'F':
                logging.error("申请失败")
                return False
            elif status == 'R':
                logging.error("授信拒绝")
                return False
            elif status == 'P':
                logging.info("处理中，1分钟后继续查询...")
                time.sleep(60)
            elif status == 'U':
                logging.error("该申请号不存在（掉单）")
                return False
            else:
                logging.info("未知状态，等待中...")
                time.sleep(60)
# ========== pytest测试用例 ==========
@pytest.mark.order(1)
def test_full_credit_flow():
    #
    logging.info("开始执行完整授信流程测试用例")
    test_suite = CreditTestSuite()

    # 执行测试步骤链
    test_suite.step1_send_verify_code()
    test_suite.step2_login()
    # test_suite.step3_get_customer_info()
    test_suite.step7_credit_flow()
    test_suite._query_credit_status()
    test_suite._wait_for_credit_result()


    # 查询用户信息判断是否需要授信
    if test_suite.token:
        query_url = f"{test_suite.base_url}/api/loan/credit/getLoanUserInfo"
        headers = {"Authorization": f"Bearer {test_suite.token}"}
        try:
            logging.info("开始查询用户信息判断是否需要授信")
            resp = requests.get(query_url, headers=headers)
            resp.raise_for_status()
            if 'creditAmt' not in resp.json():
                logging.info("用户信息中无授信额度，再次执行授信流程")
                test_suite.step7_credit_flow()
            else:
                logging.info("用户信息中已有授信额度，无需再次执行授信流程")
        except requests.RequestException as e:
            logging.error(f"查询用户信息请求出错: {e}")


# 执行测试并生成报告：pytest --html=report.html
if __name__ == "__main__":
    pytest.main()
