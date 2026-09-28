import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PROJECT : LOGIC // GAME",
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

    @font-face {{
        font-family: "NeoDungGeunMo";
        src: url(data:font/ttf;base64,{font_data});
    }}

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

        z-index: 999999 !important;
    }}


    .st-key-pause_button button {{
        width: 140px !important;
        height: 45px !important;

        margin: 0 !important;
        padding: 0 !important;

        border: 1px solid #666666 !important;
        border-radius: 0 !important;

        background: rgba(0, 0, 0, 0.9) !important;

        color: #ffffff !important;

        font-family: "NeoDungGeunMo", monospace !important;
        font-size: 15px !important;

        box-shadow: none !important;

        transition:
            background 0.15s ease,
            color 0.15s ease,
            border-color 0.15s ease !important;
    }}


    .st-key-pause_button button:hover {{
        background: #ffffff !important;
        color: #000000 !important;
        border-color: #ffffff !important;
    }}


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
# PAUSE STATE
# =========================================================

if not st.session_state.game_finished:

    with st.container(key="pause_button"):

        pause_clicked = st.button(
            "RESUME" if st.session_state.game_paused else "PAUSE",
            key="pause_game_button",
        )

    if pause_clicked:

        st.session_state.game_paused = not st.session_state.game_paused

        st.rerun()


# =========================================================
# GAME SCREEN
# =========================================================

paused = st.session_state.game_paused
finished = st.session_state.game_finished
remaining = st.session_state.remaining_seconds


html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

/* =====================================================
   FONT
   ===================================================== */

@font-face {{
    font-family: "NeoDungGeunMo";
    src: url(data:font/ttf;base64,{font_data});
}}


* {{
    box-sizing: border-box;
}}


html,
body {{
    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    background: #000000;

    font-family: "NeoDungGeunMo", monospace;
}}


/* =====================================================
   GAME SCREEN
   ===================================================== */

.game {{
    position: relative;

    width: 100%;
    height: 100vh;

    min-height: 650px;

    background: #050505;

    color: #ffffff;

    overflow: hidden;
}}


/* =====================================================
   TOP INFORMATION
   ===================================================== */

.top-bar {{
    position: absolute;

    top: 25px;
    left: 30px;

    display: flex;
    align-items: center;

    gap: 20px;

    z-index: 20;
}}


.system-label {{
    color: #777777;

    font-size: 13px;

    letter-spacing: 1px;
}}


/* =====================================================
   TIMER
   ===================================================== */

.timer {{
    position: absolute;

    top: 25px;
    left: 50%;

    transform: translateX(-50%);

    z-index: 30;

    font-size: 25px;

    letter-spacing: 2px;

    color: #ffffff;
}}


.timer-label {{
    color: #666666;

    font-size: 11px;

    margin-right: 8px;

    letter-spacing: 1px;
}}


/* =====================================================
   GAME AREA
   ===================================================== */

.game-area {{
    position: absolute;

    left: 50%;
    top: 50%;

    transform: translate(-50%, -50%);

    width: min(1100px, 88vw);
    height: min(650px, 72vh);

    border: 1px solid #222222;

    background: #080808;

    overflow: hidden;
}}


/* =====================================================
   TEMPORARY GAME PLACEHOLDER
   ===================================================== */

.placeholder {{
    position: absolute;

    left: 50%;
    top: 50%;

    transform: translate(-50%, -50%);

    text-align: center;
}}


.placeholder-title {{
    font-size: 25px;

    letter-spacing: 3px;

    margin-bottom: 18px;
}}


.placeholder-text {{
    color: #666666;

    font-size: 13px;

    line-height: 2;
}}


/* =====================================================
   SYSTEM STATUS
   ===================================================== */

.status {{
    position: absolute;

    left: 30px;
    bottom: 25px;

    color: #444444;

    font-size: 11px;

    letter-spacing: 1px;

    z-index: 20;
}}


/* =====================================================
   HELP OVERLAY
   ===================================================== */

.help-overlay {{
    position: fixed;

    inset: 0;

    display: none;

    align-items: center;
    justify-content: center;

    background: rgba(0, 0, 0, 0.82);

    z-index: 1000;
}}


.help-overlay.active {{
    display: flex;
}}


.help-box {{
    width: min(650px, 85vw);

    border: 1px solid #777777;

    background: #050505;

    padding: 30px;
}}


.help-header {{
    display: flex;

    justify-content: space-between;
    align-items: center;

    padding-bottom: 18px;

    border-bottom: 1px solid #333333;

    margin-bottom: 25px;
}}


.help-title {{
    font-size: 21px;

    letter-spacing: 2px;
}}


.help-close {{
    color: #666666;

    font-size: 12px;
}}


.help-row {{
    display: flex;

    align-items: center;

    gap: 20px;

    margin-bottom: 18px;
}}


.help-key {{
    width: 65px;
    height: 35px;

    display: flex;

    align-items: center;
    justify-content: center;

    border: 1px solid #777777;

    background: #111111;

    font-size: 14px;
}}


.help-description {{
    color: #999999;

    font-size: 13px;
}}


.help-important {{
    margin-top: 25px;

    padding-top: 20px;

    border-top: 1px solid #333333;

    color: #666666;

    font-size: 12px;

    line-height: 1.8;
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

    background: rgba(0, 0, 0, 0.88);

    z-index: 900;
}}


.pause-overlay.active {{
    display: flex;
}}


.pause-box {{
    text-align: center;
}}


.pause-title {{
    font-size: 32px;

    letter-spacing: 5px;

    margin-bottom: 18px;
}}


