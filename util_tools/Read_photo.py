#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:36
import base64
from config.Base_Env import PHOTO_PATH


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        # 读取图片文件内容
        img_data = img_file.read()
        # 对读取的图片内容进行base64编码
        base64_data = base64.b64encode(img_data)
        # 将bytes类型转换为字符串类型
        base64_str = base64_data.decode('utf-8')
        return base64_str


# 转换身份证正面
def get_positive_photo():
    # 替换为你本地图片的路径
    image_path = PHOTO_PATH + 'zhengmian.png'
    return image_to_base64(image_path)


# 转换身份证反面
def get_negative_photo():
    # 替换为你本地图片的路径
    image_path = PHOTO_PATH + 'fanmian.png'
    return image_to_base64(image_path)


# 转换身份证反面
def get_best_photo():
    # 替换为你本地图片的路径
    image_path = PHOTO_PATH + 'best_photo.png'
    return image_to_base64(image_path)


if __name__ == '__main__':
    # 转换图片为base64编码字符串
    # 打印base64编码字符串
    print(get_negative_photo())
