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
    while True:
        #time.sleep(1)
        if aimbot_key():
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            image = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            b, g, r = cv2.split(image)
            output_image = np.zeros_like(image)
            # 条件掩码：r > 100 and g < 60 and b < 60
            mask = (r > 100) & (g < 60) & (b < 60)
            # 应用掩码到输出图像
            output_image[mask] = image[mask]

            results = model.predict(output_image,verbose=False)

            result=results[0]
            x=-10000
            y=-10000
            cls=0
            conf=0
            for box in result.boxes:
                    if(box.cls>1):
                        continue
                #if box.cls == 0:  # 如果是person类别
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    new_cls=box.cls
                    new_conf = box.conf.cpu().numpy()
                    if(new_conf<0.2):
                        continue
                    new_x=(int)((x1+x2)/2)
                    new_y=(int)((y1+y2)/2)
                    if(new_cls>cls or (new_cls==cls and ((new_x+new_y-target_x-target_y)<(x+y-target_x-target_y) or x==-10000))):
                        cls=new_cls
                        x=(int)((x1+x2)/2)
                        y=(int)((y1+y2)/2)
            if(abs(x)+abs(y)<5 or x==-10000):
                 #print("no")
                 continue
            else:
                 #print(cls,conf)
                 final_x=x-target_x
                 final_y=y-target_y
                 final_x=int(final_x*0.25)
                 final_y=int(final_y*0.25)
                 print(final_x,final_y," ",cls)
                 #pydirectinput.move(final_x,final_y)
                 win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,final_x,final_y)
            
            #else:time.sleep(1)
launch()