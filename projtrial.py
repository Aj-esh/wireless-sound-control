import cv2
import numpy as np
import mediapipe as mp
import math 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()


 
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

while True:
    sucess , im = cap.read()
    img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmlist=[]
            for id, lm in enumerate(handLms.landmark):
                
                h ,w ,c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)
                lmlist.append([id,cx,cy])
                
            if lmlist:    
                tx , ty , fx , fy = lmlist[4][1] , lmlist[4][2] , lmlist[8][1] , lmlist[8][2] 
                cv2.circle( img , ( tx , ty ) , 15 , (120,220,210) , cv2.FILLED  ) 
                cv2.circle( img , ( fx , fy ) , 15 , (120,220,210) , cv2.FILLED  )
                cv2.line(img, (tx,ty) , (fx,fy) , (130,123,260) ,10 )
    
                ln = math.hypot(tx-fx,ty-fy)
                #print(ln)
                if ln < 30:
                    zx,zy  = (tx+fx)//2,  (fy+ty)//2
                    cv2.circle( img , ( zx , zy ) , 30 , (200,190,120) , cv2.FILLED  ) 

            vrge = volume.GetVolumeRange() 
            m,M = vrge[0], vrge[1]
            vol = np.interp( ln , [30,250] , [m,M] )
            volume.SetMasterVolumeLevel(vol, None)
        dx , dy , Dx , Dy = lmlist[17][1] , lmlist[17][2] , lmlist[20][1] , lmlist[20][2] 
        disc = math.hypot(Dx-dx,Dy-dy)
         
        if disc >=80:
            cv2.circle( img , ( Dx , Dy ) , 15 , (120,220,210) , cv2.FILLED  ) 
            cv2.circle( img , ( dx , dy ) , 15 , (120,220,210) , cv2.FILLED  )
            cv2.line(img, (dx,dy) , (Dx,Dy) , (130,123,260) ,10 ) 
        if disc >110:
            break
    cv2.imshow("cam 1 ",img)
    cv2.waitKey(1)
