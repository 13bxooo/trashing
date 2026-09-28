import streamlit as st

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

if "save_exists" not in st.session_state:
    st.session_state.save_exists = False

if "continue_message" not in st.session_state:
    st.session_state.continue_message = ""


# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

/* =========================================================
   STREAMLIT 기본 UI 제거
========================================================= */

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


/* =========================================================
   전체 화면
========================================================= */

.stApp {
    background: #000000;
}

[data-testid="stAppViewContainer"] {
    background: #000000;
}

.block-container {
    padding: 0 !important;
    max-width: none !important;
}


/* =========================================================
   PROJECT : LOGIC
========================================================= */

.main-title {

    position: fixed;

    top: 70px;
    left: 50%;

    transform: translateX(-50%);

    color: #ffffff;

    font-family: monospace;

    font-size: 38px;

    font-weight: normal;

    letter-spacing: 7px;

    white-space: nowrap;

    text-align: center;

    z-index: 5;
}


/* =========================================================
   SUBTITLE
========================================================= */

.subtitle {

    position: fixed;

    top: 125px;
    left: 50%;

    transform: translateX(-50%);

    color: #777777;

    font-family: monospace;

    font-size: 11px;

    letter-spacing: 4px;

    white-space: nowrap;

    z-index: 5;
}


/* =========================================================
   메뉴 전체 영역
========================================================= */

.menu-area {

    position: fixed;

    top: 300px;
    left: 50%;

    transform: translateX(-50%);

    width: 520px;

    height: 150px;

    z-index: 10;
}


/* =========================================================
   START
========================================================= */

.start-position {

    position: absolute;

    left: 50%;
    top: 0;

    transform: translateX(-50%);

    width: 250px;
}


/* =========================================================
   HOW TO PLAY
========================================================= */

.how-position {

    position: absolute;

    left: 50%;
    top: 64px;

    transform: translateX(-50%);

    width: 250px;
}


/* =========================================================
   기본 버튼
========================================================= */

.stButton > button {

    width: 250px !important;

    height: 48px !important;

    background: #000000 !important;

    color: #ffffff !important;

    border: 1px solid #ffffff !important;

    border-radius: 0 !important;

    font-family: monospace !important;

    font-size: 13px !important;

    letter-spacing: 3px !important;

    transition:
        background 0.15s ease,
        color 0.15s ease !important;
}


.stButton > button:hover {

    background: #ffffff !important;

    color: #000000 !important;

    border-color: #ffffff !important;
}


.stButton > button:focus {

    box-shadow: none !important;

}


/* =========================================================
   START 오른쪽 오버레이
========================================================= */

.start-overlay {

    position: absolute;

    left: calc(50% + 140px);

    top: -1px;

    width: 190px;

    padding: 8px;

    background: #000000;

    border: 1px solid #ffffff;

    z-index: 100;

}


/* =========================================================
   오버레이 내부 버튼
========================================================= */

.overlay-button .stButton > button {

    width: 172px !important;

    height: 40px !important;

    border: 0 !important;

    background: #000000 !important;

    color: #ffffff !important;

    font-size: 12px !important;

    letter-spacing: 2px !important;
}


.overlay-button .stButton > button:hover {

    background: #ffffff !important;

    color: #000000 !important;
}


/* =========================================================
   CONTINUE 오류 메시지
========================================================= */

.continue-warning {

    position: fixed;

    left: 50%;
    bottom: 50px;

    transform: translateX(-50%);

    width: 500px;

    padding: 14px 20px;

    background: #000000;

    border: 1px solid #777777;

    color: #ffffff;

    font-family: monospace;

    font-size: 12px;

    line-height: 1.7;

    text-align: center;

    z-index: 200;
}


/* =========================================================
   VERSION
========================================================= */

.version {

    position: fixed;

    bottom: 20px;
    left: 25px;

    color: #333333;

    font-family: monospace;

    font-size: 9px;

    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown("""
<div class="main-title">
    PROJECT : LOGIC
</div>

<div class="subtitle">
    INFORMATION IS NOT ALWAYS TRUE
</div>

<div class="version">
    SYSTEM // LOGIC-001
</div>
""", unsafe_allow_html=True)


# =========================================================
# MENU AREA
# =========================================================

st.markdown(
    '<div class="menu-area">',
    unsafe_allow_html=True
)


# =========================================================
# START
# =========================================================

st.markdown(
    '<div class="start-position">',
    unsafe_allow_html=True
)

if st.button(
    "START",
    key="start_button"
):

    st.session_state.show_start_menu = (
        not st.session_state.show_start_menu
    )

    st.session_state.continue_message = ""

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# START OVERLAY
# =========================================================

if st.session_state.show_start_menu:

    st.markdown(
        '<div class="start-overlay">',
        unsafe_allow_html=True
    )

    # CONTINUE
    st.markdown(
        '<div class="overlay-button">',
        unsafe_allow_html=True
    )

    if st.button(
        "CONTINUE",
        key="continue_button"
    ):

        if st.session_state.save_exists:

            st.session_state.show_start_menu = False
            st.session_state.continue_message = ""

            st.switch_page("pages/1_Game.py")

        else:

            st.session_state.continue_message = (
                "이전 플레이 기록이 존재하지 않습니다.<br>"
                "새 게임을 시작해주세요."
            )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # NEW GAME
    st.markdown(
        '<div class="overlay-button">',
        unsafe_allow_html=True
    )

    if st.button(
        "NEW GAME",
        key="new_game_button"
    ):

        # =================================================
        # 게임 초기화
        # =================================================

        st.session_state.save_exists = True

        st.session_state.game_started = True

        st.session_state.current_room = "CONTROL ROOM"

        st.session_state.player_x = 50
        st.session_state.player_y = 50

        st.session_state.inventory = []

        st.session_state.echo_log = []

        st.session_state.solved_puzzles = []

        st.session_state.game_time = 59 * 60

        st.session_state.game_state = "GAME"

        st.session_state.show_start_menu = False

        st.session_state.continue_message = ""

        st.switch_page("pages/1_Game.py")

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# HOW TO PLAY
# =========================================================

st.markdown(
    '<div class="how-position">',
    unsafe_allow_html=True
)

if st.button(
    "HOW TO PLAY",
    key="how_to_play"
):

    st.session_state.show_start_menu = False

    st.switch_page("pages/2_How_to_Play.py")

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CONTINUE ERROR
# =========================================================

if st.session_state.continue_message:

    st.markdown(
        f"""
        <div class="continue-warning">
            {st.session_state.continue_message}
        </div>
        """,
        unsafe_allow_html=True
    )
