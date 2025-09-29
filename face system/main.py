import cv2
import numpy as np
from datetime import datetime
import pickle

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load name mapping
with open("names.pkl", "rb") as f:
    names = pickle.load(f)

cam = cv2.VideoCapture(0)

def markAttendance(name):
    with open("Attendance.csv", "a+") as f:
        f.seek(0)
        entries = f.readlines()
        nameList = [line.split(",")[0] for line in entries]
        if name not in nameList:   # mark once per session
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.write(f"{name},Present,{dtString}\n")

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

    for (x,y,w,h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 60:   # good match
            name = names.get(id, "Unknown")
            cv2.putText(img, name, (x+5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            markAttendance(name)
        else:
            name = "Unknown"
            cv2.putText(img, name, (x+5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

    cv2.imshow('camera', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
