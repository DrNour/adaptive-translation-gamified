import streamlit as st
import sqlite3

# --- Database setup ---
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- User registration ---
def register_user(username, password, role):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  (username, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# --- User login ---
def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# --- Dashboards ---
def student_dashboard():
    st.subheader("🎓 Student Dashboard")
    st.write("Here you can practice translations, play games, and track progress.")

def instructor_dashboard():
    st.subheader("👨‍🏫 Instructor Dashboard")
    st.write("Here you can create tasks, review student work, and analyze performance.")

def admin_dashboard():
    st.subheader("🛡️ Admin Dashboard")
    st.write("Here you can manage users and oversee platform activity.")

# --- Main App ---
def main():
    st.title("🌍 Adaptive Translation Gamified Platform")

    # Initialize DB
    init_db()

    # Sidebar menu
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None

    # --- Login page ---
    if choice == "Login":
        st.subheader("Login Section")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            role = login_user(username, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.username = username
                st.success(f"Welcome {username}! Logged in as {role}")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

    # --- Registration page ---
    elif choice == "Register":
        st.subheader("Create a New Account")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["student", "instructor", "admin"])

        if st.button("Register"):
            if register_user(new_user, new_password, role):
                st.success("Account created successfully!")
                st.info("Go to Login to access the platform")
            else:
                st.error("Username already exists")

    # --- Dashboards after login ---
    if st.session_state.logged_in:
        if st.session_state.role == "student":
            student_dashboard()
        elif st.session_state.role == "instructor":
            instructor_dashboard()
        elif st.session_state.role == "admin":
            admin_dashboard()

        # --- Logout button ---
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()


if __name__ == "__main__":
    main()
