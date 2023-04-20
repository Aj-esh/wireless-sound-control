import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

def uplim(a):
    if a<0:
        m=-10
        while True:
            if (a>=m):
                break
            else:
                m*=10
    elif a>=0:
        m=10
        while True:
            if(a<=m):
                break
            else:
                m*=10
    return m

def x(x,M):
    rg = volume.GetVolumeRange()
    z = np.interp( x , [ 0 , uplim( x ) ] , rg[:2]  ) 
    print(z)
    return z



def change(ar):
    t = x(ar,uplim(ar))
    print(t)
    volume.SetMasterVolumeLevel(t, None)


while True:
    a = float(input())
    change(a)



