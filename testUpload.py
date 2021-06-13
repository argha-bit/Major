import smtplib
import pyrebase
import uuid
import os
import pymongo
from pymongo import MongoClient
import numpy as np
import smtplib

cluster = MongoClient("mongodb+srv://argha1234:1234@cluster0.qcavj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")

db = cluster["QuickPeek"]
collection = db["Userdata"]


firbaseConfig = {
    "apiKey": "AIzaSyAoSIRRFkXpt9mp33j8MgaAlxzQ1qQaKcg",
    "authDomain": "quickpeek-e03da.firebaseapp.com",
    "projectId": "quickpeek-e03da",
    "storageBucket": "quickpeek-e03da.appspot.com",
    "messagingSenderId": "346992347751",
    "appId": "1:346992347751:web:2a0fe4cf73c861a00aa2c2",
    "measurementId": "G-Z4S10TY5N8",
    "databaseURL" : ""
}
firebase = pyrebase.initialize_app(firbaseConfig)
storage = firebase.storage()

def sendMail(email):
    se="quickpeek985@gmail.com"
    re=email
    msg="hey someone trying to enter into your house!!!"
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    password="quickpeek123"
    server.login(se,password)
    print("login success!")
    server.sendmail(se,re,msg)
    print("done")

def uploadFile(USERID):
    entries = os.listdir("UnAuthorized//")
    urlRepo = []
    print("Initializing Cloud Upload")
    for entry in entries:
        file = "UnAuthorized//"+entry
        cloudNickName = "/UnAuthorized/"+str(USERID)+"/"+str(USERID)+os.path.splitext(entry)[0]+".avi"
        storage.child(cloudNickName).put(file)
        #urlRepo.append(storage.child(cloudNickName).get_url(None))
        dt = storage.child(cloudNickName).get_url(None)
        collection.update_one({'_id':USERID},{"$push":{"dataRepo":dt}})
        # os.remove(entry)
        os.remove(file)
    print("Cloud Upload Finished")