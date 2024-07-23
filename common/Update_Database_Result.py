#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午6:30

from util_tools.Database_Conn import Mysql


class Update_Sql_Result(Mysql):
    def __init__(self):
        super().__init__()

    # 查询fr_api_order_info表订单信息,根据借款流水号来查询
    def update_api_binding_bank_card_result(self, req_seq_no):
        update_sql = f"UPDATE finance_router.fr_api_binding_bank_card SET result_code='1001', result_msg = '签约成功',bind_id = '732855302144952973',messageNo = '200604000014372-17200785447440696447852' WHERE loanseqno = '{req_seq_no}';"
        result = Mysql().update_db(update_sql)
        self.logging.info(f"数据库执行完成：==={result}")
        return result


if __name__ == '__main__':
    req_seq_no = "ZLCHY1718791785461"
    db = Update_Sql_Result().update_api_binding_bank_card_result()
    data = db.select_api_order_info_result(req_seq_no)
    print(data)
