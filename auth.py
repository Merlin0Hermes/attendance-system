from storage import get_user_id_by_name
import yaml
from yaml import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth

CONFIG_PATH = ".streamlit/config.yaml"

def load_config(path=CONFIG_PATH):
    try:
        with open(path) as file:
            return yaml.load(file, Loader=SafeLoader)
    except FileNotFoundError:
        with open(path, "w") as file:
            data = {
                "cookie": {
                    "expiry_days": 30,
                    "name": "attendance_monitoring_system"
                },
                "credentials": {
                    "usernames": {}
                }
            }
            yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)
            with open(path) as file:
                return yaml.load(file, Loader=SafeLoader)



def save_config(config=None, path=CONFIG_PATH):
    if not config:
        config = st.session_state.get("auth_config")
    with open(path, "w") as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

def init_auth():

    if "auth_config" not in st.session_state:
        st.session_state.auth_config = load_config()

    config = st.session_state.auth_config

    if "authenticator" not in st.session_state:
        st.session_state.authenticator = stauth.Authenticate(
            config["credentials"],
            config["cookie"]["name"],
            st.secrets["cookie_key"],
            config["cookie"]["expiry_days"],
        )

    if st.session_state.get('authentication_status'):
        st.session_state.user_id = get_user_id_by_name(st.session_state.get("username"))

    return st.session_state.authenticator

