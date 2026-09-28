import base64
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


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

if "game_started" not in st.session_state:
    st.session_state.game_started = True

if "game_paused" not in st.session_state:
    st.session_state.game_paused = False

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False

if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 15 * 60

# 타이머가 실제로 시작된 시각
if "timer_deadline" not in st.session_state:
    st.session_state.timer_deadline = time.time() + 15 * 60


# =========================================================
# TIMER
# =========================================================

# 일시정지 상태가 아니라면 현재 시각을 기준으로 남은 시간 계산
if not st.session_state.game_paused:
    current_time = time.time()

    st.session_state.remaining_seconds = max(
        0,
        int(
            st.session_state.timer_deadline
            - current_time
        )
    )

    if st.session_state.remaining_seconds <= 0:
        st.session_state.game_finished = True


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
            font_data = base64.b64encode(
                f.read()
            ).decode("utf-8")
        break


# =========================================================
# PAUSE BUTTON
# =========================================================

if not st.session_state.game_finished:

    with st.container(key="pause_button"):

        pause_clicked = st.button(
            "RESUME"
            if st.session_state.game_paused
            else "PAUSE",
            key="pause_game_button",
        )

    if pause_clicked:

        # -------------------------------------------------
        # PAUSE
        # -------------------------------------------------

        if not st.session_state.game_paused:

            current_time = time.time()

            st.session_state.remaining_seconds = max(
                0,
                int(
                    st.session_state.timer_deadline
                    - current_time
                )
            )

            st.session_state.game_paused = True

        # -------------------------------------------------
        # RESUME
        # -------------------------------------------------

        else:

            st.session_state.timer_deadline = (
                time.time()
                + st.session_state.remaining_seconds
            )

            st.session_state.game_paused = False

        st.rerun()


