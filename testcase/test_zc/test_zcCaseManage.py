import json
from datetime import datetime
from config.testconfig import config,config_cookies
uri = config["test_url_host"]
cookie=config_cookies["cookies"]
headers = {
    "Authorization": config_cookies["Authorization"]
}
config_hearders={
    "cookies":" rememberMe=true; Admin-Expires-In=30; username=admin; os-username=wanglei@te; sidebarStatus=1; SECKEY_ABVK=rfgKMqeIunBW8wtCLN6UW07HVpsjePY4bJ9Rc5ljnwQ%3D; BMAP_SECKEY=MRM1DwwOiO5mRCCD7jpBBYWagWydoQJDX8r2Uhb8lkdnl4QgdXwv1zKGu8gF_FVIgTp08Xy2Z11rwLy-NirTx4VKw1HMzf7bpBQIyDneXNaz7SrUholDRcDkprBRwPc3POfwk9FsIGbUpckkvHhtNx-Jsdg7zqHl7O-Nws0GwlvKxTPpzvF-I6a02rt1eWZC; os-Token=eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxMDAxMjAsInVzZXJfa2V5IjoiZDc5YTQwMGMtNmU2MC00NWJkLWFjZDEtOWRmOGQ0NmVhYTlmIiwidXNlcm5hbWUiOiJ3YW5nbGVpIn0.kAlC8fBvDdK08m_7fSz4I1DDXkRXfZQg3H1SgiBGRW_kqsKZ5E8kDgJYK9YmsRGERkT4vCH4s0G-YORK_-F33A; password=JTvSaQceXp5QTwRZ+pBOSdjCWXjPBroinn5/3YhMsMRqxKNrXG+G4MxcFSdrSLuS8twEeW7pElqyLXetKjLB9A==; Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2tleSI6IjUwYTAwNDgyLTRiNTAtNDJlNC04YTNkLTFmZWMzZTcxODRjOSIsInVzZXJuYW1lIjoiYWRtaW4ifQ.d1UVUihE1QdERb3_zlOSvWTEZTwA2M7_PVPpha0A0aRJPHA4h61MJqCsrYNo1hSfeSt3yQkkF93G2_qGvGOHEQ",
    "Authorization":" Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2tleSI6IjUwYTAwNDgyLTRiNTAtNDJlNC04YTNkLTFmZWMzZTcxODRjOSIsInVzZXJuYW1lIjoiYWRtaW4ifQ.d1UVUihE1QdERb3_zlOSvWTEZTwA2M7_PVPpha0A0aRJPHA4h61MJqCsrYNo1hSfeSt3yQkkF93G2_qGvGOHEQ"
                }



import requests
import allure
import pytest
@allure.feature("资产管理平台")
@allure.story("资产管理功能-资产案件库")
@allure.title("查询案件库中未分配案件")
def test_zc():
    #查询案件库中未分配案件
    url_library_list = uri + "/case/library/list?pageNum=1&pageSize=10&allocateCaseState=%E6%9C%AA%E5%88%86%E9%85%8D&allQuery=false&settleState=%E6%9C%AA%E7%BB%93%E6%B8%85"

    req_library_list = requests.get(url=url_library_list)
    req_prebindCard_q = req_library_list.json()
    print("\n")
    print(json.dumps(req_prebindCard_q, indent=4, sort_keys=True, ensure_ascii=False))

    rows=req_prebindCard_q["rows"]
    caseId01=rows[0]["id"]
    caseId02=rows[1]["id"]
    print(rows[0]["id"])
    return caseId01,caseId02



@allure.feature("资产管理平台")
@allure.story("资产管理功能-资产案件库")
@allure.title("分配案件到案件池")
def test_zc_fp():
    #分配案件到案件池
    url_assignToCaseManage = uri + "/case/library/assignToCaseManage"
    data_assignToCaseManage={"caseIds": [test_zc()[0],test_zc()[1]]}

    req_assignToCaseManage = requests.post(url=url_assignToCaseManage,json=data_assignToCaseManage)
    req_assignToCaseManage_rq = req_assignToCaseManage.json()
    print("\n")
    print(json.dumps(req_assignToCaseManage_rq, indent=4, sort_keys=True, ensure_ascii=False))


