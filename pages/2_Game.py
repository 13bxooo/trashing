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
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# SESSION STATE
# =========================================================

if "game_paused" not in st.session_state:
    st.session_state.game_paused = False

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False

if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 15 * 60

if "timer_deadline" not in st.session_state:
    st.session_state.timer_deadline = time.time() + 15 * 60


# =========================================================
# SYSTEM FAILURE BUTTONS
# =========================================================
# iframe 내부 버튼이 아니라 Streamlit 버튼으로 처리해서
# RESTART / TITLE이 확실하게 작동하도록 함.
# =========================================================

if st.session_state.game_finished:

    restart_clicked = False
    title_clicked = False

    with st.container(key="failure_buttons"):

        restart_clicked = st.button(
            "RESTART",
            key="failure_restart",
        )

        title_clicked = st.button(
            "TITLE",
            key="failure_title",
        )

    if restart_clicked:

        st.session_state.game_paused = False
        st.session_state.game_finished = False
        st.session_state.remaining_seconds = 15 * 60
        st.session_state.timer_deadline = (
            time.time() + 15 * 60
        )

        st.rerun()

    if title_clicked:

        st.switch_page("main.py")


# =========================================================
# TIMER
# =========================================================

if not st.session_state.game_paused:
    current_time = time.time()

    st.session_state.remaining_seconds = max(
        0,
        int(
            st.session_state.timer_deadline
            - current_time
        ),
    )

    if st.session_state.remaining_seconds <= 0:
        st.session_state.game_finished = True


remaining = st.session_state.remaining_seconds
paused = st.session_state.game_paused
finished = st.session_state.game_finished

minutes = remaining // 60
seconds = remaining % 60

timer_text = f"{minutes:02d}:{seconds:02d}"


# =========================================================
# FONT
# =========================================================

font_path = None

for name in [
    "neodgm.ttf",
    "neodgm(2).ttf",
]:

    candidate = Path(name)

    if candidate.exists():
        font_path = candidate
        break


if font_path:

    font_base64 = base64.b64encode(
        font_path.read_bytes()
    ).decode("utf-8")

else:

    font_base64 = ""


# =========================================================
# STREAMLIT CSS
# =========================================================

