# Save as attendance_persistent_final.py
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Attendance Web App", layout="wide")
st.markdown("<h1 style='text-align:center; color: #4CAF50;'>📋 Student Attendance Management System</h1>", unsafe_allow_html=True)

# ----------------------------
# Step 1: Date Picker
# ----------------------------
selected_date = st.date_input("Select Date")

if 'attendance_status' not in st.session_state:
    st.session_state.attendance_status = {}

if 'student_list' not in st.session_state:
    # Predefined students
    predefined_students = [
        "SAPTANSHU", "SHREYA SINGH", "ABHISHEK CHAURASIYA", "AJMAL HASHMI",
        "AKANKSHA YADAV", "AKASH SINGH CHAUHAN", "AKASH YADAV", "AMAN KUMAR",
        "AMAN SINGH", "AMAR SAROJ", "ANAND KUMAR YADAV", "ANKUR YADAV",
        "ANUPAM YADAV", "ANURAG", "ASHUTOSH YADAV", "AYUSH KUMAR",
        "CHANDAN GUPTA", "HARI OM YADAV", "HRISHIKESH SINGH", "KARTIK SAHU",
        "KAUSHAL PANDEY", "KHUSHI SINGH", "KOMAL SAHU", "KUNAL PANDEY",
        "LAKSHMAN YADAV", "MADHUKAR RAI", "MO AFJAL ANSARI", "MOHAMMED SHAAD",
        "MOHD UZAIF ANSARI", "MOHIT RAJBHAR", "MUSTKIM", "NITISH NISHAD",
        "PALAK SINGH", "PATEL SURAJ JATASHANKAR", "PRATEEK YADAV", "PREETI YADAV",
        "PRERIT KUMAR SINGH", "PRINCE MAURYA", "PRINCE YADAV", "PRIYANSHU YADAV",
        "RISHI YADAV", "RUTVIK CHAUDHARY", "SACHIN YADAV", "SAKSHI MAURYA",
        "SAURABH YADAV", "SHIKSHA PAL", "SHIVAM DUBEY", "SHUBHAM SONI",
        "SURAJ SETH", "UTTAM KUMAR", "VIKASH YADAV", "VINAY YADAV",
        "VISHAL MALI", "NIKHIL KUMAR PRAJAPATI", "RAHUL YADAV",
        "SAHIL KUSHWAHA", "SINKI YADAV"
    ]
    st.session_state.student_list = predefined_students.copy()
    for student in st.session_state.student_list:
        st.session_state.attendance_status[student] = False


# ----------------------------
# Step 2: Initialize session state
# ----------------------------
if 'attendance_status' not in st.session_state:
    st.session_state.attendance_status = {}  # Stores student_key: present_status

if 'student_list' not in st.session_state:
    st.session_state.student_list = []  # Keeps order of students

# ----------------------------
# Step 3: Add Students Manually (Name, Year, Branch)
# ----------------------------
st.subheader("➕ Add Students to Attendance")
col1, col2, col3 = st.columns(3)
with col1:
    new_name = st.text_input("Name", key="name_input")
with col2:
    new_year = st.text_input("Year", key="year_input")
with col3:
    new_branch = st.text_input("Branch", key="branch_input")

if st.button("Add Student"):
    if new_name.strip() != "":
        student_key = f"{new_name.strip()} ({new_year.strip()} {new_branch.strip()})" if new_year or new_branch else new_name.strip()
        if student_key not in st.session_state.student_list:
            st.session_state.student_list.append(student_key)
            st.session_state.attendance_status[student_key] = False
            st.success(f"Student '{student_key}' added! ✅ Will persist until manually deleted.")
        else:
            st.warning(f"Student '{student_key}' already exists!")
    else:
        st.warning("Please enter a valid name.")

# ----------------------------
# Step 4: Attendance Checkboxes (Two-column)
# ----------------------------
st.subheader("✅ Mark Attendance")
if st.session_state.student_list:
    cols = st.columns(2)
    for i, student in enumerate(st.session_state.student_list):
        col = cols[i % 2]
        checked = st.session_state.attendance_status[student]
        st.session_state.attendance_status[student] = col.checkbox(student, value=checked)
else:
    st.info("No students added yet. Please add students above.")

# ----------------------------
# Step 5: Delete Student
# ----------------------------
st.subheader("🗑️ Delete Students")
students_to_delete = st.multiselect("Select students to delete", options=st.session_state.student_list)
if st.button("Delete Selected Students"):
    for s in students_to_delete:
        if s in st.session_state.student_list:
            st.session_state.student_list.remove(s)
            st.session_state.attendance_status.pop(s, None)
    st.success("Selected students deleted.")

# ----------------------------
# Step 6: Save & Download CSV
# ----------------------------
if st.button("💾 Save & Download Attendance"):
    if not st.session_state.student_list:
        st.warning("No students to save.")
    else:
        date_str = selected_date.strftime("%Y-%m-%d")
        data = []
        for student_name in st.session_state.student_list:
            present = st.session_state.attendance_status[student_name]
            data.append([date_str, student_name, "Present" if present else "Absent"])
        df = pd.DataFrame(data, columns=["Date", "Student Name", "Status"])

        # Convert to CSV in memory
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue()

        st.download_button(
            label="📥 Download Attendance CSV",
            data=csv_bytes,
            file_name=f"attendance_{date_str}.csv",
            mime="text/csv"
        )
        st.success("Attendance CSV ready to download!")
