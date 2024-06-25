import cv2
import numpy as np
import os
import shutil

# 使用示例
image_path ="D:\\aimbot\data\datasets\\1.png"
image = cv2.imread(image_path)
print(image_path)

# 分离颜色通道
b, g, r = cv2.split(image)

# 创建一个黑色图像
output_image = np.zeros_like(image)

# 条件掩码：r > 100 and g < 60 and b < 60
mask = (r > 180) & (g < 100) & (b < 100)

# 应用掩码到输出图像
output_image[mask] = image[mask]

output_path ="D:\\aimbot\data\datasets\\1_res.png"
cv2.imwrite(output_path, output_image)