#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午3:20
import pytest

from common.Update_Database_Result import Update_Sql_Result
from runscripts.run_jinmx import *


@pytest.fixture(scope="function", autouse=True)
def get_channel():
    db = Update_Sql_Result()
    channel = os.environ.get('TEST_CHANNEL')
    if not channel:
        channel = "ICE_ZLSK_36"
    yield channel
    # 收尾，修改为资金路由模式
    Update_Sql_Result().update_api_chanel_non_funds(channel)


@pytest.fixture(scope="function", autouse=True)
def get_loan_perid():
    loan_perid = os.environ.get('LOAN_PERIOD')
    if not loan_perid:
        loan_perid = "12"
    return loan_perid
