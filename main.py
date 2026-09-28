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

/* ---------------------------------------------------------
   STREAMLIT 기본 UI 제거
--------------------------------------------------------- */

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


/* ---------------------------------------------------------
   전체 화면
--------------------------------------------------------- */

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


/* ---------------------------------------------------------
   타이틀
--------------------------------------------------------- */

.main-title {
    position: fixed;

    top: 50%;
    left: 50%;

    transform: translate(-50%, -105%);

    color: #ffffff;

    font-family: monospace;

    font-size: 42px;

    font-weight: bold;

    letter-spacing: 8px;

    white-space: nowrap;

    text-align: center;
}


/* ---------------------------------------------------------
   부제
--------------------------------------------------------- */

.subtitle {
    position: fixed;

    top: calc(50% + 5px);
    left: 50%;

    transform: translateX(-50%);

    color: #8c8c8c;

    font-family: monospace;

    font-size: 12px;

    letter-spacing: 4px;

    white-space: nowrap;
}


/* ---------------------------------------------------------
   버튼 영역
--------------------------------------------------------- */

.menu-wrapper {

    position: fixed;

    left: 50%;
    top: calc(50% + 90px);

    transform: translateX(-50%);

    width: 330px;

    text-align: center;
}


/* ---------------------------------------------------------
   Streamlit 버튼
--------------------------------------------------------- */

.stButton > button {

    width: 100% !important;

    height: 48px !important;

    background: #000000 !important;

    color: #ffffff !important;

    border: 1px solid #ffffff !important;

    border-radius: 0 !important;

    font-family: monospace !important;

    font-size: 14px !important;

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


/* ---------------------------------------------------------
   START 하위 메뉴
--------------------------------------------------------- */

.start-menu {

    width: 330px;

    margin-top: 8px;

    margin-bottom: 8px;

    padding: 8px;

    background: #000000;

    border: 1px solid #ffffff;
}


/* ---------------------------------------------------------
   오류 메시지
--------------------------------------------------------- */

.continue-warning {

    position: fixed;

    left: 50%;
    bottom: 45px;

    transform: translateX(-50%);

    width: 520px;

    padding: 13px 20px;

    background: #000000;

    border: 1px solid #777777;

    color: #ffffff;

    font-family: monospace;

    font-size: 13px;

    line-height: 1.7;

    text-align: center;
}


/* ---------------------------------------------------------
   버전 표시
--------------------------------------------------------- */

.version {

    position: fixed;

    bottom: 20px;
    left: 25px;

    color: #444444;

    font-family: monospace;

    font-size: 10px;

    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    """
    <div class="main-title">
        PROJECT : LOGIC
    </div>

    <div class="subtitle">
        INFORMATION IS NOT ALWAYS TRUE
    </div>

    <div class="version">
        SYSTEM // LOGIC-001
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MENU
# =========================================================

# 화면 중앙에 메뉴를 배치하기 위한 여백
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")


menu_left, menu_center, menu_right = st.columns(
    [2.2, 1, 2.2]
)

with menu_center:

    # -----------------------------------------------------
    # START
    # -----------------------------------------------------

    if st.button(
        "START",
        key="start_button",
        use_container_width=True
    ):
        st.session_state.show_start_menu = (
            not st.session_state.show_start_menu
        )

        st.session_state.continue_message = ""


    # -----------------------------------------------------
    # START SUB MENU
    # -----------------------------------------------------

    if st.session_state.show_start_menu:

        st.markdown(
            '<div class="start-menu">',
            unsafe_allow_html=True
        )

        if st.button(
            "CONTINUE",
            key="continue_button",
            use_container_width=True
        ):

            # 저장된 게임이 존재하는 경우
            if st.session_state.save_exists:

                st.session_state.show_start_menu = False
                st.session_state.continue_message = ""

                st.switch_page("pages/1_Game.py")

            # 저장된 게임이 없는 경우
            else:

                st.session_state.continue_message = (
                    "이전 플레이 기록이 존재하지 않습니다.<br>"
                    "새 게임을 시작해주세요."
                )

        if st.button(
            "NEW GAME",
            key="new_game_button",
            use_container_width=True
        ):

            # =================================================
            # 새로운 게임 데이터 초기화
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

            # 게임 페이지로 이동
            st.switch_page("pages/1_Game.py")

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # HOW TO PLAY
    # -----------------------------------------------------

    if st.button(
        "HOW TO PLAY",
        key="how_to_play",
        use_container_width=True
    ):

        st.session_state.show_start_menu = False

        st.switch_page("pages/2_How_to_Play.py")


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
