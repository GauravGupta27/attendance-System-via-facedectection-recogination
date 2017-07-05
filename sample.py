import cv2
import numpy as np
import sqlite3
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);
rec=cv2.createLBPHFaceRecognizer();
rec.load("recognizer/trainningData.yml")
font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,1,1,0,1)
status="Yes"
def getProfile(id):
    conn=sqlite3.connect("Facebased.db")
    
    cmd="SELECT * FROM Persons WHERE ID="+  str(id)

    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

while(True):
    ret, img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)
        if(profile!=None):
        #print id
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[0]),(x,y+h+0),font,255)
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[1]),(x,y+h+20),font,255)
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[2]),(x,y+h+40),font,255)
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[4]),(x,y+h+60),font,255)
            cmd="UPDATE Persons SET Attendance='1' WHERE ID="+  str(id)
            conn=sqlite3.connect("Facebased.db")

            conn.execute(cmd)
            conn.close()

    cv2.imshow("Face",img);
    if(cv2.waitKey(1)==ord('q')):
        break;
cam.release()
cv2.destroyAllWindows()
