import streamlit as st
# ------------- Auth Views -------------


def view_auth():
st.markdown("### Login or Register")
col1, col2 = st.columns(2)


with col1:
st.subheader("Login")
u = st.text_input("Username", key="login_user")
p = st.text_input("Password", type="password", key="login_pass")
if st.button("Login", use_container_width=True):
role = authenticate_user(u, p)
if role:
st.session_state.logged_in = True
st.session_state.username = u
st.session_state.role = role
st.experimental_rerun()
else:
st.error("Invalid username or password.")


with col2:
st.subheader("Register")
ru = st.text_input("New username", key="reg_user")
rp = st.text_input("New password", type="password", key="reg_pass")
role = st.selectbox("Role", ["Student", "Instructor"], index=0)
if st.button("Register", use_container_width=True):
ok, msg = register_user(ru, rp, role)
if ok:
st.success(msg)
else:
st.error(msg)




# ------------- Student View -------------


def view_student():
st.markdown("### 🧑‍🎓 Student — Translate & Earn Points")


tab_task, tab_free, tab_my = st.tabs(["Assigned Tasks", "Free Translate", "My Score & History"])


with tab_task:
tasks = list_tasks()
if not tasks:
st.info("No tasks yet. Ask your instructor to create one in Instructor tab.")
else:
cols = st.columns([1, 2, 5, 2])
cols[0].markdown("**ID**")
cols[1].markdown("**Direction**")
cols[2].markdown("**Snippet**")
cols[3].markdown("**Open**")
for t_id, direction, snippet in tasks:
c = st.columns([1, 2, 5, 2])
c[0].write(t_id)
c[1].write(direction)
c[2].write(snippet + ("…" if len(snippet) == 120 else ""))
if c[3].button(f"Open {t_id}"):
st.session_state.current_task_id = t_id
st.session_state.source_text = ""
st.session_state