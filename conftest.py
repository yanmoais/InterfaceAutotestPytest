#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午3:20
import pytest
from runscripts.run_jinmx import *


@pytest.fixture(scope="function", autouse=True)
def get_channel():
    channel = os.environ.get('TEST_CHANNEL')
    if not channel:
        channel = "ICE_ZLSK_36"
    return channel

