import cv2
import numpy as np
from datetime import datetime
import pickle
import os

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load name mapping (section included)
with open("names.pkl", "rb") as f:
    names = pickle.load(f)

cam = cv2.VideoCapture(0)
marked_today = set()  # To avoid marking multiple times

def markAttendance(full_name):
    """Marks attendance in Attendance.csv"""
    if "_" in full_name:
        section, student_name = full_name.split("_", 1)
    else:
        section = "Unknown"
        student_name = full_name

    key = f"{section}_{student_name}"
    if key in marked_today:
        return
    marked_today.add(key)

    now = datetime.now()
    dtString = now.strftime("%H:%M:%S")

    # Ensure CSV exists
    if not os.path.exists("Attendance.csv"):
        with open("Attendance.csv", "w") as f:
            f.write("Section,Name,Status,Time\n")

    with open("Attendance.csv", "a") as f:
        f.write(f"{section},{student_name},Present,{dtString}\n")

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 60:
            full_name = names.get(id, "Unknown")
            cv2.putText(img, full_name, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            markAttendance(full_name)
        else:
            full_name = "Unknown"
            cv2.putText(img, full_name, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)

    cv2.imshow('camera', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
