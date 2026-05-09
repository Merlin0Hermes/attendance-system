from auth import init_auth
import streamlit as st
from storage import create_tables

create_tables()
init_auth()

st.session_state.authenticator.login(location="unrendered")

pages = [
        st.Page("camera.py", title="Attendance"),
        st.Page("registration.py", title="Registration"),
        st.Page("history.py", title="History"),
        st.Page("configuration.py", title="Configuration"),
    ]



if not st.session_state.get('authentication_status'):
    pages = [
        st.Page("login.py", title="Login"),
        st.Page("register.py", title="Register")
    ]


pg = st.navigation(pages)
pg.run()
