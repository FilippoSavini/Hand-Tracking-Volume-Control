import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
# Windows
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# Linux
from subprocess import call


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0 # previous time
cTime = 0 # current time
vol = 0
volBar = 400
volume = 0

detector = htm.handDetector(detectionCon=0.7)


while True:
    success, img = cap.read()
    
    # Find Hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)
    if len(lmList) != 0:    

        x1, y1 = lmList[4][1], lmList[4][2] # tip of the thumb
        x2, y2 = lmList[8][1], lmList[8][2] # tip of the index finger
        cx, cy = (x1+x2)//2, (y1+y2)//2 # center of the line between the thumb and the index finger
        
        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3) # line between the thumb and the index finger
        cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
        
        length = math.hypot(x2-x1, y2-y1)
        
        # Hand range 50 - 200
        # Volume range 0 - 100
        
        vol = np.interp(length, [50,200], [0,100])
        volBar = np.interp(length, [50,200], [400,150])
        volume = int(vol)
        call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
        
        if length < 50:
            cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)
        
    # volume bar      
    cv2.rectangle(img, (50,150), (85,400), (0,255,0), 3) 
    cv2.rectangle(img, (50, int(volBar)), (85,400), (0,255,0), cv2.FILLED)
    cv2.putText(img, f'{volume}%', (40,450), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)  # img, %, position, font, scale, color, thickness
    
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img, f'FPS: {int(fps)}', (20,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)  # img, fps, position, font, scale, color, thickness
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)