# =========================================================
# CSS
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
       PAUSE BUTTON
       ===================================================== */

    .st-key-pause_button {{
        position: fixed !important;

        top: 25px !important;
        right: 30px !important;

        width: 140px !important;
        height: 45px !important;

        margin: 0 !important;
        padding: 0 !important;

        z-index: 1000 !important;
    }}


    .st-key-pause_button button {{
        width: 140px !important;
        height: 45px !important;

        margin: 0 !important;
        padding: 0 !important;

        border: 1px solid #555555 !important;
        border-radius: 0 !important;

        background: #000000 !important;
        color: #ffffff !important;

        font-family: "NeoDungGeunMo", monospace !important;
        font-size: 15px !important;

        box-shadow: none !important;

        transition:
            background 0.15s ease,
            color 0.15s ease !important;
    }}


    .st-key-pause_button button:hover {{
        background: #ffffff !important;
        color: #000000 !important;
        border-color: #ffffff !important;
    }}


    .st-key-pause_button button:focus {{
        box-shadow: none !important;
    }}


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 700px) {{

        .st-key-pause_button {{
            top: 18px !important;
            right: 18px !important;

            width: 115px !important;
            height: 40px !important;
        }}

        .st-key-pause_button button {{
            width: 115px !important;
            height: 40px !important;

            font-size: 13px !important;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# GAME SCREEN
# =========================================================

remaining = st.session_state.remaining_seconds

paused = st.session_state.game_paused

finished = st.session_state.game_finished


game_html = f"""
<!DOCTYPE html>

<html>

<head>

<style>

* {{
    box-sizing: border-box;
}}

html,
body {{
    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    background: #000000;

    overflow: hidden;

    font-family: "Courier New", monospace;
}}


/* =====================================================
   GAME BACKGROUND
   ===================================================== */

.game-screen {{
    position: relative;

    width: 100%;
    height: 100vh;

    min-height: 700px;

    background: #000000;

    color: #ffffff;
}}


/* =====================================================
   TOP LEFT
   ===================================================== */

.project-label {{
    position: absolute;

    top: 25px;
    left: 30px;

    color: #777777;

    font-family: "Courier New", monospace;

    font-size: 13px;

    letter-spacing: 2px;
}}


/* =====================================================
   TIMER
   ===================================================== */

.timer {{
    position: absolute;

    top: 25px;
    left: 50%;

    transform: translateX(-50%);

    color: #ffffff;

    font-family: "Courier New", monospace;

    font-size: 20px;

    letter-spacing: 2px;
}}


/* =====================================================
   GAME AREA
   ===================================================== */

.game-area {{
    position: absolute;

    top: 105px;
    left: 50%;

    transform: translateX(-50%);

    width: min(1100px, 86vw);
    height: calc(100vh - 210px);

    min-height: 480px;

    border: 1px solid #333333;

    background:
        linear-gradient(
            rgba(255,255,255,0.015) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(255,255,255,0.015) 1px,
            transparent 1px
        );

    background-size: 32px 32px;
}}


/* =====================================================
   CENTER SYSTEM
   ===================================================== */

.system-center {{
    position: absolute;

    top: 50%;
    left: 50%;

    transform: translate(-50%, -50%);

    text-align: center;

    white-space: nowrap;
}}


.system-title {{
    font-size: 20px;

    letter-spacing: 4px;

    margin-bottom: 18px;
}}


.system-line {{
    color: #666666;

    font-size: 12px;

    letter-spacing: 2px;

    margin: 7px 0;
}}


/* =====================================================
   BOTTOM STATUS
   ===================================================== */

.status {{
    position: absolute;

    bottom: 25px;
    left: 30px;

    color: #555555;

    font-size: 11px;

    letter-spacing: 2px;
}}


/* =====================================================
   HOW TO PLAY OVERLAY
   ===================================================== */

.overlay {{
    position: fixed;

    inset: 0;

    display: none;

    align-items: center;
    justify-content: center;

    background: rgba(0,0,0,0.92);

    z-index: 5000;
}}


.overlay.active {{
    display: flex;
}}


.help-box {{
    width: min(760px, 86vw);

    max-height: 82vh;

    overflow-y: auto;

    padding: 38px 45px;

    border: 1px solid #555555;

    background: #050505;

    color: #ffffff;
}}


.help-header {{
    display: flex;

    justify-content: space-between;

    align-items: center;

    padding-bottom: 18px;

    margin-bottom: 25px;

    border-bottom: 1px solid #333333;
}}


.help-title {{
    font-size: 22px;

    letter-spacing: 3px;
}}


.help-close {{
    color: #777777;

    font-size: 11px;

    letter-spacing: 1px;
}}


.help-section {{
    margin-bottom: 25px;
}}


.help-number {{
    color: #777777;

    font-size: 11px;

    letter-spacing: 2px;

    margin-bottom: 7px;
}}


.help-name {{
    font-size: 15px;

    letter-spacing: 2px;

    margin-bottom: 7px;
}}


.help-description {{
    color: #999999;

    font-size: 12px;

    line-height: 1.8;

    letter-spacing: 0.5px;
}}


.help-warning {{
    margin-top: 30px;

    padding-top: 20px;

    border-top: 1px solid #333333;

    color: #bbbbbb;

    font-size: 11px;

    line-height: 1.8;

    letter-spacing: 0.5px;
}}


.help-footer {{
    margin-top: 20px;

    color: #555555;

    font-size: 10px;

    letter-spacing: 2px;
}}


/* =====================================================
   PAUSE OVERLAY
   ===================================================== */

.pause-overlay {{
    position: fixed;

    inset: 0;

    display: none;

    align-items: center;
    justify-content: center;

    background: rgba(0,0,0,0.92);

    z-index: 4000;
}}


.pause-overlay.active {{
    display: flex;
}}


.pause-box {{
    text-align: center;
}}


.pause-title {{
    font-size: 24px;

    letter-spacing: 5px;

    margin-bottom: 15px;
}}


.pause-text {{
    color: #666666;

    font-size: 11px;

    letter-spacing: 2px;
}}


/* =====================================================
   TIME OVER
   ===================================================== */

.game-over {{
    position: fixed;

    inset: 0;

    display: none;

    align-items: center;
    justify-content: center;

    background: #000000;

    z-index: 6000;
}}


.game-over.active {{
    display: flex;
}}


.game-over-box {{
    text-align: center;
}}


.game-over-title {{
    font-size: 30px;

    letter-spacing: 5px;

    margin-bottom: 20px;
}}


.game-over-line {{
    color: #666666;

    font-size: 11px;

    letter-spacing: 2px;

    margin: 8px;
}}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {{

    .project-label {{
        left: 18px;
        top: 20px;
        font-size: 10px;
    }}

    .timer {{
        top: 20px;
        font-size: 16px;
    }}

    .game-area {{
        top: 90px;

        width: 92vw;

        height: calc(100vh - 170px);

        min-height: 450px;
    }}

    .status {{
        left: 18px;
        bottom: 18px;
    }}

    .help-box {{
        padding: 28px 24px;

        width: 90vw;
    }}

    .help-title {{
        font-size: 18px;
    }}

    .help-close {{
        font-size: 9px;
    }}

}}

</style>

</head>


<body>


<div class="game-screen">


    <!-- =================================================
         TOP
         ================================================= -->

    <div class="project-label">
        PROJECT : LOGIC
    </div>


    <div
        id="timer"
        class="timer"
    >
        REMAINING 00:00
    </div>


    <!-- =================================================
         GAME AREA
         ================================================= -->

    <div class="game-area">

        <div class="system-center">

            <div class="system-title">
                SYSTEM INITIALIZING
            </div>

            <div class="system-line">
                ECHO SYSTEM // ONLINE
            </div>

            <div class="system-line">
                FACILITY STATUS // UNKNOWN
            </div>

            <div class="system-line">
                PRESS H TO VIEW CONTROLS
            </div>

        </div>

    </div>


    <!-- =================================================
         STATUS
         ================================================= -->

    <div class="status">
        ECHO SYSTEM // CONNECTION ESTABLISHED
    </div>


    <!-- =================================================
         HOW TO PLAY
         ================================================= -->

    <div
        id="helpOverlay"
        class="overlay"
    >

        <div class="help-box">

            <div class="help-header">

                <div class="help-title">
                    HOW TO PLAY
                </div>

                <div class="help-close">
                    ESC TO CLOSE
                </div>

            </div>


            <div class="help-section">

                <div class="help-number">
                    01
                </div>

                <div class="help-name">
                    MOVEMENT // W A S D
                </div>

                <div class="help-description">
                    연구시설 내부를 이동합니다.
                </div>

            </div>


            <div class="help-section">

                <div class="help-number">
                    02
                </div>

                <div class="help-name">
                    INTERACTION // E
                </div>

                <div class="help-description">
                    주변의 물체를 조사하거나
                    아이템을 획득합니다.
                </div>

            </div>


            <div class="help-section">

                <div class="help-number">
                    03
                </div>

                <div class="help-name">
                    INVENTORY // I
                </div>

                <div class="help-description">
                    획득한 아이템과 기록을 확인합니다.
                    ESC로 닫을 수 있습니다.
                </div>

            </div>


            <div class="help-section">

                <div class="help-number">
                    04
                </div>

                <div class="help-name">
                    SYSTEM MESSAGE // SPACE
                </div>

                <div class="help-description">
                    ECHO의 시스템 메시지와
                    대화를 확인합니다.
                </div>

            </div>


            <div class="help-section">

                <div class="help-number">
                    05
                </div>

                <div class="help-name">
                    HOW TO PLAY // H
                </div>

                <div class="help-description">
                    현재 화면에서 조작 방법을 확인합니다.
                </div>

            </div>


            <div class="help-warning">

                IMPORTANT // 모든 물체와 기록을 주의 깊게 조사하세요.<br>
                ECHO가 제공하는 모든 정보가 사실이라고 가정하지 마세요.<br>
                서로 모순되는 단서가 발견될 수 있습니다.

            </div>


            <div class="help-footer">
                ECHO SYSTEM // INFORMATION IS NOT ALWAYS TRUE
            </div>

        </div>

    </div>


    <!-- =================================================
         PAUSE OVERLAY
         ================================================= -->

    <div
        id="pauseOverlay"
        class="pause-overlay"
    >

        <div class="pause-box">

            <div class="pause-title">
                GAME PAUSED
            </div>

            <div class="pause-text">
                PRESS RESUME TO CONTINUE
            </div>

        </div>

    </div>


    <!-- =================================================
         TIME OVER
         ================================================= -->

    <div
        id="gameOver"
        class="game-over"
    >

        <div class="game-over-box">

            <div class="game-over-title">
                TIME OVER
            </div>

            <div class="game-over-line">
                FACILITY RESET INITIATED
            </div>

            <div class="game-over-line">
                ECHO CONNECTION TERMINATED
            </div>

            <div class="game-over-line">
                THE INVESTIGATION HAS ENDED
            </div>

        </div>

    </div>


</div>


<script>


// =========================================================
// INITIAL STATE
// =========================================================

let remaining = {remaining};

let paused = {"true" if paused else "false"};

let finished = {"true" if finished else "false"};

let helpOpen = false;


// =========================================================
// ELEMENTS
// =========================================================

const timerElement =
    document.getElementById("timer");

const helpOverlay =
    document.getElementById("helpOverlay");

const pauseOverlay =
    document.getElementById("pauseOverlay");

const gameOver =
    document.getElementById("gameOver");


// =========================================================
// TIMER
// =========================================================

function renderTimer() {{

    let minutes =
        Math.floor(remaining / 60);

    let seconds =
        remaining % 60;

    timerElement.textContent =
        "REMAINING "
        + String(minutes).padStart(2, "0")
        + ":"
        + String(seconds).padStart(2, "0");
}}


function updateTimer() {{

    renderTimer();

    if (finished) {{
        gameOver.classList.add("active");
        return;
    }}

    if (paused || helpOpen) {{
        return;
    }}

    if (remaining <= 0) {{

        remaining = 0;

        renderTimer();

        finished = true;

        gameOver.classList.add("active");

        return;
    }}

    remaining--;
}}


renderTimer();


// =========================================================
// PAUSE STATE
// =========================================================

if (paused) {{
    pauseOverlay.classList.add("active");
}}


// =========================================================
// TIMER LOOP
// =========================================================

setInterval(
    updateTimer,
    1000
);


// =========================================================
// KEYBOARD
// =========================================================

document.addEventListener(
    "keydown",
    function(event) {{

        const key =
            event.key.toLowerCase();


        // -----------------------------------------------
        // H
        // -----------------------------------------------

        if (key === "h") {{

            if (!finished) {{

                helpOpen = true;

                helpOverlay.classList.add(
                    "active"
                );

            }}

            event.preventDefault();

        }}


        // -----------------------------------------------
        // ESC
        // -----------------------------------------------

        if (event.key === "Escape") {{

            if (helpOpen) {{

                helpOpen = false;

                helpOverlay.classList.remove(
                    "active"
                );

                event.preventDefault();

            }}

        }}

    }}
);


</script>


</body>

</html>
"""


# =========================================================
# RENDER GAME
# =========================================================

components.html(
    game_html,
    height=1000,
    scrolling=False,
)
