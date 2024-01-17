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
import os
import re

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0 # previous time
cTime = 0 # current time
vol = 0
volBar = 400
volume = 0
area = 0

detector = htm.handDetector(detectionCon=0.7)


def get_volume():
    try:
        # Run the amixer command to get the current volume
        result = os.popen("amixer sget Master").read()

        # Use regular expression to extract the volume percentage
        volume_match = re.search(r'\[(\d+)%\]', result)
        if volume_match:
            return int(volume_match.group(1))
        else:
            print("Unable to parse volume.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None




while True:
    success, img = cap.read()
    
    
    # Find Hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)
    if len(lmList) != 0:    
        
        # Filter based on size
        area = (bbox[2]-bbox[0])* (bbox[3]-bbox[1])//100 # width and height of the bounding box
        
        if 250 < area < 1000:
            #print("yes")
            # Find distance between index and thumb
            length, img, lineInfo = detector.findDistance(4,8,img)
            
            # Convert volume
            vol = np.interp(length, [50,180], [0,100])
            volBar = np.interp(length, [50,200], [400,150])
            volume = int(vol)
            
            # Reduce resolution to make it smoother
            smoothness = 5
            volume = smoothness * round(volume/smoothness)
            
            # Check fingers up
            fingers = detector.fingerUp()
            #print(fingers)
            
            # if pinky is down set volume
            if not fingers[4]:
                # Windows
                # volume.SetMasterVolumeLevelScalar(volume/100, None)
                # Linux
                cv2.circle(img, (lineInfo[4],lineInfo[5]), 15, (0,255,0), cv2.FILLED)
        
                call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
            # Drawings
            #if 'DISPLAY' in os.environ:
            # volume bar      
            cv2.rectangle(img, (50,150), (85,400), (255,0,0), 3) 
            cv2.rectangle(img, (50, int(volBar)), (85,400), (255,0,0), cv2.FILLED)
            cv2.putText(img, f'{volume}%', (40,450), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)  # img, %, position, font, scale, color, thickness
            cVol = get_volume()
            cv2.putText(img, f'Volume Set: {int(cVol)}', (450,30), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2) 
            
            # Frame rate
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            #if 'DISPLAY' in os.environ:
            cv2.putText(img, f'FPS: {int(fps)}', (20,30), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)  # img, fps, position, font, scale, color, thickness
    
        

            cv2.imshow("Image", img)
    cv2.waitKey(1)