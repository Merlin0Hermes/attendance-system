from auth import save_config
import streamlit as st


try:
    st.session_state.authenticator.login()
    if st.session_state.get('authentication_status'):
        save_config()
        st.success("Logged in")
    elif st.session_state.get("authentication_status") == False:  # noqa: E712
        st.error("Invalid username or password")
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please enter your username and password')

except Exception as e:
    st.error(e)
