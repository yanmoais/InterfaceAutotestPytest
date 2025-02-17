from flask import Flask, render_template, jsonify, send_from_directory
from routes.app_control_routes import app_control_bp
from routes.risk_control_routes import risk_control_bp
from routes.redis_routes import redis_bp
from routes.data_construct_routes import data_construct_bp
from routes.auto_execution_routes import auto_execution_bp
from flask import Flask
import os
import signal

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# 注册蓝图
app.register_blueprint(app_control_bp)
app.register_blueprint(risk_control_bp)
app.register_blueprint(redis_bp)
app.register_blueprint(data_construct_bp)
app.register_blueprint(auto_execution_bp)
# 全局变量存储当前运行的进程 ID
current_test_process = None


# 基础页面路由
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/riskControl')
def riskControl():
    return render_template('riskControl.html')


@app.route('/idgenerate')
def idgenerate():
    return render_template('idgrnerate.html')


@app.route('/delredis')
def delredis():
    return render_template('delredis.html')


@app.route('/appcontrol')
def appcontrol():
    return render_template('appControl.html')


@app.route('/dataConstruct')
def datastructure():
    return render_template('dataConstruct.html')


@app.route('/autoExecution')
def auto_execution():
    return render_template('autoExecution.html')


@app.route('/pressureTest')
def pressure_test():
    return render_template('pressureTest.html')


@app.route('/report/html/<path:filename>')
def serve_report(filename):
    try:
        if os.name == 'nt':
            # 使用环境变量或配置文件来设置项目根目录
            PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        else:
            PROJECT_ROOT = '/home/interface_autotest_pytest/ZL_testplatform'

        # 构建报告目录的完整路径
        report_dir = os.path.join(PROJECT_ROOT, 'report', 'html')

        # 添加日志
        app.logger.info(f"Project root: {PROJECT_ROOT}")
        app.logger.info(f"Report directory: {report_dir}")
        app.logger.info(f"Requested file: {filename}")

        # 确保目录存在
        if not os.path.exists(report_dir):
            os.makedirs(report_dir, exist_ok=True)

        return send_from_directory(report_dir, filename)
    except Exception as e:
        app.logger.error(f"Error serving report: {str(e)}")
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)
