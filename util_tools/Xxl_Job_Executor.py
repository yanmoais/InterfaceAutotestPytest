#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午11:00
import datetime
import time
import allure
from common.Xxl_Job import xxlJob
from util_tools.Faker import *


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
        time.sleep(3)

    # 调用授信签章定时任务
    def apply_credit_sign_xxljob(self):
        self.excute_xxl_job.trigger_xxl_job(195)
        self.logging.info(f"执行授信签章定时任务成功!")
        time.sleep(3)

    # 调用放款任务处理定时任务
    def apply_loan_xxljob(self, loanApplyNo):
        param_data = {"loanApplyNo": loanApplyNo, "limit": 0}
        self.excute_xxl_job.trigger_xxl_job(198, f'{param_data}')
        self.logging.info(f"执行放款任务处理定时任务成功：======申请单号为{loanApplyNo}")
        time.sleep(3)

    # 调用放款签章定时任务
    def apply_loan_sign_xxljob(self):
        self.excute_xxl_job.trigger_xxl_job(197)
        self.logging.info(f"执行放款签章定时任务成功!")
        time.sleep(3)

    # 调用新长银批扣 D0 定时任务，到期日批扣
    # 新长银批扣需要满足条件：当前系统日期 - 到期日 >= 0
    def new_cy_batch_d0_repay_apply(self, date=datetime.datetime.now().strftime("%Y%m%d")):
        self.excute_xxl_job.trigger_xxl_job(601, f'{date}')
        self.logging.info(f"执行新长银批扣 D0 定时任务成功：======日期为{date}")
        time.sleep(5)

    # 调用查询批扣结果任务，传loanApplyNo
    def new_cy_d0_batch_repayment_query(self, loanApplyNo):
        param_data = {"loanApplyNo": loanApplyNo}
        self.excute_xxl_job.trigger_xxl_job(578, f'{param_data}')
        self.logging.info(f"执行查询批扣结果任务成功!")
        time.sleep(5)

    # 调用推送客户中心任务，传creditApplyNo
    def push_credit_info_to_customer_center(self, creditApplyNo):
        param_data = {"limit": 10, "cutTimeStr": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                      "creditApplyNoList": [f"{creditApplyNo}"]}
        self.excute_xxl_job.trigger_xxl_job(430, f'{json_dump_cn(param_data)}')
        self.logging.info(f"执行推送客户中心任务成功!")
        time.sleep(5)

    # 调用单笔还款处理任务
    def single_repay(self):
        self.excute_xxl_job.trigger_xxl_job(199)
        self.logging.info(f"调用单笔还款处理任务成功!")
        time.sleep(5)

    # 调用单笔还款结果查询
    def single_query_result(self):
        self.excute_xxl_job.trigger_xxl_job(200)
        self.logging.info(f"调用单笔还款查询任务成功!")
        time.sleep(5)


if __name__ == '__main__':
    # loanApplyNo = "ZLTEST_202410211729493860807"
    # execute_xxl_job().push_credit_info_to_customer_center(loanApplyNo)
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    pass
