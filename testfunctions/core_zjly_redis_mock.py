#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午2:28
from common.Update_Database_Result import *


# 更新金美信为Mock环境
def test_update_jmx_to_mock():
    Update_Sql_Result().update_jmx_zjly_mock()


# 更新金美信为资方测试环境
def test_update_jmx_to_test():
    Update_Sql_Result().update_jmx_zjly_test()


# 更新海峡为Mock环境
def test_update_haixia_to_mock():
    Update_Sql_Result().update_haixia_zjly_mock()


# 更新海峡为资方测试环境
def test_update_haixia_to_test():
    Update_Sql_Result().update_haixia_zjly_test()


# 更新中原提前花为Mock环境
def test_update_zytqh_to_mock():
    Update_Sql_Result().update_zytqh_zjly_mock()


# 更新中原提前花为资方测试环境
def test_update_zytqh_to_test():
    Update_Sql_Result().update_zytqh_zjly_test()


# 更新润楼为Mock环境
def test_update_runlou_to_mock():
    Update_Sql_Result().update_runlou_zjly_mock()


# 更新润楼为资方测试环境
def test_update_runlou_to_test():
    Update_Sql_Result().update_runlou_zjly_test()
