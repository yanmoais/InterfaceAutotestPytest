"""
    测试环境参数配置项
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_YAML_PATH = BASE_DIR + os.sep + "Config" + os.sep + "database_config.yaml"
CASE_FILE_PATH = BASE_DIR + os.sep + "Test_Data" + os.sep + "test_file.xlsx"
SHEET_NAME_PATH = "Sheet1"
XXL_JOB_USERNMAE = 'admin'
XXL_JOB_PASSWORD = '123456'
XXL_JOB_HOST = 'http://192.168.1.167:8080/'


if __name__ == '__main__':
    print(BASE_DIR)
    print(DB_YAML_PATH)
    print(CASE_FILE_PATH)
