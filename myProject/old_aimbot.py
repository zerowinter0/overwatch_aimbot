import numpy as np
import cv2
import mss
import mss.tools
import ctypes
import pyautogui
import time
import win32api
import threading
import sys
import random
import win32con
from ultralytics import YOLO
from win32con import MOUSEEVENTF_WHEEL
from pynput.mouse import Controller
import os
import pydirectinput

pyautogui.FAILSAFE =False  
#pyautogui.PAUSE = 1    
# print(pyautogui.size())   # 返回所用显示器的分辨率； 输出：Size(width=1920, height=1080)
# width,height = pyautogui.size()
# for i in range(0,5):
#     time.sleep(1)
#     print(width,height)  # 1920 1080
#     print(pyautogui.position())   # 得到当前鼠标位置；输出：Point(x=200, y=800)

target_x=1280
target_y=720

# for i in range(0,10):
#     #pyautogui.moveTo(100,300,duration=0.001)   
#     pyautogui.moveTo(1000,300,duration=0.001)   
#     pyautogui.click(100,300,button='left')

def aimbot_key():
    return 1
    #return win32api.GetAsyncKeyState(0x01) & 0x8000 != 0

model=YOLO("D:/aimbot/myProject/best.pt")
sct=mss.mss()
monitor = sct.monitors[2]
cnt=0
def launch():
    # file_path = os.path.abspath(os.path.dirname(__file__)) # 当前路径
    # dll = ctypes.CDLL(f'{file_path}/logitech_driver.dll') # 打开路径文件
    # state = (dll.device_open() == 1) # 启动, 并返回是否成功
    # WAIT_TIME = 0.5 # 等待时间
    # RANDOM_NUM = 0.1 # 最大时间随机数
    # if not state:
    #     print('错误, 未找到GHUB或LGS驱动程序')
    while True:
        #time.sleep(1)
        if aimbot_key():
            screenshot = sct.grab(monitor)
            #mss.tools.to_png(screenshot.rgb, screenshot.size, output='D:/aimbot/myProject/screenshot'+str(cnt)+'.png')
            # pyautogui.moveTo(100,300,duration=0.001)
            # pyautogui.moveTo(1000,300,duration=0.001)

            # 将截图转换为numpy数组
            img = np.array(screenshot)

            # 将BGRA转换为BGR（OpenCV格式）
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            results = model.predict(img,verbose=False)

            for result in results:
                x=-1
                y=-1
                cls=0
                conf=0
                for box in result.boxes:
                    #if box.cls == 0:  # 如果是person类别
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        new_cls=box.cls
                        new_conf = box.conf.cpu().numpy()
                        if(new_cls>cls or (new_cls==cls and new_conf>conf)):
                            cls=new_cls
                            conf=new_conf
                            x=(int)((x1+x2)/2)
                            y=(int)((y1+y2)/2)
            if(x==-1 or y==-1):
                 continue
            else:
                 #print(cls,conf)
                 final_x=x-target_x
                 final_y=y-target_y
                 final_x=int(final_x*0.33)
                 final_y=int(final_y*0.33)
                 #print(final_x,final_y)
                 win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,final_x,final_y)
            
            # 按下'q'键退出循环
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            #else:time.sleep(1)
launch()