@allure.title("查询当前启用标签")
@allure.feature("资产管理平台")
@allure.story("资产管理功能-委托案件池")
def test_getLabels():
    url_getLabels = uri + "/case/start/getLabels"
    data_getLabels = {}

    req_getLabels = requests.get(url=url_getLabels, json=data_getLabels)
    req_getLabels_rq = req_getLabels.json()
    print("\n")
    print(json.dumps(req_getLabels_rq, indent=4, sort_keys=True, ensure_ascii=False))
    data_getLabels_req=req_getLabels_rq["data"]
    print(data_getLabels_req[0]["id"])
    return data_getLabels_req[0]["id"]



@allure.title("新增标签")
@allure.feature("资产管理平台")
@allure.story("资产管理功能-委托案件池")
def test_addCaseLabel():
    #查询委托案件池中数据
    url_check=uri + "/case/manage/list?pageNum=1&pageSize=10&batchNum=&allQuery=false&settleState=0"
    req_check=requests.get(url_check)
    req_check_rq=req_check.json()
    caseId=req_check_rq["rows"][0]["caseId"]
    print(caseId)
    #给查询出来的案件新增标签
    url_addCaseLabel = uri + "/case/manage/addCaseLabel"
    data_addCaseLabel ={
    "caseIds": [
        caseId
            ],
    "labels": [
        {
            "beginDate": "2024-06-06T16:00:00.000Z",
            "endDate": "2024-06-06T16:00:00.000Z",
            "labelId": test_getLabels()
        }
    ]
}

    req_addCaseLabel = requests.post(url=url_addCaseLabel, json=data_addCaseLabel)
    req_addCaseLabel_rq = req_addCaseLabel.json()
    print("\n")
    print(json.dumps(req_addCaseLabel_rq, indent=4, sort_keys=True, ensure_ascii=False))
    assert   req_addCaseLabel_rq["code"]==200
    return caseId


@allure.title("修改标签")
@allure.feature("资产管理平台")
@allure.story("资产管理功能-委托案件池")
def test_setCaseLabel():
    url_setCaseLabel=uri+"/case/manage/setCaseLabel"
    data_setCaseLabel={
    "caseIds": [
        test_addCaseLabel()
    ],
    "labels": [
        {
            "beginDate": "2024-06-18T16:00:00.000Z",
            "endDate": "2024-06-18T16:00:00.000Z",
            "labelId": "24"
        }
    ]
}
    req_setCaseLabel=requests.post(url=url_setCaseLabel, json=data_setCaseLabel)
    req_setCaseLabel_rq = req_setCaseLabel.json()
    print(json.dumps(req_setCaseLabel_rq, indent=4, sort_keys=True, ensure_ascii=False))
    assert   req_setCaseLabel_rq["code"]==200

    # 修改后标签是否修改成功
    url_check_case=uri+"/case/manage/list?pageNum=1&pageSize=10&caseId=%s&batchNum=&allQuery=false&settleState=0"%test_addCaseLabel()
    req_check_case = requests.get(url=url_check_case)
    req_check_case_rq=req_check_case.json()
    assert req_check_case_rq["rows"][0]["labels"][0]["labelId"] == 24



@allure.feature("资产管理平台")
@allure.story("资产管理功能-委托案件池")
@allure.title("快速分案")
def test_fastAllocation():
    #委托案件池中查询未分配案件
    url_check_case=uri+"/case/manage/list?pageNum=1&pageSize=10&allocatedStateStr=0&batchNum=&allQuery=false&settleState=0"
    req_check_case = requests.get(url=url_check_case,headers=headers)
    req_check_case_rq=req_check_case.json()
    #获取未分配案件id
    caseid=req_check_case_rq["rows"][0]["caseId"]
    print(caseid)

    #查询分案委案批次号
    '''
    获取系统当前时间，输出格式为年月日时分秒
    '''
    # 获取当前系统时间
    now = datetime.now()
    # 转换为没有分隔符的年月日时分秒的字符串格式
    formatted_time = now.strftime("%Y%m%d%H%M%S")
    #拼接生成委案批次号
    entrustingCaseBatchNum=str(76)+formatted_time
    print(entrustingCaseBatchNum)
