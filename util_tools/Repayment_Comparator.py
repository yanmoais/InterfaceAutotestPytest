import logging
import os

import pandas as pd
from flask import jsonify


def get_excel_repayment_plan():
    try:
        # 读取 Excel 文件
        excel_file_path = os.path.join('testdata', 'test_case_excel', 'excle_repayment_plan.xlsx')
        df = pd.read_excel(excel_file_path)

        # 获取首行字段
        headers = df.columns.tolist()

        # 将数据转换为字典列表，每行一个字典
        data = df.to_dict(orient='records')

        # 渲染到前端的数据结构
        result = {
            "headers": headers,
            "data": data
        }

        return jsonify(result)

    except Exception as e:
        logging.error(f"查询出错: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    ss = get_excel_repayment_plan()
    print(ss)
