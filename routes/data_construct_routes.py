from flask import Blueprint, jsonify, request, Response
import json
import threading
import queue
import importlib
import psutil
import subprocess
import os
import time
import platform

data_construct_bp = Blueprint('data_construct', __name__, url_prefix='/data_construct')
log_queue = queue.Queue()


def run_test(channel, funder, testType):
    funder_mapping = {
        '金美信': 'runscripts.run_jinmx',
        '小米': 'runscripts.run_xiaomi',
        '振兴': 'runscripts.run_zhenxing'
    }

    try:
        module_name = funder_mapping.get(funder)
        if not module_name:
            raise ValueError(f"未知的资方: {funder}")

        module = importlib.import_module(module_name)
        result = module.run_test(channel, log_queue, testType)

        # 确保结果包含所有必要字段
        formatted_result = {
            'userId': result.get('userId', ''),
            'loanApplyNo': result.get('loanApplyNo', ''),
            'fundsCode': result.get('fundsCode', ''),
            'loanAmount': result.get('loanAmount', ''),
            'loanDate': result.get('loanDate', ''),
            'phoneNumber': result.get('phoneNumber', ''),
            'userName': result.get('userName', ''),
            'idCard': result.get('idCard', ''),
            'bankCard': result.get('bankCard', '')
        }

        # 将结果通过日志队列发送
        log_queue.put(json.dumps({"result": formatted_result, "testType": testType}))
        return {"status": "success"}

    except Exception as e:
        error_msg = f"执行出错: {str(e)}"
        log_queue.put(error_msg)
        return {"status": "error", "message": error_msg}


@data_construct_bp.route('/execute', methods=['POST'])
def execute():
    try:
        # 清空日志队列
        while not log_queue.empty():
            log_queue.get()

        channel = request.json['channel']
        funder = request.json['funder']
        testType = request.json['testType']

        def run():
            run_test(channel, funder, testType)
            log_queue.put("TEST_COMPLETE")

        thread = threading.Thread(target=run)
        thread.start()

        return jsonify({"status": "started"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_construct_bp.route('/logs')
def get_logs():
    def generate():
        while True:
            try:
                log = log_queue.get()
                if log == "TEST_COMPLETE":
                    break
                try:
                    # 尝试解析JSON格式的日志
                    data = json.loads(log)
                    if "result" in data:
                        # 确保结果数据包含所有字段
                        result = data["result"]
                        result.setdefault('userId', '')
                        result.setdefault('loanApplyNo', '')
                        result.setdefault('fundsCode', '')
                        result.setdefault('loanAmount', '')
                        result.setdefault('loanDate', '')
                        result.setdefault('phoneNumber', '')
                        result.setdefault('userName', '')
                        result.setdefault('idCard', '')
                        result.setdefault('bankCard', '')
                    yield f"data: {json.dumps(data)}\n\n"
                except json.JSONDecodeError:
                    # 普通文本日志
                    yield f"data: {json.dumps({'message': log})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break

    return Response(generate(), mimetype='text/event-stream')


@data_construct_bp.route('/stop_test', methods=['POST'])
def stop_test():
    try:
        # 获取当前运行的进程并终止
        if hasattr(data_construct_bp, 'current_process') and data_construct_bp.current_process:
            data_construct_bp.current_process.terminate()
            data_construct_bp.current_process = None
        
        def delayed_restart():
            # 等待2秒确保HTTP响应已发送
            time.sleep(2)
            
            # 获取当前Python进程的PID
            current_pid = os.getpid()
            current_process = psutil.Process(current_pid)
            
            # 获取操作系统类型
            system_type = platform.system().lower()
            
            # 获取项目根目录路径
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            if system_type == 'windows':
                # Windows系统下，终止当前Python进程及其子进程
                for child in current_process.children(recursive=True):
                    try:
                        child.terminate()
                    except:
                        pass
                # Windows系统下的启动命令
                subprocess.Popen(
                    ['python', 'app.py'],
                    cwd=root_dir,
                    start_new_session=True,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                # Linux系统下，使用pm2重启
                try:
                    # 先终止当前进程及其子进程
                    for child in current_process.children(recursive=True):
                        try:
                            child.terminate()
                        except:
                            pass
                    # 使用pm2重启应用
                    subprocess.run(['pm2', 'restart', '0'], check=True)
                except subprocess.CalledProcessError:
                    # 如果pm2命令失败，尝试重新启动pm2
                    subprocess.run(['pm2', 'start', 'app.py', '--name', 'app'], check=True)
            
            # 终止当前进程
            os._exit(0)
        
        # 在新线程中执行延迟重启
        threading.Thread(target=delayed_restart, daemon=True).start()
        
        return jsonify({
            'status': 'success', 
            'message': '测试已停止，应用程序将在2秒后重启'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