#     url_previewAllocationResults=uri+"/case/manage/previewAllocationResults"
#     data_previewAllocationResults={
#     "caseIds": [
#         28342
#     ],
#     "allocationMode": 1,
#     "bringDiary": "false",
#     "aiDringDiary": "true",
#     "allocationTeamList": [
#         {
#             "id": "temd:76",
#             "label": "鹏姚",
#             "unifiedCode": "null",
#             "children": "null",
#             "caseNum": 1,
#             "teamName": "鹏姚",
#             "entrustingCaseBatchNum": entrustingCaseBatchNum,
#             "targetBackMoney": "80",
#             "teamId": "76",
#             "sort": 1
#         }
#     ],
#     "jointDebt": "false",
#     "intervalMonth": "false"
# }

    #进行快速分案
    url_fastAllocation=uri+"/case/manage/fastAllocation"
    data_fastAllocation={
    "caseIds": [
        caseid
    ],
    "allocationMode": 1,
    "bringDiary": "false",
    "aiDringDiary": "true",
    "allocationTeamList": [
        {
            "id": "temd:76",
            "label": "鹏姚",
            "unifiedCode": "null",
            "children": "null",
            "caseNum": 1,
            "teamName": "鹏姚",
            "entrustingCaseBatchNum": entrustingCaseBatchNum,
            "targetBackMoney": "80",
            "teamId": "76",
            "sort": 1
        }
    ],
    "jointDebt": "false",
    "intervalMonth": "false"
}
    req_fastAllocation=requests.post(url=url_fastAllocation,json=data_fastAllocation)
    req_fastAllocation_rq=req_fastAllocation.json()
    print(json.dumps(req_fastAllocation_rq, indent=4, sort_keys=True, ensure_ascii=False))
    assert req_fastAllocation_rq["code"]==200
    return entrustingCaseBatchNum




@allure.title("案件审核通过")
@allure.feature("资产管理平台")
@allure.story("资产管理功能-案件审核")
def test_pass():
    with allure.step("查询委案待审核数据"):
    #查询委案待审核数据
        url_allocated=uri+"/approve/allocated/list?pageNum=1&pageSize=10&allQuery=false&approveState=2"
        req_allocated=requests.get(url=url_allocated,headers=headers)
        req_allocated_rq=req_allocated.json()
    # response_data=json.dumps(req_allocated_rq, indent=4, sort_keys=True, ensure_ascii=False)
    with allure.step("判断是否有待审核数据"):
        if len(req_allocated_rq["rows"])>0:
            id=req_allocated_rq["rows"][0]["id"]
            print(id)
        else:
            print("暂无数据")




    # # 假设这是你从接口获取的JSON字符串
    # # 解析JSON字符串为Python字典
    # response_data=json.dumps(req_allocated_rq, indent=4, sort_keys=True, ensure_ascii=False)
    # print(response_data)
    # response_data01 = json.loads(response_data)
    #
    # # 遍历rows列表查找匹配的entrustingBatchNum
    # found = False
    # matching_id = None
    # # 遍历rows列表中的每个字典项
    # for row in response_data01.get('rows', []):
    #     # 检查entrustingBatchNum键是否存在且值是否匹配
    #     if 'entrustingBatchNum' in row and row['entrustingBatchNum'] == test_fastAllocation():
    #         # 如果找到匹配的项，获取其id值
    #         id_value = row['id']
    #         print(f"找到了匹配的entrustingBatchNum，其对应的id值为：{id_value}")
    #         break  # 找到后退出循环
    # else:
    #     # 如果循环结束仍未找到匹配的项，则打印消息
    #     print("没有找到匹配的entrustingBatchNum")



    with allure.step("开始审核委案案件"):
        url_pass=uri+"/approve/allocated/pass"
        data_pass={
        "queryParam": {
            "allQuery": "false"
        },
        "ids": [
            id
        ]
    }
        req_pass=requests.post(url=url_pass,json=data_pass,headers=headers)
        req_pass_rq = req_pass.json()
        print(json.dumps(req_pass_rq, indent=4, sort_keys=True, ensure_ascii=False))
        assert req_pass_rq["code"] == 200
    code_snippet = """13222"""

    allure.attach(code_snippet,name="Square function code", attachment_type=allure.attachment_type.TEXT)



@allure.title("回收案件")
def test_zc_fp02():
    #分配案件到案件池
    pass


@allure.title("退案")
def test_zc_fp03():
    #分配案件到案件池
    pass


@allure.title("留案")
def test_zc_fp04():
    #分配案件到案件池
    pass






# if __name__ == '__main__':
#     # pytest.main(["-s","allure-test.py"])
#     '''
#     -q: 安静模式, 不输出环境信息
#     -v: 丰富信息模式, 输出更详细的用例执行信息
#     -s: 显示程序中的print/logging输出
#     '''
#     pytest.main(['-s', '-q','testProgrammes.py','--clean-alluredir','--alluredir=allure-results'])
#     os.system(r"allure generate -c -o allure-report")
