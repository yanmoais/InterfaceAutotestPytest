import schedule
import time
import subprocess
from config.Base_Env import BASE_DIR


def run_script():
    print("Running script...")
    subprocess.run(["python", f"{BASE_DIR}/config/run.py"])


# 每天的特定时间执行
schedule.every().day.at("11:01").do(run_script)

# 每小时执行
# schedule.every().hour.do(run_script)

# 每隔一段时间执行一次
# schedule.every(10).minutes.do(run_script)
while True:
    schedule.run_pending()
    time.sleep(1)