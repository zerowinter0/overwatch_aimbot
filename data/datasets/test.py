from PIL import Image
from ultralytics import YOLO
import cv2
import numpy as np
if __name__ == '__main__':
# Load a pretrained YOLOv8n model
    image_path='D:\\aimbot\data\datasets\\1.png'
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

    output_path=image_path
    cv2.imwrite(output_path, output_image)

