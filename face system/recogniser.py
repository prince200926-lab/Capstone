import cv2
import numpy as np
from PIL import Image
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

path = 'dataset'

# Mapping student names to numeric IDs
names = {}
current_id = 0

def getImagesAndLabels(path):
    faceSamples = []
    ids = []
    global names
    current_id = 0

    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            current_id += 1
            names[current_id] = dir_name  # id → name mapping
            student_folder = os.path.join(root, dir_name)

            for file in os.listdir(student_folder):
                if file.endswith("jpg") or file.endswith("png"):
                    imagePath = os.path.join(student_folder, file)
                    pilImage = Image.open(imagePath).convert('L')
                    imageNp = np.array(pilImage, 'uint8')
                    faces = detector.detectMultiScale(imageNp)

                    for (x,y,w,h) in faces:
                        faceSamples.append(imageNp[y:y+h, x:x+w])
                        ids.append(current_id)
    return faceSamples, ids

faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
recognizer.write('trainer.yml')
print("Training complete!")
print("Name mapping:", names)

# Save mapping
import pickle
with open("names.pkl", "wb") as f:
    pickle.dump(names, f)
