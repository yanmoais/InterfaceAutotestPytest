from datetime import datetime


def calculate_id_card_info(apply_age):
    # 有效期判断
    if apply_age < 16:
        validity = 5
    elif 16 <= apply_age <= 25:
        validity = 10
    elif 26 <= apply_age <= 45:
        validity = 20
    else:
        validity = "长期"

    # 计算到期日
    if validity == "长期":
        expiry_date = datetime(2099, 12, 31)
        validity_years = 46  # 用于计算签发年份的基准
    else:
        expiry_date = datetime(2026, 3, 25)
        validity_years = validity

    # 计算签发日期（起始日期）
    start_date = datetime(expiry_date.year - validity_years, expiry_date.month, expiry_date.day)

    # 计算出生日期（签发年份 - 申请年龄）
    birth_year = start_date.year - apply_age
    birth_date = datetime(birth_year, 3, 25)

    # 格式化输出
    return (
        f"{apply_age}岁申请 | {validity}年有效期 | "
        f"出生日期：{birth_date.strftime('%Y%m%d')} | "
        f"起始日期：{start_date.strftime('%Y.%m.%d')} | "
        f"到期日：{expiry_date.strftime('%Y.%m.%d')}"
    )


# 使用示例
if __name__ == "__main__":
    print(calculate_id_card_info(16))  # 15岁申请
    print(calculate_id_card_info(25))  # 25岁申请
    print(calculate_id_card_info(26))  # 26岁申请
    print(calculate_id_card_info(46))  # 46岁申请