#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午11:00
import allure
from common.Xxl_Job import xxlJob


class execute_xxl_job(xxlJob):
    def __init__(self):
        super().__init__()
        self.excute_xxl_job = xxlJob()

    # 调用融360图片拉取
    def fetchRong360CreditPhoto(self, loan_apply_no=None):
        self.excute_xxl_job.trigger_xxl_job(349, {"creditApplyNo": loan_apply_no})


if __name__ == '__main__':
    print(execute_xxl_job().fetchRong360CreditPhoto())
