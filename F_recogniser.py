import cv2
import numpy as np
from PIL import Image
import os
import pickle

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

path = 'dataset'

# Mapping student names (including section) to numeric IDs
names = {}
current_id = 0

def getImagesAndLabels(path):
    faceSamples = []
    ids = []
    global names
    current_id = 0

    for section_name in os.listdir(path):
        section_folder = os.path.join(path, section_name)
        if not os.path.isdir(section_folder):
            continue
        for student_name in os.listdir(section_folder):
            student_folder = os.path.join(section_folder, student_name)
            if not os.path.isdir(student_folder):
                continue
            current_id += 1
            # Include section in the label
            full_name = f"{section_name}_{student_name}"
            names[current_id] = full_name

            for file in os.listdir(student_folder):
                if file.endswith("jpg") or file.endswith("png"):
                    imagePath = os.path.join(student_folder, file)
                    pilImage = Image.open(imagePath).convert('L')
                    imageNp = np.array(pilImage, 'uint8')
                    faces = detector.detectMultiScale(imageNp)

                    for (x, y, w, h) in faces:
                        faceSamples.append(imageNp[y:y+h, x:x+w])
                        ids.append(current_id)
    return faceSamples, ids

faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
recognizer.write('trainer.yml')
print("Training complete!")
print("Name mapping:", names)

# Save mapping
with open("names.pkl", "wb") as f:
    pickle.dump(names, f)
