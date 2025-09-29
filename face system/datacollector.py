import cv2
import os

# Student name input
student_name = input("Enter Student Name: ")

# Create subfolder if not exists
path = f"dataset/{student_name}"
os.makedirs(path, exist_ok=True)

cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

count = 0

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        count += 1
        cv2.imwrite(f"{path}/{count}.jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

    cv2.imshow('image', img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    elif count >= 75:   # capture 75 images
        break

cam.release()
cv2.destroyAllWindows()
print(f"Dataset created for {student_name}")
