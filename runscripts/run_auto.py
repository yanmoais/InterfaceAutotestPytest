import logging
import json
import time
from datetime import datetime
import os
import pytest
import sys
from multiprocessing import Process, Event
from common.Update_Database_Result import *
import requests


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        try:
            msg = self.format(record)
            # 确保消息以JSON格式发送
            self.log_queue.put(json.dumps({"message": msg}))
        except Exception as e:
            self.handleError(record)


class TestExecutor:
    def __init__(self):
        self._stop_flag = False

    def stop(self):
        self._stop_flag = True

    def should_stop(self):
        return self._stop_flag


# 创建全局执行器实例
test_executor = TestExecutor()
# 替换为您的钉钉机器人的Webhook URL
DINGTALK_WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=70996a6d738bb7a45cd9bbac13c8ff7d25f38da0edc3ab2e1601621f82b21b0f'


def send_ding(report_dir, event):
    # 等待事件被设置，即等待报告生成完成
    event.wait()
    time.sleep(1)  # 可以根据实际情况调整等待时间

    # 读取Allure报告的结果json文件并构建消息
    summary_json_path = os.path.join(report_dir, 'widgets', 'summary.json')
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
        report_url = f"http://192.168.33.254:7777/{report_dir}/index.html"
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
    response = requests.post(url=DINGTALK_WEBHOOK_URL, json=data, headers=headers)
    print(f"钉钉消息发送结果：{response}")


# 创建全局当前时间
def get_current_time():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def send_ding_report(report_dir, event):
    event.wait()
    time.sleep(3)
    # 创建并启动进程
    p1 = Process(target=send_ding, args=(report_dir, event))
    p1.start()
    p1.join()


def run_test(business_line, funders, regression_date, log_queue):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    report_path_current_time = get_current_time()
    event = Event()

    # 清除现有的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 添加队列处理器
    queue_handler = QueueHandler(log_queue)
    queue_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(queue_handler)

    try:
        # 业务线映射
        business_line_map = {
            'zjly': '资金路由',
            'api': '核心API',
            'tyh': 'TYH'
        }

        # 资方映射
        funder_map = {
            'all': '全资方',
            'jmx': '金美信',
            'xiaomi': '小米',
            'zx': '振兴'
        }

        logger.info(f"开始执行回归测试")
        logger.info(f"业务线: {business_line_map.get(business_line, business_line)}")
        logger.info(f"资方: {', '.join([funder_map.get(f, f) for f in funders])}")
        logger.info(f"回归日期: {regression_date}")

        # 总体通过率计算
        total_success_rate = 0
        executed_files = 0
        # 遍历所有选中的资方，执行对应的测试文件
        total_case_total = 0
        for funder in funders:
            if test_executor.should_stop():
                logger.info("测试执行被手动停止")
                break

            test_file = get_test_file(business_line, funder)
            if test_file:
                logger.info(f"执行测试文件: {test_file}")
                if test_executor.should_stop():
                    break
                success_rate, current_case_total = execute_test_file(test_file, logger, report_path_current_time)
                total_success_rate += success_rate
                total_case_total += current_case_total
                logger.info(f"当前已执行用例总数: {total_case_total}")
                executed_files += 1
            else:
                logger.info(f"未找到资方 {funder_map.get(funder, funder)} 对应的测试文件")

        # 重置停止标志
        test_executor._stop_flag = False

        # 所有测试执行完成后生成报告
        report_path = generate_allure_report(logger, report_path_current_time)

        # 计算平均通过率
        pass_rate = f"{round(total_success_rate / executed_files) if executed_files > 0 else 0}%"

        # 构建测试结果
        result = {
            'businessType': business_line_map.get(business_line, business_line),
            'regressionFunder': ', '.join([funder_map.get(f, f) for f in funders]),
            'regressionDate': regression_date,
            'passRate': pass_rate,
            'reportPath': report_path,
            'totalCaseTotal': total_case_total
        }

        logger.info("回归测试执行完成")
        logger.info(f"测试报告的目录是: {report_path}")
        log_queue.put(json.dumps({"result": result}))
        return result

    except Exception as e:
        logger.error(f"回归测试执行出错: {str(e)}")
        error_result = {
            'businessType': business_line_map.get(business_line, business_line),
            'regressionFunder': ', '.join([funder_map.get(f, f) for f in funders]),
            'regressionDate': regression_date,
            'passRate': '0%',
            'reportPath': '-',
            'totalCaseTotal': '-'
        }
        log_queue.put(json.dumps({"result": error_result}))
        return error_result
    finally:
        logger.info(f"钉钉报告发送进程已启动")
        event.set()
        send_ding_report(report_path, event)