.pause-subtitle {{
    color: #666666;

    font-size: 12px;

    letter-spacing: 1px;
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

    z-index: 2000;
}}


.game-over.active {{
    display: flex;
}}


.game-over-box {{
    text-align: center;
}}


.game-over-title {{
    font-size: 38px;

    letter-spacing: 5px;

    margin-bottom: 20px;
}}


.game-over-text {{
    color: #666666;

    font-size: 13px;

    line-height: 2;
}}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {{

    .top-bar {{
        top: 18px;
        left: 18px;
    }}

    .system-label {{
        font-size: 10px;
    }}

    .timer {{
        top: 65px;

        font-size: 21px;
    }}

    .game-area {{
        width: 92vw;
        height: 65vh;
    }}

    .placeholder-title {{
        font-size: 19px;
    }}

}}

</style>

</head>


<body>


<div class="game">


    <!-- =================================================
         TOP BAR
         ================================================= -->

    <div class="top-bar">

        <div class="system-label">
            PROJECT : LOGIC
        </div>

    </div>


    <!-- =================================================
         TIMER
         ================================================= -->

    <div class="timer">

        <span class="timer-label">
            REMAINING
        </span>

        <span id="timer">
            15:00
        </span>

    </div>


    <!-- =================================================
         GAME AREA
         ================================================= -->

    <div class="game-area">

        <div class="placeholder">

            <div class="placeholder-title">
                SYSTEM INITIALIZING
            </div>

            <div class="placeholder-text">

                ECHO SYSTEM // ONLINE

                <br>

                FACILITY STATUS // UNKNOWN

                <br>

                <br>

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
         HELP OVERLAY
         ================================================= -->

    <div
        id="helpOverlay"
        class="help-overlay"
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


            <div class="help-row">

                <div class="help-key">
                    W A S D
                </div>

                <div class="help-description">
                    연구시설 내부를 이동합니다.
                </div>

            </div>


            <div class="help-row">

                <div class="help-key">
                    E
                </div>

                <div class="help-description">
                    주변의 물체를 조사하거나 아이템을 획득합니다.
                </div>

            </div>


            <div class="help-row">

                <div class="help-key">
                    I
                </div>

                <div class="help-description">
                    인벤토리와 획득한 단서를 확인합니다.
                </div>

            </div>


            <div class="help-row">

                <div class="help-key">
                    SPACE
                </div>

                <div class="help-description">
                    대화 및 시스템 메시지를 진행합니다.
                </div>

            </div>


            <div class="help-row">

                <div class="help-key">
                    H
                </div>

                <div class="help-description">
                    게임 조작법을 다시 확인합니다.
                </div>

            </div>


            <div class="help-row">

                <div class="help-key">
                    ESC
                </div>

                <div class="help-description">
                    현재 열려 있는 창을 닫습니다.
                </div>

            </div>


            <div class="help-important">

                주변의 물체와 기록을 자세히 조사하십시오.

                <br>

                ECHO가 제공하는 모든 정보가 사실이라고 가정하지 마십시오.

            </div>

        </div>

    </div>


    <!-- =================================================
         PAUSE OVERLAY
         ================================================= -->

    <div
        id="pauseOverlay"
        class="pause-overlay
        {"active" if paused else ""}"
    >

        <div class="pause-box">

            <div class="pause-title">
                GAME PAUSED
            </div>

            <div class="pause-subtitle">
                PRESS RESUME TO CONTINUE
            </div>

        </div>

    </div>


    <!-- =================================================
         TIME OVER
         ================================================= -->

    <div
        id="gameOver"
        class="game-over
        {"active" if finished else ""}"
    >

        <div class="game-over-box">

            <div class="game-over-title">
                TIME OVER
            </div>

            <div class="game-over-text">

                FACILITY RESET INITIATED.

                <br>

                ECHO CONNECTION TERMINATED.

                <br>

                <br>

                THE INVESTIGATION HAS ENDED.

            </div>

        </div>

    </div>


</div>


<script>

/* =========================================================
   TIMER
   ========================================================= */

let remaining = {remaining};

let paused = {"true" if paused else "false"};
let finished = {"true" if finished else "false"};

const timerElement = document.getElementById("timer");
const helpOverlay = document.getElementById("helpOverlay");


function updateTimer() {{

    if (finished) {{
        return;
    }}

    if (paused) {{
        return;
    }}

    let minutes = Math.floor(remaining / 60);
    let seconds = remaining % 60;

    let minuteText = String(minutes).padStart(2, "0");
    let secondText = String(seconds).padStart(2, "0");

    timerElement.textContent =
        minuteText + ":" + secondText;


    if (remaining <= 0) {{

        remaining = 0;

        timerElement.textContent = "00:00";

        document.getElementById("gameOver")
            .classList.add("active");

        finished = true;

        return;
    }}

    remaining--;
}}


if (!paused && !finished) {{

    updateTimer();

    setInterval(updateTimer, 1000);

}}


/* =========================================================
   KEYBOARD CONTROLS
   ========================================================= */

document.addEventListener("keydown", function(event) {{

    const key = event.key.toLowerCase();


    /* -----------------------------------------------------
       H : HELP
       ----------------------------------------------------- */

    if (key === "h") {{

        if (!finished) {{

            helpOverlay.classList.add("active");

        }}

        event.preventDefault();

    }}


    /* -----------------------------------------------------
       ESC : CLOSE HELP
       ----------------------------------------------------- */

    if (event.key === "Escape") {{

        helpOverlay.classList.remove("active");

    }}

}});

</script>


</body>

</html>
"""


# =========================================================
# RENDER GAME
# =========================================================

components.html(
    html,
    height=1000,
    scrolling=False,
)
