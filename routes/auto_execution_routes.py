import os
import platform
import subprocess
import time
from flask import Blueprint, request, jsonify, Response, render_template
import json
import threading
import queue
import importlib
from datetime import datetime

import psutil

# 确保这个变量名称正确，并且在文件顶部定义
auto_execution_bp = Blueprint('auto_execution', __name__, url_prefix='/auto_execution')
log_queue = queue.Queue()


@auto_execution_bp.route('/execute', methods=['POST'])
def execute():
    try:
        # 清空之前的日志
        while not log_queue.empty():
            log_queue.get()

        data = request.json
        business_line = data.get('businessLine')
        funders = data.get('funders', [])  # 修改为接收资方列表
        regression_date = data.get('regressionDate')

        def run():
            try:
                from runscripts.run_auto import run_test
                run_test(business_line, funders, regression_date, log_queue)
            except Exception as e:
                log_queue.put(json.dumps({"message": f"执行出错: {str(e)}"}))
            finally:
                log_queue.put("TEST_COMPLETE")

        thread = threading.Thread(target=run)
        thread.daemon = True  # 设置为守护线程
        thread.start()

        return jsonify({"status": "success", "message": "回归测试已启动"})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@auto_execution_bp.route('/logs')
def logs():
    def generate():
        while True:
            try:
                message = log_queue.get(timeout=1)  # 添加超时
                if message == "TEST_COMPLETE":
                    break
                if isinstance(message, str):
                    try:
                        # 尝试解析JSON
                        json.loads(message)
                        yield f"data: {message}\n\n"
                    except json.JSONDecodeError:
                        # 如果不是JSON，封装成消息格式
                        yield f"data: {json.dumps({'message': message})}\n\n"
                else:
                    yield f"data: {json.dumps(message)}\n\n"
            except queue.Empty:
                continue  # 超时后继续等待
            except Exception as e:
                print(f"Error in logs route: {e}")
                yield f"data: {json.dumps({'message': f'日志处理错误: {str(e)}'})}\n\n"
                break

    response = Response(generate(), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    return response


@auto_execution_bp.route('/stop_test', methods=['POST'])
def stop_test():
    try:
        # 获取当前运行的进程并终止
        if hasattr(auto_execution_bp, 'current_process') and auto_execution_bp.current_process:
            auto_execution_bp.current_process.terminate()
            auto_execution_bp.current_process = None
        
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
