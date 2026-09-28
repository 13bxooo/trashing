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

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "save_exists" not in st.session_state:
    st.session_state.save_exists = False

if "show_start_menu" not in st.session_state:
    st.session_state.show_start_menu = False

if "continue_message" not in st.session_state:
    st.session_state.continue_message = ""

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    margin: 0;
    padding: 0;
    background: #111820;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    padding: 0 !important;
    max-width: none !important;
}

/* 전체 화면 */

.logic-screen {
    position: relative;
    width: 100vw;
    min-height: 100vh;

    background:
        repeating-linear-gradient(
            0deg,
            #182631 0px,
            #182631 39px,
            #1c2c38 40px
        );

    color: white;
    font-family: monospace;

    overflow: hidden;
}


/* 상단 제목 */

.logic-title {
    position: absolute;
    top: 24px;
    left: 28px;

    padding: 10px 16px;

    background: #101820;

    border: 2px solid #71889a;

    font-family: monospace;
    font-size: 18px;
    font-weight: bold;

    letter-spacing: 2px;

    z-index: 5;
}


/* 타이머 */

.logic-timer {
    position: absolute;

    top: 24px;
    right: 28px;

    padding: 10px 16px;

    background: #101820;

    border: 2px solid #71889a;

    font-family: monospace;

    font-size: 17px;

    letter-spacing: 1px;

    z-index: 5;
}


/* 게임 영역 */

.logic-room {

    position: absolute;

    left: 7%;
    right: 7%;

    top: 100px;
    bottom: 150px;

    border: 3px solid #536b7c;

    background:
        repeating-linear-gradient(
            0deg,
            #1b2a35 0px,
            #1b2a35 39px,
            #20313d 40px
        );

    box-shadow:
        inset 0 0 0 2px #0d151c,
        0 0 30px rgba(0,0,0,0.4);
}


/* ECHO */

.echo-text {

    position: absolute;

    top: 20%;
    left: 50%;

    transform: translateX(-50%);

    color: #9db3c4;

    font-size: 14px;

    letter-spacing: 8px;
}


/* 연구시설 */

.room-center {

    position: absolute;

    top: 45%;
    left: 50%;

    transform: translate(-50%, -50%);

    width: 230px;
    height: 120px;

    border: 2px solid #405766;

    display: flex;

    justify-content: center;
    align-items: center;

    text-align: center;

    color: #8097a8;

    font-size: 14px;

    line-height: 1.7;
}


/* 메뉴 영역 */

.menu-area {

    position: absolute;

    left: 50%;
    bottom: 185px;

    transform: translateX(-50%);

    display: flex;

    align-items: flex-start;

    gap: 14px;

    z-index: 10;
}


/* 메뉴 버튼 */

.stButton > button {

    background: #101820 !important;

    color: #dce6ec !important;

    border: 2px solid #71889a !important;

    border-radius: 0 !important;

    font-family: monospace !important;

    font-size: 14px !important;

    letter-spacing: 1px !important;

    min-width: 150px !important;

    height: 45px !important;

    transition: 0.15s !important;
}

.stButton > button:hover {

    background: #243746 !important;

    border-color: #a7bac8 !important;

    color: white !important;
}


/* START 하위 메뉴 */

.start-submenu {

    position: absolute;

    left: 0;

    top: 54px;

    width: 150px;

    background: #101820;

    border: 2px solid #71889a;

    padding: 8px;

    z-index: 20;
}


/* 메시지 */

.system-message {

    position: absolute;

    left: 7%;
    right: 7%;

    bottom: 25px;

    min-height: 75px;

    background: #f1f1f1;

    border: 3px solid #536b7c;

    color: #111820;

    display: flex;

    align-items: center;

    padding: 15px 20px;

    z-index: 4;
}


.message-label {

    width: 130px;

    color: #243746;

    font-size: 13px;

    font-weight: bold;

    letter-spacing: 1px;
}


.message-text {

    color: #111820;

    font-size: 15px;

    line-height: 1.6;
}


/* 안내 메시지 */

.continue-warning {

    position: absolute;

    left: 50%;

    bottom: 130px;

    transform: translateX(-50%);

    width: 420px;

    padding: 14px 20px;

    background: #101820;

    border: 2px solid #71889a;

    color: #dce6ec;

    text-align: center;

    font-family: monospace;

    font-size: 13px;

    line-height: 1.7;

    z-index: 30;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# BACKGROUND
# =========================================================

st.markdown("""
<div class="logic-screen">

    <div class="logic-title">
        ☰ PROJECT : LOGIC
    </div>

    <div class="logic-timer">
        TIME&nbsp;&nbsp;59:59
    </div>

    <div class="logic-room">

        <div class="echo-text">
            E C H O
        </div>

        <div class="room-center">
            RESEARCH FACILITY
            <br>
            CONTROL ROOM
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# MAIN MENU
# =========================================================

# 버튼을 화면 중앙 하단에 배치하기 위한 컬럼
left_space, menu_col, right_space = st.columns([1.8, 1, 1.8])

with menu_col:

    start_col, how_col = st.columns(2)

    with start_col:

        if st.button(
            "START",
            key="start_button",
            use_container_width=True
        ):
            st.session_state.show_start_menu = (
                not st.session_state.show_start_menu
            )

    with how_col:

        if st.button(
            "HOW TO PLAY",
            key="how_button",
            use_container_width=True
        ):
            st.switch_page("pages/2_How_to_Play.py")


# =========================================================
# START SUB MENU
# =========================================================

if st.session_state.show_start_menu:

    sub_left, sub_menu, sub_right = st.columns([2.1, 0.9, 2])

    with sub_menu:

        st.markdown(
            '<div class="start-submenu">',
            unsafe_allow_html=True
        )

        if st.button(
            "CONTINUE",
            key="continue_button",
            use_container_width=True
        ):

            if st.session_state.save_exists:

                st.session_state.game_started = True
                st.session_state.show_start_menu = False
                st.session_state.continue_message = ""

                st.switch_page("pages/1_Game.py")

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

            # 새로운 게임 시작
            st.session_state.game_started = True
            st.session_state.save_exists = True

            # 게임 데이터 초기화
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


# =========================================================
# CONTINUE ERROR MESSAGE
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


# =========================================================
# SYSTEM MESSAGE
# =========================================================

st.markdown("""
<div class="system-message">

    <div class="message-label">
        SYSTEM
    </div>

    <div class="message-text">
        시스템이 초기화되었습니다.
        <br>
        <b>ECHO</b> 연결을 확인하고 있습니다...
    </div>

</div>
""", unsafe_allow_html=True)
