import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands # max number of hands
        self.detectionCon = detectionCon # detection confidence
        self.trackCon = trackCon # tracking confidence
        self.lmList = []
        self.tipIds = [4,8,12,16,20] # tip of the fingers
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
    
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img
    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        
        self.lmList = []
    
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark): # id is the index of the landmark, lm is the landmark
                # print(id ,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h) # center of the landmark
                xList.append(cx)
                yList.append(cy)
                
                self.lmList.append([id, cx, cy])
                # if draw:
                #     cv2.circle(img, (cx,cy), 15, (0,0,255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
            
            if draw:
                cv2.rectangle(img, (bbox[0]-20,bbox[1]-20), (bbox[2]+20,bbox[3]+20), (0,255,0), 2)
            
        return self.lmList, bbox
    
    def fingerUp(self):
        fingers = []
        # Each finger has 2 values, 1 means up, 0 means down
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    
    def findDistance(self, p1, p2, img, draw=True):
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        
        if draw:
            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3) # line between the thumb and the index finger
            cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
        
        length = math.hypot(x2-x1, y2-y1)
        return length, img, [x1,y1,x2,y2,cx,cy]
      
def main():
    cap = cv2.VideoCapture(0)
    pTime = 0 # previous time
    cTime = 0 # current time
    detector = handDetector()
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4]) # tip of the thumb
            print(lmList[8]) # tip of the index finger
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
    
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)  # img, fps, position, font, scale, color, thickness
    
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    
if __name__ == "__main__": 
    main()