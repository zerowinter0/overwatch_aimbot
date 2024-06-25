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
import keyboard
target_x=1280
target_y=720

# target_x=320
# target_y=320

def aimbot_key():
    return 1
    #return win32api.GetAsyncKeyState(0x01) & 0x8000 != 0
#model=YOLO(r"D:\aimbot\train4\weights\best.pt")
model=YOLO("D:/aimbot/myProject/final_8n_best.pt")
sct=mss.mss()
monitor = sct.monitors[2]
COLORS = np.random.uniform(0, 255, size=(1500, 3))
def launch():
    aimbot_key=True
    cnt=0
    while True:
        if aimbot_key:
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            #img=cv2.resize(img,(640,640))
            img=cv2.resize(img,(int(2560/2),int(1440/2)))
            #results = model.predict(img)
            results = model.predict(img,verbose=False)

            # image = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            # b, g, r = cv2.split(image)
            # output_image = np.zeros_like(image)
            # # 条件掩码：r > 100 and g < 60 and b < 60
            # mask = (r > 100) & (g < 80) & (b < 80)
            # # 应用掩码到输出图像
            # output_image[mask] = image[mask]

            # results = model.predict(output_image,verbose=False)

            result=results[0]
            x=-10000
            y=-10000
            cls=0
            conf=0
            for box in result.boxes:
                    if(box.cls!=1):
                        continue
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    new_cls=box.cls
                    new_conf = box.conf.cpu().numpy()
                    if(new_conf<0.5):
                        continue
                    else:
                        print(new_conf)
                    new_x=(int)((x1+x2)/2)
                    new_y=(int)((y1+y2)/2)
                    cv2.rectangle(img,(x1,y1), (x2,y2),COLORS[0], 2)

                    if(((new_x-target_x)*(new_x-target_x)+(new_y-target_y)*(new_y-target_y))
                       <(x-target_x)*(x-target_x)+(y-target_y)*(y-target_y)
                         or x==-10000):
                        cls=new_cls
                        x=new_x
                        y=new_y
                        print(x,y)

            if(x==-10000):
                 cnt+=1
                 img=result.plot()
                 cv2.imshow('Live Feed', img)
                 if (cv2.waitKey(1) & 0xFF) == ord('q'):
                    exit()
                 if(cnt==10):
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)#抬起
                 continue
            else:
                cnt=0
                #print(cls,conf)
                final_x=x-target_x
                final_y=y-target_y
                final_x=int(final_x*0.6)
                final_y=int(final_y*0.6)
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,final_x,final_y)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)#按下
                img=result.plot()
                cv2.imshow('Live Feed', img)
                if (cv2.waitKey(1) & 0xFF) == ord('q'):
                    exit()
                #time.sleep(3)
launch()