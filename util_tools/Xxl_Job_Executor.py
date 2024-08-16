#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午11:00
import datetime

import allure
from common.Xxl_Job import xxlJob


class execute_xxl_job(xxlJob):
    def __init__(self):
        super().__init__()
        self.excute_xxl_job = xxlJob()
        self.date = datetime.datetime.now()

    # 调用融360图片拉取
    def fetchRong360CreditPhoto(self, loan_apply_no=None):
        self.excute_xxl_job.trigger_xxl_job(349, {"creditApplyNo": loan_apply_no})

    # 调用授信处理定时任务
    def apply_credit_xxljob(self, credit_applyNo):
        param_data = {"creditApplyNo": credit_applyNo}
        self.excute_xxl_job.trigger_xxl_job(196, f'{param_data}')
        self.logging.info(f"执行授信处理定时任务成功：======申请单号为{credit_applyNo}")

    # 调用授信签章定时任务
    def apply_credit_sign_xxljob(self):
        self.excute_xxl_job.trigger_xxl_job(195)
        self.logging.info(f"执行授信签章定时任务成功!")

    # 调用放款任务处理定时任务
    def apply_loan_xxljob(self, loanApplyNo):
        param_data = {"loanApplyNo": loanApplyNo, "limit": 0}
        self.excute_xxl_job.trigger_xxl_job(198, f'{param_data}')
        self.logging.info(f"执行放款任务处理定时任务成功：======申请单号为{loanApplyNo}")

    # 调用新长银批扣 D0 定时任务，到期日批扣
    # 新长银批扣需要满足条件：当前系统日期 - 到期日 >= 0
    def new_cy_batch_repay_apply(self, date=datetime.datetime.now().strftime("%Y%m%d")):
        self.excute_xxl_job.trigger_xxl_job(309, f'{date}')
        self.logging.info(f"执行新长银批扣 D0 定时任务成功：======日期为{date}")


if __name__ == '__main__':
    loanApplyNo = "SLN3487668801"
    execute_xxl_job().new_cy_batch_repay_apply()
