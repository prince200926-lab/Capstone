import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")  # path to your Firebase service account key
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://capstone-b37ca-default-rtdb.asia-southeast1.firebasedatabase.app/"  # replace with your DB URL
})

# Reference to "students" node
ref = db.reference("students")

# Input all students at once
student_input = input("Enter all student names separated by commas: ")
students = [name.strip() for name in student_input.split(",") if name.strip()]

# Push to Firebase with numeric keys
for index, name in enumerate(students, start=1):
    ref.child(str(index)).set(name)

print("✅ All students added successfully!")
