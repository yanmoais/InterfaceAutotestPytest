import subprocess
import sys
import threading
import queue
import logging
import json
import os
from datetime import datetime
import signal


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        try:
            msg = self.format(record)
            self.log_queue.put(msg)
        except Exception:
            self.handleError(record)


def run_test(channel, log_queue, testType):
    try:
        # 配置日志处理
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        queue_handler = QueueHandler(log_queue)
        queue_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(queue_handler)

        # 设置环境变量传递参数
        os.environ['TEST_CHANNEL'] = channel
        os.environ['TEST_TYPE'] = testType
        logger.info(f"当前渠道: {channel}")
        logger.info(f"当前选择的测试类型: {testType}")
        log_queue.put(f"开始执行金美信测试，功能：{testType}")

        test_file_path = r"./testcase/test_api_flow/test_JmxLoanRepay_Api_Flow.py"
        if testType == "credit":
            test_functions = r"test_jmx_credit_success_api_flow"
        elif testType == "loan":
            test_functions = r"test_jmx_loan_success_api_flow"
        print(test_file_path)
        # 执行pytest测试
        pytest_args = [
            "pytest",
            f"{test_file_path}::{test_functions}",
            "-v",
            "-p", "no:warnings",
            "--capture=no"
        ]

        process = subprocess.Popen(
            pytest_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        test_result = None

        for line in process.stdout:
            line = line.strip()
            if line:
                log_queue.put(line)
                # 检查是否包含测试结果数据
                if "TEST_RESULT:" in line:
                    try:
                        # 只取TEST_RESULT:后面的JSON部分
                        result_str = line.split("TEST_RESULT:")[1].strip()
                        # 调试日志
                        log_queue.put(f"正在解析JSON: {result_str}")
                        test_result = json.loads(result_str)
                    except json.JSONDecodeError as e:
                        log_queue.put(f"解析测试结果出错: {str(e)}")
                        log_queue.put(f"原始数据: {result_str}")
                        continue

        process.wait()

        if process.returncode == 0:
            log_queue.put("测试执行完成")
            if test_result:
                # 确保所有字段都存在
                result = {
                    'userId': test_result.get('userId', ''),
                    'loanApplyNo': test_result.get('loanApplyNo', ''),
                    'fundsCode': test_result.get('fundsCode', ''),
                    'loanAmount': test_result.get('loanAmount', ''),
                    'loanDate': test_result.get('loanDate', ''),
                    'phoneNumber': test_result.get('phoneNumber', ''),
                    'userName': test_result.get('userName', ''),
                    'idCard': test_result.get('idCard', ''),
                    'bankCard': test_result.get('bankCard', '')
                }
                # 发送结果到前端
                log_queue.put(json.dumps({"result": result}))
                return result
            else:
                log_queue.put("未获取到测试结果，使用默认值")
                return {
                    'userId': '',
                    'loanApplyNo': '',
                    'fundsCode': '',
                    'loanAmount': '',
                    'loanDate': '',
                    'phoneNumber': '',
                    'userName': '',
                    'idCard': '',
                    'bankCard': ''
                }
        else:
            raise Exception("测试执行失败")

    except Exception as e:
        log_queue.put(f"测试执行出错: {str(e)}")
        return {
            'userId': '',
            'loanApplyNo': '',
            'fundsCode': '',
            'loanAmount': '',
            'loanDate': '',
            'phoneNumber': '',
            'userName': '',
            'idCard': '',
            'bankCard': ''
        }


def signal_handler(signum, frame):
    print("收到终止信号，正在停止测试...")
    sys.exit(0)


def main():
    # 注册信号处理器
    signal.signal(signal.SIGTERM, signal_handler)
    if sys.platform == 'win32':
        signal.signal(signal.SIGBREAK, signal_handler)

    try:
        # 您的测试代码
        pass
    except KeyboardInterrupt:
        print("测试被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"测试执行出错: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
