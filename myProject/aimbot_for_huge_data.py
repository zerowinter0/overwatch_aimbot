import numpy as np
import cv2
import mss
import mss.tools
import win32api
import win32con
from ultralytics import YOLO

def launch(auto_shoot):
    cnt=0
    target_x=320
    target_y=320

    model=YOLO("D:\\aimbot\myProject\huge_data.pt")
    sct=mss.mss()
    monitor = sct.monitors[2]
    while True:
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img=cv2.resize(img,(640,640))
        results = model.predict(img,verbose=False)
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
                cv2.imshow('检测结果', img)
                if (cv2.waitKey(1) & 0xFF) == ord('q'):
                    exit()
                if(cnt==10 and auto_shoot):
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
            if(auto_shoot):
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)#按下
            img=result.plot()
            cv2.imshow('检测结果', img)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                exit()
if __name__=='__main__':
    launch(0)