import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from datetime import date, datetime

# --- Firebase setup ---
cred = credentials.Certificate("W_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://capstone-b37ca-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# --- Read CSV without headers ---
df = pd.read_csv("attendance.csv", header=None)

# Assume CSV structure: Class, StudentName, Status, Time
# If your CSV only has Class and StudentName, Status/Time will be filled automatically
if df.shape[1] < 4:
    # Add missing columns
    for i in range(df.shape[1], 4):
        df[i] = None

df.columns = ['Class', 'StudentName', 'Status', 'Time']

# Fill missing Status/Time
df['Status'] = df['Status'].fillna('Present')
df['Time'] = df['Time'].fillna(datetime.now().strftime("%H:%M"))

# --- Normalize names to remove spaces ---
def normalize_name(name):
    return str(name).strip()

# --- Get today's date ---
today = date.today().isoformat()  # YYYY-MM-DD

# --- Reference to attendance node ---
ref = db.reference('attendance')

# --- Prepare data to push ---
data_to_push = {}
for class_name, group in df.groupby('Class'):
    students_dict = {}
    for _, row in group.iterrows():
        clean_name = normalize_name(row['StudentName'])
        students_dict[clean_name] = {
            "Status": row['Status'],
            "Time": row['Time']
        }
    if class_name not in data_to_push:
        data_to_push[class_name] = {}
    data_to_push[class_name][today] = students_dict

# --- Push to Firebase ---
ref.update(data_to_push)

print("Attendance uploaded successfully!")