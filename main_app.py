import streamlit as st
from db_utils import init_db, register_user, authenticate_user, create_task, get_tasks, submit_translation, get_leaderboard

# Initialize database
init_db()

# --- Login / Register ---
def login_or_register():
    st.sidebar.title("Login / Register")
    action = st.sidebar.radio("Choose Action", ["Login", "Register"])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    role = st.sidebar.selectbox("Role", ["Student", "Instructor"])

    if action == "Register":
        if st.sidebar.button("Register"):
            success = register_user(username, password, role)
            if success:
                st.sidebar.success("Registration successful. Please login.")
            else:
                st.sidebar.error("Username already exists. Try again.")

    elif action == "Login":
        if st.sidebar.button("Login"):
            if authenticate_user(username, password, role):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.sidebar.success(f"Welcome {username} ({role})!")
            else:
                st.sidebar.error("Invalid credentials.")

# --- Instructor Dashboard ---
def instructor_dashboard():
    st.header("📚 Instructor Dashboard")

    st.subheader("➕ Create a New Task")
    task_text = st.text_area("Enter source text for translation")
    if st.button("Add Task"):
        if task_text.strip():
            create_task(task_text)
            st.success("Task created successfully.")
        else:
            st.warning("Task cannot be empty.")

    st.subheader("👀 Existing Tasks")
    tasks = get_tasks()
    if tasks:
        for task_id, text in tasks:
            st.write(f"**Task {task_id}:** {text}")
    else:
        st.info("No tasks available.")

# --- Student Dashboard ---
def student_dashboard():
    st.header("🎓 Student Dashboard")

    st.subheader("📝 Available Translation Tasks")
    tasks = get_tasks()
    if tasks:
        for task_id, text in tasks:
            st.markdown(f"**Task {task_id}:** {text}")
            translation = st.text_area(f"Enter your translation for Task {task_id}", key=f"task_{task_id}")
            if st.button(f"Submit for Task {task_id}", key=f"submit_{task_id}"):
                if translation.strip():
                    submit_translation(st.session_state.username, task_id, translation)
                    st.success("Translation submitted successfully!")
                else:
                    st.warning("Translation cannot be empty.")
    else:
        st.info("No tasks available.")

    st.subheader("🏆 Leaderboard")
    leaderboard = get_leaderboard()
    if leaderboard:
        for i, (user, score) in enumerate(leaderboard, start=1):
            st.write(f"{i}. {user} — {score} points")
    else:
        st.info("No submissions yet.")

# --- Main App ---
def main():
    st.title("🌍 Gamified Translation Learning Platform")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_or_register()
    else:
        if st.session_state.role == "Instructor":
            instructor_dashboard()
        elif st.session_state.role == "Student":
            student_dashboard()

if __name__ == "__main__":
    main()
