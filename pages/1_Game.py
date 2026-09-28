import streamlit as st

st.set_page_config(
    page_title="PROJECT : LOGIC",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# GAME STATE
# =========================================================

if "current_room" not in st.session_state:
    st.session_state.current_room = "CONTROL ROOM"

if "player_x" not in st.session_state:
    st.session_state.player_x = 50

if "player_y" not in st.session_state:
    st.session_state.player_y = 50

if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "echo_log" not in st.session_state:
    st.session_state.echo_log = []

if "solved_puzzles" not in st.session_state:
    st.session_state.solved_puzzles = []

if "game_time" not in st.session_state:
    st.session_state.game_time = 59 * 60

if "game_state" not in st.session_state:
    st.session_state.game_state = "GAME"


# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

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


/* GAME */

.game {

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

    font-family: monospace;

    overflow: hidden;
}


/* TITLE */

.title {

    position: absolute;

    top: 24px;
    left: 28px;

    padding: 10px 16px;

    background: #101820;

    border: 2px solid #71889a;

    color: white;

    font-size: 18px;

    font-weight: bold;

    letter-spacing: 2px;
}


/* TIMER */

.timer {

    position: absolute;

    top: 24px;
    right: 28px;

    padding: 10px 16px;

    background: #101820;

    border: 2px solid #71889a;

    color: white;

    font-size: 17px;

    letter-spacing: 1px;
}


/* ROOM */

.room {

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


/* ROOM NAME */

.room-name {

    position: absolute;

    top: 18px;
    left: 24px;

    color: #71889a;

    font-size: 12px;

    letter-spacing: 2px;
}


/* ECHO */

.echo {

    position: absolute;

    top: 20%;
    left: 50%;

    transform: translateX(-50%);

    color: #9db3c4;

    font-size: 14px;

    letter-spacing: 6px;
}


/* PLAYER PLACEHOLDER */

.player {

    position: absolute;

    left: 50%;
    top: 65%;

    transform: translate(-50%, -50%);

    width: 24px;
    height: 24px;

    background: #dce6ec;

    border: 2px solid #71889a;

    box-shadow:
        4px 4px 0 #405766;
}


/* MESSAGE */

.message {

    position: absolute;

    left: 7%;
    right: 7%;

    bottom: 25px;

    min-height: 90px;

    background: #f1f1f1;

    border: 3px solid #536b7c;

    display: flex;

    align-items: center;

    padding: 15px 20px;
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


/* HINT */

.controls {

    position: absolute;

    right: 7%;

    bottom: 135px;

    color: #71889a;

    font-size: 11px;

    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# GAME SCREEN
# =========================================================

minutes = st.session_state.game_time // 60
seconds = st.session_state.game_time % 60

time_text = f"{minutes:02d}:{seconds:02d}"

st.markdown(
    f"""
    <div class="game">

        <div class="title">
            ☰ PROJECT : LOGIC
        </div>

        <div class="timer">
            TIME&nbsp;&nbsp;{time_text}
        </div>

        <div class="room">

            <div class="room-name">
                {st.session_state.current_room}
            </div>

            <div class="echo">
                E C H O
            </div>

            <div class="player"></div>

        </div>

        <div class="controls">
            WASD : MOVE &nbsp;&nbsp; E : INTERACT &nbsp;&nbsp; I : INVENTORY
        </div>

        <div class="message">

            <div class="message-label">
                SYSTEM
            </div>

            <div class="message-text">
                게임이 시작되었습니다.
                <br>
                연구 시설을 탐색하여 탈출 방법을 찾아내십시오.
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SAVE
# =========================================================

# 실제 게임 기능이 추가되면 이 부분에서
# 플레이어 위치, 아이템, 퍼즐 진행도 등을 자동 저장하게 됨.

st.session_state.save_exists = True
