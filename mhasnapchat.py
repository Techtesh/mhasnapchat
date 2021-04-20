# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:39:37 2021

@author: Hitesh
"""


import cv2
import numpy as np
import dlib


def dist(p0,p1):
    return int(((p0[0]-p1[0])**2+(p0[1]-p1[1])**2)**0.5)
   
def doNothing(x):
    pass

def drawdeku(landmarks):
    edge_left=(landmarks.part(0).x,landmarks.part(0).y)
    edge_right=(landmarks.part(16).x,landmarks.part(16).y)
    top_center=(landmarks.part(27).x,landmarks.part(27).y)
    chin_base=(landmarks.part(8).x,landmarks.part(8).y)
    
    width=int(dist(edge_left,edge_right)*1.25)
    height=int(dist(top_center,chin_base)*1.5)

    dekuhair=cv2.imread("dekuhair.png")  
    
    dekuhair=cv2.resize(dekuhair,(int(width),int(height)))
    dekuhair_gray=cv2.cvtColor(dekuhair,cv2.COLOR_BGR2GRAY)
    width,height,_=(dekuhair.shape)
    _,deku_mask=cv2.threshold(dekuhair_gray, 25 , 255, cv2.THRESH_BINARY_INV)
    top_left=(edge_left[0],edge_left[1]-int(height))
    corrY=40
    corrX=-25
    hair_area=frame[top_left[1]+corrY:top_left[1]+width+corrY,top_left[0]+corrX:top_left[0]+height+corrX]   
    if(dekuhair.shape==hair_area.shape):
        #cv2.imshow("sub frame",hair_area)
        hair_removed=cv2.bitwise_and(hair_area, hair_area,mask=deku_mask)
        replaced_hair=cv2.add(hair_removed,dekuhair)
        frame[top_left[1]+corrY:top_left[1]+width+corrY,top_left[0]+corrX:top_left[0]+height+corrX]=replaced_hair
 
    
def drawEraserhead(landmarks):
    left_ear=(landmarks.part(0).x,landmarks.part(0).y)
    right_ear=(landmarks.part(16).x,landmarks.part(16).y)
    edge_left=(landmarks.part(0).x,landmarks.part(0).y)
    edge_right=(landmarks.part(16).x,landmarks.part(16).y)
    width=int(dist(left_ear,right_ear))
    width2=int(dist(edge_left,edge_right))
    #print(width2)
    
    img1=cv2.imread("aizawa2.png")
    img2=cv2.imread("aizawa3.png")
    scale=width/img1.shape[1]
    height=int(img1.shape[0]*scale)
    Ycorr=-50
    ycorr2=-200
    
    #applying glasses
    if left_ear[1]<right_ear[1]:
        subframe=frame[left_ear[1]+Ycorr:left_ear[1]+height+Ycorr,left_ear[0]:right_ear[0]]
    else:
        subframe=frame[right_ear[1]+Ycorr:right_ear[1]+height+Ycorr,left_ear[0]:right_ear[0]]
    img1=cv2.resize(img1, (width,height))
   
    if (img1.shape==subframe.shape):
        img1_gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        _,mask=cv2.threshold(img1_gray, 25 , 255, cv2.THRESH_BINARY_INV)
       
        removed=cv2.bitwise_and(subframe, subframe,mask=mask)
        replaced=cv2.add(removed,img1)
        subframe=cv2.add(subframe, img1)
        
        if left_ear[1]<right_ear[1]:
            frame[left_ear[1]+Ycorr:left_ear[1]+height+Ycorr,left_ear[0]:right_ear[0]]=replaced
        else:
            frame[right_ear[1]+Ycorr:right_ear[1]+height+Ycorr,left_ear[0]:right_ear[0]]=replaced
    
    #adding hair
    start=(edge_left[0],edge_left[1]+ycorr2)
    inner_width=int(dist(edge_left,edge_right))
    scalenew=inner_width/180
    new_width=int(scalenew*img2.shape[1])
    new_height=int(scalenew*img2.shape[0])
    img2=cv2.resize(img2, (new_width,new_height))
    ycorr2x=-1*int(270*scalenew)
    ycorr2y=-1*int(180*scalenew)
    start=(edge_left[0]+ycorr2x,edge_left[1]+ycorr2y)
    cv2.circle(frame, start, 5, (255,255,255))
   
    subframestart=(edge_left[0]-int(270*scalenew),edge_left[1]-int(180*scalenew))
    subframe =frame[subframestart[1]:,subframestart[0]:] 
    #to do solve -ve start bug
   
    if start[0]<0:
        limmin=(-1*start[0],0)
        limmax=(subframe.shape[0]+limmin[0],subframe.shape[1])
    else:
        limmin=(0,0)    
        limmax=subframe.shape
    
    subimg3=img2[limmin[0]:limmax[0],limmin[1]:limmax[1]]
   
   
    if(subimg3.shape==subframe.shape):
        img3_gray=cv2.cvtColor(subimg3, cv2.COLOR_BGR2GRAY) 
        _,mask=cv2.threshold(img3_gray, 25 , 255, cv2.THRESH_BINARY_INV)
        
        try:
            removed=cv2.bitwise_and(subframe, subframe,mask=mask)
            replaced=cv2.addWeighted(removed,0.1,subimg3,1,2)
            subframe=cv2.add(subframe, subimg3)
            #cv2.imshow("finalop",subframe)
            frame[subframestart[1]:,subframestart[0]:]=subframe 
        except Exception as e:
             
            pass


def generichats(landmarks,file,const=(193,203,188),filtermin=25,beta=2):
    edge_left=(landmarks.part(0).x,landmarks.part(0).y)
    edge_right=(landmarks.part(16).x,landmarks.part(16).y)
    face_width=dist(edge_left,edge_right)
    inner_width_img=const[0]#to do get const from function def
    scale=face_width/inner_width_img
    img=cv2.imread(file)
    height,width,_=img.shape
    height=int(height*scale)
    width=int(width*scale)
    img=cv2.resize(img, (width,height))
    xcorr=int(const[1]*scale)
    ycorr=int(const[2]*scale)
    center=(edge_left[0]-xcorr,edge_left[1]-ycorr)

    subframe=frame[center[1]:center[1]+height,center[0]:center[0]+width]
    subframestart=center
   
    #to do handle center is -ve so choosing subframe and subimg accordingly
    if (center[0]<0 and center[1]<0):
        subframestart=(0,0)
        img=img[-1*center[1]:,-1*center[0]:]
        subframe=frame[0:img.shape[0],0:img.shape[1]]
        pass
    #only x is -ve
    elif (center[0]<0):
        subframestart=(0,subframestart[1])
        img=img[0:,-1*center[0]:]
        subframe=frame[center[1]:center[1]+img.shape[0],0:0+img.shape[1]]

    #only y is -ve
    elif (center[1]<0):
        subframestart=(subframestart[0],0)
        img=img[-1*center[1]:]
        subframe=frame[0:img.shape[0],center[0]:min(center[0]+img.shape[1],frame.shape[1])]
       
    #to do handle over and underflow
    # handeling overflow error 
    xover = frame.shape[1]<center[0]+img.shape[1]    
    yover = frame.shape[0]<center[1]+img.shape[0]
    
    if (xover and yover):
        img=img[0:subframe.shape[0],0:subframe.shape[1]]
        pass
    
    elif yover:
        #print("+ve error on y")
        img=img[0:subframe.shape[0]]
    elif xover:
        img=img[0:,0:subframe.shape[1]]
    
    
    if (subframe.shape==img.shape):
        img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        _,mask=cv2.threshold(img_gray, filtermin , 255, cv2.THRESH_BINARY)
        removed=cv2.bitwise_and(subframe, subframe,mask=mask)
        subframe=cv2.addWeighted(subframe, 1, img, beta, 2)
        frame[subframestart[1]:subframestart[1]+subframe.shape[0],subframestart[0]:subframestart[0]+subframe.shape[1]]=subframe
    else:
        print("you shall not pass")
        
cap=cv2.VideoCapture(0)
detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") 

cv2.namedWindow("frame")
cv2.createTrackbar("test", "frame", 0, 10, doNothing)

while True:
    ret,frame=cap.read()  
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=detector(gray)
    for face in faces:
        landmarks=predictor(gray,face)
        #use switch case here
        val=cv2.getTrackbarPos("test", "frame")
        if (val==1):drawdeku(landmarks)
        if (val==2):generichats(landmarks,"bakugov2.png",(450,250,900),25)
        if (val==3):generichats(landmarks,"denki.png",(450,250,600))
        if (val==4):generichats(landmarks,"kiroshima30v2.png",(990,420,1200))
        if (val==5):generichats(landmarks,"hatsumi2.png",(133,80,160))
        if (val==6):generichats(landmarks,"gran30.png",(900,50,550),25)
        if (val==7):generichats(landmarks, "hawks100.png",(450,250,650),beta=0.7)
        if (val==8):drawEraserhead(landmarks)
        
    cv2.imshow("frame",frame)
    key=cv2.waitKey(1)
    if key==27:
        print("here2")
        break
cv2.destroyAllWindows()