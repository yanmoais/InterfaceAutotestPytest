#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午6:30
import datetime
import time
from util_tools.Database_Conn import Mysql
from dateutil.relativedelta import relativedelta
from common.Select_Database_Result import Select_Sql_Result
from util_tools.Redis_Conn import Redis


class Update_Sql_Result(Mysql):
    def __init__(self):
        super().__init__()

    # 查询批发侧fr_api_order_info表订单信息,根据借款流水号来查询
    def update_api_binding_bank_card_result(self, req_seq_no):
        update_sql = f"UPDATE finance_router.fr_api_binding_bank_card SET result_code='1001', result_msg = '签约成功',bind_id = '732855302144952973',messageNo = '200604000014372-17200785447440696447852' WHERE loanseqno = '{req_seq_no}';"
        result = Mysql().update_db(update_sql)
        self.logging.info(f"数据库执行完成：==={result}")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zx_credit_applicant_info表
    def update_api_flow_zx_credit_applicant_info(self, funds_code, user_id, test_db="api"):
        update_sql = f"UPDATE zx_credit_applicant_info as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql(test_db).update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zx_credit_applicant_result表
    def update_api_flow_zx_credit_applicant_result(self, funds_code, user_id, test_db="api"):
        update_sql = f"UPDATE zx_credit_applicant_result as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql(test_db).update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zx_credit_user_info表
    def update_api_flow_zx_credit_user_info(self, funds_code, user_id, test_db="api"):
        update_sql = f"UPDATE zx_credit_user_info as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql(test_db).update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zl_drms_judgements表
    def update_api_flow_zl_drms_judgements(self, funds_code, user_id, test_db="api"):
        update_sql = f"UPDATE zl_drms_judgements as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql(test_db).update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api授信绑卡前对api侧进行修改成需要的对应资方,更新zx_credit_info表
    def update_api_flow_zx_credit_info(self, funds_code, user_id, test_db="api"):
        update_sql = f"UPDATE zx_credit_info as cai SET cai.funds_code = '{funds_code}' WHERE cai.user_id = '{user_id}';"
        result = Mysql(test_db).update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api操作还款前对api侧zx_loan_plan_info放款日期与还款计划进行修改,根据loan_apply_no来模糊查询,根据对应期数来修改日期
    def update_api_flow_zx_loan_plan_info_d0(self, loan_apply_no, term, test_db="api"):
        update_sql = f"UPDATE zx_loan_plan_info as cai SET cai.start_date = '{(datetime.datetime.now() - relativedelta(months=1)).strftime('%Y%m%d')}', cai.due_date = '{(datetime.datetime.now().strftime('%Y%m%d'))}' WHERE cai.plan_no LIKE '{loan_apply_no}%' AND cai.term = '{term}';"
        result = Mysql(test_db).update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api操作还款前对api侧zx_loan_note_info放款日期与还款计划进行修改,根据loan_apply_no来模糊查询,根据对应期数来修改日期
    def update_api_flow_zx_loan_note_info_d0(self, loan_apply_no, test_db="api"):
        update_sql = f"UPDATE zx_loan_note_info as cai SET cai.loan_time = '{(datetime.datetime.now() - relativedelta(months=1)).strftime('%Y%m%d%H%M%S')}', cai.cash_date = '{((datetime.datetime.now() - relativedelta(months=1)).strftime('%Y%m%d'))}', cai.inst_date = '{((datetime.datetime.now() - relativedelta(months=1)).strftime('%Y%m%d'))}' WHERE cai.loan_apply_no = '{loan_apply_no}';"
        result = Mysql(test_db).update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api操作还款前对批发侧fr_api_repayment_plan还款计划进行修改,根据loan_apply_no来查询,根据对应期数来修改日期
    def update_api_core_fr_api_repayment_plan_d0(self, loan_apply_no, term):
        core_loan_no = Select_Sql_Result().select_fr_api_repayment_plan(loan_apply_no)[0]['loan_no']
        update_sql = f"UPDATE finance_router.fr_api_repayment_plan as fr SET fr.ps_due_dt = '{(datetime.datetime.now().strftime('%Y-%m-%d'))}' WHERE fr.loan_no = '{core_loan_no}' AND fr.period = '{term}';"
        result = Mysql().update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api操作还款前对批发侧fr_api_order_info订单表进行修改,根据loan_apply_no来查询,修改日期
    def update_api_core_fr_api_order_info_d0(self, loan_apply_no):
        req_seq_no = Select_Sql_Result().select_zx_loan_apply_record(loan_apply_no)['loan_no']
        now_date = (datetime.datetime.now() - relativedelta(months=1))
        update_sql = f"UPDATE finance_router.fr_api_order_info as fr SET fr.settle_time = '{now_date.strftime('%Y-%m-%d %H:%M:%S')}',fr.apply_dt = '{now_date.strftime('%Y-%m-%d')}', fr.repay_day = '{now_date.strftime('%Y-%m-%d')}' WHERE fr.req_seq_no = '{req_seq_no}';"
        result = Mysql().update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # 资金批发路由操作还款前对批发侧fr_api_repayment_plan还款计划进行修改,根据req_seq_no来查询,根据对应期数来修改日期
    def update_zjly_fr_api_repayment_plan_due_day(self, req_seq_no, term):
        update_sql1 = f"SELECT ord.order_no FROM finance_router.fr_api_order_info ord WHERE ord.req_seq_no = '{req_seq_no}';"
        order_no = Mysql().select_db(update_sql1)[0]['order_no']
        print(order_no)
        update_sql2 = f"UPDATE finance_router.fr_api_repayment_plan as fr SET fr.ps_due_dt = '{(datetime.datetime.now().strftime('%Y-%m-%d'))}' WHERE fr.order_no = '{order_no}' AND fr.period = '{term}';"
        result = Mysql().update_db(update_sql2)
        self.logging.info(f"数据库执行完成!")
        return result

    # 集合更新api侧绑卡前的funds_code
    def update_api_flow_all_table(self, funds_code, user_id, test_db="api"):
        db = Update_Sql_Result()
        db.update_api_flow_zx_credit_user_info(funds_code, user_id, test_db)
        db.update_api_flow_zx_credit_applicant_result(funds_code, user_id, test_db)
        db.update_api_flow_zl_drms_judgements(funds_code, user_id, test_db)
        db.update_api_flow_zx_credit_applicant_info(funds_code, user_id, test_db)
        db.update_api_flow_zx_credit_info(funds_code, user_id, test_db)
        self.logging.info(f"全部执行完毕！")

    # 修改金美信走Mock环境
    def update_jmx_zjly_mock(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('金美信mock')
        if results['code'] == "jinMeiXin_mock":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'jinMeiXin_temp' WHERE fr.name = '金美信mock';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'jinMeiXin_mock' WHERE fr.name = '金美信-测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'jinMeiXin' WHERE fr.name = '金美信mock';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除金美信Redis的Key值
            try:
                redis_clinet.delete_redis_key("zijinluyou:api:param_config:::jinMeiXin")
            except Exception as e:
                self.logging.error(f"请求发生错误：{e}")
            # 关闭redis
            finally:
                self.logging.info("当前已切换为Mock环境！")
                redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为Mock环境，无需切换！")

    # 修改金美信走资方测试环境
    def update_jmx_zjly_test(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('金美信mock')
        if results['code'] == "jinMeiXin":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'jinMeiXin_temp' WHERE fr.name = '金美信mock';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'jinMeiXin' WHERE fr.name = '金美信-测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'jinMeiXin_mock' WHERE fr.name = '金美信mock';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除金美信Redis的Key值
            redis_clinet.delete_redis_key("zijinluyou:api:param_config:::jinMeiXin")
            # 关闭redis
            redis_clinet.close_db()
            self.logging.info("当前已切为资方测试环境！")
            return result
        else:
            self.logging.info("当前模式为资方测试环境，无需切换！")

    # 修改海峡走Mock环境
    def update_haixia_zjly_mock(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('海峡mock')
        if results['code'] == "haiXia_mock":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'haiXia_temp' WHERE fr.name = '海峡mock';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'haiXia_mock' WHERE fr.name = '海峡';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'haiXia' WHERE fr.name = '海峡mock';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除海峡Redis的Key值
            try:
                redis_clinet.delete_redis_key("zijinluyou:api:param_config:::haiXia")
            except Exception as e:
                self.logging.error(f"请求发生错误：{e}")
            # 关闭redis
            finally:
                redis_clinet.close_db()
            self.logging.info("已切换为为Mock环境！")
            return result
        else:
            self.logging.info("当前模式为Mock环境，无需切换！")

    # 修改海峡走资方测试环境
    def update_haixia_zjly_test(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('海峡mock')
        if results['code'] == "haiXia":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'haiXia_temp' WHERE fr.name = '海峡mock';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'haiXia' WHERE fr.name = '海峡';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'haiXia_mock' WHERE fr.name = '海峡mock';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除海峡Redis的Key值
            redis_clinet.delete_redis_key("zijinluyou:api:param_config:::haiXia")
            # 关闭redis
            redis_clinet.close_db()
            self.logging.info("已切换为为资金方测试环境！")
            return result
        else:
            self.logging.info("当前模式为资金方测试环境，无需切换！")

    # 修改中原提前花走Mock环境
    def update_zytqh_zjly_mock(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('中原提钱花MOCK')
        if results['code'] == "zhongYuanTqh_mock":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'zhongYuanTqh_temp' WHERE fr.name = '中原提钱花MOCK';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'zhongYuanTqh_mock' WHERE fr.name = '中原提钱花-测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'zhongYuanTqh' WHERE fr.name = '中原提钱花MOCK';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除中原提前花Redis的Key值
            try:
                redis_clinet.delete_redis_key("zijinluyou:api:param_config:::zhongYuanTqh")
            except Exception as e:
                self.logging.error(f"请求发生错误：{e}")
            # 关闭redis
            finally:
                redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为Mock环境，无需切换！")

    # 修改中原提前花走资方测试环境
    def update_zytqh_zjly_test(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('中原提钱花MOCK')
        if results['code'] == "zhongYuanTqh":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'zhongYuanTqh_temp' WHERE fr.name = '中原提钱花MOCK';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'zhongYuanTqh' WHERE fr.name = '中原提钱花-测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'zhongYuanTqh_mock' WHERE fr.name = '中原提钱花MOCK';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除中原提前花Redis的Key值
            redis_clinet.delete_redis_key("zijinluyou:api:param_config:::zhongYuanTqh")
            # 关闭redis
            redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为资方测试环境，无需切换！")

    # 修改润楼走Mock环境
    def update_runlou_zjly_mock(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('润楼-MOCK')
        if results['code'] == "runLou_mock":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'runLou_temp' WHERE fr.name = '润楼-MOCK';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'runLou_mock' WHERE fr.name = '润楼-测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'runLou' WHERE fr.name = '润楼-MOCK';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除润楼Redis的Key值
            try:
                redis_clinet.delete_redis_key("zijinluyou:api:param_config:::runLou")
            except Exception as e:
                self.logging.error(f"请求发生错误：{e}")
            # 关闭redis
            finally:
                redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为Mock环境，无需切换！")

    # 修改润楼走资方测试环境
    def update_runlou_zjly_test(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('润楼-MOCK')
        if results['code'] == "runLou":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'runLou_temp' WHERE fr.name = '润楼-MOCK';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'runLou' WHERE fr.name = '润楼-测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'runLou_mock' WHERE fr.name = '润楼-MOCK';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除润楼Redis的Key值
            redis_clinet.delete_redis_key("zijinluyou:api:param_config:::runLou")
            # 关闭redis
            redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为资方测试环境，无需切换！")

    # 修改小米走Mock环境
    def update_xiaomi_zjly_mock(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('小米mock')
        if results['code'] == "xiaoMi_mock":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'xiaoMi_temp' WHERE fr.name = '小米mock';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'xiaoMi_mock' WHERE fr.name = '小米测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'xiaoMi' WHERE fr.name = '小米mock';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除润楼Redis的Key值
            try:
                redis_clinet.delete_redis_key("zijinluyou:api:param_config:::xiaoMi")
            except Exception as e:
                self.logging.error(f"请求发生错误：{e}")
            # 关闭redis
            finally:
                redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为Mock环境，无需切换！")

    # 修改小米走资方测试环境
    def update_xiaomi_zjly_test(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('小米mock')
        if results['code'] == "xiaoMi":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'xiaoMi_temp' WHERE fr.name = '小米mock';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'xiaoMi' WHERE fr.name = '小米测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'xiaoMi_mock' WHERE fr.name = '小米mock';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除润楼Redis的Key值
            redis_clinet.delete_redis_key("zijinluyou:api:param_config:::xiaoMi")
            # 关闭redis
            redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为资方测试环境，无需切换！")

    # 修改长银布客走Mock环境
    def update_cybuke_zjly_mock(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('长银步客Mock')
        if results['code'] == "changYinBuKeMock":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'changYinBuKeMock_temp' WHERE fr.name = '长银步客Mock';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'changYinBuKeMock' WHERE fr.name = '长银步客-测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'changYinBuKe' WHERE fr.name = '长银步客Mock';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除润楼Redis的Key值
            try:
                redis_clinet.delete_redis_key("zijinluyou:api:param_config:::changYinBuKe")
            except Exception as e:
                self.logging.error(f"请求发生错误：{e}")
            # 关闭redis
            finally:
                redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为Mock环境，无需切换！")

    # 修改长银布客走资方测试环境
    def update_cybuke_zjly_test(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('长银步客Mock')
        if results['code'] == "changYinBuKe":
            update_sql_1 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'changYinBuKeMock_temp' WHERE fr.name = '长银步客Mock';"
            update_sql_2 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'changYinBuKe' WHERE fr.name = '长银步客-测试';"
            update_sql_3 = f"UPDATE finance_router.fr_channel_config as fr SET fr.code = 'changYinBuKeMock' WHERE fr.name = '长银步客Mock';"
            Mysql().update_db(update_sql_1)
            time.sleep(1)
            Mysql().update_db(update_sql_2)
            time.sleep(1)
            result = Mysql().update_db(update_sql_3)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis()
            # 删除润楼Redis的Key值
            redis_clinet.delete_redis_key("zijinluyou:api:param_config:::changYinBuKe")
            # 关闭redis
            redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为资方测试环境，无需切换！")

    # 修改Api侧对应渠道为限流模式
    def update_api_chanel_non_funds(self, channel_code, test_db="api"):
        # 获取当前是否为限流模式
        results = Select_Sql_Result().select_zl_api_user(channel_code)
        if results['funds_router'] == "1":
            update_sql = f"UPDATE zl_api_user zl SET zl.funds_router = '' WHERE zl.channel_code = '{channel_code}';"
            result = Mysql(test_db).update_db(update_sql)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis(test_db)
            # 删除Redis的Key值
            redis_clinet.delete_redis_key('zl_cashloan:zl_api_user:::' + channel_code)
            # 关闭redis
            redis_clinet.close_db()
            self.logging.info("已切换为限流模式！")
            return result
        else:
            self.logging.info("当前渠道为限流模式，无需切换！")

    # 修改Api侧对应渠道为路由模式
    def update_api_chanel_funds_router(self, channel_code, test_db="api"):
        # 获取当前是否为路由模式
        results = Select_Sql_Result().select_zl_api_user(channel_code)
        if results['funds_router'] == "":
            update_sql = f"UPDATE zl_api_user zl SET zl.funds_router = '1' WHERE zl.channel_code = '{channel_code}';"
            result = Mysql(test_db).update_db(update_sql)
            self.logging.info(f"数据库执行完成!")

            # 实例化Redis连接
            redis_clinet = Redis(test_db)
            # 删除Redis的Key值
            redis_clinet.delete_redis_key('zl_cashloan:zl_api_user:::' + channel_code)
            # 关闭redis
            redis_clinet.close_db()
            self.logging.info("已切换为路由模式！")
            return result
        else:
            self.logging.info("当前渠道为路由模式，无需切换！")


if __name__ == '__main__':
    user_id = "ZLTEST_202410161729069481126"
    funds_code = "FR_RUN_LOU"
    Update_Sql_Result().update_jmx_zjly_test()
    # print((datetime.datetime.now() - relativedelta(months=1)).strftime("%Y-%m-%d %H:%M:%S"))
