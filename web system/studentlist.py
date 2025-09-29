import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("key.json")  # path to your Firebase service account key
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://capstone-b37ca-default-rtdb.asia-southeast1.firebasedatabase.app/"  # your RTDB URL
})

ref = db.reference("students")

def normalize_data(data):
    """Ensure data is a dictionary with string keys"""
    if isinstance(data, list):
        return {str(i+1): name for i, name in enumerate(data) if name}
    return data or {}

def show_sections():
    data = normalize_data(ref.get())
    if not data:
        print("No sections found.")
        return
    for section in data:
        students = normalize_data(data[section])
        student_list = [students[k] for k in sorted(students.keys(), key=int)]
        print(f"Class-Section: {section} | Students: {student_list}")

def add_section():
    section = input("Enter new section name (e.g., 10D): ").strip()
    if not section:
        print("Invalid section name!")
        return
    student_input = input("Enter student names separated by commas: ")
    students = [s.strip() for s in student_input.split(",") if s.strip()]
    for idx, name in enumerate(students, start=1):
        ref.child(section).child(str(idx)).set(name)
    print(f"Section {section} added successfully!")

def add_students(section):
    section_ref = ref.child(section)
    students = normalize_data(section_ref.get())
    student_input = input("Enter student names to add separated by commas: ")
    new_students = [s.strip() for s in student_input.split(",") if s.strip()]
    start_idx = len(students) + 1 if students else 1
    for idx, name in enumerate(new_students, start=start_idx):
        section_ref.child(str(idx)).set(name)
    print("Students added successfully!")

def remove_students(section):
    section_ref = ref.child(section)
    current_data = section_ref.get()
    if not current_data:
        print("Section is empty or does not exist.")
        return

    # Normalize data to dictionary
    current_data = normalize_data(current_data)

    # Build display map: 1-based numbering for user
    sorted_keys = sorted(current_data.keys(), key=int)
    display_map = {str(i+1): sorted_keys[i] for i in range(len(sorted_keys))}

    # Show students
    print("Students:")
    for i, k in display_map.items():
        print(f"{i}: {current_data[k]}")

    remove_input = input("Enter student numbers to remove (comma-separated): ")
    remove_list = [r.strip() for r in remove_input.split(",")]

    # Build new student list excluding removed ones
    new_students = [current_data[display_map[i]] for i in display_map if i not in remove_list]

    # Clear section and rewrite students consecutively
    section_ref.delete()
    for idx, name in enumerate(new_students, start=1):
        section_ref.child(str(idx)).set(name)

    print("Selected students removed and roll numbers updated.")

def edit_section():
    section = input("Enter section to edit: ").strip()
    section_ref = ref.child(section)
    if not section_ref.get():
        print("Section does not exist!")
        return

    print("1. Add student\n2. Remove student")
    choice = input("Choose an option: ").strip()
    if choice == "1":
        add_students(section)
    elif choice == "2":
        remove_students(section)
    else:
        print("Invalid option!")

def delete_section():
    section = input("Enter section to delete: ").strip()
    if ref.child(section).get():
        ref.child(section).delete()
        print(f"Section {section} deleted successfully!")
    else:
        print("Section does not exist!")

# Main loop
while True:
    print("\n--- Attendance Manager ---")
    print("1. Show sections")
    print("2. Add new section")
    print("3. Edit section")
    print("4. Delete section")
    print("5. Exit")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        show_sections()
    elif choice == "2":
        add_section()
    elif choice == "3":
        edit_section()
    elif choice == "4":
        delete_section()
    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid choice! Try again.")
