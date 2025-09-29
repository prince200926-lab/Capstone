import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import datetime

# Load Firebase credentials
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://capstone-b37ca-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

df = pd.read_csv("Attendance.csv", header=None, names=["Name", "Status", "Time"])

# Convert DataFrame to dictionary
attendance_data = df.to_dict(orient="records")

# Get today's date
today = datetime.date.today().strftime("%Y-%m-%d")

# Reference to the Firebase path
ref = db.reference(f"attendance/{today}")

# Upload data
ref.set(attendance_data)
print("✅ Attendance uploaded to Firebase successfully!")