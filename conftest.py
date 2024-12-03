# #
# # -*- coding：utf-8 —*-
# # @Author : Blues.Lan
# # Them：Pyhon自动化
# # @Time :  下午3:20
# import pytest
# from config.testconfig import test_files
# from util_tools.Read_Excle import read_excel
#
# import pytest
#
#
# @pytest.fixture(scope="session", autouse=True)
# def case_check_fixture():
#     sheet_obj = read_excel()
#     datas = sheet_obj.get_case_data()
#     case_list = sheet_obj.get_case_private_params(datas, '自动化用例名')
#     path = test_files
#
#     func_list = []
#     for file_path in path:
#         with open(file_path, "r", encoding="UTF-8") as file:
#             func_list.extend(line.split('(')[0][4:] for line in file if line.startswith('def '))
#     not_found_case = [funcs for funcs in case_list if funcs not in func_list]
#
#     for func in case_list:
#         if func in func_list:
#             print(f"预编写案例 {func} 已完成编写！")
#             sheet_obj.write_save_excel(func, "已完成")
#         else:
#             print(f"预编写案例 {func} 未完成编写，或者名称编写是否正确，请检查！")
#             sheet_obj.write_save_excel(func, "未完成")
#
#     if not_found_case:
#         pytest.exit(f"\n存在未编写的案例集 {not_found_case} 请仔细检查是否已完成编写或名称是否正确")
#
#
# def test_example_1():
#     print("这是测试用例1，如果前置成功，打印！")
#
#
# def test_example_2():
#     print("这是测试用例2，如果前置成功，打印！")
