import streamlit as st
import sqlite3
import hashlib

# --- Helper: password hashing ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

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
                  (username, hash_password(password), role))
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
    c.execute("SELECT password, role FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result and verify_password(password, result[0]):
        return result[1]   # return role
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

    # Ensure session state keys exist
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None

    # If logged in, show dashboard directly
    if st.session_state.logged_in:
        st.sidebar.write(f"👋 Logged in as {st.session_state.username} ({st.session_state.role})")

        if st.session_state.role == "student":
            student_dashboard()
        elif st.session_state.role == "instructor":
            instructor_dashboard()
        elif st.session_state.role == "admin":
            admin_dashboard()

        # Logout button resets session
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.username = None

    else:
        # Sidebar menu only when not logged in
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

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


if __name__ == "__main__":
    main()
