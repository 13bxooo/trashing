import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PROJECT : LOGIC",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# PAGE ACTION
# =========================================================

action = st.query_params.get("action")


if action == "restart":

    st.session_state.game_paused = False

    st.query_params.clear()

    st.rerun()


elif action == "title":

    st.session_state.game_paused = False
    st.session_state.show_continue_warning = True
    st.query_params.clear()
    st.switch_page("main.py")

elif action == "stage01":

    st.session_state.game_paused = False
    st.session_state.stage01_started = True
    st.query_params.clear()
    st.switch_page("pages/3_Stage_01.py")


# =========================================================
# SESSION STATE
# =========================================================

if "game_paused" not in st.session_state:

    st.session_state.game_paused = False


# =========================================================
# FONT
# =========================================================

font_path = None

for name in ["neodgm.ttf", "neodgm(2).ttf"]:

    candidate = Path(name)

    if candidate.exists():

        font_path = candidate

        break


if font_path:

    font_base64 = base64.b64encode(
        font_path.read_bytes()
    ).decode("utf-8")

else:

    font_base64 = ""


# =========================================================
# STREAMLIT CSS
# =========================================================

st.markdown(
    f"""
<style>

@font-face {{
    font-family: 'NeoDungGeunMo';

    src:
        url(data:font/ttf;base64,{font_base64})
        format('truetype');
}}


html,
body,
[class*="css"] {{
    font-family:
        'NeoDungGeunMo',
        monospace !important;
}}


#MainMenu,
header,
footer {{
    visibility: hidden;
}}


.stApp {{
    background: #000000 !important;
}}


.block-container {{
    padding: 0 !important;
    max-width: 100vw !important;
}}
