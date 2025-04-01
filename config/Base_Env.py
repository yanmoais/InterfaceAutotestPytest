"""
    测试环境参数配置项
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_YAML_PATH = BASE_DIR + os.sep + "config" + os.sep + "database_config.yaml"
RISK_PHONE_PATH = BASE_DIR + os.sep + "testdata" + os.sep + "risk_phone" + os.sep + "user_phone.txt"
CASE_FILE_PATH = BASE_DIR + os.sep + "testdata" + os.sep + "test_case_excel" + os.sep + "excle_repayment_plan.xlsx"
SHEET_NAME_PATH = "Sheet_12"
XXL_JOB_USERNMAE = 'admin'
XXL_JOB_PASSWORD = '123456'
XXL_JOB_SIT_LLH_USERNMAE = 'admin'
XXL_JOB_SIT_LLH_PASSWORD = 'xVT5dVhWo9y7K$Hm'
XXL_JOB_HOST_CORE_API = 'http://192.168.1.187:8080/'
XXL_JOB_HOST_FLOW_API = 'http://192.168.1.167:8080/'
XXL_JBO_HOST_SIT_LLH = 'https://xxl-job-sit.zhonglishuke.com/'
PHOTO_PATH = BASE_DIR + "/testdata/photo_data/image/"


if __name__ == '__main__':
    print(CASE_FILE_PATH)
