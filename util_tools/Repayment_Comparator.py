#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午6:26


import pandas as pd
import pymysql
from sqlalchemy import create_engine
import numpy as np
from util_tools.Read_Yaml import read_db_yaml


class RepaymentPlanComparator:
    def __init__(self):
        # 数据库连接配置
        config = read_db_yaml()
        self.db_config = {
            'host': config['api']['api_flow']['host'],
            'user': config['api']['api_flow']['username'],
            'port': config['api']['api_flow']['port'],
            'password': config['api']['api_flow']['password'],
            'database': config['api']['api_flow']['db_name']
        }

    def get_db_data(self, loan_apply_no):
        """从数据库获取还款计划数据"""
        try:
            # 创建数据库连接
            engine = create_engine(
                f'mysql+pymysql://{self.db_config["user"]}:{self.db_config["password"]}@{self.db_config["host"]}:{self.db_config["port"]}/{self.db_config["database"]}'
            )

            # SQL查询 - 使用参数化查询
            query = """
                SELECT term, prin_amt, int_amt, guarantee_amt, advice_amt 
                FROM zws_middleware_360.zx_loan_plan_info 
                WHERE plan_no LIKE %(pattern)s 
                ORDER BY term
            """

            # 构造 LIKE 模式
            pattern = f"{loan_apply_no}%"

            # 读取数据到DataFrame，使用参数字典
            db_data = pd.read_sql(query, engine, params={'pattern': pattern})
            return db_data

        except Exception as e:
            print(f"数据库查询错误: {str(e)}")
            return None

    def read_excel_data(self, excel_path, sheet_name=0):
        """读取Excel文件数据"""
        try:
            # 读取Excel文件
            excel_data = pd.read_excel(excel_path, sheet_name=sheet_name)

            # 确保列名匹配
            column_mapping = {
                '期数': 'term',
                '应还本金': 'prin_amt',
                '应还利息': 'int_amt',
                '担保费': 'guarantee_amt',
                '咨询费': 'advice_amt'
            }

            excel_data = excel_data.rename(columns=column_mapping)
            return excel_data

        except Exception as e:
            print(f"Excel读取错误: {str(e)}")
            return None

    def compare_data(self, db_data, excel_data, tolerance=0.01):
        """比较数据库和Excel数据"""
        if db_data is None or excel_data is None:
            return False, "数据读取失败"

        # 确保数据按期数排序
        db_data = db_data.sort_values('term')
        excel_data = excel_data.sort_values('term')

        # 检查期数是否匹配
        if len(db_data) != len(excel_data):
            return False, f"期数不匹配: 数据库{len(db_data)}期 vs Excel{len(excel_data)}期"

        # 比较每个字段
        comparison_results = []
        columns_to_compare = ['prin_amt', 'int_amt', 'guarantee_amt', 'advice_amt']

        for term in db_data['term'].unique():
            db_row = db_data[db_data['term'] == term].iloc[0]
            excel_row = excel_data[excel_data['term'] == term].iloc[0]

            term_differences = []
            for col in columns_to_compare:
                db_value = float(db_row[col])
                excel_value = float(excel_row[col])

                # 检查差异是否在容差范围内
                if abs(db_value - excel_value) > tolerance:
                    term_differences.append({
                        'field': col,
                        'db_value': db_value,
                        'excel_value': excel_value,
                        'difference': db_value - excel_value
                    })

            if term_differences:
                comparison_results.append({
                    'term': term,
                    'differences': term_differences
                })

        return len(comparison_results) == 0, comparison_results

    def generate_report(self, comparison_results):
        """生成对比报告"""
        if isinstance(comparison_results, bool):
            return "数据完全匹配" if comparison_results else "对比失败"

        report = []
        report.append("还款计划对比报告")
        report.append("=" * 50)

        for result in comparison_results:
            term = result['term']
            report.append(f"\n第{term}期存在差异:")

            for diff in result['differences']:
                report.append(f"  {diff['field']}:")
                report.append(f"    数据库值: {diff['db_value']:.2f}")
                report.append(f"    Excel值: {diff['excel_value']:.2f}")
                report.append(f"    差异: {diff['difference']:.2f}")

        return "\n".join(report)


# 使用示例
if __name__ == "__main__":
    # 初始化比较器
    comparator = RepaymentPlanComparator()

    # 获取数据
    loan_no = 'SLN7070352051'
    db_data = comparator.get_db_data(loan_no)
    print(db_data)
    # excel_data = comparator.read_excel_data('path_to_your_excel.xlsx')
    #
    # # 比较数据
    # is_match, results = comparator.compare_data(db_data, excel_data)
    #
    # # 生成报告
    # report = comparator.generate_report(results)
    # print(report)