st.markdown(
    f"""
    <style>

    @font-face {{
        font-family: 'NeoDungGeunMo';

        src:
            url(data:font/ttf;base64,{font_base64})
            format('truetype');
    }}


    html,
    body,
    [class*="css"] {{
        font-family:
            'NeoDungGeunMo',
            monospace !important;
    }}


    #MainMenu,
    header,
    footer {{
        visibility: hidden;
    }}


    .stApp {{
        background: #000000 !important;
    }}


    .block-container {{
        padding: 0 !important;
        max-width: 100vw !important;
    }}


    /* =====================================================
       PAUSE
       ===================================================== */

    .st-key-pause_game_button {{

        position: fixed !important;

        top: 24px !important;
        right: 28px !important;

        width: 45px !important;
        height: 45px !important;

        z-index: 999999 !important;

        padding: 0 !important;
        margin: 0 !important;

    }}


    .st-key-pause_game_button button {{

        width: 45px !important;
        height: 45px !important;

        padding: 0 !important;
        margin: 0 !important;

        border: none !important;
        outline: none !important;
        box-shadow: none !important;

        border-radius: 0 !important;

        background: #000000 !important;
        color: #ffffff !important;

        font-family:
            'NeoDungGeunMo',
            monospace !important;

        font-size: 24px !important;

        cursor: pointer !important;

    }}


    .st-key-pause_game_button button:hover {{

        background: #ffffff !important;
        color: #000000 !important;

    }}


    /* =====================================================
       SYSTEM FAILURE BUTTONS
       ===================================================== */

    .st-key-failure_buttons {{

        position: fixed !important;

        left: 50% !important;
        top: 61% !important;

        transform:
            translateX(-50%) !important;

        width: 170px !important;

        z-index: 9999999 !important;

        display: flex !important;

        flex-direction: column !important;

        gap: 8px !important;

    }}


    .st-key-failure_buttons button {{

        width: 170px !important;
        height: 44px !important;

        padding: 0 !important;
        margin: 0 !important;

        border: none !important;
        outline: none !important;
        box-shadow: none !important;

        border-radius: 0 !important;

        background: #000000 !important;
        color: #ffffff !important;

        font-family:
            'NeoDungGeunMo',
            monospace !important;

        font-size: 15px !important;

        cursor: pointer !important;

    }}


    .st-key-failure_buttons button:hover {{

        background: #ffffff !important;
        color: #000000 !important;

    }}


    @media (max-width: 700px) {{

        .st-key-pause_game_button {{

            top: 16px !important;
            right: 16px !important;

            width: 40px !important;
            height: 40px !important;

        }}


        .st-key-pause_game_button button {{

            width: 40px !important;
            height: 40px !important;

            font-size: 21px !important;

        }}


        .st-key-failure_buttons {{

            top: 63% !important;

            width: 150px !important;

        }}


        .st-key-failure_buttons button {{

            width: 150px !important;
            height: 42px !important;

            font-size: 13px !important;

        }}

    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PAUSE
# =========================================================

pause_clicked = st.button(
    "▶" if st.session_state.game_paused else "||",
    key="pause_game_button",
)


if pause_clicked:

    if not st.session_state.game_paused:

        current_time = time.time()

        st.session_state.remaining_seconds = max(
            0,
            int(
                st.session_state.timer_deadline
                - current_time
            ),
        )

        st.session_state.game_paused = True

    else:

        st.session_state.timer_deadline = (
            time.time()
            + st.session_state.remaining_seconds
        )

        st.session_state.game_paused = False

    st.rerun()


# =========================================================
# GAME HTML
# =========================================================

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

    font-family:
        'NeoDungGeunMo';

    src:
        url(data:font/ttf;base64,{font_base64})
        format('truetype');

}}


* {{

    box-sizing: border-box;

    user-select: none;

    -webkit-user-select: none;

}}


html,
body {{

    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    background: #000000;

    font-family:
        'NeoDungGeunMo',
        monospace;

}}


body {{

    color: #ffffff;

}}


/* =====================================================
   GAME
   ===================================================== */

.game {{

    position: relative;

    width: 100vw;
    height: 100vh;

    background: #000000;

    overflow: hidden;

    outline: none;

}}


/* =====================================================
   TOP UI
   ===================================================== */

.project-title {{

    position: absolute;

    top: 24px;
    left: 28px;

    font-size: 18px;

    letter-spacing: 1px;

    z-index: 20;

}}


.stage-title {{

    position: absolute;

    top: 52px;
    left: 28px;

    font-size: 13px;

    color: #777777;

    letter-spacing: 1px;

    z-index: 20;

}}


.timer {{

    position: absolute;

    top: 24px;
    left: 50%;

    transform:
        translateX(-50%);

    font-size: 22px;

    letter-spacing: 2px;

    z-index: 20;

}}


/* =====================================================
   GAME AREA
   ===================================================== */

.game-area {{

    position: absolute;

    top: 90px;
    left: 28px;
    right: 28px;
    bottom: 70px;

    overflow: hidden;

    background-color: #080808;

    background-image:

        linear-gradient(
            rgba(255,255,255,0.045) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,0.045) 1px,
            transparent 1px
        );

    background-size: 40px 40px;

}}


/* =====================================================
   ROOM
   ===================================================== */

.room {{

    position: absolute;

    left: 7%;
    top: 8%;

    width: 86%;
    height: 82%;

    border:
        1px solid
        rgba(255,255,255,0.12);

    overflow: hidden;

}}


.room-line-horizontal {{

    position: absolute;

    left: 0;
    right: 0;

    top: 50%;

    height: 1px;

    background:
        rgba(255,255,255,0.045);

}}


.room-line-vertical {{

    position: absolute;

    top: 0;
    bottom: 0;

    left: 50%;

    width: 1px;

    background:
        rgba(255,255,255,0.045);

}}


/* =====================================================
   OBJECTS
   ===================================================== */

.object {{

    position: absolute;

    display: flex;

    align-items: center;
    justify-content: center;

    background: #0b0b0b;

    border:
        1px solid
        rgba(255,255,255,0.22);

    color: #777777;

    font-size: 12px;

    text-align: center;

}}


.monitor {{

    left: 43%;
    top: 13%;

    width: 14%;
    height: 12%;

}}


.desk {{

    left: 35%;
    top: 62%;

    width: 30%;
    height: 12%;

}}


.terminal {{

    left: 18%;
    top: 35%;

    width: 14%;
    height: 17%;

}}


.exit-door {{

    right: 0;

    top: 35%;

    width: 8%;
    height: 30%;

    background: #111111;

    writing-mode:
        vertical-rl;

    letter-spacing: 2px;

}}


.object-label {{

    position: absolute;

    bottom: -22px;
    left: 50%;

    transform:
        translateX(-50%);

    white-space: nowrap;

    font-size: 10px;

    color: #555555;

}}


/* =====================================================
   PLAYER
   ===================================================== */

.player {{

    position: absolute;

    width: 24px;
    height: 24px;

    left: 50%;
    top: 43%;

    transform:
        translate(-50%, -50%);

    background: #ffffff;

    z-index: 15;

    box-shadow:
        0 0 0 1px #000000;

}}


.player::after {{

    content: "";

    position: absolute;

    left: 4px;
    right: 4px;

    bottom: -5px;

    height: 4px;

    background:
        rgba(255,255,255,0.15);

}}


/* =====================================================
   INTERACTION MESSAGE
   ===================================================== */

.interaction-message {{

    position: absolute;

    left: 50%;
    bottom: 5%;

    transform:
        translateX(-50%);

    padding: 10px 18px;

    background: #000000;

    font-size: 13px;

    color: #ffffff;

    opacity: 0;

    pointer-events: none;

    transition:
        opacity 0.1s linear;

    z-index: 30;

}}


.interaction-message.visible {{

    opacity: 1;

}}


/* =====================================================
   STATUS
   ===================================================== */

.status {{

    position: absolute;

    bottom: 24px;
    left: 28px;

    font-size: 14px;

    color: #777777;

    z-index: 20;

}}


/* =====================================================
   ECHO CHAT BAR
   ===================================================== */

.echo-dialogue {{

    position: absolute;

    left: 50%;
    bottom: 4%;

    transform:
        translateX(-50%);

    width: min(760px, 82vw);

    min-height: 105px;

    background: #050505;

    border:
        1px solid #555555;

    padding: 18px 22px;

    z-index: 180;

    display: none;

    cursor: pointer;

}}


.echo-dialogue.visible {{

    display: block;

}}


.echo-name {{

    font-size: 13px;

    color: #ffffff;

    margin-bottom: 10px;

    letter-spacing: 1px;

}}


.echo-text {{

    font-size: 13px;

    color: #aaaaaa;

    line-height: 1.8;

    padding-right: 30px;

}}


.echo-next {{

    position: absolute;

    right: 16px;
    bottom: 12px;

    color: #555555;

    font-size: 10px;

}}


/* =====================================================
   COMPUTER SCREEN
   ===================================================== */

.computer-overlay {{

    position: absolute;

    inset: 0;

    z-index: 160;

    background:
        rgba(0,0,0,0.94);

    display: none;

    align-items: center;

    justify-content: center;

}}


.computer-overlay.visible {{

    display: flex;

}}


.computer-panel {{

    width: min(560px, 82vw);

    background: #050505;

    border:
        1px solid #555555;

    padding: 30px;

}}


.computer-title {{

    font-size: 20px;

    margin-bottom: 8px;

}}


.computer-subtitle {{

    color: #666666;

    font-size: 11px;

    margin-bottom: 24px;

}}


.computer-display {{

    min-height: 75px;

    padding: 16px;

    margin-bottom: 18px;

    border:
        1px solid #292929;

    background: #090909;

    color: #888888;

    font-size: 12px;

    line-height: 1.8;

}}


.code-input {{

    width: 100%;

    height: 48px;

    padding: 0 14px;

    border:
        1px solid #555555;

    border-radius: 0;

    outline: none;

    background: #000000;

    color: #ffffff;

    font-family:
        'NeoDungGeunMo',
        monospace;

    font-size: 18px;

    letter-spacing: 5px;

    text-align: center;

}}


.code-input:focus {{

    border-color: #ffffff;

}}


.computer-buttons {{

    display: flex;

    justify-content: flex-end;

    gap: 8px;

    margin-top: 14px;

}}


.computer-button {{

    width: 120px;

    height: 40px;

    border: none;

    border-radius: 0;

    background: #000000;

    color: #ffffff;

    font-family:
        'NeoDungGeunMo',
        monospace;

    font-size: 13px;

    cursor: pointer;

}}


.computer-button:hover {{

    background: #ffffff;

    color: #000000;

}}


/* =====================================================
   INVENTORY
   ===================================================== */

.inventory-overlay {{

    position: absolute;

    inset: 0;

    z-index: 150;

    display: none;

    align-items: center;

    justify-content: center;

    background:
        rgba(0,0,0,0.92);

}}


.inventory-overlay.visible {{

    display: flex;

}}


.inventory-panel {{

    width: min(820px, 88vw);

    background: #050505;

    padding: 34px 38px;

}}


.inventory-header {{

    display: flex;

    justify-content:
        space-between;

    align-items: center;

    padding-bottom: 18px;

    margin-bottom: 22px;

    border-bottom:
        1px solid #333333;

}}


.inventory-title {{

    font-size: 24px;

}}


.inventory-close {{

    font-size: 12px;

    color: #666666;

}}


.inventory-grid {{

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 10px;

}}


.inventory-slot {{

    position: relative;

    aspect-ratio: 1 / 1;

    background: #090909;

    border:
        1px solid #292929;

    display: flex;

    align-items: center;
    justify-content: center;

}}


.slot-number {{

    position: absolute;

    top: 7px;
    left: 9px;

    font-size: 10px;

    color: #555555;

}}


.item-name {{

    font-size: 13px;

    text-align: center;

}}


.empty-text {{

    color: #444444;

    font-size: 11px;

}}


/* =====================================================
   HELP
   ===================================================== */

.help-overlay {{

    position: absolute;

    inset: 0;

    z-index: 150;

    display: none;

    align-items: center;

    justify-content: center;

    background:
        rgba(0,0,0,0.92);

}}


.help-overlay.visible {{

    display: flex;

}}


.help-panel {{

    width: min(760px, 86vw);

    max-height: 82vh;

    overflow-y: auto;

    background: #050505;

    padding: 36px 40px;

}}


.help-header {{

    display: flex;

    justify-content:
        space-between;

    padding-bottom: 18px;

    margin-bottom: 20px;

    border-bottom:
        1px solid #333333;

}}


.help-title {{

    font-size: 24px;

}}


.help-close {{

    font-size: 12px;

    color: #666666;

}}


.help-row {{

    display: flex;

    gap: 20px;

    padding: 14px 0;

    border-bottom:
        1px solid #1f1f1f;

}}


.help-number {{

    width: 30px;

    color: #555555;

}}


.help-key {{

    width: 145px;

    font-size: 14px;

}}


.help-description {{

    color: #888888;

    font-size: 12px;

    line-height: 1.7;

}}


/* =====================================================
   PAUSE
   ===================================================== */

.pause-overlay {{

    position: absolute;

    inset: 0;

    z-index: 190;

    display: none;

    align-items: center;

    justify-content: center;

    background:
        rgba(0,0,0,0.90);

}}


.pause-overlay.visible {{

    display: flex;

}}


.pause-title {{

    font-size: 28px;

    text-align: center;

    margin-bottom: 14px;

}}


.pause-sub {{

    color: #777777;

    font-size: 13px;

    text-align: center;

}}


/* =====================================================
   SYSTEM FAILURE
   ===================================================== */

.time-over {{

    position: absolute;

    inset: 0;

    z-index: 300;

    display: none;

    align-items: center;

    justify-content: center;

    background: #000000;

}}


.time-over.visible {{

    display: flex;

}}


.time-over-content {{

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    text-align: center;

}}


.time-over-title {{

    font-size: 30px;

    margin-bottom: 16px;

}}


.time-over-text {{

    color: #777777;

    font-size: 13px;

    line-height: 1.8;

}}


/* =====================================================
   MOBILE CONTROLS
   ===================================================== */

.mobile-controls {{

    display: none;

    position: absolute;

    right: 22px;
    bottom: 22px;

    width: 132px;
    height: 132px;

    z-index: 150;

}}


.control-button {{

    position: absolute;

    width: 42px;
    height: 42px;

    padding: 0;

    border:
        1px solid #555555;

    background:
        rgba(0,0,0,0.88);

    color: #ffffff;

    font-family:
        'NeoDungGeunMo',
        monospace;

    font-size: 20px;

    display: flex;

    align-items: center;
    justify-content: center;

    touch-action: none;

}}


.control-button:active {{

    background: #ffffff;

    color: #000000;

}}


.control-up {{
    top: 0;
    left: 45px;
}}


.control-left {{
    top: 45px;
    left: 0;
}}


.control-right {{
    top: 45px;
    right: 0;
}}


.control-down {{
    bottom: 0;
    left: 45px;
}}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {{

    .project-title {{

        top: 18px;
        left: 16px;

        font-size: 14px;

    }}


    .stage-title {{

        top: 40px;
        left: 16px;

        font-size: 11px;

    }}


    .timer {{

        top: 18px;

        font-size: 17px;

    }}


    .game-area {{

        top: 68px;

        left: 16px;
        right: 16px;

        bottom: 58px;

        background-size: 30px 30px;

    }}


    .status {{

        left: 16px;

        bottom: 18px;

        font-size: 11px;

    }}


    .echo-dialogue {{

        width: 88vw;

        min-height: 110px;

        padding: 15px 17px;

    }}


    .echo-name {{

        font-size: 11px;

    }}


    .echo-text {{

        font-size: 10px;

    }}


    .computer-panel {{

        width: 88vw;

        padding: 22px;

    }}


    .mobile-controls {{

        display: block;

    }}

}}

</style>

</head>


<body>


<div
    class="game"
    id="gameRoot"
    tabindex="0"
    autofocus
>


    <!-- =================================================
         TOP
         ================================================= -->

    <div class="project-title">
        PROJECT : LOGIC
    </div>


    <div class="stage-title">
        STAGE 01 // CONTROL ROOM
    </div>


    <div class="timer" id="timer">
        {timer_text}
    </div>


    <!-- =================================================
         GAME AREA
         ================================================= -->

    <div class="game-area">


        <!-- =================================================
             ROOM
             ================================================= -->

        <div class="room">


            <div class="room-line-horizontal"></div>

            <div class="room-line-vertical"></div>


            <!-- =================================================
                 MONITOR
                 ================================================= -->

            <div
                class="object monitor"
                id="monitor"
            >

                MONITOR

                <div class="object-label">
                    CENTRAL MONITOR
                </div>

            </div>


            <!-- =================================================
                 DESK
                 ================================================= -->

            <div
                class="object desk"
                id="desk"
            >

                DESK

                <div class="object-label">
                    RESEARCH DESK
                </div>

            </div>


            <!-- =================================================
                 COMPUTER
                 ================================================= -->

            <div
                class="object terminal"
                id="terminal"
            >

                COMPUTER

                <div class="object-label">
                    SECURITY COMPUTER
                </div>

            </div>


            <!-- =================================================
                 EXIT
                 ================================================= -->

            <div
                class="object exit-door"
                id="exitDoor"
            >

                EXIT

                <div class="object-label">
                    SECURITY DOOR
                </div>

            </div>


            <!-- =================================================
                 PLAYER
                 ================================================= -->

            <div
                class="player"
                id="player"
            ></div>


            <!-- =================================================
                 INTERACTION
                 ================================================= -->

            <div
                class="interaction-message"
                id="interactionMessage"
            >
                PRESS E
            </div>


        </div>


        <!-- =================================================
             ECHO DIALOGUE
             ================================================= -->

        <div
            class="echo-dialogue visible"
            id="echoDialogue"
        >

            <div class="echo-name">
                ECHO // SYSTEM AI
            </div>

            <div
                class="echo-text"
                id="echoText"
            >
                연결이 확인되었습니다. 이 시설의
                현재 상황을 설명하겠습니다.
            </div>

            <div class="echo-next">
                [ SPACE ]
            </div>

        </div>


        <!-- =================================================
             COMPUTER
             ================================================= -->

        <div
            class="computer-overlay"
            id="computerOverlay"
        >

            <div class="computer-panel">

                <div class="computer-title">
                    SECURITY COMPUTER
                </div>

                <div class="computer-subtitle">
                    ECHO TERMINAL // AUTHORIZATION REQUIRED
                </div>

                <div
                    class="computer-display"
                    id="computerDisplay"
                >
                    ECHO가 전달한 인증 번호를 입력하십시오.
                </div>

                <input
                    class="code-input"
                    id="codeInput"
                    type="text"
                    inputmode="numeric"
                    maxlength="4"
                    autocomplete="off"
                    placeholder="----"
                >

                <div class="computer-buttons">

                    <button
                        class="computer-button"
                        id="computerClose"
                        type="button"
                    >
                        CLOSE
                    </button>

                    <button
                        class="computer-button"
                        id="computerSubmit"
                        type="button"
                    >
                        ENTER
                    </button>

                </div>

            </div>

        </div>


        <!-- =================================================
             INVENTORY
             ================================================= -->

        <div
            class="inventory-overlay"
            id="inventoryOverlay"
        >

            <div class="inventory-panel">

                <div class="inventory-header">

                    <div class="inventory-title">
                        INVENTORY
                    </div>

                    <div class="inventory-close">
                        I / ESC TO CLOSE
                    </div>

                </div>


                <div class="inventory-grid">

                    <div class="inventory-slot">

                        <div class="slot-number">
                            01
                        </div>

                        <div
                            class="empty-text"
                            id="slot0"
                        >
                            EMPTY
                        </div>

                    </div>


                    <div class="inventory-slot">

                        <div class="slot-number">
                            02
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div class="inventory-slot">

                        <div class="slot-number">
                            03
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div class="inventory-slot">

                        <div class="slot-number">
                            04
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div class="inventory-slot">

                        <div class="slot-number">
                            05
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div class="inventory-slot">

                        <div class="slot-number">
                            06
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div class="inventory-slot">

                        <div class="slot-number">
                            07
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div class="inventory-slot">

                        <div class="slot-number">
                            08
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>

                </div>

            </div>

        </div>


        <!-- =================================================
             HELP
             ================================================= -->

        <div
            class="help-overlay"
            id="helpOverlay"
        >

            <div class="help-panel">

                <div class="help-header">

                    <div class="help-title">
                        HOW TO PLAY
                    </div>

                    <div class="help-close">
                        H / ESC TO CLOSE
                    </div>

                </div>


                <div class="help-row">

                    <div class="help-number">
                        01
                    </div>

                    <div class="help-key">
                        MOVEMENT<br>
                        W A S D
                    </div>

                    <div class="help-description">
                        연구시설 내부를 이동합니다.
                    </div>

                </div>


                <div class="help-row">

                    <div class="help-number">
                        02
                    </div>

                    <div class="help-key">
                        INTERACTION<br>
                        E
                    </div>

                    <div class="help-description">
                        가까운 물체를 조사하거나
                        아이템을 획득합니다.
                    </div>

                </div>


                <div class="help-row">

                    <div class="help-number">
                        03
                    </div>

                    <div class="help-key">
                        INVENTORY<br>
                        I
                    </div>

                    <div class="help-description">
                        획득한 아이템을 확인합니다.
                    </div>

                </div>


                <div class="help-row">

                    <div class="help-number">
                        04
                    </div>

                    <div class="help-key">
                        DIALOGUE<br>
                        SPACE
                    </div>

                    <div class="help-description">
                        ECHO의 안내를 진행합니다.
                    </div>

                </div>


                <div class="help-row">

                    <div class="help-number">
                        05
                    </div>

                    <div class="help-key">
                        SYSTEM<br>
                        H
                    </div>

                    <div class="help-description">
                        조작 방법을 다시 확인합니다.
                    </div>

                </div>

            </div>

        </div>


        <!-- =================================================
             PAUSE
             ================================================= -->

        <div
            class="pause-overlay"
            id="pauseOverlay"
        >

            <div>

                <div class="pause-title">
                    GAME PAUSED
                </div>

                <div class="pause-sub">
                    PRESS ▶ TO CONTINUE
                </div>

            </div>

        </div>


        <!-- =================================================
             SYSTEM FAILURE
             ================================================= -->

        <div
            class="time-over"
            id="timeOver"
        >

            <div class="time-over-content">

                <div class="time-over-title">
                    SYSTEM FAILURE
                </div>

                <div class="time-over-text">

                    FACILITY RESET INITIATED
                    <br>
                    CONNECTION TO ECHO LOST

                </div>

            </div>

        </div>


        <!-- =================================================
             MOBILE CONTROLS
             ================================================= -->

        <div class="mobile-controls">

            <button
                class="control-button control-up"
                data-direction="w"
                type="button"
            >
                ▲
            </button>

            <button
                class="control-button control-left"
                data-direction="a"
                type="button"
            >
                ◀
            </button>

            <button
                class="control-button control-right"
                data-direction="d"
                type="button"
            >
                ▶
            </button>

            <button
                class="control-button control-down"
                data-direction="s"
                type="button"
            >
                ▼
            </button>

        </div>


    </div>


    <!-- =================================================
         STATUS
         ================================================= -->

    <div
        class="status"
        id="status"
    >
        ECHO SYSTEM // ONLINE
    </div>


</div>


<script>

/* =====================================================
   GAME ROOT
   ===================================================== */

const gameRoot =
    document.getElementById(
        "gameRoot"
    );


/* =====================================================
   PLAYER
   ===================================================== */

const player =
    document.getElementById(
        "player"
    );


let playerX = 50;

let playerY = 43;

const moveSpeed = 0.65;


/* =====================================================
   KEYS
   ===================================================== */

const keys = {{

    w: false,
    a: false,
    s: false,
    d: false

}};


/* =====================================================
   STATES
   ===================================================== */

let paused = {str(paused).lower()};

let finished = {str(finished).lower()};

let helpOpen = false;

let inventoryOpen = false;

let computerOpen = false;


/* =====================================================
   TUTORIAL
   ===================================================== */

/*
   0 = 시작 안내
   1 = 컴퓨터로 이동
   2 = 컴퓨터 인증번호 입력
   3 = 책상으로 이동
   4 = ACCESS KEY 획득
   5 = 튜토리얼 종료
*/

let tutorialStep = 0;

let accessKeyObtained = false;

let computerUnlocked = false;


/*
   ECHO가 알려주는 인증 번호
*/

const echoCode = "4172";


/* =====================================================
   OBJECTS
   ===================================================== */

const objects = [

    {{
        id: "monitor",

        name: "CENTRAL MONITOR",

        x: 43,
        y: 13,

        width: 14,
        height: 12
    }},


    {{
        id: "desk",

        name: "RESEARCH DESK",

        x: 35,
        y: 62,

        width: 30,
        height: 12
    }},


    {{
        id: "terminal",

        name: "SECURITY COMPUTER",

        x: 18,
        y: 35,

        width: 14,
        height: 17
    }},


    {{
        id: "exitDoor",

        name: "SECURITY DOOR",

        x: 92,
        y: 35,

        width: 8,
        height: 30
    }}

];


let nearbyObject = null;


/* =====================================================
   ECHO DIALOGUE
   ===================================================== */

const echoDialogue =
    document.getElementById(
        "echoDialogue"
    );


const echoText =
    document.getElementById(
        "echoText"
    );


const status =
    document.getElementById(
        "status"
    );


const echoMessages = [

    "연결이 확인되었습니다. 이 시설의 현재 상황을 설명하겠습니다.",

    "현재 당신은 연구시설의 CONTROL ROOM에 있습니다.",

    "시설의 보안 시스템이 비정상적으로 작동하고 있습니다. 이곳에서 탈출하려면 순서대로 보안 절차를 복구해야 합니다.",

    "걱정하지 마십시오. 제가 필요한 절차를 안내하겠습니다.",

    "우선 왼쪽에 있는 SECURITY COMPUTER로 이동하십시오. 가까이 다가가면 E 키를 눌러 조사할 수 있습니다.",

    "좋습니다. COMPUTER를 조사하면 인증 번호를 입력할 수 있습니다.",

    "인증 번호는 4172입니다. 화면에 표시된 입력창에 제가 말한 숫자를 그대로 입력하십시오.",

    "인증이 완료되었습니다. 이제 연구용 책상으로 이동하십시오.",

    "책상에서 ACCESS KEY를 획득할 수 있습니다. 가까이 다가간 뒤 E 키를 누르십시오.",

    "ACCESS KEY가 확인되었습니다. 이제부터 본격적인 시설 탐색을 시작할 수 있습니다."

];


function showEchoMessage(index){{

    if (
        index < 0 ||
        index >= echoMessages.length
    ){{

        return;

    }}


    echoText.textContent =
        echoMessages[index];


    echoDialogue.classList.add(
        "visible"
    );

}}


function hideEchoDialogue(){{

    echoDialogue.classList.remove(
        "visible"
    );

}}


/* =====================================================
   DIALOGUE PROGRESS
   ===================================================== */

function progressDialogue(){{

    if (!echoDialogue.classList.contains("visible")){{

        return;

    }}


    /*
       현재 단계에서 ECHO의 안내를
       한 문장씩 진행한다.
    */

    if (tutorialStep < echoMessages.length - 1){{

        tutorialStep++;

        showEchoMessage(
            tutorialStep
        );

    }} else {{

        hideEchoDialogue();

    }}

}}


/* =====================================================
   INVENTORY
   ===================================================== */

const inventoryOverlay =
    document.getElementById(
        "inventoryOverlay"
    );


const slot0 =
    document.getElementById(
        "slot0"
    );


function giveAccessKey(){{

    accessKeyObtained = true;

    slot0.textContent =
        "ACCESS KEY";

    slot0.classList.remove(
        "empty-text"
    );

    slot0.classList.add(
        "item-name"
    );

    status.textContent =
        "SYSTEM // ACCESS KEY ACQUIRED";

}}


/* =====================================================
   COMPUTER
   ===================================================== */

const computerOverlay =
    document.getElementById(
        "computerOverlay"
    );


const codeInput =
    document.getElementById(
        "codeInput"
    );


const computerDisplay =
    document.getElementById(
        "computerDisplay"
    );


const computerSubmit =
    document.getElementById(
        "computerSubmit"
    );


const computerClose =
    document.getElementById(
        "computerClose"
    );


function openComputer(){{

    computerOpen = true;

    computerOverlay.classList.add(
        "visible"
    );

    codeInput.value = "";

    computerDisplay.innerHTML =
        "ECHO가 전달한 인증 번호를 입력하십시오.";

    clearMovementKeys();

    setTimeout(
        function(){{

            codeInput.focus();

        }},
        50
    );

}}


function closeComputer(){{

    computerOpen = false;

    computerOverlay.classList.remove(
        "visible"
    );

    focusGame();

}}


function submitCode(){{

    const entered =
        codeInput.value.trim();


    if (entered === echoCode){{

        computerUnlocked = true;

        computerDisplay.innerHTML =
            "AUTHORIZATION ACCEPTED<br><br>"
            + "SECURITY ACCESS KEY가 생성되었습니다.";

        status.textContent =
            "COMPUTER // AUTHORIZATION ACCEPTED";


        /*
           책상으로 가는 단계
        */

        if (tutorialStep < 7){{

            tutorialStep = 7;

            showEchoMessage(
                7
            );

        }}


        setTimeout(
            function(){{

                closeComputer();

            }},
            900
        );


    }} else {{

        computerDisplay.innerHTML =
            "ACCESS DENIED<br><br>"
            + "ECHO가 알려준 숫자를 그대로 입력하십시오.";

        status.textContent =
            "COMPUTER // ACCESS DENIED";

    }}

}}


computerSubmit.addEventListener(
    "click",
    submitCode
);


computerClose.addEventListener(
    "click",
    closeComputer
);


codeInput.addEventListener(
    "keydown",
    function(event){{

        if (event.key === "Enter"){{

            submitCode();

            event.preventDefault();

        }}

        if (event.key === "Escape"){{

            closeComputer();

            event.preventDefault();

        }}

    }}
);


/* =====================================================
   DISTANCE
   ===================================================== */

function distanceToObject(object){{

    const centerX =
        object.x +
        object.width / 2;


    const centerY =
        object.y +
        object.height / 2;


    const dx =
        playerX - centerX;


    const dy =
        playerY - centerY;


    return Math.sqrt(
        dx * dx +
        dy * dy
    );

}}


/* =====================================================
   INTERACTION CHECK
   ===================================================== */

const interactionMessage =
    document.getElementById(
        "interactionMessage"
    );


function checkInteraction(){{

    nearbyObject = null;


    let closestDistance =
        Infinity;


    objects.forEach(
        function(object){{

            const distance =
                distanceToObject(
                    object
                );


            if (
                distance < 12 &&
                distance < closestDistance
            ){{

                nearbyObject =
                    object;

                closestDistance =
                    distance;

            }}

        }}
    );


    if (nearbyObject){{

        interactionMessage.textContent =
            "E  //  "
            + nearbyObject.name;

        interactionMessage.classList.add(
            "visible"
        );

    }} else {{

        interactionMessage.classList.remove(
            "visible"
        );

    }}

}}


/* =====================================================
   INTERACTION
   ===================================================== */

function interact(){{

    if (
        paused ||
        helpOpen ||
        inventoryOpen ||
        computerOpen ||
        finished
    ){{

        return;

    }}


    if (!nearbyObject){{

        return;

    }}


    /* =================================================
       COMPUTER
       ================================================= */

    if (
        nearbyObject.id ===
        "terminal"
    ){{

        /*
           튜토리얼 순서를 건너뛰고
           컴퓨터 이전의 과정을 하려고 할 경우
        */

        if (tutorialStep < 4){{

            status.textContent =
                "접근할 수 없는 과정입니다.";

            showTemporaryStatus();

            return;

        }}


        openComputer();

        return;

    }}


    /* =================================================
       DESK
       ================================================= */

    if (
        nearbyObject.id ===
        "desk"
    ){{

        /*
           컴퓨터 인증을 완료하지 않았다면
           책상 접근 불가
        */

        if (!computerUnlocked){{

            status.textContent =
                "접근할 수 없는 과정입니다.";

            showTemporaryStatus();

            return;

        }}


        /*
           ACCESS KEY가 아직 없는 경우
        */

        if (!accessKeyObtained){{

            giveAccessKey();

            tutorialStep = 9;

            showEchoMessage(
                9
            );

            return;

        }}


        return;

    }}


    /* =================================================
       MONITOR
       ================================================= */

    if (
        nearbyObject.id ===
        "monitor"
    ){{

        /*
           튜토리얼 초기에는
           모니터를 먼저 조사할 수 없음
        */

        if (tutorialStep < 9){{

            status.textContent =
                "접근할 수 없는 과정입니다.";

            showTemporaryStatus();

            return;

        }}


        status.textContent =
            "MONITOR // SIGNAL UNSTABLE";

        return;

    }}


    /* =================================================
       EXIT
       ================================================= */

    if (
        nearbyObject.id ===
        "exitDoor"
    ){{

        if (!accessKeyObtained){{

            status.textContent =
                "접근할 수 없는 과정입니다.";

            showTemporaryStatus();

            return;

        }}


        status.textContent =
            "SECURITY DOOR // ACCESS GRANTED";

    }}

}}


/* =====================================================
   TEMPORARY STATUS
   ===================================================== */

let statusTimer = null;


function showTemporaryStatus(){{

    if (statusTimer){{

        clearTimeout(
            statusTimer
        );

    }}


    statusTimer =
        setTimeout(
            function(){{

                status.textContent =
                    "ECHO SYSTEM // ONLINE";

            }},
            1600
        );

}}


/* =====================================================
   FOCUS
   ===================================================== */

function focusGame(){{

    try{{

        gameRoot.focus({{
            preventScroll: true
        }});

    }} catch(error){{

        try{{

            gameRoot.focus();

        }} catch(error2){{}}

    }}

}}


window.addEventListener(
    "load",
    function(){{

        focusGame();

        setTimeout(
            function(){{

                focusGame();

            }},
            100
        );

    }}
);


gameRoot.addEventListener(
    "pointerdown",
    function(){{

        if (!computerOpen){{

            focusGame();

        }}

    }}
);


gameRoot.addEventListener(
    "click",
    function(){{

        if (!computerOpen){{

            focusGame();

        }}

    }}
);


/* =====================================================
   CLEAR KEYS
   ===================================================== */

function clearMovementKeys(){{

    keys.w = false;
    keys.a = false;
    keys.s = false;
    keys.d = false;

}}


/* =====================================================
   MOVEMENT
   ===================================================== */

function updatePlayer(){{

    if (
        !paused &&
        !helpOpen &&
        !inventoryOpen &&
        !computerOpen &&
        !finished
    ){{

        if (keys.w)
            playerY -= moveSpeed;

        if (keys.s)
            playerY += moveSpeed;

        if (keys.a)
            playerX -= moveSpeed;

        if (keys.d)
            playerX += moveSpeed;


        playerX =
            Math.max(
                2,
                Math.min(
                    98,
                    playerX
                )
            );


        playerY =
            Math.max(
                2,
                Math.min(
                    98,
                    playerY
                )
            );


        player.style.left =
            playerX + "%";


        player.style.top =
            playerY + "%";


        checkInteraction();

    }}


    requestAnimationFrame(
        updatePlayer
    );

}}


/* =====================================================
   KEYBOARD
   ===================================================== */

function handleKeyDown(event){{

    const key =
        event.key.toLowerCase();


    /*
       컴퓨터 입력창에서는
       게임 단축키를 막는다.
    */

    if (
        computerOpen &&
        document.activeElement === codeInput
    ){{

        return;

    }}


    /* =================================================
       ESC
       ================================================= */

    if (key === "escape"){{

        if (computerOpen){{

            closeComputer();

            event.preventDefault();

            return;

        }}


        if (helpOpen){{

            helpOpen = false;

            document
                .getElementById("helpOverlay")
                .classList.remove("visible");

            focusGame();

            event.preventDefault();

            return;

        }}


        if (inventoryOpen){{

            inventoryOpen = false;

            inventoryOverlay.classList.remove(
                "visible"
            );

            focusGame();

            event.preventDefault();

            return;

        }}

    }}


    /* =================================================
       SPACE
       ================================================= */

    if (key === " "){{

        if (
            !paused &&
            !finished &&
            !computerOpen &&
            !inventoryOpen &&
            !helpOpen
        ){{

            if (
                echoDialogue.classList.contains(
                    "visible"
                )
            ){{

                progressDialogue();

            }}

        }}

        event.preventDefault();

        return;

    }}


    /* =================================================
       H
       ================================================= */

    if (key === "h"){{

        if (
            !paused &&
            !finished &&
            !computerOpen
        ){{

            const overlay =
                document.getElementById(
                    "helpOverlay"
                );


            if (helpOpen){{

                helpOpen = false;

                overlay.classList.remove(
                    "visible"
                );

            }} else {{

                helpOpen = true;

                inventoryOpen = false;

                inventoryOverlay.classList.remove(
                    "visible"
                );

                overlay.classList.add(
                    "visible"
                );

                clearMovementKeys();

            }}

        }}

        event.preventDefault();

        return;

    }}


    /* =================================================
       I
       ================================================= */

    if (key === "i"){{

        if (
            !paused &&
            !finished &&
            !computerOpen
        ){{

            if (inventoryOpen){{

                inventoryOpen = false;

                inventoryOverlay.classList.remove(
                    "visible"
                );

            }} else {{

                inventoryOpen = true;

                helpOpen = false;

                document
                    .getElementById("helpOverlay")
                    .classList.remove("visible");

                inventoryOverlay.classList.add(
                    "visible"
                );

                clearMovementKeys();

            }}

        }}

        event.preventDefault();

        return;

    }}


    /* =================================================
       E
       ================================================= */

    if (key === "e"){{

        interact();

        event.preventDefault();

        return;

    }}


    /* =================================================
       MOVEMENT
       ================================================= */

    if (
        key === "w" ||
        key === "a" ||
        key === "s" ||
        key === "d"
    ){{

        if (
            !paused &&
            !helpOpen &&
            !inventoryOpen &&
            !computerOpen &&
            !finished
        ){{

            keys[key] = true;

        }}

        event.preventDefault();

    }}

}}


function handleKeyUp(event){{

    const key =
        event.key.toLowerCase();


    if (
        key === "w" ||
        key === "a" ||
        key === "s" ||
        key === "d"
    ){{

        keys[key] = false;

        event.preventDefault();

    }}

}}


window.addEventListener(
    "keydown",
    handleKeyDown,
    true
);


window.addEventListener(
    "keyup",
    handleKeyUp,
    true
);


window.addEventListener(
    "blur",
    function(){{

        clearMovementKeys();

    }}
);


/* =====================================================
   MOBILE CONTROLS
   ===================================================== */

const mobileButtons =
    document.querySelectorAll(
        ".control-button"
    );


mobileButtons.forEach(
    function(button){{

        const direction =
            button.dataset.direction;


        button.addEventListener(
            "pointerdown",
            function(event){{

                event.preventDefault();

                if (
                    !paused &&
                    !helpOpen &&
                    !inventoryOpen &&
                    !computerOpen &&
                    !finished
                ){{

                    keys[direction] =
                        true;

                }}

            }}
        );


        button.addEventListener(
            "pointerup",
            function(event){{

                event.preventDefault();

                keys[direction] =
                    false;

            }}
        );


        button.addEventListener(
            "pointercancel",
            function(){{

                keys[direction] =
                    false;

            }}
        );


        button.addEventListener(
            "pointerleave",
            function(){{

                keys[direction] =
                    false;

            }}
        );

    }}
);


/* =====================================================
   TIMER DISPLAY
   ===================================================== */

function formatTime(seconds){{

    const min =
        Math.floor(
            seconds / 60
        );


    const sec =
        seconds % 60;


    return String(min).padStart(2, "0")
        + ":"
        + String(sec).padStart(2, "0");

}}


function showTimeOver(){{

    finished = true;

    clearMovementKeys();

    document
        .getElementById("timeOver")
        .classList.add("visible");

}}


function updateTimer(){{

    if (
        paused ||
        finished
    ){{

        return;

    }}


    if (remaining <= 0){{

        remaining = 0;

        showTimeOver();

        return;

    }}


    remaining--;

    document
        .getElementById("timer")
        .textContent =
        formatTime(remaining);


    if (remaining <= 0){{

        showTimeOver();

    }}

}}


setInterval(
    updateTimer,
    1000
);


/* =====================================================
   INITIAL
   ===================================================== */

player.style.left =
    playerX + "%";


player.style.top =
    playerY + "%";


/*
   처음에는 ECHO의 첫 번째 메시지가
   자동으로 표시된다.
*/

showEchoMessage(0);


/*
   게임 시작
*/

requestAnimationFrame(
    updatePlayer
);


focusGame();


setTimeout(
    function(){{

        focusGame();

    }},
    100
);


</script>


</body>

</html>
"""


# =========================================================
# RENDER
# =========================================================

components.html(
    html,
    height=1000,
    scrolling=False,
)
