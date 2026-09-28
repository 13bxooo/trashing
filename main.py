import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PROJECT : LOGIC",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

if "show_start_menu" not in st.session_state:
    st.session_state.show_start_menu = False

if "continue_message" not in st.session_state:
    st.session_state.continue_message = ""


# =========================================================
# FUNCTIONS
# =========================================================

def toggle_start_menu():
    st.session_state.show_start_menu = not st.session_state.show_start_menu


def new_game():
    st.session_state.show_start_menu = False
    st.switch_page("pages/1_Game.py")


def continue_game():
    st.session_state.show_start_menu = False

    # 아직 저장 시스템을 만들지 않았으므로
    # 현재는 저장 데이터가 없는 상태
    save_exists = False

    if save_exists:
        st.switch_page("pages/1_Game.py")
    else:
        st.session_state.continue_message = (
            "이전 플레이 기록이 존재하지 않습니다. "
            "새 게임을 시작해주세요."
        )


def how_to_play():
    st.switch_page("pages/2_How_to_Play.py")


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       STREAMLIT 기본 UI 제거
    ========================================= */

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stHeader"] {
        display: none;
    }

    [data-testid="stToolbar"] {
        display: none;
    }


    /* =========================================
       전체 화면
    ========================================= */

    .stApp {
        background: #000000 !important;
    }

    [data-testid="stAppViewContainer"] {
        background: #000000 !important;
    }

    [data-testid="stMain"] {
        background: #000000 !important;
    }

    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: none !important;
    }


    /* =========================================
       PROJECT : LOGIC
    ========================================= */

    .project-title {
        position: fixed;

        top: 12vh;
        left: 50%;

        transform: translateX(-50%);

        color: white;

        font-family:
            "Courier New",
            Consolas,
            monospace;

        font-size: clamp(32px, 4vw, 58px);

        font-weight: bold;

        letter-spacing: 0.12em;

        white-space: nowrap;

        z-index: 10;

        animation: project-flicker 4s infinite;

        text-shadow:
            0 0 4px rgba(255,255,255,0.8),
            0 0 12px rgba(255,255,255,0.25);
    }


    /* =========================================
       SUBTITLE
    ========================================= */

    .project-subtitle {
        position: fixed;

        top: 22vh;
        left: 50%;

        transform: translateX(-50%);

        color: #9a9a9a;

        font-family:
            "Courier New",
            Consolas,
            monospace;

        font-size: clamp(10px, 1.1vw, 15px);

        letter-spacing: 0.25em;

        white-space: nowrap;

        z-index: 10;
    }


    /* =========================================
       모든 버튼 공통
    ========================================= */

    div[data-testid="stButton"] {
        position: fixed;

        z-index: 20;
    }

    div[data-testid="stButton"] > button {

        background: transparent !important;

        border: none !important;

        color: #ffffff !important;

        box-shadow: none !important;

        border-radius: 0 !important;

        font-family:
            "Courier New",
            Consolas,
            monospace !important;

        cursor: pointer;

        transition: none !important;
    }

    div[data-testid="stButton"] > button:hover {

        background: transparent !important;

        color: #ffffff !important;

        border: none !important;

        box-shadow:
            0 0 5px rgba(255,255,255,0.3) !important;
    }


    /* =========================================
       START
    ========================================= */

    div[data-testid="stButton"]:has(button[key="start_button"]) {

        top: 51vh;

        left: 50%;

        transform: translateX(-50%);

        width: 170px;

        height: 55px;
    }

    div[data-testid="stButton"]:has(button[key="start_button"]) button {

        font-size: 22px !important;

        letter-spacing: 0.12em;

        height: 55px;

        width: 170px;
    }


    /* =========================================
       HOW TO PLAY
    ========================================= */

    div[data-testid="stButton"]:has(button[key="how_button"]) {

        top: 65vh;

        left: 50%;

        transform: translateX(-50%);

        width: 220px;

        height: 55px;
    }

    div[data-testid="stButton"]:has(button[key="how_button"]) button {

        font-size: 17px !important;

        letter-spacing: 0.12em;

        height: 55px;

        width: 220px;
    }


    /* =========================================
       START SUB MENU
    ========================================= */

    div[data-testid="stButton"]:has(button[key="continue_button"]) {

        top: 49vh;

        left: calc(50% + 120px);

        width: 175px;

        height: 45px;

        background: #080808;
    }

    div[data-testid="stButton"]:has(button[key="new_game_button"]) {

        top: 56vh;

        left: calc(50% + 120px);

        width: 175px;

        height: 45px;

        background: #080808;
    }


    /* 메뉴 테두리 */

    div[data-testid="stButton"]:has(button[key="continue_button"])::before {

        content: "";

        position: absolute;

        inset: -1px;

        border: 1px solid #555555;

        pointer-events: none;
    }

    div[data-testid="stButton"]:has(button[key="new_game_button"])::after {

        content: "";

        position: absolute;

        left: -1px;
        right: -1px;
        bottom: -1px;

        height: 1px;

        background: #555555;

        pointer-events: none;
    }


    /* =========================================
       CONTINUE / NEW GAME
       마우스 올렸을 때 깜빡임
    ========================================= */

    div[data-testid="stButton"]:has(button[key="continue_button"]) button,
    div[data-testid="stButton"]:has(button[key="new_game_button"]) button {

        font-size: 14px !important;

        letter-spacing: 0.1em;

        height: 45px;

        width: 175px;

        text-align: left;

        padding-left: 18px !important;
    }


    div[data-testid="stButton"]:has(button[key="continue_button"]) button:hover,
    div[data-testid="stButton"]:has(button[key="new_game_button"]) button:hover {

        background: #ffffff !important;

        color: #000000 !important;

        animation:
            menu-flicker 0.55s steps(1, end) infinite;
    }


    /* =========================================
       CONTINUE 오류 메시지
    ========================================= */

    .continue-message {

        position: fixed;

        top: 76vh;

        left: 50%;

        transform: translateX(-50%);

        width: 520px;

        max-width: 80vw;

        padding: 12px 18px;

        background: #080808;

        border: 1px solid #444444;

        color: #d0d0d0;

        text-align: center;

        font-family:
            "Courier New",
            Consolas,
            monospace;

        font-size: 12px;

        letter-spacing: 0.04em;

        z-index: 30;
    }


    /* =========================================
       PROJECT LOGIC 깜빡임
    ========================================= */

    @keyframes project-flicker {

        0%, 4% {
            opacity: 1;
        }

        5% {
            opacity: 0.45;
        }

        6% {
            opacity: 1;
        }

        13% {
            opacity: 1;
        }

        14% {
            opacity: 0.2;
        }

        15% {
            opacity: 0.85;
        }

        16% {
            opacity: 1;
        }

        38% {
            opacity: 1;
        }

        39% {
            opacity: 0.4;
        }

        40% {
            opacity: 0.1;
        }

        41% {
            opacity: 0.9;
        }

        42% {
            opacity: 1;
        }

        70% {
            opacity: 1;
        }

        71% {
            opacity: 0.3;
        }

        72% {
            opacity: 1;
        }

        100% {
            opacity: 1;
        }
    }


    /* =========================================
       메뉴 깜빡임
    ========================================= */

    @keyframes menu-flicker {

        0% {
            opacity: 1;
        }

        20% {
            opacity: 0.15;
        }

        21% {
            opacity: 1;
        }

        42% {
            opacity: 0.35;
        }

        43% {
            opacity: 1;
        }

        64% {
            opacity: 0.1;
        }

        65% {
            opacity: 1;
        }

        82% {
            opacity: 0.4;
        }

        83% {
            opacity: 1;
        }

        100% {
            opacity: 1;
        }
    }


    /* =========================================
       모바일
    ========================================= */

    @media (max-width: 700px) {

        .project-title {
            top: 12vh;
            font-size: 30px;
        }

        .project-subtitle {
            top: 21vh;
            font-size: 9px;
        }

        div[data-testid="stButton"]:has(button[key="continue_button"]),
        div[data-testid="stButton"]:has(button[key="new_game_button"]) {

            left: 50%;

            transform: translateX(-50%);
        }

        div[data-testid="stButton"]:has(button[key="continue_button"]) {
            top: 59vh;
        }

        div[data-testid="stButton"]:has(button[key="new_game_button"]) {
            top: 66vh;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
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
        INFORMATION IS NOT ALWAYS TRUE
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# START
# =========================================================

st.button(
    "START",
    key="start_button",
    on_click=toggle_start_menu
)


# =========================================================
# START SUB MENU
# =========================================================

if st.session_state.show_start_menu:

    st.button(
        "CONTINUE",
        key="continue_button",
        on_click=continue_game
    )

    st.button(
        "NEW GAME",
        key="new_game_button",
        on_click=new_game
    )


# =========================================================
# HOW TO PLAY
# =========================================================

st.button(
    "HOW TO PLAY",
    key="how_button",
    on_click=how_to_play
)


# =========================================================
# CONTINUE MESSAGE
# =========================================================

if st.session_state.continue_message:

    st.markdown(
        f"""
        <div class="continue-message">
            {st.session_state.continue_message}
        </div>
        """,
        unsafe_allow_html=True
    )
