import cv2
import numpy as np
import os
import shutil
import os

def rename_files_in_directory(directory):
    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(directory):
        # 检查文件名是否以“屏幕截图 ”开头
        if filename.startswith("屏幕截图 "):
            # 新的文件名去掉“屏幕截图 ”前缀
            new_filename = filename.replace("屏幕截图 ", "", 1)
            # 获取完整的旧文件路径和新文件路径
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            # 重命名文件
            os.rename(old_file, new_file)
            print(f'Renamed: {old_file} to {new_file}')
    

def process_images(input_dir, output_dir):
    """处理目录中的所有图像，保留偏红色部分"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        new_filename=filename
        if new_filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            image_path = os.path.join(input_dir, new_filename)
            image = cv2.imread(image_path)
            print(image_path)

            # 分离颜色通道
            b, g, r = cv2.split(image)

            # 创建一个黑色图像
            output_image = np.zeros_like(image)

            # 条件掩码：r > 100 and g < 60 and b < 60
            mask = (r > 100) & (g < 80) & (b < 80)

            # 应用掩码到输出图像
            output_image[mask] = image[mask]

            output_path = os.path.join(output_dir, new_filename)
            cv2.imwrite(output_path, output_image)
        else:
            src_label_path=os.path.join(input_dir,filename)
            dst_label_path=os.path.join(output_dir,new_filename)
            shutil.copy(src_label_path, dst_label_path)

# 使用示例
input_directory = 'D:\\aimbot\data\datasets\data\overwatch.v2i.yolov8_without_friend\\test\images'
output_directory = 'D:\\aimbot\data\datasets\data\overwatch.v2i.yolov8_without_friend\\test\images'
rename_files_in_directory(input_directory)
process_images(input_directory, output_directory)
