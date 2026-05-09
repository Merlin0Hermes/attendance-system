from streamlit_authenticator.utilities.exceptions import RegisterError
import time
from storage import add_user
from auth import save_config
import streamlit as st

st.set_page_config(page_title="Register")
st.session_state.authenticator.login(location="unrendered")

try:
    email, username, name = st.session_state.authenticator.register_user(password_hint=False)
    if email:
        st.success("User registered successfully")
        save_config()
        add_user(username) 
        with st.spinner("Going to login page...", show_time=True):
            time.sleep(3)
        st.switch_page("login.py")
except RegisterError as e:
    st.error(e)