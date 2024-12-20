import os
import sys
object_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(object_path)
from config.Base_Env import BASE_DIR
import subprocess




def run_script():
    print("Running script...")
    subprocess.run(["python", f"{BASE_DIR}/config/run.py"])


run_script()
# # 创建一个BlockingScheduler实例
# scheduler = BlockingScheduler()
#
# # # 添加一个cron类型的定时任务，比如每天下午3点15分执行
# # scheduler.add_job(run_script, 'cron', hour=9, minute=35)
#
# # 启动调度器
# scheduler.start(run_script)
