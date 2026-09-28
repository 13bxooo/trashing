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
# SESSION STATE
# =========================================================

if "start_open" not in st.session_state:
    st.session_state.start_open = False

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_paused" not in st.session_state:
    st.session_state.game_paused = False

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False

if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 15 * 60


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
# STREAMLIT UI HIDDEN
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
        background: #000000;
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
        left: 0;

        width: 100%;

        text-align: center;

        color: #ffffff;

        font-family: "NeoDungGeunMo", monospace;

        font-size: 42px;

        letter-spacing: 3px;

        z-index: 10;

        animation: titleFlicker 4s infinite;
    }}


    .project-subtitle {{
        position: fixed;

        top: 22vh;
        left: 0;

        width: 100%;

        text-align: center;

        color: #555555;

        font-family: "NeoDungGeunMo", monospace;

        font-size: 13px;

        letter-spacing: 2px;

        z-index: 10;
    }}


    /* =====================================================
       TITLE FLICKER
       ===================================================== */

    @keyframes titleFlicker {{

        0% {{
            opacity: 1;
        }}

        3% {{
            opacity: 0.75;
        }}

        4% {{
            opacity: 1;
        }}

        8% {{
            opacity: 0.9;
        }}

        9% {{
            opacity: 1;
        }}

        100% {{
            opacity: 1;
        }}

    }}


    /* =====================================================
       START BUTTON
       ===================================================== */

    .st-key-start_button {{
        position: fixed !important;

        top: 51vh !important;
        left: 50% !important;

        transform: translateX(-50%) !important;

        width: 170px !important;
        height: 55px !important;

        margin: 0 !important;
        padding: 0 !important;

        z-index: 100 !important;
    }}


    .st-key-start_button button {{
        width: 170px !important;
        height: 55px !important;

        margin: 0 !important;
        padding: 0 !important;

        border: none !important;
        border-radius: 0 !important;

        background: #000000 !important;

        color: #ffffff !important;

        font-family: "NeoDungGeunMo", monospace !important;

        font-size: 19px !important;

        box-shadow: none !important;

        outline: none !important;

        transition:
            background 0.15s ease,
            color 0.15s ease !important;
    }}


    .st-key-start_button button:hover {{
        background: #ffffff !important;

        color: #000000 !important;

        border: none !important;
    }}


    .st-key-start_button button:focus {{
        box-shadow: none !important;

        outline: none !important;

        border: none !important;
    }}


    /* =====================================================
       HOW TO PLAY BUTTON
       ===================================================== */

    .st-key-how_to_play_button {{
        position: fixed !important;

        top: 65vh !important;
        left: 50% !important;

        transform: translateX(-50%) !important;

        width: 220px !important;
        height: 55px !important;

        margin: 0 !important;
        padding: 0 !important;

        z-index: 100 !important;
    }}


    .st-key-how_to_play_button button {{
        width: 220px !important;
        height: 55px !important;

        margin: 0 !important;
        padding: 0 !important;

        border: none !important;
        border-radius: 0 !important;

        background: #000000 !important;

        color: #ffffff !important;

        font-family: "NeoDungGeunMo", monospace !important;

        font-size: 19px !important;

        box-shadow: none !important;

        outline: none !important;

        transition:
            background 0.15s ease,
            color 0.15s ease !important;
    }}


    .st-key-how_to_play_button button:hover {{
        background: #ffffff !important;

        color: #000000 !important;

        border: none !important;
    }}


    .st-key-how_to_play_button button:focus {{
        box-shadow: none !important;

        outline: none !important;

        border: none !important;
    }}


    /* =====================================================
       START POPUP
       ===================================================== */

    .st-key-popup {{
        position: fixed !important;

        top: calc(51vh - 3px) !important;
        left: calc(50% + 105px) !important;

        width: 190px !important;

        margin: 0 !important;
        padding: 6px !important;

        background: #000000 !important;

        /* 팝업 바깥쪽 테두리는 유지 */

        border: 1px solid #555555 !important;

        z-index: 200 !important;
    }}


    /* =====================================================
       CONTINUE / NEW GAME
       ===================================================== */

    .st-key-popup button {{
        width: 100% !important;
        height: 42px !important;

        margin: 0 0 6px 0 !important;
        padding: 0 !important;

        /* 버튼 자체에는 테두리 없음 */

        border: none !important;
        border-radius: 0 !important;

        background: #000000 !important;

        color: #ffffff !important;

        font-family: "NeoDungGeunMo", monospace !important;

        font-size: 14px !important;

        box-shadow: none !important;

        outline: none !important;

        transition:
            background 0.15s ease,
            color 0.15s ease !important;
    }}


    .st-key-popup button:last-child {{
        margin-bottom: 0 !important;
    }}


    .st-key-popup button:hover {{
        background: #ffffff !important;

        color: #000000 !important;

        border: none !important;
    }}


    .st-key-popup button:focus {{
        box-shadow: none !important;

        outline: none !important;

        border: none !important;
    }}


    /* =====================================================
       WARNING / INFO
       ===================================================== */

    [data-testid="stAlert"] {{
        position: fixed !important;

        top: calc(51vh + 115px) !important;
        left: 50% !important;

        transform: translateX(-50%) !important;

        width: 390px !important;

        z-index: 300 !important;

        font-family: "NeoDungGeunMo", monospace !important;

        font-size: 13px !important;
    }}


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 700px) {{

        .project-title {{
            top: 15vh;

            font-size: 30px;

            letter-spacing: 2px;
        }}

        .project-subtitle {{
            top: 23vh;

            font-size: 10px;
        }}


        .st-key-start_button {{
            top: 56vh !important;

            width: 160px !important;
        }}


        .st-key-start_button button {{
            width: 160px !important;
        }}


        .st-key-how_to_play_button {{
            top: 73vh !important;

            width: 200px !important;
        }}


        .st-key-how_to_play_button button {{
            width: 200px !important;
        }}


        .st-key-popup {{
            top: 59vh !important;

            left: 50% !important;

            transform: translateX(-50%) !important;

            width: 180px !important;
        }}


        [data-testid="stAlert"] {{
            width: 85vw !important;

            top: 70vh !important;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    """
    <div class="project-title">
        PROJECT : LOGIC
    </div>

    <div class="project-subtitle">
        FACILITY CONTROL SYSTEM
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
# HOW TO PLAY BUTTON
# =========================================================

with st.container(key="how_to_play_button"):

    how_to_play_clicked = st.button(
        "HOW TO PLAY",
        key="how_to_play",
        use_container_width=True,
    )


if how_to_play_clicked:

    st.switch_page("pages/1_How_To_Play.py")


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


    # =====================================================
    # CONTINUE
    # =====================================================

    if continue_clicked:

        st.warning(
            "이전 플레이 기록이 존재하지 않습니다. 새 게임을 시작해주세요."
        )


    # =====================================================
    # NEW GAME
    # =====================================================

    if new_game_clicked:

        # -------------------------------------------------
        # 새로운 게임 상태 초기화
        # -------------------------------------------------

        st.session_state.game_started = True

        st.session_state.game_paused = False

        st.session_state.game_finished = False

        # 15분 = 900초

        st.session_state.remaining_seconds = 15 * 60

        # -------------------------------------------------
        # START POPUP 닫기
        # -------------------------------------------------

        st.session_state.start_open = False

        # -------------------------------------------------
        # GAME 화면으로 이동
        # -------------------------------------------------

        st.switch_page("pages/2_Game.py")
