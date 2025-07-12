import random


# 读取现有手机号
def read_existing_numbers(filename):
    with open(filename, 'r') as f:
        return set(line.strip() for line in f)


# 生成新的手机号
def generate_new_phone_number():
    return '153' + ''.join(random.choices('0123456789', k=8))


# 生成不重复的新手机号
def generate_unique_numbers(existing_numbers, count):
    new_numbers = set()
    while len(new_numbers) < count:
        new_num = generate_new_phone_number()
        if new_num not in existing_numbers and new_num not in new_numbers:
            new_numbers.add(new_num)
    return new_numbers


if __name__ == '__main__':

    # 主程序
    try:
        # 读取现有号码
        existing_numbers = read_existing_numbers(r'D:\interface-autotest-pytest\testdata\risk_phone\user_phone.txt')

        # 生成1000个新号码（你可以修改这个数量）
        new_numbers = generate_unique_numbers(existing_numbers, 10000)

        # 写入新文件
        with open(r'D:\interface-autotest-pytest\testdata\risk_phone\user_phone_2.txt', 'w') as f:
            for number in sorted(new_numbers):
                f.write(number + '\n')

        print(f"成功生成 {len(new_numbers)} 个新手机号并写入 user_phone_2.txt")

    except FileNotFoundError:
        print("找不到源文件")
    except Exception as e:
        print(f"发生错误: {str(e)}")

