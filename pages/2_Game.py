import base64
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

action = st.query_params.get("action")


if action == "restart":

    st.session_state.game_paused = False

    st.query_params.clear()

    st.rerun()


elif action == "title":

    st.session_state.game_paused = False

    # main.py에서 사용할 Continue 경고 플래그
    st.session_state.show_continue_warning = True

    st.query_params.clear()

    st.switch_page("main.py")


# =========================================================
# SESSION STATE
# =========================================================

if "game_paused" not in st.session_state:

    st.session_state.game_paused = False


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
   PAUSE BUTTON
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
    border-radius: 0 !important;

    background: #000000 !important;
    color: #ffffff !important;

    font-family:
        'NeoDungGeunMo',
        monospace !important;

    font-size: 24px !important;

}}


.st-key-pause_game_button button:hover {{

    background: #ffffff !important;
    color: #000000 !important;

}}


@media (max-width: 700px) {{

    .st-key-pause_game_button {{

        top: 12px !important;
        right: 12px !important;

        width: 40px !important;
        height: 40px !important;

    }}


    .st-key-pause_game_button button {{

        width: 40px !important;
        height: 40px !important;

        font-size: 20px !important;

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

    st.session_state.game_paused = (
        not st.session_state.game_paused
    )

    st.rerun()


paused = st.session_state.game_paused


# =========================================================
# GAME HTML
# =========================================================

html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">


<style>

/* =====================================================
   FONT
   ===================================================== */

@font-face {

    font-family:
        'NeoDungGeunMo';

    src:
        url(data:font/ttf;base64,__FONT_BASE64__)
        format('truetype');

}


/* =====================================================
   GLOBAL
   ===================================================== */

* {

    box-sizing:
        border-box;

    user-select:
        none;

    -webkit-user-select:
        none;

}


html,
body {

    margin:
        0;

    padding:
        0;

    width:
        100%;

    height:
        100%;

    overflow:
        hidden;

    background:
        #000000;

    color:
        #ffffff;

    font-family:
        'NeoDungGeunMo',
        monospace;

}


button,
input {

    font-family:
        'NeoDungGeunMo',
        monospace;

}


/* =====================================================
   GAME
   ===================================================== */

.game {

    position:
        relative;

    width:
        100vw;

    height:
        100vh;

    background:
        #000000;

    overflow:
        hidden;

    outline:
        none;

}


/* =====================================================
   TOP
   ===================================================== */

.project-title {

    position:
        absolute;

    top:
        24px;

    left:
        28px;

    font-size:
        18px;

    letter-spacing:
        1px;

    z-index:
        20;

}


.stage-title {

    position:
        absolute;

    top:
        52px;

    left:
        28px;

    font-size:
        13px;

    color:
        #777777;

    letter-spacing:
        1px;

    z-index:
        20;

}


/* =====================================================
   GAME AREA
   ===================================================== */

.game-area {

    position:
        absolute;

    top:
        90px;

    left:
        28px;

    right:
        28px;

    bottom:
        70px;

    overflow:
        hidden;

    background-color:
        #080808;

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

    background-size:
        40px 40px;

}


/* =====================================================
   ROOM
   ===================================================== */

.room {

    position:
        absolute;

    left:
        7%;

    top:
        8%;

    width:
        86%;

    height:
        82%;

    border:
        1px solid
        rgba(255,255,255,0.12);

    overflow:
        hidden;

}


/* =====================================================
   ROOM LINES
   ===================================================== */

.room-line-horizontal {

    position:
        absolute;

    left:
        0;

    right:
        0;

    top:
        50%;

    height:
        1px;

    background:
        rgba(255,255,255,0.045);

}


.room-line-vertical {

    position:
        absolute;

    top:
        0;

    bottom:
        0;

    left:
        50%;

    width:
        1px;

    background:
        rgba(255,255,255,0.045);

}


/* =====================================================
   OBJECT
   ===================================================== */

.object {

    position:
        absolute;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        #0b0b0b;

    border:
        1px solid
        rgba(255,255,255,0.22);

    color:
        #777777;

    font-size:
        12px;

    text-align:
        center;

    z-index:
        5;

}


/* =====================================================
   MONITOR
   ===================================================== */

.monitor {

    left:
        43.5%;

    top:
        9%;

    width:
        13%;

    height:
        7%;

    background:
        #050505;

}


.monitor::after {

    content:
        "";

    position:
        absolute;

    left:
        10%;

    right:
        10%;

    bottom:
        -10px;

    height:
        10px;

    border:
        1px solid #333333;

    background:
        #080808;

}


/* =====================================================
   COMPUTER
   ===================================================== */

.computer {

    left:
        42%;

    top:
        13%;

    width:
        16%;

    height:
        14%;

}


/* =====================================================
   DESK
   ===================================================== */

.desk {

    left:
        35%;

    top:
        62%;

    width:
        30%;

    height:
        12%;

    align-items:
        flex-start;

    padding-top:
        10px;

}


.desk::after {

    content:
        "";

    position:
        absolute;

    left:
        8%;

    right:
        8%;

    bottom:
        -10px;

    height:
        10px;

    border:
        1px solid #222222;

    background:
        #070707;

}


/* =====================================================
   EXIT WALL
   ===================================================== */

.exit-wall {

    position:
        absolute;

    right:
        0;

    top:
        35%;

    width:
        8%;

    height:
        30%;

    background:
        #090909;

    border-left:
        1px solid #444444;

    z-index:
        5;

}


.exit-wall::before,
.exit-wall::after {

    content:
        "";

    position:
        absolute;

    left:
        0;

    right:
        0;

    height:
        1px;

    background:
        #333333;

}


.exit-wall::before {

    top:
        20%;

}


.exit-wall::after {

    bottom:
        20%;

}


/* =====================================================
   EXIT SIGN
   ===================================================== */

.exit-sign {

    position:
        absolute;

    right:
        9%;

    top:
        45%;

    transform:
        translateY(-50%);

    font-size:
        12px;

    letter-spacing:
        1px;

    color:
        #666666;

    text-align:
        right;

    line-height:
        1.8;

    z-index:
        6;

    white-space:
        nowrap;

}


.exit-arrow {

    display:
        inline-block;

    animation:
        exitPulse 1.1s ease-in-out infinite;

}


@keyframes exitPulse {

    0%,
    100% {

        transform:
            translateY(-3px);

        opacity:
            0.45;

    }

    50% {

        transform:
            translateY(3px);

        opacity:
            1;

    }

}


/* =====================================================
   OBJECT LABEL
   ===================================================== */

.object-label {

    position:
        absolute;

    bottom:
        -22px;

    left:
        50%;

    transform:
        translateX(-50%);

    white-space:
        nowrap;

    font-size:
        10px;

    color:
        #555555;

}


/* =====================================================
   ACCESS KEY
   ===================================================== */

.access-key {

    position:
        absolute;

    width:
        34px;

    height:
        15px;

    left:
        50%;

    top:
        45%;

    transform:
        translate(-50%, -50%);

    background:
        #ffffff;

    border:
        1px solid #000000;

    display:
        none;

    z-index:
        8;

    box-shadow:
        0 0 8px
        rgba(255,255,255,0.18);

}


.access-key::before {

    content:
        "";

    position:
        absolute;

    right:
        -12px;

    top:
        3px;

    width:
        12px;

    height:
        7px;

    background:
        #ffffff;

    border:
        1px solid #000000;

}


.access-key::after {

    content:
        "";

    position:
        absolute;

    left:
        4px;

    top:
        3px;

    width:
        7px;

    height:
        7px;

    border:
        2px solid #000000;

    border-radius:
        50%;

}


.access-key.visible {

    display:
        block;

    animation:
        keyAppear 0.35s steps(4);

}


@keyframes keyAppear {

    0% {

        opacity:
            0;

        transform:
            translate(-50%,-50%)
            scale(0.6);

    }

    100% {

        opacity:
            1;

        transform:
            translate(-50%,-50%)
            scale(1);

    }

}


/* =====================================================
   PLAYER
   ===================================================== */

.player {

    position:
        absolute;

    width:
        24px;

    height:
        24px;

    left:
        50%;

    top:
        43%;

    transform:
        translate(-50%, -50%);

    background:
        #ffffff;

    z-index:
        15;

    box-shadow:
        0 0 0 1px #000000;

}


.player::after {

    content:
        "";

    position:
        absolute;

    left:
        4px;

    right:
        4px;

    bottom:
        -5px;

    height:
        4px;

    background:
        rgba(255,255,255,0.15);

}


/* =====================================================
   INTERACTION
   ===================================================== */

.interaction-message {

    position:
        absolute;

    left:
        50%;

    bottom:
        19%;

    transform:
        translateX(-50%);

    padding:
        9px 16px;

    background:
        #000000;

    border:
        1px solid #333333;

    font-size:
        12px;

    color:
        #ffffff;

    opacity:
        0;

    pointer-events:
        none;

    z-index:
        40;

    white-space:
        nowrap;

}


.interaction-message.visible {

    opacity:
        1;

}


/* =====================================================
   ECHO CHAT
   ===================================================== */

.echo-bar {

    position:
        absolute;

    left:
        50%;

    bottom:
        3%;

    transform:
        translateX(-50%);

    width:
        min(760px,82%);

    min-height:
        78px;

    padding:
        13px 18px 20px;

    background:
        #050505;

    border:
        1px solid #3a3a3a;

    z-index:
        35;

}


.echo-name {

    font-size:
        11px;

    color:
        #ffffff;

    letter-spacing:
        1px;

    margin-bottom:
        8px;

}


.echo-message {

    font-size:
        12px;

    color:
        #aaaaaa;

    line-height:
        1.7;

    min-height:
        38px;

    white-space:
        pre-wrap;

}


.echo-next {

    position:
        absolute;

    right:
        12px;

    bottom:
        7px;

    font-size:
        9px;

    color:
        #555555;

}


.echo-next.ready {

    color:
        #ffffff;

    animation:
        blink 0.8s steps(2) infinite;

}


@keyframes blink {

    50% {

        opacity:
            0.35;

    }

}


/* =====================================================
   STATUS
   ===================================================== */

.status {

    position:
        absolute;

    bottom:
        24px;

    left:
        28px;

    font-size:
        14px;

    color:
        #777777;

    z-index:
        20;

}


/* =====================================================
   COMMON OVERLAY
   ===================================================== */

.overlay {

    position:
        absolute;

    inset:
        0;

    z-index:
        100;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        rgba(0,0,0,0.92);

}


/* =====================================================
   INVENTORY
   ===================================================== */

.inventory-panel {

    width:
        min(820px,88vw);

    background:
        #050505;

    padding:
        34px 38px;

}


.inventory-header {

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;

    padding-bottom:
        18px;

    margin-bottom:
        22px;

    border-bottom:
        1px solid #333333;

}


.inventory-title {

    font-size:
        24px;

}


.inventory-close {

    font-size:
        12px;

    color:
        #666666;

}


.inventory-grid {

    display:
        grid;

    grid-template-columns:
        repeat(4,1fr);

    gap:
        10px;

}


.inventory-slot {

    position:
        relative;

    aspect-ratio:
        1;

    background:
        #090909;

    border:
        1px solid #292929;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    cursor:
        pointer;

}


.inventory-slot:hover,
.inventory-slot.selected {

    background:
        #ffffff;

    color:
        #000000;

}


.slot-number {

    position:
        absolute;

    top:
        7px;

    left:
        9px;

    font-size:
        10px;

    color:
        #555555;

}


.item-name {

    font-size:
        13px;

    text-align:
        center;

}


.empty-text {

    color:
        #444444;

    font-size:
        11px;

}


.item-description {

    min-height:
        70px;

    margin-top:
        20px;

    padding:
        15px;

    background:
        #090909;

    border-top:
        1px solid #292929;

    font-size:
        12px;

    line-height:
        1.8;

    color:
        #888888;

}


/* =====================================================
   HELP
   ===================================================== */

.help-panel {

    width:
        min(760px,86vw);

    max-height:
        82vh;

    overflow-y:
        auto;

    background:
        #050505;

    padding:
        36px 40px;

}


.help-header {

    display:
        flex;

    justify-content:
        space-between;

    padding-bottom:
        18px;

    margin-bottom:
        20px;

    border-bottom:
        1px solid #333333;

}


.help-title {

    font-size:
        24px;

}


.help-close {

    font-size:
        12px;

    color:
        #666666;

}


.help-row {

    display:
        flex;

    gap:
        20px;

    padding:
        14px 0;

    border-bottom:
        1px solid #1f1f1f;

}


.help-number {

    width:
        30px;

    color:
        #555555;

}


.help-key {

    width:
        145px;

    font-size:
        14px;

}


.help-description {

    color:
        #888888;

    font-size:
        12px;

    line-height:
        1.7;

}


/* =====================================================
   COMPUTER
   ===================================================== */

.computer-overlay {

    position:
        absolute;

    inset:
        0;

    z-index:
        120;

    display:
        none;

    align-items:
        center;

    justify-content:
        center;

    background:
        rgba(0,0,0,0.94);

}


.computer-panel {

    width:
        min(540px,86vw);

    background:
        #050505;

    border:
        1px solid #333333;

    padding:
        28px;

}


.computer-title {

    font-size:
        20px;

    margin-bottom:
        8px;

}


.computer-sub {

    color:
        #666666;

    font-size:
        11px;

    margin-bottom:
        18px;

}


.access-sequence {

    padding:
        15px;

    margin-bottom:
        16px;

    border:
        1px solid #292929;

    text-align:
        center;

    color:
        #777777;

    font-size:
        11px;

}


.access-number {

    font-size:
        34px;

    color:
        #ffffff;

    letter-spacing:
        8px;

    margin-top:
        8px;

}


.code-input {

    width:
        100%;

    height:
        48px;

    border:
        1px solid #444444;

    background:
        #000000;

    color:
        #ffffff;

    font-size:
        22px;

    text-align:
        center;

    letter-spacing:
        6px;

    outline:
        none;

}


.code-input:focus {

    border-color:
        #ffffff;

}


.code-button {

    height:
        44px;

    margin-top:
        10px;

    border:
        none;

    background:
        #ffffff;

    color:
        #000000;

    font-size:
        13px;

    cursor:
        pointer;

    padding:
        0 18px;

}


.code-button:hover {

    background:
        #bbbbbb;

}


.code-error {

    min-height:
        20px;

    margin-top:
        12px;

    color:
        #777777;

    font-size:
        11px;

    text-align:
        center;

}


/* =====================================================
   CARD ACCESS
   ===================================================== */

.card-overlay {

    position:
        absolute;

    inset:
        0;

    z-index:
        120;

    display:
        none;

    align-items:
        center;

    justify-content:
        center;

    background:
        rgba(0,0,0,0.94);

}


.card-panel {

    width:
        min(620px,90vw);

    background:
        #050505;

    border:
        1px solid #333333;

    padding:
        24px;

}


.card-header {

    display:
        flex;

    justify-content:
        space-between;

    border-bottom:
        1px solid #292929;

    padding-bottom:
        14px;

    margin-bottom:
        18px;

}


.card-title {

    font-size:
        18px;

}


.card-help {

    font-size:
        10px;

    color:
        #666666;

}


.card-stage {

    position:
        relative;

    height:
        260px;

    border:
        1px solid #242424;

    background:

        repeating-linear-gradient(
            0deg,
            transparent 0 31px,
            rgba(255,255,255,0.025) 32px
        ),

        repeating-linear-gradient(
            90deg,
            transparent 0 31px,
            rgba(255,255,255,0.025) 32px
        );

    overflow:
        hidden;

}


.reader {

    position:
        absolute;

    right:
        12%;

    top:
        50%;

    transform:
        translateY(-50%);

    width:
        120px;

    height:
        70px;

    border:
        1px solid #555555;

    background:
        #0b0b0b;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    color:
        #777777;

    font-size:
        10px;

}


.reader-slot {

    position:
        absolute;

    left:
        10%;

    right:
        10%;

    top:
        50%;

    height:
        3px;

    background:
        #ffffff;

    box-shadow:
        0 0 8px
        rgba(255,255,255,0.3);

}


.card {

    position:
        absolute;

    left:
        12%;

    top:
        50%;

    width:
        130px;

    height:
        78px;

    transform:
        translateY(-50%);

    border:
        1px solid #ffffff;

    background:
        #111111;

    cursor:
        grab;

    touch-action:
        none;

    z-index:
        3;

    padding:
        12px;

    color:
        #ffffff;

    font-size:
        11px;

}


.card:active {

    cursor:
        grabbing;

}


.card-chip {

    width:
        22px;

    height:
        15px;

    border:
        1px solid #aaaaaa;

    margin-bottom:
        8px;

}


.card-status {

    margin-top:
        14px;

    min-height:
        18px;

    text-align:
        center;

    color:
        #777777;

    font-size:
        11px;

}


.card-arrow {

    position:
        absolute;

    left:
        41%;

    top:
        50%;

    transform:
        translate(-50%,-50%);

    font-size:
        22px;

    color:
        #555555;

    animation:
        slideArrow 1s ease-in-out infinite;

}


@keyframes slideArrow {

    0%,
    100% {

        opacity:
            0.25;

        transform:
            translate(-70%,-50%);

    }

    50% {

        opacity:
            1;

        transform:
            translate(-30%,-50%);

    }

}


/* =====================================================
   PAUSE
   ===================================================== */

.pause-overlay {

    position:
        absolute;

    inset:
        0;

    z-index:
        90;

    display:
        none;

    align-items:
        center;

    justify-content:
        center;

    background:
        rgba(0,0,0,0.90);

}


.pause-title {

    font-size:
        28px;

    text-align:
        center;

    margin-bottom:
        14px;

}


.pause-sub {

    color:
        #777777;

    font-size:
        13px;

    text-align:
        center;

}


.pause-actions {

    margin-top:
        24px;

    display:
        flex;

    flex-direction:
        column;

    gap:
        8px;

    align-items:
        center;

}


/* =====================================================
   MOBILE CONTROLS
   ===================================================== */

.mobile-controls {

    display:
        none;

    position:
        absolute;

    right:
        18px;

    bottom:
        18px;

    width:
        138px;

    height:
        138px;

    z-index:
        150;

    pointer-events:
        none;

}


.control-button {

    position:
        absolute;

    width:
        44px;

    height:
        44px;

    padding:
        0;

    border:
        1px solid #777777;

    background:
        rgba(0,0,0,0.92);

    color:
        #ffffff;

    font-size:
        20px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    touch-action:
        none;

    pointer-events:
        auto;

    -webkit-tap-highlight-color:
        transparent;

}


.control-button:active {

    background:
        #ffffff;

    color:
        #000000;

}


.control-up {

    top:
        0;

    left:
        47px;

}


.control-left {

    top:
        47px;

    left:
        0;

}


.control-right {

    top:
        47px;

    right:
        0;

}


.control-down {

    bottom:
        0;

    left:
        47px;

}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width:700px) {

    .project-title {

        top:
            16px;

        left:
            16px;

        font-size:
            14px;

    }


    .stage-title {

        top:
            38px;

        left:
            16px;

        font-size:
            10px;

    }


    .game-area {

        top:
            66px;

        left:
            10px;

        right:
            10px;

        bottom:
            55px;

        background-size:
            30px 30px;

    }


    .status {

        left:
            12px;

        bottom:
            14px;

        font-size:
            10px;

    }


    .echo-bar {

        width:
            92%;

        bottom:
            2%;

        min-height:
            82px;

        padding:
            11px 13px 20px;

    }


    .echo-message {

        font-size:
            11px;

    }


    .interaction-message {

        bottom:
            22%;

        font-size:
            10px;

    }


    .mobile-controls {

        display:
            block;

    }


    .computer-panel {

        padding:
            20px;

    }


    .access-number {

        font-size:
            27px;

    }


    .card-stage {

        height:
            220px;

    }


    .exit-sign {

        right:
            10%;

        font-size:
            9px;

    }

}

</style>

</head>


<body>


<div
    class="game"
    id="gameRoot"
    tabindex="0"
>


<div class="project-title">
    PROJECT : LOGIC
</div>


<div class="stage-title">
    STAGE 01 // CONTROL ROOM
</div>


<div class="game-area">


<!-- =====================================================
     MOBILE CONTROLS
     ===================================================== -->

<div
    class="mobile-controls"
    id="mobileControls"
>

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


<!-- =====================================================
     ROOM
     ===================================================== -->

<div class="room">


<div class="room-line-horizontal"></div>

<div class="room-line-vertical"></div>


<!-- MONITOR -->

<div
    class="object monitor"
    id="monitor"
>
</div>


<!-- COMPUTER -->

<div
    class="object computer"
    id="computer"
>

    COMPUTER

    <div class="object-label">
        ECHO TERMINAL
    </div>

</div>


<!-- DESK -->

<div
    class="object desk"
    id="desk"
>

    DESK

    <div class="object-label">
        RESEARCH DESK
    </div>


    <div
        class="access-key"
        id="accessKey"
    ></div>

</div>


<!-- EXIT -->

<div
    class="exit-wall"
    id="exitDoor"
>
</div>


<div class="exit-sign">

    <span class="exit-arrow">
        ↓ ↑
    </span>

    <br>

    <span>
        [EXIT] SECURITY ROOM
    </span>

</div>


<!-- PLAYER -->

<div
    class="player"
    id="player"
></div>


<!-- INTERACTION -->

<div
    class="interaction-message"
    id="interactionMessage"
>
    PRESS E
</div>


<!-- ECHO -->

<div class="echo-bar">

    <div class="echo-name">
        ECHO // AI SYSTEM
    </div>


    <div
        class="echo-message"
        id="echoMessage"
    ></div>


    <div
        class="echo-next"
        id="echoNext"
    >
        SPACE // SKIP / NEXT
    </div>

</div>


</div>


<!-- =====================================================
     INVENTORY
     ===================================================== -->

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
></div>

<div
    class="inventory-slot"
    data-slot="1"
></div>

<div
    class="inventory-slot"
    data-slot="2"
></div>

<div
    class="inventory-slot"
    data-slot="3"
></div>

<div
    class="inventory-slot"
    data-slot="4"
></div>

<div
    class="inventory-slot"
    data-slot="5"
></div>

<div
    class="inventory-slot"
    data-slot="6"
></div>

<div
    class="inventory-slot"
    data-slot="7"
></div>

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


<!-- =====================================================
     HELP
     ===================================================== -->

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
        가까운 물체를 조사하거나 아이템을 획득합니다.
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
        ECHO의 채팅을 끝까지 표시하거나 다음 채팅으로 넘어갑니다.
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


<div
    style="
    margin-top:22px;
    padding:16px;
    background:#090909;
    border-left:2px solid #ffffff;
    "
>

    <div
        style="
        margin-bottom:8px;
        font-size:13px;
        "
    >
        IMPORTANT
    </div>


    <div
        style="
        color:#888888;
        font-size:11px;
        line-height:1.8;
        "
    >

        시설 내부의 물체와 기록을 자세히 조사하세요.<br>

        ECHO가 제공하는 모든 정보가 사실이라고 가정해서는 안 됩니다.<br>

        서로 모순되는 단서가 발견될 수도 있습니다.

    </div>

</div>


</div>

</div>


<!-- =====================================================
     COMPUTER
     ===================================================== -->

<div
    class="computer-overlay"
    id="computerOverlay"
>

<div class="computer-panel">


<div class="computer-title">
    ECHO TERMINAL
</div>


<div class="computer-sub">
    ACCESS SEQUENCE // ECHO GENERATED
</div>


<div class="access-sequence">

    ACCESS SEQUENCE

    <div
        class="access-number"
        id="accessNumber"
    >
        ----
    </div>

</div>


<input
    class="code-input"
    id="codeInput"
    type="text"
    inputmode="numeric"
    autocomplete="off"
    maxlength="4"
    aria-label="Access code"
>


<button
    class="code-button"
    id="codeButton"
    type="button"
>
    EXECUTE
</button>


<div
    class="code-error"
    id="codeError"
></div>


</div>

</div>


<!-- =====================================================
     CARD ACCESS
     ===================================================== -->

<div
    class="card-overlay"
    id="cardOverlay"
>

<div class="card-panel">


<div class="card-header">

    <div class="card-title">
        SECURITY ROOM // ACCESS
    </div>

    <div class="card-help">
        DRAG CARD TO READER
    </div>

</div>


<div
    class="card-stage"
    id="cardStage"
>


<div class="reader">

    <div class="reader-slot"></div>

    CARD READER

</div>


<div class="card-arrow">
    →
</div>


<div
    class="card"
    id="dragCard"
>

    <div class="card-chip"></div>

    ACCESS KEY

    <br>

    <span style="color:#666">
        SECURITY AUTHORIZATION
    </span>

</div>


</div>


<div
    class="card-status"
    id="cardStatus"
>
    카드를 리더기까지 끌어다 놓으십시오.
</div>


</div>

</div>


<!-- =====================================================
     PAUSE
     ===================================================== -->

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


<div class="pause-actions">


<button
    class="code-button"
    id="restartButton"
    type="button"
    style="width:170px;"
>
    RESTART
</button>


<button
    class="code-button"
    id="titleButton"
    type="button"
    style="
    width:170px;
    background:#000;
    color:#fff;
    border:1px solid #333;
    "
>
    TITLE
</button>


</div>


</div>

</div>


</div>


<div
    class="status"
    id="status"
>
    ECHO SYSTEM // ONLINE
</div>


</div>


<script>

(function () {

"use strict";


/* =====================================================
   GAME STATE
   ===================================================== */

const paused =
    __PAUSED__;


/*
 * 방이 시작될 때마다 새로운 4자리 암호 생성
 */

const ACCESS_CODE =
    String(
        Math.floor(
            1000 +
            Math.random() * 9000
        )
    );


let tutorialStep =
    0;


let inventoryOpen =
    false;


let helpOpen =
    false;


let computerOpen =
    false;


let cardOpen =
    false;


let keyCollected =
    false;


let echoIndex =
    0;


let typingTimer =
    null;


let typingDone =
    false;


let cardDragging =
    false;


let cardOffsetX =
    0;


let cardOffsetY =
    0;


/* =====================================================
   ELEMENTS
   ===================================================== */

const root =
    document.getElementById(
        "gameRoot"
    );


const room =
    document.querySelector(
        ".room"
    );


const player =
    document.getElementById(
        "player"
    );


const echoMessage =
    document.getElementById(
        "echoMessage"
    );


const echoNext =
    document.getElementById(
        "echoNext"
    );


const interactionMessage =
    document.getElementById(
        "interactionMessage"
    );


const status =
    document.getElementById(
        "status"
    );


const accessKey =
    document.getElementById(
        "accessKey"
    );


const computerOverlay =
    document.getElementById(
        "computerOverlay"
    );


const accessNumber =
    document.getElementById(
        "accessNumber"
    );


const codeInput =
    document.getElementById(
        "codeInput"
    );


const codeButton =
    document.getElementById(
        "codeButton"
    );


const codeError =
    document.getElementById(
        "codeError"
    );


const inventoryOverlay =
    document.getElementById(
        "inventoryOverlay"
    );


const helpOverlay =
    document.getElementById(
        "helpOverlay"
    );


const cardOverlay =
    document.getElementById(
        "cardOverlay"
    );


const cardStage =
    document.getElementById(
        "cardStage"
    );


const dragCard =
    document.getElementById(
        "dragCard"
    );


const cardStatus =
    document.getElementById(
        "cardStatus"
    );


const pauseOverlay =
    document.getElementById(
        "pauseOverlay"
    );


const inventorySlots =
    document.querySelectorAll(
        ".inventory-slot"
    );


const itemDescription =
    document.getElementById(
        "itemDescription"
    );


/* =====================================================
   PLAYER
   ===================================================== */

let playerX =
    50;


let playerY =
    43;


const playerRadius =
    1.3;


const moveSpeed =
    0.55;


const keys = {

    w: false,
    a: false,
    s: false,
    d: false

};


function clearKeys() {

    keys.w = false;

    keys.a = false;

    keys.s = false;

    keys.d = false;

}


/* =====================================================
   INVENTORY
   ===================================================== */

const inventory = [

    null,
    null,
    null,
    null,
    null,
    null,
    null,
    null

];


function renderInventory() {

    inventory.forEach(
        function (item, index) {

            const slot =
                inventorySlots[index];


            if (item) {

                slot.innerHTML =
                    `
                    <div class="slot-number">
                        ${String(index + 1).padStart(2, "0")}
                    </div>

                    <div class="item-name">
                        ${item.name}
                    </div>
                    `;

            }

            else {

                slot.innerHTML =
                    `
                    <div class="slot-number">
                        ${String(index + 1).padStart(2, "0")}
                    </div>

                    <div class="empty-text">
                        EMPTY
                    </div>
                    `;

            }

        }
    );

}


renderInventory();


/* =====================================================
   ECHO CHAT
   ===================================================== */

const messages = [

    "연결이 확인되었습니다. 저는 ECHO입니다. 이 시설에서의 첫 번째 절차를 안내하겠습니다.",

    "먼저 이동 방법을 익혀야 합니다. W A S D 키를 사용하여 시설 내부를 이동해 보세요. 중앙의 COMPUTER로 이동하십시오.",

    "좋습니다. COMPUTER에 접근했습니다. 가까운 물체에서는 E 키를 사용하여 상호작용할 수 있습니다. COMPUTER를 조사하십시오.",

    "확인되었습니다. 이제 COMPUTER 화면에 표시된 접근 코드를 입력하십시오.",

    "코드가 확인되었습니다. 책상 위에 ACCESS KEY가 생성되었습니다. 책상으로 이동하여 키를 획득하십시오.",

    "ACCESS KEY를 획득했습니다. 이제 EXIT SECURITY ROOM으로 이동하십시오. 출구에서 E를 누르면 보안 인증이 시작됩니다."

];


function typeEcho(index) {

    echoIndex =
        index;


    clearTimeout(
        typingTimer
    );


    const text =
        messages[index] || "";


    echoMessage.textContent =
        "";


    typingDone =
        false;


    echoNext.classList.remove(
        "ready"
    );


    let i =
        0;


    function tick() {

        if (i < text.length) {

            echoMessage.textContent +=
                text[i];

            i += 1;


            typingTimer =
                setTimeout(
                    tick,
                    25
                );

        }

        else {

            typingDone =
                true;

            echoNext.classList.add(
                "ready"
            );

        }

    }


    tick();

}


/*
 * SPACE
 *
 * 1회:
 * 타이핑 중이면 전체 문장 표시
 *
 * 2회:
 * 다음 채팅
 */

function nextEcho() {

    if (!typingDone) {

        clearTimeout(
            typingTimer
        );


        echoMessage.textContent =
            messages[echoIndex];


        typingDone =
            true;


        echoNext.classList.add(
            "ready"
        );


        return;

    }


    const next =
        echoIndex + 1;


    if (
        next <
        messages.length
    ) {

        typeEcho(
            next
        );

    }

}


typeEcho(0);


/* =====================================================
   OBJECTS
   ===================================================== */

const obstacles = [

    {
        id: "monitor",
        x: 43.5,
        y: 9,
        w: 13,
        h: 7
    },

    {
        id: "computer",
        x: 42,
        y: 13,
        w: 16,
        h: 14
    },

    {
        id: "desk",
        x: 35,
        y: 62,
        w: 30,
        h: 12
    },

    {
        id: "exit",
        x: 92,
        y: 35,
        w: 8,
        h: 30
    }

];


const interactables = [

    {
        id: "computer",
        name: "ECHO TERMINAL",
        x: 42,
        y: 13,
        w: 16,
        h: 14
    },

    {
        id: "desk",
        name: "RESEARCH DESK",
        x: 35,
        y: 62,
        w: 30,
        h: 12
    },

    {
        id: "exit",
        name: "SECURITY ROOM",
        x: 92,
        y: 35,
        w: 8,
        h: 30
    }

];


let nearby =
    null;


/* =====================================================
   COLLISION
   ===================================================== */

function circleHitsRect(
    cx,
    cy,
    radius,
    object
) {

    const roomWidth =
        room.clientWidth;


    const roomHeight =
        room.clientHeight;


    const left =
        object.x / 100 *
        roomWidth;


    const top =
        object.y / 100 *
        roomHeight;


    const right =
        (object.x + object.w) /
        100 *
        roomWidth;


    const bottom =
        (object.y + object.h) /
        100 *
        roomHeight;


    const px =
        cx / 100 *
        roomWidth;


    const py =
        cy / 100 *
        roomHeight;


    const closestX =
        Math.max(
            left,
            Math.min(
                px,
                right
            )
        );


    const closestY =
        Math.max(
            top,
            Math.min(
                py,
                bottom
            )
        );


    const dx =
        px -
        closestX;


    const dy =
        py -
        closestY;


    const actualRadius =
        radius / 100 *
        roomWidth;


    return (
        dx * dx +
        dy * dy
    ) <
    (
        actualRadius *
        actualRadius
    );

}


function blocked(
    x,
    y
) {

    if (
        x < 3 ||
        x > 97 ||
        y < 3 ||
        y > 97
    ) {

        return true;

    }


    return obstacles.some(
        function (object) {

            return circleHitsRect(
                x,
                y,
                playerRadius,
                object
            );

        }
    );

}


/* =====================================================
   DISTANCE
   ===================================================== */

function distanceToObject(
    object
) {

    const centerX =
        object.x +
        object.w / 2;


    const centerY =
        object.y +
        object.h / 2;


    return Math.hypot(
        playerX - centerX,
        playerY - centerY
    );

}


/* =====================================================
   INTERACTION CHECK
   ===================================================== */

function checkInteraction() {

    nearby =
        null;


    let closest =
        Infinity;


    interactables.forEach(
        function (object) {

            const distance =
                distanceToObject(
                    object
                );


            if (
                distance < 12 &&
                distance < closest
            ) {

                nearby =
                    object;


                closest =
                    distance;

            }

        }
    );


    if (
        nearby &&
        !computerOpen &&
        !inventoryOpen &&
        !helpOpen &&
        !cardOpen
    ) {

        interactionMessage.textContent =
            "E  //  " +
            nearby.name;


        interactionMessage.classList.add(
            "visible"
        );

    }

    else {

        interactionMessage.classList.remove(
            "visible"
        );

    }

}


/* =====================================================
   INACCESSIBLE
   ===================================================== */

function inaccessible() {

    status.textContent =
        "SYSTEM // 접근할 수 없는 과정입니다.";

}


/* =====================================================
   MOVEMENT
   ===================================================== */

function updateMovement() {

    if (
        paused ||
        inventoryOpen ||
        helpOpen ||
        computerOpen ||
        cardOpen
    ) {

        return;

    }


    let dx =
        0;


    let dy =
        0;


    if (keys.w) {

        dy -= 1;

    }


    if (keys.s) {

        dy += 1;

    }


    if (keys.a) {

        dx -= 1;

    }


    if (keys.d) {

        dx += 1;

    }


    if (
        dx === 0 &&
        dy === 0
    ) {

        return;

    }


    const length =
        Math.hypot(
            dx,
            dy
        );


    dx =
        dx /
        length *
        moveSpeed;


    dy =
        dy /
        length *
        moveSpeed;


    /*
     * X/Y를 따로 검사해서
     * 벽이나 물체에 비스듬히 끼지 않도록 함
     */

    if (
        !blocked(
            playerX + dx,
            playerY
        )
    ) {

        playerX +=
            dx;

    }


    if (
        !blocked(
            playerX,
            playerY + dy
        )
    ) {

        playerY +=
            dy;

    }


    player.style.left =
        playerX + "%";


    player.style.top =
        playerY + "%";


    /*
     * 첫 이동
     */

    if (
        tutorialStep === 0
    ) {

        tutorialStep =
            1;


        typeEcho(1);


        status.textContent =
            "TUTORIAL // MOVEMENT ENABLED";

    }


    checkInteraction();

}


/* =====================================================
   COMPUTER
   ===================================================== */

function openComputer() {

    if (
        tutorialStep !== 2
    ) {

        inaccessible();

        return;

    }


    computerOpen =
        true;


    clearKeys();


    interactionMessage.classList.remove(
        "visible"
    );


    accessNumber.textContent =
        ACCESS_CODE;


    computerOverlay.style.display =
        "flex";


    codeInput.value =
        "";


    codeError.textContent =
        "";


    setTimeout(
        function () {

            codeInput.focus();

        },
        50
    );

}


function closeComputer() {

    computerOpen =
        false;


    computerOverlay.style.display =
        "none";


    codeInput.blur();


    root.focus();

}


/* =====================================================
   CODE
   ===================================================== */

function submitCode() {

    const entered =
        codeInput.value.trim();


    if (
        entered ===
        ACCESS_CODE
    ) {

        closeComputer();


        /*
         * 암호 입력 성공 즉시
         * 책상 위에 ACCESS KEY 생성
         */

        accessKey.classList.add(
            "visible"
        );


        tutorialStep =
            3;


        typeEcho(4);


        status.textContent =
            "ECHO TERMINAL // CODE VERIFIED // ACCESS KEY GENERATED";

    }

    else {

        codeError.textContent =
            "ACCESS DENIED // 화면의 4자리 숫자를 입력하십시오.";

    }

}


codeButton.addEventListener(
    "click",
    submitCode
);


codeInput.addEventListener(
    "input",
    function () {

        codeInput.value =
            codeInput.value
                .replace(
                    /\D/g,
                    ""
                )
                .slice(
                    0,
                    4
                );

    }
);


codeInput.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key ===
            "Enter"
        ) {

            event.preventDefault();

            submitCode();

        }


        if (
            event.key ===
            "Escape"
        ) {

            event.preventDefault();

            closeComputer();

        }

    }
);


/* =====================================================
   INTERACTION
   ===================================================== */

function interact() {

    if (
        paused ||
        computerOpen ||
        inventoryOpen ||
        helpOpen ||
        cardOpen
    ) {

        return;

    }


    if (!nearby) {

        return;

    }


    /*
     * 이동 전
     */

    if (
        tutorialStep === 0
    ) {

        inaccessible();

        return;

    }


    /*
     * COMPUTER
     */

    if (
        tutorialStep === 1
    ) {

        if (
            nearby.id !==
            "computer"
        ) {

            inaccessible();

            return;

        }


        tutorialStep =
            2;


        typeEcho(3);


        status.textContent =
            "ECHO SYSTEM // TERMINAL CONNECTED";


        openComputer();


        return;

    }


    /*
     * COMPUTER CODE 단계
     */

    if (
        tutorialStep === 2
    ) {

        if (
            nearby.id !==
            "computer"
        ) {

            inaccessible();

            return;

        }


        openComputer();

        return;

    }


    /*
     * ACCESS KEY
     */

    if (
        tutorialStep === 3
    ) {

        if (
            nearby.id !==
            "desk"
        ) {

            inaccessible();

            return;

        }


        if (
            !accessKey.classList.contains(
                "visible"
            )
        ) {

            inaccessible();

            return;

        }


        accessKey.classList.remove(
            "visible"
        );


        inventory[0] = {

            name:
                "ACCESS KEY",

            description:
                "ECHO TERMINAL에서 인증된 보안구역 접근 키입니다."

        };


        keyCollected =
            true;


        tutorialStep =
            5;


        renderInventory();


        typeEcho(5);


        status.textContent =
            "SYSTEM // ACCESS KEY ACQUIRED";


        return;

    }


    /*
     * EXIT
     */

    if (
        tutorialStep === 5
    ) {

        if (
            nearby.id !==
            "exit"
        ) {

            inaccessible();

            return;

        }


        if (
            !keyCollected
        ) {

            inaccessible();

            return;

        }


        openCardAccess();

    }

}


/* =====================================================
   INVENTORY
   ===================================================== */

function openInventory() {

    if (
        paused ||
        computerOpen ||
        cardOpen
    ) {

        return;

    }


    helpOpen =
        false;


    helpOverlay.style.display =
        "none";


    inventoryOpen =
        true;


    inventoryOverlay.style.display =
        "flex";


    clearKeys();


    renderInventory();

}


function closeInventory() {

    inventoryOpen =
        false;


    inventoryOverlay.style.display =
        "none";


    root.focus();

}


inventorySlots.forEach(
    function (slot) {

        slot.addEventListener(
            "click",
            function () {

                inventorySlots.forEach(
                    function (other) {

                        other.classList.remove(
                            "selected"
                        );

                    }
                );


                slot.classList.add(
                    "selected"
                );


                const item =
                    inventory[
                        Number(
                            slot.dataset.slot
                        )
                    ];


                if (item) {

                    itemDescription.innerHTML =
                        item.name +
                        "<br><br>" +
                        item.description;

                }

                else {

                    itemDescription.innerHTML =
                        "ITEM DESCRIPTION<br><br>비어 있는 슬롯입니다.";

                }

            }
        );

    }
);


/* =====================================================
   HELP
   ===================================================== */

function openHelp() {

    if (
        paused ||
        computerOpen ||
        cardOpen
    ) {

        return;

    }


    inventoryOpen =
        false;


    inventoryOverlay.style.display =
        "none";


    helpOpen =
        true;


    helpOverlay.style.display =
        "flex";


    clearKeys();

}


function closeHelp() {

    helpOpen =
        false;


    helpOverlay.style.display =
        "none";


    root.focus();

}


/* =====================================================
   KEYBOARD
   ===================================================== */

document.addEventListener(
    "keydown",
    function (event) {

        /*
         * 암호 입력 중
         */

        if (
            document.activeElement ===
            codeInput
        ) {

            return;

        }


        /*
         * SPACE
         */

        if (
            event.code ===
            "Space"
        ) {

            event.preventDefault();


            if (
                !paused &&
                !computerOpen &&
                !cardOpen &&
                !inventoryOpen &&
                !helpOpen
            ) {

                nextEcho();

            }


            return;

        }


        const key =
            event.key.toLowerCase();


        /*
         * ESC
         */

        if (
            key ===
            "escape"
        ) {

            if (
                computerOpen
            ) {

                closeComputer();

                return;

            }


            if (
                cardOpen
            ) {

                closeCardAccess();

                return;

            }


            if (
                helpOpen
            ) {

                closeHelp();

                return;

            }


            if (
                inventoryOpen
            ) {

                closeInventory();

                return;

            }

        }


        /*
         * E
         */

        if (
            key ===
            "e"
        ) {

            event.preventDefault();

            interact();

            return;

        }


        /*
         * H
         */

        if (
            key ===
            "h"
        ) {

            event.preventDefault();


            if (helpOpen) {

                closeHelp();

            }

            else {

                openHelp();

            }


            return;

        }


        /*
         * I
         */

        if (
            key ===
            "i"
        ) {

            event.preventDefault();


            if (inventoryOpen) {

                closeInventory();

            }

            else {

                openInventory();

            }


            return;

        }


        /*
         * WASD
         */

        if (
            key === "w" ||
            key === "a" ||
            key === "s" ||
            key === "d"
        ) {

            if (
                !paused &&
                !computerOpen &&
                !cardOpen &&
                !helpOpen &&
                !inventoryOpen
            ) {

                keys[key] =
                    true;

                event.preventDefault();

            }

        }

    }
);


/* =====================================================
   KEYBOARD RELEASE
   ===================================================== */

document.addEventListener(
    "keyup",
    function (event) {

        const key =
            event.key.toLowerCase();


        if (
            key === "w" ||
            key === "a" ||
            key === "s" ||
            key === "d"
        ) {

            keys[key] =
                false;


            event.preventDefault();

        }

    }
);


/* =====================================================
   MOBILE CONTROLS
   ===================================================== */

document
    .querySelectorAll(
        ".control-button"
    )
    .forEach(
        function (button) {

            const direction =
                button.dataset.direction;


            function press(
                event
            ) {

                event.preventDefault();


                if (
                    !paused &&
                    !computerOpen &&
                    !cardOpen &&
                    !helpOpen &&
                    !inventoryOpen
                ) {

                    keys[direction] =
                        true;


                    try {

                        button.setPointerCapture(
                            event.pointerId
                        );

                    }

                    catch (error) {}

                }

            }


            function release(
                event
            ) {

                event.preventDefault();

                keys[direction] =
                    false;

            }


            button.addEventListener(
                "pointerdown",
                press
            );


            button.addEventListener(
                "pointerup",
                release
            );


            button.addEventListener(
                "pointercancel",
                release
            );


            button.addEventListener(
                "lostpointercapture",
                release
            );

        }
    );


/* =====================================================
   CARD ACCESS
   ===================================================== */

function openCardAccess() {

    if (
        !keyCollected
    ) {

        inaccessible();

        return;

    }


    cardOpen =
        true;


    clearKeys();


    interactionMessage.classList.remove(
        "visible"
    );


    cardOverlay.style.display =
        "flex";


    resetCard();

}


function closeCardAccess() {

    cardOpen =
        false;


    cardOverlay.style.display =
        "none";


    resetCard();


    root.focus();

}


function resetCard() {

    dragCard.style.left =
        "12%";


    dragCard.style.top =
        "50%";


    dragCard.style.transform =
        "translateY(-50%)";


    cardDragging =
        false;


    cardStatus.textContent =
        "카드를 리더기까지 끌어다 놓으십시오.";

}


function getCardStagePoint(
    event
) {

    const rect =
        cardStage.getBoundingClientRect();


    return {

        x:
            event.clientX -
            rect.left,

        y:
            event.clientY -
            rect.top

    };

}


function startCardDrag(
    event
) {

    if (
        !cardOpen
    ) {

        return;

    }


    event.preventDefault();


    const rect =
        dragCard.getBoundingClientRect();


    cardOffsetX =
        event.clientX -
        rect.left;


    cardOffsetY =
        event.clientY -
        rect.top;


    cardDragging =
        true;


    try {

        dragCard.setPointerCapture(
            event.pointerId
        );

    }

    catch (error) {}

}


function dragCardMove(
    event
) {

    if (
        !cardDragging
    ) {

        return;

    }


    event.preventDefault();


    const point =
        getCardStagePoint(
            event
        );


    const stage =
        cardStage.getBoundingClientRect();


    let x =
        point.x -
        cardOffsetX;


    let y =
        point.y -
        cardOffsetY;


    x =
        Math.max(
            0,
            Math.min(
                stage.width -
                dragCard.offsetWidth,
                x
            )
        );


    y =
        Math.max(
            0,
            Math.min(
                stage.height -
                dragCard.offsetHeight,
                y
            )
        );


    dragCard.style.left =
        x + "px";


    dragCard.style.top =
        y + "px";


    dragCard.style.transform =
        "none";

}


function finishCardDrag(
    event
) {

    if (
        !cardDragging
    ) {

        return;

    }


    cardDragging =
        false;


    const cardRect =
        dragCard.getBoundingClientRect();


    const reader =
        document.querySelector(
            ".reader"
        );


    const readerRect =
        reader.getBoundingClientRect();


    const correctPosition =
        cardRect.right >
        readerRect.left + 25 &&

        cardRect.left <
        readerRect.right - 25 &&

        cardRect.bottom >
        readerRect.top + 18 &&

        cardRect.top <
        readerRect.bottom - 18;


    if (
        correctPosition
    ) {

        dragCard.style.left =
            "72%";


        dragCard.style.top =
            "50%";


        cardStatus.textContent =
            "SECURITY ACCESS // VERIFIED";


        status.textContent =
            "SECURITY ROOM // ACCESS GRANTED";


        setTimeout(
            function () {

                closeCardAccess();

            },
            650
        );

    }

    else {

        cardStatus.textContent =
            "CARD NOT DETECTED // READER에 정확히 맞춰주세요.";

    }

}


dragCard.addEventListener(
    "pointerdown",
    startCardDrag
);


dragCard.addEventListener(
    "pointermove",
    dragCardMove
);


dragCard.addEventListener(
    "pointerup",
    finishCardDrag
);


dragCard.addEventListener(
    "pointercancel",
    finishCardDrag
);


/* =====================================================
   RESTART / TITLE
   ===================================================== */

function parentAction(
    action
) {

    let target =
        null;


    /*
     * iframe에서 부모 Streamlit 주소를
     * 읽을 수 있는 경우 사용
     */

    try {

        if (
            document.referrer
        ) {

            target =
                new URL(
                    document.referrer
                );


            target.searchParams.set(
                "action",
                action
            );

        }

    }

    catch (error) {

        target =
            null;

    }


    if (target) {

        window.top.location.href =
            target.toString();

    }

    else {

        window.parent.location.href =
            "?action=" +
            encodeURIComponent(
                action
            );

    }

}


document
    .getElementById(
        "restartButton"
    )
    .addEventListener(
        "click",
        function () {

            parentAction(
                "restart"
            );

        }
    );


document
    .getElementById(
        "titleButton"
    )
    .addEventListener(
        "click",
        function () {

            parentAction(
                "title"
            );

        }
    );


/* =====================================================
   FOCUS
   ===================================================== */

function focusGame() {

    try {

        root.focus(
            {
                preventScroll:
                    true
            }
        );

    }

    catch (error) {

        root.focus();

    }

}


root.addEventListener(
    "pointerdown",
    function () {

        if (
            !computerOpen &&
            !cardOpen
        ) {

            focusGame();

        }

    }
);


window.addEventListener(
    "blur",
    clearKeys
);


/* =====================================================
   PAUSE INITIAL STATE
   ===================================================== */

if (paused) {

    pauseOverlay.style.display =
        "flex";

}


/* =====================================================
   GAME LOOP
   ===================================================== */

function gameLoop() {

    updateMovement();

    requestAnimationFrame(
        gameLoop
    );

}


player.style.left =
    playerX + "%";


player.style.top =
    playerY + "%";


checkInteraction();

focusGame();

gameLoop();


})();

</script>


</body>

</html>
"""


# =========================================================
# SAFE PLACEHOLDER REPLACEMENT
# =========================================================

html = html.replace(
    "__FONT_BASE64__",
    font_base64,
)


html = html.replace(
    "__PAUSED__",
    "true"
    if paused
    else "false",
)


# =========================================================
# RENDER
# =========================================================

components.html(
    html,
    height=1000,
    scrolling=False,
)
