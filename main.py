import base64
from pathlib import Path

import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PROJECT : LOGIC",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# FONT
# =========================================================

font_candidates = [
    Path("neodgm.ttf"),
    Path("neodgm(2).ttf"),
]

font_data = ""

for font_path in font_candidates:
    if font_path.exists():
        with open(font_path, "rb") as f:
            font_data = base64.b64encode(f.read()).decode("utf-8")
        break


# =========================================================
# SESSION STATE
# =========================================================

if "start_open" not in st.session_state:
    st.session_state.start_open = False


# =========================================================
# HIDE STREAMLIT UI
# =========================================================

st.markdown(
    f"""
    <style>

    /* =====================================================
       FONT
       ===================================================== */

    @font-face {{
        font-family: "NeoDungGeunMo";
        src: url(data:font/ttf;base64,{font_data});
    }}


    /* =====================================================
       STREAMLIT UI
       ===================================================== */

    #MainMenu {{
        visibility: hidden;
    }}

    header {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    [data-testid="stSidebar"] {{
        display: none;
    }}

    .stApp {{
        background: #000000 !important;
    }}

    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}


    /* =====================================================
       TITLE
       ===================================================== */

    .project-title {{
        position: fixed;

        top: 12vh;
        left: 50%;

        transform: translateX(-50%);

        white-space: nowrap;

        color: #ffffff;

        font-family: "NeoDungGeunMo", monospace;

        font-size: clamp(28px, 4vw, 48px);

        letter-spacing: 2px;

        z-index: 10;

        animation: title-flicker 4s infinite;
    }}


    /* =====================================================
       SUBTITLE
       ===================================================== */

    .project-subtitle {{
        position: fixed;

        top: 22vh;
        left: 50%;

        transform: translateX(-50%);

        white-space: nowrap;

        color: #9c9c9c;

        font-family: "NeoDungGeunMo", monospace;

        font-size: clamp(13px, 1.5vw, 18px);

        letter-spacing: 1px;

        z-index: 10;
    }}


    /* =====================================================
       START CONTAINER
       ===================================================== */

    .st-key-start_button {{
        position: fixed !important;

        top: 51vh !important;
        left: 50% !important;

        transform: translateX(-50%) !important;

        width: 170px !important;
        height: 55px !important;

        padding: 0 !important;
        margin: 0 !important;

        z-index: 1000 !important;
    }}


    /* =====================================================
       START BUTTON
       ===================================================== */

    .st-key-start_button button {{
        width: 170px !important;
        height: 55px !important;

        margin: 0 !important;
        padding: 0 !important;

        border: none !important;
        border-radius: 0 !important;

        background: transparent !important;

        color: #ffffff !important;

        font-family: "NeoDungGeunMo", monospace !important;

        font-size: 19px !important;

        box-shadow: none !important;

        cursor: pointer !important;
    }}


    .st-key-start_button button:hover {{
        background: #ffffff !important;
        color: #000000 !important;
        border: none !important;
    }}


    .st-key-start_button button:focus {{
        background: transparent !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: none !important;
    }}


    .st-key-start_button button:focus:hover {{
        background: #ffffff !important;
        color: #000000 !important;
    }}


    /* =====================================================
       HOW TO PLAY CONTAINER
       ===================================================== */

    .st-key-how_to_play_button {{
        position: fixed !important;

        top: 65vh !important;
        left: 50% !important;

        transform: translateX(-50%) !important;

        width: 220px !important;
        height: 55px !important;

        padding: 0 !important;
        margin: 0 !important;

        z-index: 1000 !important;
    }}


    /* =====================================================
       HOW TO PLAY BUTTON
       ===================================================== */

    .st-key-how_to_play_button button {{
        width: 220px !important;
        height: 55px !important;

        margin: 0 !important;
        padding: 0 !important;

        border: none !important;
        border-radius: 0 !important;

        background: transparent !important;

        color: #ffffff !important;

        font-family: "NeoDungGeunMo", monospace !important;

        font-size: 19px !important;

        box-shadow: none !important;

        cursor: pointer !important;
    }}


    .st-key-how_to_play_button button:hover {{
        background: #ffffff !important;
        color: #000000 !important;
        border: none !important;
    }}


    .st-key-how_to_play_button button:focus {{
        background: transparent !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: none !important;
    }}


    .st-key-how_to_play_button button:focus:hover {{
        background: #ffffff !important;
        color: #000000 !important;
    }}


    /* =====================================================
       POPUP
       ===================================================== */

    .st-key-popup {{
        position: fixed !important;

        top: calc(51vh - 3px) !important;
        left: calc(50% + 105px) !important;

        width: 190px !important;

        padding: 0 !important;
        margin: 0 !important;

        border: 1px solid #ffffff !important;

        background: #050505 !important;

        z-index: 2000 !important;
    }}


    /* =====================================================
       POPUP BUTTON
       ===================================================== */

    .st-key-popup button {{
        width: 188px !important;
        height: 42px !important;

        margin: 0 !important;
        padding: 0 18px !important;

        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;

        border: none !important;
        border-radius: 0 !important;

        background: #050505 !important;

        color: #ffffff !important;

        font-family: "NeoDungGeunMo", monospace !important;

        font-size: 14px !important;

        text-align: left !important;

        box-shadow: none !important;

        cursor: pointer !important;
    }}


    .st-key-popup button:hover {{
        background: #ffffff !important;
        color: #000000 !important;
    }}


    .st-key-popup button:focus {{
        background: #050505 !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: none !important;
    }}


    .st-key-popup button:focus:hover {{
        background: #ffffff !important;
        color: #000000 !important;
    }}


    /* =====================================================
       TITLE FLICKER
       ===================================================== */

    @keyframes title-flicker {{

        0%, 18%, 20%, 22%, 63%, 65%, 100% {{
            opacity: 1;
        }}

        19% {{
            opacity: 0.35;
        }}

        21% {{
            opacity: 0.65;
        }}

        64% {{
            opacity: 0.15;
        }}

    }}


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 600px) {{

        .st-key-start_button {{
            top: 51vh !important;
        }}

        .st-key-how_to_play_button {{
            top: 73vh !important;
        }}

        .st-key-popup {{
            top: 59vh !important;
            left: 50% !important;

            transform: translateX(-50%) !important;
        }}

    }}

    </style>

    <div class="project-title">
        PROJECT : LOGIC
    </div>

    <div class="project-subtitle">
        INFORMATION IS NOT ALWAYS TRUE
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# START BUTTON
# =========================================================

with st.container(key="start_button"):

    start_clicked = st.button(
        "START",
        key="start",
        use_container_width=True,
    )


if start_clicked:
    st.session_state.start_open = (
        not st.session_state.start_open
    )


# =========================================================
# START POPUP
# =========================================================

if st.session_state.start_open:

    with st.container(key="popup"):

        continue_clicked = st.button(
            "CONTINUE",
            key="continue",
            use_container_width=True,
        )

        new_game_clicked = st.button(
            "NEW GAME",
            key="new_game",
            use_container_width=True,
        )

    if continue_clicked:

        st.warning(
            "이전 플레이 기록이 존재하지 않습니다. 새 게임을 시작해주세요."
        )

    if new_game_clicked:

        st.info(
            "GAME SYSTEM은 현재 준비 중입니다."
        )


# =========================================================
# HOW TO PLAY
# =========================================================

with st.container(key="how_to_play_button"):

    how_to_play_clicked = st.button(
        "HOW TO PLAY",
        key="how_to_play",
        use_container_width=True,
    )


# =========================================================
# PAGE NAVIGATION
# =========================================================

if how_to_play_clicked:

    st.switch_page(
        "pages/1_How_To_Play.py"
    )
