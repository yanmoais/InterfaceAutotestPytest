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
        update_sql = f"UPDATE finace_router_sit.fr_api_binding_bank_card SET result_code='1001', result_msg = '签约成功',bind_id = '732855302144952973',messageNo = '200604000014372-17200785447440696447852' WHERE loanseqno = '{req_seq_no}';"
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
        update_sql = f"UPDATE finace_router_sit.fr_api_repayment_plan as fr SET fr.ps_due_dt = '{(datetime.datetime.now().strftime('%Y-%m-%d'))}' WHERE fr.loan_no = '{core_loan_no}' AND fr.period = '{term}';"
        result = Mysql().update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # api操作还款前对批发侧fr_api_order_info订单表进行修改,根据loan_apply_no来查询,修改日期
    def update_api_core_fr_api_order_info_d0(self, loan_apply_no):
        req_seq_no = Select_Sql_Result().select_zx_loan_apply_record(loan_apply_no)['loan_no']
        now_date = (datetime.datetime.now() - relativedelta(months=1))
        update_sql = f"UPDATE finace_router_sit.fr_api_order_info as fr SET fr.settle_time = '{now_date.strftime('%Y-%m-%d %H:%M:%S')}',fr.apply_dt = '{now_date.strftime('%Y-%m-%d')}', fr.repay_day = '{now_date.strftime('%Y-%m-%d')}' WHERE fr.req_seq_no = '{req_seq_no}';"
        result = Mysql().update_db(update_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # 资金批发路由操作还款前对批发侧fr_api_repayment_plan还款计划进行修改,根据req_seq_no来查询,根据对应期数来修改日期
    def update_zjly_fr_api_repayment_plan_due_day(self, req_seq_no, term):
        update_sql1 = f"SELECT ord.order_no FROM finace_router_sit.fr_api_order_info ord WHERE ord.req_seq_no = '{req_seq_no}';"
        order_no = Mysql().select_db(update_sql1)[0]['order_no']
        print(order_no)
        update_sql2 = f"UPDATE finace_router_sit.fr_api_repayment_plan as fr SET fr.ps_due_dt = '{(datetime.datetime.now().strftime('%Y-%m-%d'))}' WHERE fr.order_no = '{order_no}' AND fr.period = '{term}';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'jinMeiXin_temp' WHERE fr.name = '金美信mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'jinMeiXin_mock' WHERE fr.name = '金美信-测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'jinMeiXin' WHERE fr.name = '金美信mock';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'jinMeiXin_temp' WHERE fr.name = '金美信mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'jinMeiXin' WHERE fr.name = '金美信-测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'jinMeiXin_mock' WHERE fr.name = '金美信mock';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'haiXia_temp' WHERE fr.name = '海峡mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'haiXia_mock' WHERE fr.name = '海峡';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'haiXia' WHERE fr.name = '海峡mock';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'haiXia_temp' WHERE fr.name = '海峡mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'haiXia' WHERE fr.name = '海峡';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'haiXia_mock' WHERE fr.name = '海峡mock';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'zhongYuanTqh_temp' WHERE fr.name = '中原提钱花MOCK';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'zhongYuanTqh_mock' WHERE fr.name = '中原提钱花-测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'zhongYuanTqh' WHERE fr.name = '中原提钱花MOCK';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'zhongYuanTqh_temp' WHERE fr.name = '中原提钱花MOCK';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'zhongYuanTqh' WHERE fr.name = '中原提钱花-测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'zhongYuanTqh_mock' WHERE fr.name = '中原提钱花MOCK';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'runLou_temp' WHERE fr.name = '润楼-MOCK';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'runLou_mock' WHERE fr.name = '润楼-测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'runLou' WHERE fr.name = '润楼-MOCK';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'runLou_temp' WHERE fr.name = '润楼-MOCK';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'runLou' WHERE fr.name = '润楼-测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'runLou_mock' WHERE fr.name = '润楼-MOCK';"
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

    # 修改蒙商走Mock环境
    def update_mengshang_zjly_mock(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('小米mock')
        if results['code'] == "xiaoMi_mock":
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'xiaoMi_temp' WHERE fr.name = '小米mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'xiaoMi_mock' WHERE fr.name = '小米测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'xiaoMi' WHERE fr.name = '小米mock';"
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

    # 修改小米走Mock环境
    def update_xiaomi_zjly_mock(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('小米mock')
        if results['code'] == "xiaoMi_mock":
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'xiaoMi_temp' WHERE fr.name = '小米mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'xiaoMi_mock' WHERE fr.name = '小米测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'xiaoMi' WHERE fr.name = '小米mock';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'xiaoMi_temp' WHERE fr.name = '小米mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'xiaoMi' WHERE fr.name = '小米测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'xiaoMi_mock' WHERE fr.name = '小米mock';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinBuKeMock_temp' WHERE fr.name = '长银步客Mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinBuKeMock' WHERE fr.name = '长银步客-测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinBuKe' WHERE fr.name = '长银步客Mock';"
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
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinBuKeMock_temp' WHERE fr.name = '长银步客Mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinBuKe' WHERE fr.name = '长银步客-测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinBuKeMock' WHERE fr.name = '长银步客Mock';"
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

    # 修改新长银走Mock环境
    def update_cynew_zjly_mock(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('长银Mock')
        if results['code'] == "changYinMock":
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinNew_temp' WHERE fr.name = '长银Mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinMock' WHERE fr.name = '长银新模式';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinNew' WHERE fr.name = '长银Mock';"
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
                redis_clinet.delete_redis_key("zijinluyou:api:param_config:::changYinNew")
            except Exception as e:
                self.logging.error(f"请求发生错误：{e}")
            # 关闭redis
            finally:
                redis_clinet.close_db()
            return result
        else:
            self.logging.info("当前模式为Mock环境，无需切换！")

    # 修改新长银走资方测试环境
    def update_cynew_zjly_test(self):
        # 获取当前是否为Mock环境
        results = Select_Sql_Result().select_fr_channel_config('长银步客Mock')
        if results['code'] == "changYinBuKe":
            update_sql_1 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinBuKeMock_temp' WHERE fr.name = '长银步客Mock';"
            update_sql_2 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinBuKe' WHERE fr.name = '长银步客-测试';"
            update_sql_3 = f"UPDATE finace_router_sit.fr_channel_config as fr SET fr.code = 'changYinBuKeMock' WHERE fr.name = '长银步客Mock';"
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

    # 插入最新跑出来的测试报告数据
    def insert_test_report_data(self, report_name, report_lob, funds_info, report_time, report_dir, case_pass_rate,
                                case_sum, case_pass_sum, case_fail_sum, case_broken_sum, case_unknown_sum,
                                case_skip_sum, status,
                                test_db="auto", ):
        # 原错误SQL应修改为：
        insert_sql = f"""
        INSERT INTO automation_test_result.test_report_result 
        (report_name, report_lob, funds_info, report_time, leader, report_dir, 
         case_pass_rate, case_sum, case_pass_sum, case_fail_sum, case_broken_sum, 
         case_unknown_sum, case_skip_sum, status) 
        VALUES (
            '{report_name}',       # 字符串添加单引号
            '{report_lob}',        # 字符串添加单引号 
            '{funds_info}',        # 字符串添加单引号
            '{report_time}',       # 格式化时间
            'admin',               # 固定值保持原样
            '{report_dir}',        # 路径
            '{case_pass_rate}%',   # 通过率
            {case_sum},            # 用例总数
            {case_pass_sum},       # 通过用例数
            '{case_fail_sum}',     # 失败用例数
            '{case_broken_sum}',   # 故障用例数
            '{case_unknown_sum}',  # 未知用例数
            '{case_skip_sum}',      # 跳过用例数
            '{status}'               # 根据status字段类型决定是否加引号（如果是数字则保留原样）
        )
        """
        result = Mysql(test_db).insert_db(insert_sql)
        self.logging.info(f"数据库执行完成!")
        return result

    # 下面几个均是还款计划修改的sql
    # api侧的到期还款，修改计划表，同步的会将批发的也修改
    def api_modify_due_repayment_plan(self, loan_apply_no, term='1', test_db="api"):
        count = 0
        try:
            for current_term in range(int(term), 0, -1):
                count += 1
                start_date = (datetime.datetime.now() - relativedelta(months=count)).strftime('%Y%m%d')
                due_date = (datetime.datetime.now() - relativedelta(months=count - 1)).strftime('%Y%m%d')
                update_sql_plan = f"UPDATE zws_middleware_360.zx_loan_plan_info t SET t.start_date = '{start_date}', t.due_date = '{due_date}' WHERE t.plan_no LIKE '{loan_apply_no}%' AND t.term = '{current_term}';"
                result = Mysql(test_db).update_db(update_sql_plan)
                self.logging.info(f"数据库执行完成! term={current_term}")
            return True
        except Exception as e:

            self.logging.error(f"请求发生错误：{e}")
            return False

    # api侧的到期还款，修改订单表
    def api_modify_due_repayment_loan_note_info(self, loan_apply_no, test_db="api"):
        try:
            update_sql_loan_note_info = f"UPDATE zws_middleware_360.zx_loan_note_info t SET t.loan_time = CONCAT(DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), '%Y%m%d'), RIGHT(t.loan_time, 6)),t.status_time = CONCAT(DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH ), '%Y%m%d'), RIGHT(t.status_time, 6)),t.cash_date = DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH ), '%Y%m%d'),t.inst_date = DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH ), '%Y%m%d') WHERE t.loan_apply_no = '{loan_apply_no}';"
            result = Mysql(test_db).update_db(update_sql_loan_note_info)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # 批发资金侧的到期还款，修改计划表
    def zjly_modify_due_repayment_plan(self, req_seq_no, term='1', test_db="zjly"):
        count = 0
        try:
            for current_term in range(int(term), 0, -1):
                count += 1
                due_date = (datetime.datetime.now() - relativedelta(months=count - 1)).strftime('%Y-%m-%d')
                update_sql_plan = f"UPDATE finace_router_sit.fr_api_repayment_plan t SET t.ps_due_dt = '{due_date}' WHERE t.order_no in (SELECT ord.order_no FROM finace_router_sit.fr_api_order_info ord WHERE ord.req_seq_no IN('{req_seq_no}')) AND t.period = '{current_term}';"
                result = Mysql(test_db).update_db(update_sql_plan)
                self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # 批发资金侧的到期还款，修改订单表
    def zjly_modify_due_repayment_fr_api_order_info(self, req_seq_no, test_db="zjly"):
        try:
            update_sql_order_info = f"UPDATE finace_router_sit.fr_api_order_info t SET t.settle_time = CONCAT(DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), '%Y-%m-%d'), RIGHT(t.settle_time, 9)),t.repay_day = DATE_FORMAT(CURRENT_DATE(), '%Y-%m-%d'),t.apply_dt = DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH ), '%Y-%m-%d') WHERE t.req_seq_no = '{req_seq_no}';"
            result = Mysql(test_db).update_db(update_sql_order_info)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # api侧的提前还当期，修改计划表
    def api_modify_pre_curr_repay_repayment_plan(self, loan_apply_no, term='1', test_db="api"):
        try:
            update_sql_plan = f"UPDATE zws_middleware_360.zx_loan_plan_info t SET t.start_date = DATE_FORMAT(DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), INTERVAL 6 DAY), '%Y%m%d'),t.due_date = DATE_FORMAT(DATE_ADD(CURRENT_DATE(), INTERVAL 6 DAY), '%Y%m%d') WHERE t.plan_no LIKE '{loan_apply_no}%' AND t.term = '{term}';"
            result = Mysql(test_db).update_db(update_sql_plan)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # api侧的提前还当期，修改订单表
    def api_modify_pre_curr_repay_repayment_loan_note_info(self, loan_apply_no, test_db="api"):
        try:
            update_sql_loan_note_info = f"UPDATE zws_middleware_360.zx_loan_note_info t SET t.loan_time = CONCAT(DATE_FORMAT(DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), INTERVAL 6 DAY), '%Y%m%d'), RIGHT(t.loan_time, 6)),t.status_time = CONCAT(DATE_FORMAT(DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), INTERVAL 6 DAY), '%Y%m%d'), RIGHT(t.status_time, 6)),t.cash_date = DATE_FORMAT(DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), INTERVAL 6 DAY), '%Y%m%d'),t.inst_date = DATE_FORMAT(DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), INTERVAL 6 DAY), '%Y%m%d') WHERE t.loan_apply_no = '{loan_apply_no}';"
            result = Mysql(test_db).update_db(update_sql_loan_note_info)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # api侧的提前结清，修改计划表
    def api_modify_pre_due_repayment_plan(self, loan_apply_no, term='1', test_db="api"):
        try:
            update_sql_plan = f"UPDATE zws_middleware_360.zx_loan_plan_info t SET t.start_date = DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), '%Y%m%d'),t.due_date = DATE_FORMAT(DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), INTERVAL 1 MONTH), '%Y%m%d') WHERE t.plan_no LIKE '{loan_apply_no}%' AND t.term = '{term}';"
            result = Mysql(test_db).update_db(update_sql_plan)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # api侧的提前结清，修改订单表
    def api_modify_pre_due_repayment_loan_note_info(self, loan_apply_no, test_db="api"):
        try:
            update_sql_loan_note_info = f"UPDATE zws_middleware_360.zx_loan_note_info t SET t.loan_time = CONCAT(DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), '%Y%m%d'), RIGHT(t.loan_time, 6)),t.status_time = CONCAT(DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), '%Y%m%d'), RIGHT(t.status_time, 6)),t.cash_date = DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), '%Y%m%d'),t.inst_date = DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), '%Y%m%d') WHERE t.loan_apply_no = '{loan_apply_no}';"
            result = Mysql(test_db).update_db(update_sql_loan_note_info)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # api侧的逾期还款，修改计划表
    def api_modify_over_due_repayment_plan(self, loan_apply_no, term='1', compensation_day=3, test_db="api"):
        count = 0
        try:
            for current_term in range(int(term), 0, -1):
                count += 1
                start_date = (datetime.datetime.now() - relativedelta(months=count) - relativedelta(
                    days=compensation_day)).strftime(
                    '%Y%m%d')
                due_date = (datetime.datetime.now() - relativedelta(months=count - 1) - relativedelta(
                    days=compensation_day)).strftime(
                    '%Y%m%d')
                update_sql_plan = f"UPDATE zws_middleware_360.zx_loan_plan_info t SET t.start_date = '{start_date}', t.due_date = '{due_date}' WHERE t.plan_no LIKE '{loan_apply_no}%' AND t.term = '{current_term}';"
                result = Mysql(test_db).update_db(update_sql_plan)
                self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # api侧的逾期还款，修改订单表
    def api_modify_over_due_repayment_loan_note_info(self, loan_apply_no, compensation_day=3, test_db="api"):
        try:
            update_sql_loan_note_info = f"UPDATE zws_middleware_360.zx_loan_note_info t SET t.loan_time = CONCAT(DATE_FORMAT(DATE_SUB(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), INTERVAL {compensation_day} DAY), '%Y%m%d'), RIGHT(t.loan_time, 6)),t.status_time = CONCAT(DATE_FORMAT(DATE_SUB(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH), INTERVAL {compensation_day} DAY), '%Y%m%d'), RIGHT(t.status_time, 6)),t.cash_date = DATE_FORMAT(DATE_SUB(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH ), INTERVAL {compensation_day} DAY), '%Y%m%d'),t.inst_date = DATE_FORMAT(DATE_SUB(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH ), INTERVAL {compensation_day} DAY), '%Y%m%d')WHERE t.loan_apply_no = '{loan_apply_no}';"
            result = Mysql(test_db).update_db(update_sql_loan_note_info)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # 批发资金侧的逾期还款，修改计划表
    def zjly_modify_over_due_repayment_plan(self, req_seq_no, term='1', compensation_day=3, test_db="zjly"):
        count = 0
        try:
            for current_term in range(int(term), 0, -1):
                count += 1
                due_date = (datetime.datetime.now() - relativedelta(months=count - 1) - relativedelta(
                    days=compensation_day)).strftime(
                    '%Y-%m-%d')
                update_sql_plan = f"UPDATE finace_router_sit.fr_api_repayment_plan t SET t.ps_due_dt = '{due_date}' WHERE t.order_no in(SELECT ord.order_no FROM finace_router_sit.fr_api_order_info ord WHERE ord.req_seq_no IN('{req_seq_no}')) AND t.period = '{current_term}';"
                result = Mysql(test_db).update_db(update_sql_plan)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # 批发资金侧的逾期还款，修改订单表
    def zjly_modify_over_due_repayment_fr_api_order_info(self, req_seq_no, test_db="zjly"):
        try:
            update_sql_order_info = f"UPDATE finace_router_sit.fr_api_order_info t SET t.settle_time = CONCAT(DATE_FORMAT(DATE_SUB(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH),INTERVAL 3 DAY), '%Y-%m-%d'), RIGHT(t.settle_time, 9)),t.repay_day = DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY ), '%Y-%m-%d'),t.apply_dt = DATE_FORMAT(DATE_SUB(DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH ), INTERVAL 3 DAY ), '%Y-%m-%d')WHERE t.req_seq_no = '{req_seq_no}';"
            result = Mysql(test_db).update_db(update_sql_order_info)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # 批发资金侧的提前结清，修改计划表
    def zjly_modify_pre_due_repayment_plan(self, req_seq_no, term='1', test_db="zjly"):
        try:
            update_sql_plan = f"UPDATE finace_router_sit.fr_api_repayment_plan t SET t.ps_due_dt = DATE_FORMAT(DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), INTERVAL 1 MONTH), '%Y-%m-%d') WHERE t.order_no in(SELECT ord.order_no FROM finace_router_sit.fr_api_order_info ord WHERE ord.req_seq_no IN('{req_seq_no}')) AND t.period = '{term}';"
            result = Mysql(test_db).update_db(update_sql_plan)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # 批发资金侧的提前结清，修改订单表
    def zjly_modify_pre_due_repayment_fr_api_order_info(self, req_seq_no, test_db="zjly"):
        try:
            update_sql_order_info = f"UPDATE finace_router_sit.fr_api_order_info t SET t.settle_time = CONCAT(DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), '%Y-%m-%d'), RIGHT(t.settle_time, 9)),t.repay_day = DATE_FORMAT(CURRENT_DATE(), '%Y-%m-%d'),t.apply_dt = DATE_FORMAT(DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY ), '%Y-%m-%d') WHERE t.req_seq_no = '{req_seq_no}';"
            result = Mysql(test_db).update_db(update_sql_order_info)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # 修改还款计划，根据申请单号进行(仅针对测试平台)
    def modify_repayment_plan(self, loan_apply_no, bill_type, term='1', compensatory='True', compensation_day=3):
        db = Update_Sql_Result()
        # 先判断借据存不存在，后续优化判断是否借款成功的借据
        loan_resp = Select_Sql_Result().select_api_zx_loan_apply_record_tools(loan_apply_no)
        loan_no = loan_resp[0]['loan_no']
        self.logging.info(f"查询到的loan_no为：{loan_resp}")
        if loan_resp:
            # 判断传进来的是什么类型
            # 到期还款
            if bill_type == "due_repay":
                try:
                    db.api_modify_due_repayment_plan(loan_apply_no, term)
                    db.api_modify_due_repayment_loan_note_info(loan_apply_no)
                    db.zjly_modify_due_repayment_plan(loan_no, term)
                    db.zjly_modify_due_repayment_fr_api_order_info(loan_no)
                    return True
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    return False
            # 提前还当期
            elif bill_type == "pre_curr_repay":
                try:
                    db.api_modify_pre_curr_repay_repayment_plan(loan_apply_no, term)
                    db.api_modify_pre_curr_repay_repayment_loan_note_info(loan_apply_no)
                    db.zjly_modify_due_repayment_plan(loan_no, term)
                    db.zjly_modify_due_repayment_fr_api_order_info(loan_no)
                    return True
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    return False
            # 提前结清
            elif bill_type == "pre_repay":
                try:
                    db.api_modify_pre_due_repayment_plan(loan_apply_no, term)
                    db.api_modify_pre_due_repayment_loan_note_info(loan_apply_no)
                    db.zjly_modify_pre_due_repayment_plan(loan_no, term)
                    db.zjly_modify_pre_due_repayment_fr_api_order_info(loan_no)
                    return True
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    return False
            # 逾期还款
            elif bill_type == "over_due_repay":
                try:
                    db.api_modify_over_due_repayment_plan(loan_apply_no, term, compensation_day)
                    db.api_modify_over_due_repayment_loan_note_info(loan_apply_no, compensation_day)
                    db.zjly_modify_over_due_repayment_plan(loan_no, term, compensation_day)
                    db.zjly_modify_over_due_repayment_fr_api_order_info(loan_no)
                    return True
                except Exception as e:
                    self.logging.error(f"请求发生错误：{e}")
                    return False
        else:
            self.logging.info(f"没有找到数据，该笔数据可能掉单，请检查数据库！")
            return False

    # 修改 zl_file_info 表需要重签的文件为假删状态
    def modify_file_info_status(self, loan_apply_no, test_db='api'):
        try:
            update_sql_file_info = f"UPDATE zws_middleware_360.zl_file_info t SET t.del_flag = 1 WHERE t.loan_apply_no = '{loan_apply_no}';"
            result = Mysql(test_db).update_db(update_sql_file_info)
            self.logging.info(f"数据库执行完成!")
            return True
        except Exception as e:
            self.logging.error(f"请求发生错误：{e}")
            return False

    # 修改 funds_loan_info 签章状态为PSL
    def modify_funds_loan_info_status(self, loan_apply_no, test_db='api'):
        try:
            update_sql_loan_info = f"UPDATE zws_middleware_360.funds_loan_info fl SET fl.sign_status = 'PSL' WHERE fl.loan_apply_no = '{loan_apply_no}';"
            result = Mysql(test_db).update_db(update_sql_loan_info)
            self.logging.info(f"数据库执行完成！")
            return True
        except Exception as e:
            self.logging.info(f"请求发生异常：{e}")
            return False

    # 修改 zx_loan_apply_record 签章状态为PSL
    def modify_zx_loan_apply_record_status(self, loan_apply_no, test_db='api'):
        try:
            update_sql_loan_apply_record = f"UPDATE zws_middleware_360.zx_loan_apply_record lp SET lp.sign_status = 'PSL' WHERE lp.loan_apply_no = '{loan_apply_no}';"
            result = Mysql(test_db).update_db(update_sql_loan_apply_record)
            self.logging.info(f"数据库执行完成！")
            return True
        except Exception as e:
            self.logging.info(f"请求发生异常：{e}")
            return False

    # 修改 zl_file_job_info 签章状态为W
    def modify_zl_file_job_info_status(self, loan_apply_no, test_db='api'):
        try:
            update_sql_file_job_info = f"UPDATE zws_middleware_360.zl_file_job_info fj SET fj.status = 'W' WHERE fj.file_serial_no = '{loan_apply_no}' AND fj.file_job_type IN ('9','3');"
            result = Mysql(test_db).update_db(update_sql_file_job_info)
            self.logging.info(f"数据库执行完成！")
            return True
        except Exception as e:
            self.logging.info(f"请求发生异常：{e}")
            return False

    # 集合修改签章协议文件相关表
    def modify_funds_sign_files(self, loan_apply_no, test_db='api'):
        # 依次修改各个表
        try:
            self.modify_file_info_status(loan_apply_no)
            self.modify_funds_loan_info_status(loan_apply_no)
            self.modify_zx_loan_apply_record_status(loan_apply_no)
            self.modify_zl_file_job_info_status(loan_apply_no)
            self.logging.info(f"已全部修改完成！")
            return True
        except Exception as e:
            self.logging.info(f"请求发生异常：{e}")
            return False


if __name__ == '__main__':
    # user_id = "ZLTEST_202410161729069481126"
    # funds_code = "FR_RUN_LOU"
    db = Update_Sql_Result()
    print(db.modify_zl_file_job_info_status('SLN2220300580'))
    # results = Select_Sql_Result().select_fr_channel_config('中原提钱花MOCK')
    # print()
    # if 'mock'.lower() not in results['code'].lower():
    #     print("当前是mock环境")
    # else:
    #     print("当前是测试环境")
    # print((datetime.datetime.now() - relativedelta(months=1)).strftime("%Y-%m-%d %H:%M:%S"))
