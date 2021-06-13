import cv2
import smtplib
import numpy as np
from os import listdir
import time
import os
from os.path import isfile,join
from datetime import date
import datetime
import pyrebase
import uuid
from pymongo import MongoClient
from testUpload import uploadFile,sendMail


USER_ID = input("Enter Your UserID")
PASSWORD= input("Enter your Password")
cluster = MongoClient("mongodb+srv://argha1234:1234@cluster0.qcavj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")

db = cluster["QuickPeek"]
collection = db["Userdata"]

resp = collection.find_one({'_id':USER_ID,'Password':PASSWORD})

if( resp == None):
    print("Sorry Invalid Credentials!! Contact QuickPeek Team")
    exit()

data_path = 'faces/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]


if not os.path.exists('UnAuthorized'):
    os.makedirs('UnAuthorized')

Training_Data, Labels = [], []



for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)

Labels = np.asarray(Labels, dtype=np.int32)

model = cv2.face.LBPHFaceRecognizer_create()

model.train(np.asarray(Training_Data), np.asarray(Labels))

print("Model Training Complete!!!!!")


face_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return img,[]
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi=img[y:y+h,x:x+w]
        roi=cv2.resize(roi,(200,200))
    return img,roi

def fileCleanser():
    lines_seen = set() 
    outfile = open("LogFinal.txt", "w")
    for line in open("LogTmp.txt", "r"):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

    
cap=cv2.VideoCapture(0)
count = 0
temp = []
today = date.today()
d1 = today.strftime("%d_%m_%Y")

# def uploadToStore():
#     entries = os.listdir("./UnAuthorized")
#     for entry in entries:



def writeVideo():
    #count= count+1
    result1 = cv2.VideoWriter("UnAuthorized\Hello "+str(d1)+"_"+str(count)+".avi", cv2.VideoWriter_fourcc(*'MJPG'),10, size)
    for i in temp:
        result1.write(i)
    result1.release()
    temp.clear()
    uploadFile(USER_ID)
    sendMail(resp['email'])
    
while True:
    rec, frame =cap.read()
    image,face=face_detector(frame)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    
    t = time.localtime()
    current_time = time.strftime("%H_%M_%S", t)    
    
    try:
        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
        result=model.predict(face)
        
        
        
        if result[1]<500:
            confidence=int(100*(1-(result[1])/300))
            display_string = str(confidence)+"% confidence it is user"
        cv2.putText(image,display_string,(100,120),cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)
        
        
        if confidence>85:
            cv2.putText(image,"Authorized!!",(250,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.imshow("Face Cropper",image)
        else:
            
            #print("Ture")
            temp.append(frame)
            if(len(temp)>300):
                writeVideo()
                count = count+1
                
                
            cv2.putText(image,"UnAuthorized!!",(250,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            cv2.imshow("Face Cropper",image)
            f = open("LogTmp.txt","a")
            f.write(str(today)+" "+current_time+" UnAuthorized Access Please Refer to video dated "+d1+"\n")
            f.close()
            
            
           
    except Exception as e:
        print(e)
        cv2.putText(image,"Face Not Found!!!",(250,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
        cv2.imshow("Face Cropper",image)
        pass
    current_video_Date = date.today()

    d2 = today.strftime("%d_%m_%Y")
    
    if cv2.waitKey(1)==13 or d1!=d2:
        writeVideo()
        d1=d2
        count = 0
        fileCleanser()
        
        break

        
cap.release()

cv2.destroyAllWindows()
