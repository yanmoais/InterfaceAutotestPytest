"""
    读取Excel文件的方法
"""
from openpyxl import load_workbook
from config.Base_Env import *


class read_excel():
    def __init__(self, excle_file=CASE_FILE_PATH, sheet_name=SHEET_NAME_PATH):
        self.excel_obj = load_workbook(excle_file)
        self.sheet_obj = self.excel_obj[sheet_name]

    def _get_title_and_data(self):
        case_datas = list(self.sheet_obj.iter_rows(values_only=True))
        case_title, case_data = case_datas[0], case_datas[1:]
        return case_title, case_data

    def _close_excel(self):
        self.excel_obj.close()

    def _save_excel(self):
        pass

    def get_case_data(self):
        case_data_list = []
        case_title, case_data = self._get_title_and_data()
        for result in case_data:
            json_data = dict(zip(case_title, result))
            case_data_list.append(json_data)
        return case_data_list


if __name__ == '__main__':
    sheet_obj = read_excel()
    print(sheet_obj.get_case_data())
