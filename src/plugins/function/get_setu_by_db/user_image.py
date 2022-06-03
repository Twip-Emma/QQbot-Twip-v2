'''
Author: 七画一只妖
Date: 2022-05-30 21:27:03
LastEditors: 七画一只妖
LastEditTime: 2022-06-03 15:18:49
Description: file content
'''
import os
from io import BytesIO
from PIL import Image


# 当前路径
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


# 获取当前路径下的所有文件路径
def get_all_files(path):
    files = os.listdir(path)
    file_paths = []
    for item in files:
        file_path = f"{path}\\{item}"
        file_paths.append(file_path)
    return file_paths


# 传入图片路径，将改图片转bytes，用BytesIO
def image_to_bytes(image_path):
    with open(image_path, "rb") as f:
        image_bytes = BytesIO(f.read())
    return image_bytes.getvalue()


# 将bytes转图片
def bytes_to_image(image_bytes, image_name, db_name):
    bytes_stream = BytesIO(image_bytes)
    image = Image.open(bytes_stream)
    image.save(f"{BASE_PATH}\\images\\{db_name}.jpg")
    return f"{BASE_PATH}\\images\\{db_name}.jpg"
    
    

# a = image_to_bytes(f"{BASE_PATH}\\image\\97972911_p0.jpg")
# print(a.getvalue())
# bytes_to_image(a.getvalue(), "test2.jpg")