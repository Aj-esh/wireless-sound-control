
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
disc, off= 1,1

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
                rx , ry , sx , sy = lmlist[0][1] , lmlist[0][2] , lmlist[17][1], lmlist[17][2]

                r = math.hypot((rx-sx),(ry-sy))
                ln = math.hypot((tx-fx)/r,(ty-fy)/r)
            
                if ln >=0.2 and ln<=2.0:
                    cv2.circle( img , ( tx , ty ) , 10 , (235, 163, 21) , cv2.FILLED  ) 
                    cv2.circle( img , ( fx , fy ) , 10 , (235, 163, 21) , cv2.FILLED  )
                    cv2.line(img, (tx,ty) , (fx,fy) , (11,230,22) ,5 )

                elif ln > 2.0:
                    cv2.circle( img , ( tx , ty ) , 10 , (11,230,22) , cv2.FILLED  ) 
                    cv2.circle( img , ( fx , fy ) , 10 , (11,230,22) , cv2.FILLED  )
                    cv2.line(img, (tx,ty) , (fx,fy) , (235, 163, 21) ,5 )

                elif ln < 0.2:
                    zx,zy  = (tx+fx)//2,  (fy+ty)//2
                    cv2.circle( img , ( zx , zy ) , 15 , (235, 163, 21) , cv2.FILLED  )
            
            
            if disc < 0.8: break

            if ln >=0.2 and ln<=2.0:
                vrge = volume.GetVolumeRange() 
                m,M = vrge[0], vrge[1]
                vol = np.interp( ln , [0.2,2.0] , [m,M] )
                volume.SetMasterVolumeLevel(vol, None)
            
        dx , dy , Dx , Dy = lmlist[15][1] , lmlist[15][2] , lmlist[20][1] , lmlist[20][2] 
        ox , oy , ofx ,ofy =lmlist[12][1] , lmlist[12][2] , lmlist[9][1] , lmlist[9][2]


        disc = math.hypot((Dx-dx)/r,(Dy-dy)/r)
        off = math.hypot((ofx-ox)/r,(ofy-oy)/r)

        print(ln,'   ',disc,'   ',off )
        if disc >=1.4:
            cv2.circle( img , ( Dx , Dy ) , 10 , (15, 0, 125) , cv2.FILLED  ) 
            cv2.circle( img , ( dx , dy ) , 10 , (15,0,125) , cv2.FILLED  )
            cv2.line(img, (dx,dy) , (Dx,Dy) , (68, 89, 207) ,5 )
        if disc >=0.8:
            cv2.circle( img , ( Dx , Dy ) , 10 , (33, 42,220) , cv2.FILLED  ) 
            cv2.circle( img , ( dx , dy ) , 10 , (33, 42,220) , cv2.FILLED  )
            cv2.line(img, (dx,dy) , (Dx,Dy) , (68, 138, 207) ,5 )

    if off > 1.2513 and ln < 0.15 and disc <0.41: break
    cv2.imshow("cam 1 ",img)
    cv2.waitKey(1)
