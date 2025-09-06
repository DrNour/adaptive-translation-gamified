import streamlit as st
import sqlite3
from db_utils import init_db, register_user, authenticate_user, create_task, submit_translation, get_leaderboard

# Initialize the database
init_db()

# Login / Register form
def login_register():
    st.markdown("### Login or Register")
    choice = st.radio("Choose:", ["Login", "Register"])

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Student", "Instructor"])
        if st.button("Login"):
            if authenticate_user(username, password, role):
                st.session_state["username"] = username
                st.session_state["role"] = role
                st.success(f"Welcome {username} ({role})!")
            else:
                st.error("Invalid credentials")
    else:
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        new_role = st.selectbox("Role", ["Student", "Instructor"])
        if st.button("Register"):
            if register_user(new_username, new_password, new_role):
                st.success("Registered successfully! Please log in.")
            else:
                st.error("Username already exists")

# Instructor dashboard
def instructor_dashboard():
    st.markdown("## Instructor Dashboard")
    task_text = st.text_area("Enter translation task (English or Arabic)")
    if st.button("Create Task"):
        create_task(task_text)
        st.success("Task created successfully!")

# Student dashboard
def student_dashboard():
    st.markdown("## Student Dashboard")
    tasks = get_tasks()
    for task_id, task_text in tasks:
        st.markdown(f"### Task {task_id}")
        st.write(task_text)
        student_translation = st.text_area(f"Your Translation for Task {task_id}", key=f"trans_{task_id}")
        if st.button(f"Submit Task {task_id}"):
            submit_translation(st.session_state["username"], task_id, student_translation)
            st.success("Submitted! You earned points.")

# Leaderboard
def show_leaderboard():
    st.markdown("## Leaderboard")
    leaderboard = get_leaderboard()
    for username, score in leaderboard:
        st.write(f"{username}: {score} points")

# App entry point
def main():
    st.title("Adaptive Translation Gamified App")

    if "username" not in st.session_state:
        login_register()
    else:
        role = st.session_state["role"]
        if role == "Instructor":
            instructor_dashboard()
        elif role == "Student":
            student_dashboard()

        show_leaderboard()

        if st.button("Logout"):
            st.session_state.clear()

if __name__ == "__main__":
    main()
