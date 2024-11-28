import random
import os

config = {
    # "test_zjly_host": "http://test-hx.zhonglishuke.com:8080/g1",
    "test_zjly_host": "http://192.168.1.187:8088",
    "test_zfpt_host": "http://192.168.1.187:8199",
    "test_api_host": "http://192.168.1.167:8801",
    "test_tyh_hy_host": "http://192.168.1.168:6801/api/1.0",
    "test_tyh_hy_end_host": "http://192.168.1.168:6803",
    "test_api_end_host": "http://192.168.1.167:8804",
    "risk_host": "http://120.77.248.212:9090"
}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 测试文件路径列表（请根据实际情况修改）
test_files = [
    f"{BASE_DIR}/testcase/test_zjly/test_JmxLoanRepay.py",
    f"{BASE_DIR}/testcase/test_zjly/test_ZyLoanRepay.py",
    f"{BASE_DIR}/testcase/test_zjly/test_NewCYLoanRepay.py",
    f"{BASE_DIR}/testcase/test_zjly/test_ZxLoanRepay.py",
    f"{BASE_DIR}/testcase/test_zjly/test_HaiXiaLoanRepay.py",
    f"{BASE_DIR}/testcase/test_zjly/test_MengShangLoanRepay.py",
    f"{BASE_DIR}/testcase/test_zjly/test_RunLouLoanRepay.py"
]

channel_codes = {"APPZY", "RP"}

config_cookies = {
    "cookies": " rememberMe=true; Admin-Expires-In=30; username=admin; os-username=wanglei@te; sidebarStatus=1; SECKEY_ABVK=rfgKMqeIunBW8wtCLN6UW07HVpsjePY4bJ9Rc5ljnwQ%3D; BMAP_SECKEY=MRM1DwwOiO5mRCCD7jpBBYWagWydoQJDX8r2Uhb8lkdnl4QgdXwv1zKGu8gF_FVIgTp08Xy2Z11rwLy-NirTx4VKw1HMzf7bpBQIyDneXNaz7SrUholDRcDkprBRwPc3POfwk9FsIGbUpckkvHhtNx-Jsdg7zqHl7O-Nws0GwlvKxTPpzvF-I6a02rt1eWZC; os-Token=eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxMDAxMjAsInVzZXJfa2V5IjoiZDc5YTQwMGMtNmU2MC00NWJkLWFjZDEtOWRmOGQ0NmVhYTlmIiwidXNlcm5hbWUiOiJ3YW5nbGVpIn0.kAlC8fBvDdK08m_7fSz4I1DDXkRXfZQg3H1SgiBGRW_kqsKZ5E8kDgJYK9YmsRGERkT4vCH4s0G-YORK_-F33A; password=JTvSaQceXp5QTwRZ+pBOSdjCWXjPBroinn5/3YhMsMRqxKNrXG+G4MxcFSdrSLuS8twEeW7pElqyLXetKjLB9A==; Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2tleSI6IjUwYTAwNDgyLTRiNTAtNDJlNC04YTNkLTFmZWMzZTcxODRjOSIsInVzZXJuYW1lIjoiYWRtaW4ifQ.d1UVUihE1QdERb3_zlOSvWTEZTwA2M7_PVPpha0A0aRJPHA4h61MJqCsrYNo1hSfeSt3yQkkF93G2_qGvGOHEQ",
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2tleSI6IjQ4MjJkYTgzLTRjZDgtNDc2MC05NmU1LWNkMGNjZGNhNWU3OSIsInVzZXJuYW1lIjoiYWRtaW4ifQ.WyNXwfhzq0PWD_Q_E73jUWk6FP8wGubyfcm2g5aNm11KZtWbyoUuGD46q89vekintH_WzZXFRDWJVriwNB-pHA"
}

if __name__ == '__main__':
    print(BASE_DIR)

# http://192.168.1.237:8083/doc.html#/default/%E5%B9%BF%E5%B7%9E%E6%8E%A5%E5%8F%A3/compensationApplyUsingPOST
