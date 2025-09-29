import os
import re


def batch_replace(folder_path, old_text, new_text, file_extension='.py'):
    """
    批量替换指定文件夹下所有.py文件中的文本内容

    参数:
        folder_path: 要搜索的文件夹路径
        old_text: 要替换的旧文本(支持正则表达式)
        new_text: 替换后的新文本
        file_extension: 文件扩展名，默认为.py
    """
    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                try:
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 替换内容
                    new_content = re.sub(old_text, new_text, content)

                    # 如果内容有变化，则写入文件
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已修改文件: {file_path}")
                    else:
                        print(f"无需修改: {file_path}")

                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {str(e)}")


if __name__ == "__main__":
    # 使用示例
    folder_to_search = r"D:\interface-autotest-pytest"
    text_to_replace = r'finance_router'
    replacement_text = r'finace_router_sit'

    batch_replace(folder_to_search, text_to_replace, replacement_text)
