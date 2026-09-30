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
# PAGE ACTION
# =========================================================
# SYSTEM FAILURE 화면에서
# RESTART / TITLE을 눌렀을 때 처리
#
# components.html 내부의 JavaScript에서는
# st.switch_page()를 직접 사용할 수 없기 때문에
# query parameter를 이용하여 Python 쪽으로 전달한다.
# =========================================================

action = st.query_params.get("action")


if action == "restart":

    # NEW GAME과 동일한 초기화

    st.session_state.game_paused = False
    st.session_state.game_finished = False

    st.session_state.remaining_seconds = 15 * 60

    st.session_state.timer_deadline = (
        time.time() + 15 * 60
    )

    st.query_params.clear()

    st.rerun()


elif action == "title":

    st.query_params.clear()

    st.switch_page("main.py")


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
    st.session_state.timer_deadline = (
        time.time() + 15 * 60
    )


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
        )
    )

    if st.session_state.remaining_seconds <= 0:

        st.session_state.game_finished = True


# =========================================================
# FONT
# =========================================================

font_path = None

for name in ["neodgm.ttf", "neodgm(2).ttf"]:

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
# PAUSE BUTTON CSS
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


    /* =========================================
       PAUSE BUTTON
       ========================================= */

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

        border: none !important;
        outline: none !important;
        box-shadow: none !important;

    }}


    .st-key-pause_game_button button:focus {{

        border: none !important;
        outline: none !important;
        box-shadow: none !important;

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

    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PAUSE
# =========================================================

pause_clicked = st.button(
    "▶"
    if st.session_state.game_paused
    else "||",
    key="pause_game_button",
)


if pause_clicked:

    current_time = time.time()

    if not st.session_state.game_paused:

        st.session_state.remaining_seconds = max(
            0,
            int(
                st.session_state.timer_deadline
                - current_time
            )
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
# INITIAL VALUES
# =========================================================

remaining = (
    st.session_state.remaining_seconds
)

paused = (
    st.session_state.game_paused
)

finished = (
    st.session_state.game_finished
)


minutes = remaining // 60

seconds = remaining % 60


timer_text = (
    f"{minutes:02d}:{seconds:02d}"
)


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
   GAME WORLD
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
   ROOM BOUNDARY
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


/* =====================================================
   ROOM DETAILS
   ===================================================== */

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
   CONTROL ROOM OBJECTS
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


/* =====================================================
   OBJECT LABEL
   ===================================================== */

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
   BOTTOM STATUS
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
   OVERLAY COMMON
   ===================================================== */

.overlay {{

    position: absolute;

    inset: 0;

    z-index: 100;

    display: flex;

    align-items: center;
    justify-content: center;

    background:
        rgba(0,0,0,0.90);

}}


/* =====================================================
   INVENTORY
   ===================================================== */

.inventory-panel {{

    width:
        min(820px, 88vw);

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

    letter-spacing: 1px;

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

    cursor: pointer;

    transition:
        background 0.1s linear,
        color 0.1s linear;

}}


.inventory-slot:hover {{

    background: #ffffff;

    color: #000000;

}}


.inventory-slot.selected {{

    background: #ffffff;

    color: #000000;

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


.item-description {{

    min-height: 70px;

    margin-top: 20px;

    padding: 15px;

    background: #090909;

    border-top:
        1px solid #292929;

    font-size: 12px;

    line-height: 1.8;

    color: #888888;

}}


/* =====================================================
   HOW TO PLAY
   ===================================================== */

.help-panel {{

    width:
        min(760px, 86vw);

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


.help-important {{

    margin-top: 22px;

    padding: 16px;

    background: #090909;

    border-left:
        2px solid #ffffff;

}}


.help-important-title {{

    margin-bottom: 8px;

    font-size: 13px;

}}


.help-important-text {{

    color: #888888;

    font-size: 11px;

    line-height: 1.8;

}}


/* =====================================================
   PAUSE
   ===================================================== */

.pause-overlay {{

    position: absolute;

    inset: 0;

    z-index: 90;

    display: flex;

    align-items: center;
    justify-content: center;

    background:
        rgba(0,0,0,0.90);

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

    z-index: 200;

    display: flex;

    align-items: center;
    justify-content: center;

    background: #000000;

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

    margin-bottom: 30px;

}}


/* =====================================================
   SYSTEM FAILURE BUTTONS
   ===================================================== */

.time-over-buttons {{

    display: flex;

    flex-direction: column;

    align-items: center;

    gap: 8px;

}}


.time-over-button {{

    width: 170px;

    height: 44px;

    padding: 0;

    margin: 0;

    border: none;

    outline: none;

    box-shadow: none;

    border-radius: 0;

    background: #000000;

    color: #ffffff;

    font-family:
        'NeoDungGeunMo',
        monospace;

    font-size: 15px;

    cursor: pointer;

}}


.time-over-button:hover {{

    background: #ffffff;

    color: #000000;

}}


.time-over-button:focus {{

    border: none;

    outline: none;

    box-shadow: none;

}}


/* =====================================================
   MOBILE DIRECTION PAD
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

    -webkit-user-select: none;
    user-select: none;

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


    .inventory-panel,
    .help-panel {{

        width: 90vw;

        padding: 24px 20px;

    }}


    .inventory-grid {{

        gap: 6px;

    }}


    .item-name {{

        font-size: 10px;

    }}


    .help-row {{

        gap: 10px;

    }}


    .help-key {{

        width: 90px;

        font-size: 11px;

    }}


    .help-description {{

        font-size: 10px;

    }}


    .mobile-controls {{

        display: block;

    }}


    .time-over-title {{

        font-size: 25px;

    }}


    .time-over-text {{

        font-size: 11px;

    }}


    .time-over-button {{

        width: 150px;

        height: 42px;

        font-size: 13px;

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


        <div class="room">


            <!-- =================================================
                 ROOM DETAILS
                 ================================================= -->

            <div class="room-line-horizontal"></div>

            <div class="room-line-vertical"></div>


            <!-- =================================================
                 OBJECTS
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


            <div
                class="object desk"
                id="desk"
            >

                DESK

                <div class="object-label">
                    RESEARCH DESK
                </div>

            </div>


            <div
                class="object terminal"
                id="terminal"
            >

                TERMINAL

                <div class="object-label">
                    SECURITY TERMINAL
                </div>

            </div>


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
                 INTERACTION MESSAGE
                 ================================================= -->

            <div
                class="interaction-message"
                id="interactionMessage"
            >
                PRESS E
            </div>


        </div>


        <!-- =================================================
             INVENTORY OVERLAY
             ================================================= -->

        <div
            class="overlay"
            id="inventoryOverlay"
            style="display:none;"
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


                    <div
                        class="inventory-slot"
                        data-slot="0"
                    >

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


                    <div
                        class="inventory-slot"
                        data-slot="1"
                    >

                        <div class="slot-number">
                            02
                        </div>

                        <div
                            class="empty-text"
                            id="slot1"
                        >
                            EMPTY
                        </div>

                    </div>


                    <div
                        class="inventory-slot"
                        data-slot="2"
                    >

                        <div class="slot-number">
                            03
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div
                        class="inventory-slot"
                        data-slot="3"
                    >

                        <div class="slot-number">
                            04
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div
                        class="inventory-slot"
                        data-slot="4"
                    >

                        <div class="slot-number">
                            05
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div
                        class="inventory-slot"
                        data-slot="5"
                    >

                        <div class="slot-number">
                            06
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div
                        class="inventory-slot"
                        data-slot="6"
                    >

                        <div class="slot-number">
                            07
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                    <div
                        class="inventory-slot"
                        data-slot="7"
                    >

                        <div class="slot-number">
                            08
                        </div>

                        <div class="empty-text">
                            EMPTY
                        </div>

                    </div>


                </div>


                <div
                    class="item-description"
                    id="itemDescription"
                >

                    ITEM DESCRIPTION
                    <br><br>

                    아이템을 선택하면 설명이 표시됩니다.

                </div>


            </div>

        </div>


        <!-- =================================================
             HOW TO PLAY
             ================================================= -->

        <div
            class="overlay"
            id="helpOverlay"
            style="display:none;"
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
                        SYSTEM<br>
                        SPACE
                    </div>

                    <div class="help-description">
                        시스템 메시지를 확인합니다.
                    </div>

                </div>


                <div class="help-row">

                    <div class="help-number">
                        05
                    </div>

                    <div class="help-key">
                        CONTROLS<br>
                        H
                    </div>

                    <div class="help-description">
                        조작 방법을 다시 확인합니다.
                    </div>

                </div>


                <div class="help-important">

                    <div class="help-important-title">
                        IMPORTANT
                    </div>

                    <div class="help-important-text">

                        시설 내부의 물체와 기록을
                        자세히 조사하세요.<br>

                        ECHO가 제공하는 모든 정보가
                        사실이라고 가정해서는 안 됩니다.<br>

                        서로 모순되는 단서가 발견될 수도 있습니다.

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
            style="display:none;"
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
            style="display:none;"
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


                <div class="time-over-buttons">


                    <button
                        class="time-over-button"
                        id="restartButton"
                        type="button"
                    >
                        RESTART
                    </button>


                    <button
                        class="time-over-button"
                        id="titleButton"
                        type="button"
                    >
                        TITLE
                    </button>


                </div>


            </div>

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
   GAME STATE
   ===================================================== */

let remaining = {remaining};

let paused = {str(paused).lower()};

let finished = {str(finished).lower()};

let helpOpen = false;

let inventoryOpen = false;


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


const room =
    document.querySelector(
        ".room"
    );


let playerX = 50;

let playerY = 43;


const moveSpeed = 0.65;


/* =====================================================
   KEY STATE
   ===================================================== */

const keys = {{

    w: false,
    a: false,
    s: false,
    d: false

}};


/* =====================================================
   OBJECTS
   ===================================================== */

const objects = [

    {{
        id: "monitor",

        name: "CENTRAL MONITOR",

        interactionKey: "E",

        x: 43,
        y: 13,

        width: 14,
        height: 12
    }},


    {{
        id: "desk",

        name: "RESEARCH DESK",

        interactionKey: "E",

        x: 35,
        y: 62,

        width: 30,
        height: 12
    }},


    {{
        id: "terminal",

        name: "SECURITY TERMINAL",

        interactionKey: "E",

        x: 18,
        y: 35,

        width: 14,
        height: 17
    }},


    {{
        id: "exitDoor",

        name: "SECURITY DOOR",

        interactionKey: "E",

        x: 92,
        y: 35,

        width: 8,
        height: 30
    }}

];


/* =====================================================
   INVENTORY
   ===================================================== */

const inventory = [

    {{
        name:
            "ACCESS CARD",

        description:
            "연구시설 보안구역에 접근할 수 있는 카드입니다."

    }},

    null,
    null,
    null,
    null,
    null,
    null,
    null

];


let selectedSlot = -1;


/* =====================================================
   INVENTORY ELEMENTS
   ===================================================== */

const inventoryOverlay =
    document.getElementById(
        "inventoryOverlay"
    );


const itemDescription =
    document.getElementById(
        "itemDescription"
    );


const inventorySlots =
    document.querySelectorAll(
        ".inventory-slot"
    );


/* =====================================================
   DRAW INVENTORY
   ===================================================== */

function renderInventory() {{

    inventory.forEach(
        function(item, index){{

            const slot =
                inventorySlots[index];


            if (!item){{

                slot.innerHTML =
                    `
                    <div class="slot-number">
                        ${{String(index + 1).padStart(2, "0")}}
                    </div>

                    <div class="empty-text">
                        EMPTY
                    </div>
                    `;

            }} else {{

                slot.innerHTML =
                    `
                    <div class="slot-number">
                        ${{String(index + 1).padStart(2, "0")}}
                    </div>

                    <div class="item-name">
                        ${{item.name}}
                    </div>
                    `;

            }}

        }}
    );

}}


/* =====================================================
   SELECT INVENTORY SLOT
   ===================================================== */

inventorySlots.forEach(
    function(slot){{

        slot.addEventListener(
            "click",
            function(){{

                const index =
                    Number(
                        slot.dataset.slot
                    );


                selectedSlot =
                    index;


                inventorySlots.forEach(
                    function(other){{

                        other.classList.remove(
                            "selected"
                        );

                    }}
                );


                slot.classList.add(
                    "selected"
                );


                const item =
                    inventory[index];


                if (item){{

                    itemDescription.innerHTML =
                        `
                        ${{item.name}}

                        <br><br>

                        ${{item.description}}
                        `;

                }} else {{

                    itemDescription.innerHTML =
                        `
                        ITEM DESCRIPTION

                        <br><br>

                        비어 있는 슬롯입니다.
                        `;

                }}

            }}
        );

    }}
);


/* =====================================================
   INITIAL INVENTORY
   ===================================================== */

renderInventory();


/* =====================================================
   OPEN INVENTORY
   ===================================================== */

function openInventory(){{

    if (finished){{

        return;

    }}


    helpOpen = false;


    helpOverlay.style.display =
        "none";


    inventoryOpen = true;


    inventoryOverlay.style.display =
        "flex";


    clearMovementKeys();

}}


/* =====================================================
   CLOSE INVENTORY
   ===================================================== */

function closeInventory(){{

    inventoryOpen = false;


    inventoryOverlay.style.display =
        "none";


    focusGame();

}}


/* =====================================================
   HELP
   ===================================================== */

const helpOverlay =
    document.getElementById(
        "helpOverlay"
    );


function openHelp(){{

    if (finished){{

        return;

    }}


    inventoryOpen = false;


    inventoryOverlay.style.display =
        "none";


    helpOpen = true;


    helpOverlay.style.display =
        "flex";


    clearMovementKeys();

}}


function closeHelp(){{

    helpOpen = false;


    helpOverlay.style.display =
        "none";


    focusGame();

}}


/* =====================================================
   FOCUS GAME
   ===================================================== */

function focusGame(){{

    try{{

        gameRoot.focus({{
            preventScroll: true
        }});

    }} catch (error){{

        try{{

            gameRoot.focus();

        }} catch (error2){{

        }}

    }}

}}


/*
   iframe이 로딩된 직후
   게임에 포커스를 준다.
*/

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


/*
   게임 영역을 터치하거나 클릭하면
   다시 키보드 입력을 활성화한다.
*/

gameRoot.addEventListener(
    "pointerdown",
    function(){{

        focusGame();

    }}
);


gameRoot.addEventListener(
    "click",
    function(){{

        focusGame();

    }}
);


/* =====================================================
   CLEAR MOVEMENT
   ===================================================== */

function clearMovementKeys(){{

    keys.w = false;

    keys.a = false;

    keys.s = false;

    keys.d = false;

}}


/* =====================================================
   MOVEMENT LOOP
   ===================================================== */

function updatePlayer(){{

    if (
        !paused &&
        !helpOpen &&
        !inventoryOpen &&
        !finished
    ){{

        if (keys.w){{

            playerY -= moveSpeed;

        }}


        if (keys.s){{

            playerY += moveSpeed;

        }}


        if (keys.a){{

            playerX -= moveSpeed;

        }}


        if (keys.d){{

            playerX += moveSpeed;

        }}


        /* =============================================
           ROOM BOUNDARY
           ============================================= */

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
   INTERACTION
   ===================================================== */

const interactionMessage =
    document.getElementById(
        "interactionMessage"
    );


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


let nearbyObject = null;


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
            nearbyObject.interactionKey
            + "  //  "
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
   INTERACT
   ===================================================== */

function interact(){{

    if (
        paused ||
        helpOpen ||
        inventoryOpen ||
        finished
    ){{

        return;

    }}


    if (!nearbyObject){{

        return;

    }}


    /* =============================================
       SECURITY TERMINAL
       ============================================= */

    if (
        nearbyObject.id ===
        "terminal"
    ){{

        if (!inventory[0]){{

            inventory[0] = {{

                name:
                    "ACCESS CARD",

                description:
                    "연구시설 보안구역에 접근할 수 있는 카드입니다."

            }};


            renderInventory();


            document.getElementById(
                "status"
            ).textContent =
                "SYSTEM // ACCESS CARD ACQUIRED";

        }} else {{

            document.getElementById(
                "status"
            ).textContent =
                "TERMINAL // NO NEW DATA";

        }}


        return;

    }}


    /* =============================================
       MONITOR
       ============================================= */

    if (
        nearbyObject.id ===
        "monitor"
    ){{

        document.getElementById(
            "status"
        ).textContent =
            "MONITOR // SIGNAL UNSTABLE";

        return;

    }}


    /* =============================================
       DESK
       ============================================= */

    if (
        nearbyObject.id ===
        "desk"
    ){{

        document.getElementById(
            "status"
        ).textContent =
            "DESK // NOTHING UNUSUAL";

        return;

    }}


    /* =============================================
       EXIT DOOR
       ============================================= */

    if (
        nearbyObject.id ===
        "exitDoor"
    ){{

        if (inventory[0]){{

            document.getElementById(
                "status"
            ).textContent =
                "SECURITY DOOR // ACCESS GRANTED";

        }} else {{

            document.getElementById(
                "status"
            ).textContent =
                "SECURITY DOOR // ACCESS CARD REQUIRED";

        }}

    }}

}}


/* =====================================================
   KEYBOARD
   ===================================================== */

function handleKeyDown(event){{

    const key =
        event.key.toLowerCase();


    /* =============================================
       ESC
       ============================================= */

    if (key === "escape"){{

        if (helpOpen){{

            closeHelp();

            event.preventDefault();

            return;

        }}


        if (inventoryOpen){{

            closeInventory();

            event.preventDefault();

            return;

        }}

    }}


    /* =============================================
       H
       ============================================= */

    if (key === "h"){{

        if (
            !paused &&
            !finished
        ){{

            if (inventoryOpen){{

                return;

            }}


            if (helpOpen){{

                closeHelp();

            }} else {{

                openHelp();

            }}

        }}


        event.preventDefault();

        return;

    }}


    /* =============================================
       I
       ============================================= */

    if (key === "i"){{

        if (
            !paused &&
            !finished
        ){{

            if (helpOpen){{

                return;

            }}


            if (inventoryOpen){{

                closeInventory();

            }} else {{

                openInventory();

            }}

        }}


        event.preventDefault();

        return;

    }}


    /* =============================================
       E
       ============================================= */

    if (key === "e"){{

        interact();

        event.preventDefault();

        return;

    }}


    /* =============================================
       MOVEMENT
       ============================================= */

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
            !finished
        ){{

            keys[key] = true;

        }}


        event.preventDefault();

        return;

    }}

}}


/* =====================================================
   KEYBOARD RELEASE
   ===================================================== */

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


/*
   window에 한 번만 등록한다.
   gameRoot에도 별도 keydown을 등록하지 않아
   H / I / E가 두 번 실행되는 문제를 방지한다.
*/

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


/* =====================================================
   WINDOW BLUR
   ===================================================== */

window.addEventListener(
    "blur",
    function(){{

        clearMovementKeys();

    }}
);


/* =====================================================
   MOBILE DIRECTION BUTTONS
   ===================================================== */

const mobileButtons =
    document.querySelectorAll(
        ".control-button"
    );


mobileButtons.forEach(
    function(button){{

        const direction =
            button.dataset.direction;


        /* =============================================
           TOUCH START
           ============================================= */

        button.addEventListener(
            "touchstart",
            function(event){{

                event.preventDefault();


                if (
                    !paused &&
                    !helpOpen &&
                    !inventoryOpen &&
                    !finished
                ){{

                    keys[direction] =
                        true;

                }}

            }},
            {{
                passive: false
            }}
        );


        /* =============================================
           TOUCH END
           ============================================= */

        button.addEventListener(
            "touchend",
            function(event){{

                event.preventDefault();

                keys[direction] =
                    false;

            }},
            {{
                passive: false
            }}
        );


        /* =============================================
           TOUCH CANCEL
           ============================================= */

        button.addEventListener(
            "touchcancel",
            function(event){{

                event.preventDefault();

                keys[direction] =
                    false;

            }},
            {{
                passive: false
            }}
        );


        /* =============================================
           POINTER DOWN
           ============================================= */

        button.addEventListener(
            "pointerdown",
            function(event){{

                event.preventDefault();


                if (
                    !paused &&
                    !helpOpen &&
                    !inventoryOpen &&
                    !finished
                ){{

                    keys[direction] =
                        true;

                }}

            }}
        );


        /* =============================================
           POINTER UP
           ============================================= */

        button.addEventListener(
            "pointerup",
            function(event){{

                event.preventDefault();

                keys[direction] =
                    false;

            }}
        );


        /* =============================================
           POINTER CANCEL
           ============================================= */

        button.addEventListener(
            "pointercancel",
            function(){{

                keys[direction] =
                    false;

            }}
        );


        /* =============================================
           POINTER LEAVE
           ============================================= */

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
   SYSTEM FAILURE BUTTONS
   ===================================================== */

const restartButton =
    document.getElementById(
        "restartButton"
    );


const titleButton =
    document.getElementById(
        "titleButton"
    );


/* =====================================================
   RESTART
   ===================================================== */

restartButton.addEventListener(
    "click",
    function(){{

        const currentURL =
            new URL(
                window.parent.location.href
            );


        currentURL.searchParams.set(
            "action",
            "restart"
        );


        window.parent.location.href =
            currentURL.toString();

    }}
);


/* =====================================================
   TITLE
   ===================================================== */

titleButton.addEventListener(
    "click",
    function(){{

        const currentURL =
            new URL(
                window.parent.location.href
            );


        currentURL.searchParams.set(
            "action",
            "title"
        );


        window.parent.location.href =
            currentURL.toString();

    }}
);


/* =====================================================
   TIMER
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


    document.getElementById(
        "timeOver"
    ).style.display =
        "flex";


    /*
       SYSTEM FAILURE가 표시되면
       게임 화면이 더 이상 키 입력을
       처리하지 않도록 한다.
    */

    focusGame();

}}


function updateTimer(){{

    if (
        paused ||
        helpOpen ||
        inventoryOpen ||
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


    document.getElementById(
        "timer"
    ).textContent =
        formatTime(
            remaining
        );


    if (remaining <= 0){{

        showTimeOver();

    }}

}}


setInterval(
    updateTimer,
    1000
);


/* =====================================================
   INITIAL STATE
   ===================================================== */

if (paused){{

    document.getElementById(
        "pauseOverlay"
    ).style.display =
        "flex";

}}


if (finished){{

    document.getElementById(
        "timeOver"
    ).style.display =
        "flex";

}}


/* =====================================================
   INITIAL POSITION
   ===================================================== */

player.style.left =
    playerX + "%";


player.style.top =
    playerY + "%";


checkInteraction();


/* =====================================================
   START MOVEMENT LOOP
   ===================================================== */

requestAnimationFrame(
    updatePlayer
);


/* =====================================================
   INITIAL FOCUS
   ===================================================== */

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