def get_test_file(business_line, funder):
    """根据业务线和资方获取对应的测试文件路径"""
    test_files = {
        ('zjly', 'jmx'): 'testcase/test_zjly/test_JmxLoanRepay.py',
        ('zjly', 'xiaomi'): 'testcase/test_zjly/test_XiaoMiLoanRepay.py',
        ('zjly', 'zx'): 'testcase/test_zjly/test_ZxLoanRepay.py',
        ('api', 'jmx'): 'testcase/test_api_flow/test_JmxLoanRepay_Api_Flow.py',
        # 可以继续添加其他业务线和资方的映射
    }
    return test_files.get((business_line, funder))


class PytestLoggerPlugin:
    """Pytest插件，用于捕获测试日志"""

    def __init__(self, logger):
        self.logger = logger
        self.passed = 0
        self.failed = 0
        self.total = 0

    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            self.total += 1
            if report.passed:
                self.passed += 1
                self.logger.info(f"测试用例通过: {report.nodeid}")
            else:
                self.failed += 1
                self.logger.error(f"测试用例失败: {report.nodeid}")
                if hasattr(report, "longrepr"):
                    self.logger.error(str(report.longrepr))


def execute_test_file(file_path, logger, report_path_current_time):
    """使用pytest执行指定的测试文件"""

    try:
        # 获取文件的绝对路径
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(current_dir, file_path)
        logger.info(f"测试文件路径: {full_path}")
        loggers = logging.getLogger()

        if not os.path.exists(full_path):
            logger.error(f"测试文件不存在: {full_path}")
            return 0

        logger.info(f"开始执行测试文件: {file_path}")

        # 创建pytest插件实例
        plugin = PytestLoggerPlugin(logger)

        # 设置pytest参数
        logger.info(f"当前的时间是: {report_path_current_time}")
        results_dir = os.path.join(current_dir, 'report', 'results', f'report_{report_path_current_time}')
        os.makedirs(results_dir, exist_ok=True)

        pytest_args = [
            full_path,
            '-v',  # 详细输出
            '--tb=short',  # 简短的错误回溯
            '-p', 'no:warnings',  # 禁用警告
            '--alluredir', results_dir  # 指定allure结果输出目录
        ]

        # 执行pytest
        pytest.main(pytest_args, plugins=[plugin])

        # 计算通过率
        if plugin.total > 0:
            success_rate = round((plugin.passed / plugin.total) * 100)
            current_case_total = plugin.total
        else:
            success_rate = 0
        logger.info(f"测试完成 - 总用例数: {plugin.total}, 通过: {plugin.passed}, 失败: {plugin.failed}")
        logger.info(f"测试通过率: {success_rate}%")

        return success_rate, current_case_total

    except Exception as e:
        logger.error(f"执行测试文件时出错: {str(e)}")
        return 0


def generate_allure_report(logger, report_path_current_time):
    """在所有测试执行完成后生成allure报告"""
    try:
        # 使用 os.path.join 确保跨平台兼容性
        logger.info(f"当前的时间是: {report_path_current_time}")
        report_path = os.path.join('report', 'html', f'report_{report_path_current_time}')

        # 获取应用根目录的绝对路径
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_report_path = os.path.join(current_dir, report_path)

        # 确保报告目录存在
        os.makedirs(full_report_path, exist_ok=True)

        # 生成 allure 报告
        results_dir = os.path.join(current_dir, 'report', 'results', f'report_{report_path_current_time}')
        os.system(f'allure generate {results_dir} -o {full_report_path} --clean')

        # 返回相对路径，使用正斜杠确保 URL 正确
        return report_path.replace('\\', '/')

    except Exception as e:
        logger.error(f"生成Allure报告时出错: {str(e)}")
        return None
