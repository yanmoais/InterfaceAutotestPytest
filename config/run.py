import os
import json
from common.Base_API import Base_Api
from multiprocessing import Process, Event
import time
from config.testconfig import BASE_DIR

# 替换为您的钉钉机器人的Webhook URL
DINGTALK_WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=4e2f50c867fd6781742498e58c0174c36c4240ba372c6c699d1ede1cc06da2c5'

ALLURE_SERVE_PORT = 63342


def allure_report(test_files, report_dir, event):
    # 构建并执行pytest命令（请根据实际情况安装pytest和allure-pytest插件）
    test_file_args = ' '.join([f'"{file}"' for file in test_files])
    os.system(f'pytest {test_file_args} --alluredir {report_dir}/result')

    # 生成Allure报告
    os.system(f'allure generate {report_dir}/result/ -o {report_dir}/html --clean')
    time.sleep(2)

    # 报告生成完成后，设置事件
    event.set()


def send_ding(report_dir, event):
    # 等待事件被设置，即等待报告生成完成
    event.wait()
    time.sleep(1)  # 可以根据实际情况调整等待时间

    # 读取Allure报告的结果json文件并构建消息
    summary_json_path = os.path.join(report_dir, 'html', 'widgets', 'summary.json')
    try:
        with open(summary_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 提取测试用例统计信息
        statistic = data.get('statistic')
        if statistic:
            case_all = statistic.get('total', 0)
            case_fail = statistic.get('failed', 0)
            case_pass = statistic.get('passed', 0)
            case_broken = statistic.get('broken', 0)
            case_unknown = statistic.get('unknown', 0)

            case_rate = round((case_pass / case_all) * 100, 2) if case_all > 0 else 0
        else:
            case_all = case_fail = case_pass = 0
            case_rate = 0

            # 构建钉钉消息内容
        report_url = f"http://192.168.3.88:{ALLURE_SERVE_PORT}/index.html"

        text = f"测试用例执行情况:\n" \
               f"通过率：{case_rate}%\n" \
               f"执行用例数：{case_all}个\n" \
               f"成功用例数：{case_pass}个\n" \
               f"失败用例数：{case_fail}个\n" \
               f"故障用例数：{case_broken}个\n" \
               f"未知用例数：{case_unknown}个\n" \
               f"测试报告地址：{report_url}\n" \
            # 发送钉钉消息
        send_to_dingtalk(text)
    except FileNotFoundError:
        print("报告文件未找到，无法发送钉钉消息。")


def send_to_dingtalk(text):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": text
        }
    }
    response = Base_Api().post_dingk(DINGTALK_WEBHOOK_URL, data, headers)
    print(f"钉钉消息发送结果：{response.json}")


if __name__ == '__main__':
    # 测试文件路径列表（请根据实际情况修改）
    test_files = [
        # f"{BASE_DIR}/testcase/test_zjly/test_JmxLoanRepay.py",
        f"{BASE_DIR}/testcase/test_zjly/test_ZyLoanRepay.py",
        f"{BASE_DIR}/testcase/test_zjly/test_NewCYLoanRepay.py",
        f"{BASE_DIR}/testcase/test_zjly/test_ZxLoanRepay.py"
        # f"{BASE_DIR}/testcase/test_zjly/test_HaiXiaLoanRepay.py"
    ]

    report_dir = f"{BASE_DIR}/report/result"

    event = Event()

    # 创建并启动进程
    p1 = Process(target=allure_report, args=(test_files, report_dir, event))
    p2 = Process(target=send_ding, args=(report_dir, event))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    # 在本地启动一个Web服务器以查看Allure报告（可选）
    # 注意：这需要在本地机器上安装Allure命令行工具
    # os.system(f'allure serve {report_dir}/result')

    os.system(f'allure serve -h 192.168.3.88 -p {ALLURE_SERVE_PORT} {report_dir}/result')
