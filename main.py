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
    """START 메뉴 열기 / 닫기"""
    st.session_state.show_start_menu = (
        not st.session_state.show_start_menu
    )


def new_game():
    """새 게임 시작"""
    st.session_state.show_start_menu = False
    st.session_state.continue_message = ""

    st.switch_page("pages/1_Game.py")


def continue_game():
    """이전 게임 이어하기"""

    st.session_state.show_start_menu = False

    # -----------------------------------------
    # 현재는 저장 시스템이 아직 없으므로 False
    # 나중에 실제 save.json 시스템으로 교체
    # -----------------------------------------

    save_exists = False

    if save_exists:

        st.switch_page("pages/1_Game.py")

    else:

        st.session_state.continue_message = (
            "이전 플레이 기록이 존재하지 않습니다. "
            "새 게임을 시작해주세요."
        )


def how_to_play():
    """게임 방법 화면으로 이동"""
    st.switch_page("pages/2_How_to_Play.py")


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       STREAMLIT 기본 UI 제거
       ===================================================== */

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


    /* =====================================================
       전체 배경
       ===================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {

        background: #000000 !important;
    }

    .stApp {

        background: #000000 !important;

        color: #ffffff !important;

        overflow: hidden !important;
    }

    .block-container {

        padding: 0 !important;

        margin: 0 !important;

        max-width: none !important;

        width: 100% !important;
    }


    /* =====================================================
       PROJECT : LOGIC
       ===================================================== */

    .project-title {

        position: fixed;

        top: 12vh;

        left: 50%;

        transform: translateX(-50%);

        z-index: 50;

        color: #ffffff;

        font-family:
            "Courier New",
            Consolas,
            monospace;

        font-size: clamp(32px, 4vw, 58px);

        font-weight: bold;

        letter-spacing: 0.12em;

        white-space: nowrap;

        text-align: center;

        animation:
            project-flicker
            4.2s
            infinite;

        text-shadow:
            0 0 4px rgba(255,255,255,0.85),
            0 0 12px rgba(255,255,255,0.25);
    }


    /* =====================================================
       SUBTITLE
       ===================================================== */

    .project-subtitle {

        position: fixed;

        top: 22vh;

        left: 50%;

        transform: translateX(-50%);

        z-index: 50;

        color: #9a9a9a;

        font-family:
            "Courier New",
            Consolas,
            monospace;

        font-size: clamp(10px, 1.1vw, 15px);

        letter-spacing: 0.25em;

        white-space: nowrap;

        text-align: center;
    }


    /* =====================================================
       START CONTAINER
       ===================================================== */

    .st-key-start-area {

        position: fixed !important;

        top: 51vh !important;

        left: 50% !important;

        transform: translateX(-50%) !important;

        width: 170px !important;

        height: 55px !important;

        padding: 0 !important;

        margin: 0 !important;

        z-index: 100 !important;
    }


    /* =====================================================
       START BUTTON
       ===================================================== */

    .st-key-start-area button {

        width: 170px !important;

        height: 55px !important;

        padding: 0 !important;

        margin: 0 !important;

        border: none !important;

        border-radius: 0 !important;

        background: transparent !important;

        color: #ffffff !important;

        box-shadow: none !important;

        font-family:
            "Courier New",
            Consolas,
            monospace !important;

        font-size: 22px !important;

        font-weight: normal !important;

        letter-spacing: 0.12em !important;

        cursor: pointer !important;

        transition: none !important;
    }

    .st-key-start-area button:hover {

        background: transparent !important;

        color: #ffffff !important;

        border: none !important;

        box-shadow:
            0 0 6px rgba(255,255,255,0.18) !important;
    }


    /* =====================================================
       START POPUP
       ===================================================== */

    .st-key-start-menu {

        position: fixed !important;

        top: 48.5vh !important;

        left: calc(50% + 105px) !important;

        width: 190px !important;

        padding: 7px 0 !important;

        margin: 0 !important;

        background: #080808 !important;

        border: 1px solid #555555 !important;

        box-sizing: border-box !important;

        z-index: 200 !important;

        animation:
            popup-appear
            0.12s
            steps(2, end);
    }


    /* =====================================================
       POPUP 내부 버튼
       ===================================================== */

    .st-key-start-menu button {

        display: block !important;

        width: 188px !important;

        height: 42px !important;

        padding: 0 18px !important;

        margin: 0 !important;

        border: none !important;

        border-radius: 0 !important;

        background: transparent !important;

        color: #ffffff !important;

        box-shadow: none !important;

        font-family:
            "Courier New",
            Consolas,
            monospace !important;

        font-size: 14px !important;

        font-weight: normal !important;

        letter-spacing: 0.1em !important;

        text-align: left !important;

        cursor: pointer !important;

        transition: none !important;
    }


    /* =====================================================
       POPUP 버튼 사이 구분
       ===================================================== */

    .st-key-start-menu button + button {

        border-top: 1px solid #222222 !important;
    }


    /* =====================================================
       CONTINUE / NEW GAME hover
       형광등 불량처럼 깜빡임
       ===================================================== */

    .st-key-start-menu button:hover {

        background: #ffffff !important;

        color: #000000 !important;

        box-shadow: none !important;

        animation:
            menu-flicker
            0.55s
            steps(1, end)
            infinite;
    }


    /* =====================================================
       HOW TO PLAY CONTAINER
       ===================================================== */

    .st-key-how-area {

        position: fixed !important;

        top: 65vh !important;

        left: 50% !important;

        transform: translateX(-50%) !important;

        width: 220px !important;

        height: 55px !important;

        padding: 0 !important;

        margin: 0 !important;

        z-index: 100 !important;
    }


    /* =====================================================
       HOW TO PLAY BUTTON
       ===================================================== */

    .st-key-how-area button {

        width: 220px !important;

        height: 55px !important;

        padding: 0 !important;

        margin: 0 !important;

        border: none !important;

        border-radius: 0 !important;

        background: transparent !important;

        color: #ffffff !important;

        box-shadow: none !important;

        font-family:
            "Courier New",
            Consolas,
            monospace !important;

        font-size: 17px !important;

        font-weight: normal !important;

        letter-spacing: 0.12em !important;

        cursor: pointer !important;

        transition: none !important;
    }

    .st-key-how-area button:hover {

        background: transparent !important;

        color: #ffffff !important;

        box-shadow:
            0 0 6px rgba(255,255,255,0.18) !important;
    }


    /* =====================================================
       CONTINUE 오류 메시지
       ===================================================== */

    .continue-message {

        position: fixed;

        left: 50%;

        top: 76vh;

        transform: translateX(-50%);

        width: 520px;

        max-width: 80vw;

        padding: 12px 18px;

        box-sizing: border-box;

        background: #080808;

        border: 1px solid #444444;

        color: #d0d0d0;

        font-family:
            "Courier New",
            Consolas,
            monospace;

        font-size: 12px;

        letter-spacing: 0.04em;

        text-align: center;

        z-index: 300;

        animation:
            message-appear
            0.2s
            steps(2, end);
    }


    /* =====================================================
       PROJECT : LOGIC 깜빡임
       ===================================================== */

    @keyframes project-flicker {

        0%,
        4% {
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


    /* =====================================================
       메뉴 hover 깜빡임
       ===================================================== */

    @keyframes menu-flicker {

        0% {
            opacity: 1;
        }

        18% {
            opacity: 0.15;
        }

        19% {
            opacity: 1;
        }

        38% {
            opacity: 0.35;
        }

        39% {
            opacity: 1;
        }

        60% {
            opacity: 0.1;
        }

        61% {
            opacity: 1;
        }

        80% {
            opacity: 0.45;
        }

        81% {
            opacity: 1;
        }

        100% {
            opacity: 1;
        }
    }


    /* =====================================================
       팝업 등장
       ===================================================== */

    @keyframes popup-appear {

        0% {
            opacity: 0;

            transform:
                translateX(-8px);
        }

        100% {
            opacity: 1;

            transform:
                translateX(0);
        }
    }


    /* =====================================================
       메시지 등장
       ===================================================== */

    @keyframes message-appear {

        0% {
            opacity: 0;
        }

        100% {
            opacity: 1;
        }
    }


    /* =====================================================
       모바일 대응
       ===================================================== */

    @media (max-width: 700px) {

        .project-title {

            top: 12vh;

            font-size: 30px;
        }

        .project-subtitle {

            top: 21vh;

            font-size: 9px;
        }

        .st-key-start-menu {

            left: 50% !important;

            top: 59vh !important;

            transform: translateX(-50%) !important;
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
# START BUTTON
# =========================================================

with st.container(key="start_area"):

    st.button(
        "START",
        key="start_button",
        on_click=toggle_start_menu
    )


# =========================================================
# START POPUP
# =========================================================

if st.session_state.show_start_menu:

    with st.container(key="start_menu"):

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

with st.container(key="how_area"):

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
