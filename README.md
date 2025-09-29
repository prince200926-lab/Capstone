# Face Recognition Attendance System

This is a Python-based Face Recognition Attendance System using OpenCV. It detects and recognizes students from a webcam feed and automatically marks attendance in a CSV file. The system supports a subfolder-per-student dataset structure.



## Features

* Real-time face detection using OpenCV Haar Cascade.
* Student recognition using LBPH Face Recognizer.
* Attendance recorded in Attendance.csv with:

  * Student Name
  * Status (Present)
  * Time of recognition
* Supports multiple students with separate folders.
* Fully offline, no internet required.



## Dataset Structure

```
dataset/
   Student1/
      1.jpg
      2.jpg
   Student2/
      1.jpg
      2.jpg
   Student3/
      1.jpg
      2.jpg
```


## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repo-folder>
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install required packages:

```bash
pip install -r requirements.txt
```


## Usage

### 1. Capture Student Dataset

Run `capture.py` to capture face images for each student:

```bash
python capture.py
```

* Enter the student name when prompted.
* The script will capture multiple images per student and save them in `dataset/<Student Name>/`.

### 2. Train the Model

Run `trainer.py` to train the LBPH recognizer:

```bash
python trainer.py
```

* This will generate:

  * `trainer.yml` → trained model
  * `names.pkl` → mapping of IDs to student names

### 3. Run Attendance System

Run `main.py` to start real-time recognition:

```bash
python main.py
```

* Attendance will be logged in `Attendance.csv`:

```
Student1,Present,12:30:15
Student2,Present,12:32:10
```

* Press `q` to quit the webcam window.

## Notes

* Make sure `opencv-contrib-python` is installed to use `cv2.face`.
* Ensure dataset images are clear frontal faces for accurate recognition.
* Attendance is appended to `Attendance.csv`. Rename or copy the file for daily logs.

## Requirements

* Python 3.x
* opencv-contrib-python
* numpy
* pillow
