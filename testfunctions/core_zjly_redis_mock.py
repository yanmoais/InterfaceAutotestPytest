#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午2:28
from common.Update_Database_Result import *


# 更新金美信为Mock环境
def update_jmx_to_mock():
    Update_Sql_Result().update_jmx_zjly_mock()


# 更新金美信为资方测试环境
def update_jmx_to_test():
    Update_Sql_Result().update_jmx_zjly_test()
