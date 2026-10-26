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

    st.query_params.clear()
    for _key in list(st.session_state.keys()):
        if _key.startswith(("s1_", "tutorial_", "stage01_")):
            del st.session_state[_key]
    st.session_state.tutorial_reset_save = True
    st.session_state.game_started = True
    st.session_state.game_paused = False
    st.session_state.game_finished = False
    st.session_state.tutorial_complete = False
    st.session_state.stage01_started = False
    st.session_state.remaining_seconds = 15 * 60
    st.switch_page("pages/2_Game.py")


elif action == "title":

    st.session_state.game_paused = False
    st.session_state.show_title_warning = True
    st.query_params.clear()
    st.switch_page("main.py")

elif action == "stage01":

    st.session_state.game_paused = False
    st.session_state.game_started = True
    st.session_state.stage01_started = True
    st.session_state.start_open = False
    st.query_params.clear()
    st.switch_page("pages/3_Stage_01.py")


# =========================================================
# SESSION STATE
# =========================================================

if "game_paused" not in st.session_state:

    st.session_state.game_paused = False

# The tutorial page represents an active run, so CONTINUE can return here.
st.session_state.game_started = True


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


/* In-game pause control and pixel-art UI styling */
.pixel-frame{{
    border:1px solid #54dfff!important;
    box-shadow:0 0 0 1px #123c4d, inset 0 0 0 1px #061923!important;
    border-radius:0!important;
    position:relative;
}}
.pixel-frame:before,.pixel-frame:after{{content:"";position:absolute;width:12px;height:12px;pointer-events:none;border-color:#8af0ff;border-style:solid}}
.pixel-frame:before{{top:-2px;left:-2px;border-width:2px 0 0 2px}}
.pixel-frame:after{{right:-2px;bottom:-2px;border-width:0 2px 2px 0}}
.inventory-panel,.item-description,.help-panel,.computer-panel,.pause-overlay>div,.item-acquired-notice,.item-acquired-dialog,.tutorial-transition-card{{border-style:solid!important;border-radius:0!important}}
.inventory-header,.help-header{{border-bottom:1px solid #2587a7!important}}
.inventory-panel{{background:#02070c!important;color:#d9faff!important;border:1px solid #48dfff!important;box-shadow:0 0 0 1px #123c4d!important}}
.inventory-header{{border-bottom:1px solid #2587a7!important}}
.inventory-title{{color:#8defff!important;text-shadow:0 0 5px #00cfff55!important}}
.inventory-close{{color:#8defff!important}}
.inventory-slot{{background:#02070c!important;color:#d9faff!important;border:1px solid #24576a!important;box-shadow:inset 0 0 0 1px #061923!important}}
.inventory-slot:hover,.inventory-slot.selected{{background:#06202b!important;color:#fff!important;border-color:#62e8ff!important;box-shadow:0 0 0 1px #1b8198!important}}
.slot-number{{color:#70e7ff!important}}
.item-name{{color:#d9faff!important}}
.empty-text{{display:none!important}}
.item-description{{background:#02070c!important;color:#d9faff!important;border:1px solid #48dfff!important;box-shadow:0 0 0 1px #123c4d!important}}
.item-description strong{{color:#8defff!important}}
.pixel-card-item{{background:#f4fcff!important;border:2px solid #008eaf!important;box-shadow:2px 0 #005a70,-2px 0 #005a70,0 2px #005a70,0 -2px #005a70,0 0 0 2px #d6faff!important}}
.access-card-image{{display:block;width:100%;height:100%;object-fit:contain;image-rendering:pixelated}}
.inventory-slot .access-card-image{{width:86%;height:78%;max-width:100px;max-height:100px}}
.pixel-card-chip{{background:#00bcd7!important;border:1px solid #004b5a!important}}
.pixel-card-mark{{color:#006b80!important}}
.pixel-card-lines{{border-color:#008eaf!important}}

/* Inventory and card keep the dark cyan pixel-art palette. */
.inventory-panel:before,.pause-menu-panel:before,.item-acquired-dialog:before,.tutorial-transition-card:before{{content:"";position:absolute;left:-2px;top:-2px;width:12px;height:12px;border-left:2px solid #8af0ff;border-top:2px solid #8af0ff;pointer-events:none}}
.inventory-panel:after,.pause-menu-panel:after,.item-acquired-dialog:after,.tutorial-transition-card:after{{content:"";position:absolute;right:-2px;bottom:-2px;width:12px;height:12px;border-right:2px solid #8af0ff;border-bottom:2px solid #8af0ff;pointer-events:none}}
</style>
""",
    unsafe_allow_html=True,
)


# Pause state is handled inside the game iframe so RESUME never reloads Streamlit.
paused = st.session_state.game_paused

# =========================================================
# GAME HTML
# =========================================================

html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">


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

    position: absolute;
    top: 24px;
    left: 28px;
    font-size: 18px;
    letter-spacing: 1px;
    z-index: 20;
    color: #f4f4f4;
    text-shadow: none;

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
    position: relative;
    width: min(820px, 88vw);
    padding: 24px 26px 26px;
    background: #02070c;
    color: #d8faff;
    border: 1px solid #48dfff;
    box-shadow: 0 0 0 1px #123c4d, 0 0 16px #00cfff22;
}


.inventory-header {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    min-height: 28px;
    padding: 0 0 8px 8px;
    margin: 0 0 14px;
    border-bottom: 1px solid #2587a7;
}


.inventory-title {
    color: #72eaff;
    font-size: 17px;
    letter-spacing: 1px;
    text-shadow: 0 0 5px #00cfff77;
}


.inventory-close {
    margin-left: auto;
    color: #4b8da0;
    font-size: 9px;
}


.inventory-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    grid-template-rows: repeat(3, minmax(0, 1fr));
    gap: 10px;
}


.inventory-slot {
    position: relative;
    aspect-ratio: 1 / 1;
    background: #01060b;
    border: 1px solid #28546a;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: inset 0 0 0 1px #06131d;
    color: #baf6ff;
}


.inventory-slot:hover,
.inventory-slot.selected {
    background: #03121b;
    color: #d8faff;
    border-color: #7cecff;
    box-shadow: 0 0 0 1px #1683a4, 0 0 9px #00cfff33;
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


/* Pixel-art access card shared by the draggable reader item and inventory icon */
.pixel-card-item{position:relative;width:42px;height:28px;margin:7px auto 5px;background:#073b58;border:2px solid #54eaff;box-shadow:2px 0 #bafaff,-2px 0 #bafaff,0 2px #bafaff,0 -2px #bafaff,0 0 8px #00dfff66;image-rendering:pixelated;transform:rotate(-8deg)}
.pixel-card-chip{position:absolute;left:5px;top:6px;width:8px;height:7px;background:#36e8ff;border:1px solid #b8fbff}
.pixel-card-mark{position:absolute;right:5px;top:2px;color:#9af7ff;font:bold 12px monospace}
.pixel-card-lines{position:absolute;left:5px;right:5px;bottom:4px;height:3px;border-top:1px solid #55eaff;border-bottom:1px solid #55eaff}
.card{background:#073b58!important;border:2px solid #54eaff!important;box-shadow:2px 0 #bafaff,-2px 0 #bafaff,0 2px #bafaff,0 -2px #bafaff,0 0 12px #00dfff66!important;image-rendering:pixelated!important}
.card-chip{background:#36e8ff!important;border:1px solid #b8fbff!important}
.card:after{content:"A";position:absolute;right:12px;top:12px;color:#9af7ff;font:bold 20px monospace;text-shadow:0 0 5px #00dfff}

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


.reader-light {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #ff3333;
    box-shadow: 0 0 8px #ff3333;
}
.reader-light.green {
    background: #36ff76;
    box-shadow: 0 0 12px #36ff76;
}
.fade-screen {
    position: absolute;
    inset: 0;
    z-index: 300;
    background: #000;
    opacity: 0;
    pointer-events: none;
    transition: opacity 1.5s linear;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.fade-screen.active { opacity: 1; pointer-events: auto; }
.fade-message {
    color: #e8e8e8;
    font-family: 'NeoDungGeunMo', monospace;
    letter-spacing: 3px;
    text-align: center;
    padding: 0 18px;
    opacity: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    text-shadow: none;
}
.fade-stage {
    font-size: clamp(22px, 3vw, 34px);
    text-shadow: 0 0 4px #fff, 0 0 12px #777;
}
.fade-room {
    font-size: clamp(12px, 1.4vw, 17px);
    letter-spacing: 2px;
    text-shadow: none;
}
.fade-screen.active .fade-message {
    opacity: 1;
}
.fade-screen.active .fade-stage {
    animation: blackoutText 1.5s steps(1, end) forwards;
}
@keyframes blackoutText {
    0% { opacity: 0; }
    18% { opacity: .95; }
    24% { opacity: .2; }
    31% { opacity: 1; }
    42% { opacity: .45; }
    50%, 100% { opacity: 1; }
}
@media (prefers-reduced-motion: reduce) {
    .fade-screen { transition: none; }
    .fade-screen.active .fade-message, .fade-screen.active .fade-stage { animation: none; opacity: 1; }
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

    visibility: hidden;
    pointer-events: none;

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



/* Pixel-art frame: crisp solid lines with stepped corner accents, not dotted lines. */
.inventory-panel,.item-description,.help-panel,.computer-panel,.pause-overlay>div,.item-acquired-notice,.item-acquired-dialog,.tutorial-transition-card{border-style:solid!important;border-radius:0!important}
.inventory-panel,.inventory-slot,.item-description,.help-panel,.computer-panel,.pause-overlay>div,.item-acquired-notice,.item-acquired-dialog,.tutorial-transition-card{image-rendering:pixelated}
.inventory-panel:before,.pause-menu-panel:before,.item-acquired-dialog:before,.tutorial-transition-card:before{content:"";position:absolute;left:-2px;top:-2px;width:12px;height:12px;border-left:2px solid #8af0ff;border-top:2px solid #8af0ff;pointer-events:none}
.inventory-panel:after,.pause-menu-panel:after,.item-acquired-dialog:after,.tutorial-transition-card:after{content:"";position:absolute;right:-2px;bottom:-2px;width:12px;height:12px;border-right:2px solid #8af0ff;border-bottom:2px solid #8af0ff;pointer-events:none}

/* Pixel-art pause button replaces the old Streamlit button completely. */
.pause-toggle{position:absolute;top:20px;right:24px;z-index:1000;width:42px;height:42px;display:flex;align-items:center;justify-content:center;background:#02070c;border:1px solid #54dfff;color:#8defff;font:20px NeoDungGeunMo,monospace;cursor:pointer;box-shadow:0 0 0 1px #123c4d}
.pause-toggle:before,.pause-toggle:after{content:"";position:absolute;width:7px;height:7px;border-color:#8af0ff;border-style:solid}
.pause-toggle:before{left:-2px;top:-2px;border-width:2px 0 0 2px}.pause-toggle:after{right:-2px;bottom:-2px;border-width:0 2px 2px 0}
.pause-toggle:hover{background:#d9faff;color:#001018}
/* Reference-matched stage and item-acquired overlays */
.tutorial-transition{position:fixed;inset:0;z-index:1000000;display:none;align-items:center;justify-content:center;background:#000;opacity:1;transition:opacity .45s steps(6,end);pointer-events:auto}
.tutorial-transition.show{display:flex}.tutorial-transition.hide{opacity:0;pointer-events:none}
.tutorial-transition-card{position:relative;width:min(350px,78vw);min-height:145px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:1px solid #57dfff;color:#f5fbff;box-shadow:0 0 0 1px #143d4c,0 0 14px #00cfff22;letter-spacing:2px}
.tutorial-transition-card{animation:neonFault 1.15s steps(1,end) infinite;text-shadow:0 0 5px #fff,0 0 12px #00dfff;}
.tutorial-transition-card:before,.tutorial-transition-card:after{content:'';position:absolute;width:18px;height:18px;border-color:#78ecff;border-style:solid}
.tutorial-transition-card:before{top:-2px;left:-2px;border-width:2px 0 0 2px}.tutorial-transition-card:after{right:-2px;bottom:-2px;border-width:0 2px 2px 0}
.tutorial-transition-stage{font-size:clamp(25px,4vw,36px);line-height:1.6;text-shadow:0 0 5px #fff,0 0 14px #57dfff;animation:neonFault .9s steps(1,end) infinite}.tutorial-transition-room{font-size:clamp(14px,2vw,20px);color:#a8f2ff;letter-spacing:1px;animation:neonFault 1.4s steps(1,end) infinite}
@keyframes neonFault{0%,18%,22%,61%,65%,100%{opacity:1;filter:none}19%,21%,62%,64%{opacity:.28;filter:brightness(.45)}40%{opacity:.78}41%{opacity:1}}
.help-panel{position:relative;background:#02070c!important;color:#d9faff!important;border:2px solid #48dfff!important;box-shadow:0 0 0 2px #123c4d,0 0 18px #00cfff22!important;image-rendering:pixelated}
.help-panel:before,.help-panel:after{content:"";position:absolute;width:14px;height:14px;border-color:#8af0ff;border-style:solid;pointer-events:none}.help-panel:before{left:-3px;top:-3px;border-width:3px 0 0 3px}.help-panel:after{right:-3px;bottom:-3px;border-width:0 3px 3px 0}
.help-row{border-bottom:1px solid #17495b!important}
.help-number,.help-key{border:1px solid #2587a7!important;background:#04121a!important;color:#8defff!important}
.help-title{color:#8defff!important;text-shadow:0 0 7px #00cfff66!important}
.item-acquired-notice{position:fixed;left:50%;bottom:5%;transform:translateX(-50%);z-index:500;display:none;grid-template-columns:minmax(120px,.78fr) minmax(240px,1.45fr);gap:14px;width:min(720px,92vw);padding:14px;background:#02070c;border:1px solid #48dfff;box-shadow:0 0 0 1px #123c4d,0 0 16px #00cfff22;cursor:pointer}
.item-acquired-notice.show{display:grid}.item-acquired-art{display:flex;align-items:center;justify-content:center;min-height:120px;position:relative}
.item-acquired-art .pixel-card-item{width:94px;height:62px;transform:rotate(-10deg) scale(1.05);margin:0;box-shadow:3px 0 #bafaff,-3px 0 #bafaff,0 3px #bafaff,0 -3px #bafaff,0 0 16px #00dfff88}
.item-acquired-dialog{border:1px solid #2587a7;padding:12px 14px;min-height:120px;position:relative}.item-acquired-tag{display:inline-block;background:#087aa1;color:#e8fbff;padding:4px 10px;font-size:12px;margin-bottom:10px}
.item-acquired-text{font-size:clamp(12px,1.5vw,16px);line-height:1.8;color:#d9faff;white-space:pre-line}.item-acquired-close{position:absolute;right:10px;bottom:8px;color:#54dfff;font-size:9px}
@media(max-width:560px){.item-acquired-notice{grid-template-columns:88px minmax(0,1fr);gap:8px;padding:9px}.item-acquired-art{min-height:105px}.item-acquired-art .access-card-image{width:88px;height:85px}.item-acquired-dialog{padding:9px;min-height:105px}.item-acquired-text{font-size:11px}}


.pause-overlay{background:rgba(0,0,0,.72)}
.pause-overlay>div{position:relative;width:min(390px,86vw);padding:34px 34px;background:#02070c;border:1px solid #54dfff;box-shadow:0 0 0 1px #123c4d,0 0 18px #00cfff22}
.pause-title,.pause-sub{display:none}
.pause-actions{visibility:visible;pointer-events:auto;margin:0;display:flex;flex-direction:column;gap:16px;align-items:stretch}
.pause-actions .pause-row{display:flex;align-items:center;gap:12px;width:100%}
.pause-actions .pause-icon{width:28px;height:28px;flex:0 0 28px;display:inline-flex;align-items:center;justify-content:center;border:1px solid #58dfff;border-radius:50%;color:#82eaff;font-size:10px}
.pause-actions .pause-nav-link,.pause-actions .pause-menu-button{flex:1;display:flex;align-items:center;min-height:32px;padding:4px 0;border:0!important;background:transparent!important;color:#d8faff!important;font-size:17px;text-decoration:none;text-align:left;cursor:pointer}
.pause-actions .pause-nav-link:hover,.pause-actions .pause-menu-button:hover{color:#fff!important;text-shadow:0 0 6px #54dfff}

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

<button class="pause-toggle" id="pauseToggle" type="button" aria-label="Pause game">Ⅱ</button>

<div class="project-title">
    PROJECT : LOGIC
</div>


<div class="stage-title">
    STAGE 00 // TUTORIAL
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

<div class="inventory-slot" data-slot="8"></div>
<div class="inventory-slot" data-slot="9"></div>
<div class="inventory-slot" data-slot="10"></div>
<div class="inventory-slot" data-slot="11"></div>

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


<div class="reader" id="cardReader">

    <div class="reader-light" id="readerLight"></div>
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

<div class="item-acquired-notice" id="itemAcquiredNotice" role="button" tabindex="0" aria-label="아이템 획득 알림을 닫으려면 클릭"><div class="item-acquired-art"><img class="access-card-image" src="data:image/png;base64,__CARD_IMAGE_BASE64__" alt="Access card"></div><div class="item-acquired-dialog"><div class="item-acquired-tag">ECHO</div><div class="item-acquired-text">카드가 인벤토리에 추가되었습니다.
이 카드는 특정 장비를 작동시키거나 인증할 때 사용됩니다.</div><div class="item-acquired-close">CLICK TO CLOSE</div></div></div>
<div class="tutorial-transition" id="tutorialTransition" aria-hidden="true"><div class="tutorial-transition-card"><div class="tutorial-transition-stage">STAGE 00</div><div class="tutorial-transition-room">:TUTORIAL</div></div></div>
<div class="pause-overlay" id="pauseOverlay"><div class="pause-menu-panel"><div class="pause-actions"><div class="pause-row"><span class="pause-icon">Ⅱ</span><button class="pause-nav-link pause-menu-button" id="resumeButton" type="button">RESUME</button></div><div class="pause-row"><span class="pause-icon">↻</span><a class="pause-nav-link" id="restartButton" href="?action=restart" target="_top" rel="noopener">RESTART</a></div><div class="pause-row"><span class="pause-icon">⌂</span><a class="pause-nav-link" id="titleButton" href="?action=title" target="_top" rel="noopener">TITLE</a></div></div></div></div>

<div
    class="status"
    id="status"
>
    ECHO SYSTEM // ONLINE
</div>


</div>

<div class="fade-screen" id="fadeScreen" aria-hidden="true"><div class="fade-message" id="fadeMessage"><span class="fade-stage">STAGE 01</span><span class="fade-room">:ARCHIVE ACCESS</span></div></div>

<script>

(function () {

"use strict";


/* =====================================================
   GAME STATE
   ===================================================== */

let paused =
    __PAUSED__;


/*
 * 방이 시작될 때마다 새로운 4자리 암호 생성
 */

let ACCESS_CODE =
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

let cardConsumed = false;


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

const readerLight = document.getElementById("readerLight");
const fadeScreen = document.getElementById("fadeScreen");


const pauseOverlay =
    document.getElementById(
        "pauseOverlay"
    );

const pauseToggle = document.getElementById("pauseToggle");
const resumeButton = document.getElementById("resumeButton");

function setPaused(nextPaused) {
    paused = nextPaused;
    pauseOverlay.style.display = paused ? "flex" : "none";
    pauseToggle.textContent = paused ? "▶" : "Ⅱ";
    pauseToggle.setAttribute("aria-label", paused ? "Resume game" : "Pause game");
    clearKeys();
    if (!paused) focusGame();
}

pauseToggle.addEventListener("click", function (event) {
    event.preventDefault();
    event.stopPropagation();
    setPaused(!paused);
});

resumeButton.addEventListener("click", function (event) {
    event.preventDefault();
    event.stopPropagation();
    setPaused(false);
});


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
                    <div class="slot-number">${String(index + 1).padStart(2, "0")}</div>
                    ${item.name === "ACCESS KEY" ? '<img class="access-card-image" src="data:image/png;base64,__CARD_IMAGE_BASE64__" alt="Access card">' : '<div class="item-name">' + item.name + '</div>'}
                    `;

            }

            else {

                slot.innerHTML =
                    `
                    <div class="slot-number">
                        ${String(index + 1).padStart(2, "0")}
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
            saveTutorialState();

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
    // 첫 SPACE는 타이핑을 완료하고, 두 번째 SPACE는 첫 이동 안내를 연다.
    if (!typingDone) {
        clearTimeout(typingTimer);
        echoMessage.textContent = messages[echoIndex] || "";
        typingDone = true;
        echoNext.classList.add("ready");
        saveTutorialState();
        return;
    }

    if (echoIndex === 0 && tutorialStep === 0) {
        typeEcho(1);
        status.textContent = "TUTORIAL // W A S D TO MOVE";
        saveTutorialState();
        return;
    }

    // 이후 대사는 이동·조사 등 실제 행동을 완료했을 때만 바뀐다.
    status.textContent = "ECHO SYSTEM // 안내된 행동을 먼저 완료하십시오.";
    saveTutorialState();
}

const TUTORIAL_SAVE_KEY = "project_logic_tutorial_save_v3";
if (__RESET_TUTORIAL_SAVE__) { try { localStorage.removeItem(TUTORIAL_SAVE_KEY); } catch (e) {} }
function saveTutorialState() {
    try {
        localStorage.setItem(TUTORIAL_SAVE_KEY, JSON.stringify({
            tutorialStep, echoIndex, echoText: echoMessage.textContent,
            typingDone, playerX, playerY, keyCollected, cardConsumed,
            accessCode: ACCESS_CODE,
            inventory: inventory.map(item => item ? {name: item.name, description: item.description} : null)
        }));
    } catch (e) {}
}
function restoreTutorialState() {
    try {
        const saved = JSON.parse(localStorage.getItem(TUTORIAL_SAVE_KEY) || "null");
        if (!saved) return false;
        if (Number.isFinite(saved.tutorialStep)) tutorialStep = saved.tutorialStep;
        if (Number.isFinite(saved.echoIndex)) echoIndex = Math.max(0, Math.min(messages.length - 1, saved.echoIndex));
        if (Number.isFinite(saved.playerX)) playerX = saved.playerX;
        if (Number.isFinite(saved.playerY)) playerY = saved.playerY;
        keyCollected = !!saved.keyCollected;
        cardConsumed = !!saved.cardConsumed;
        if (Array.isArray(saved.inventory)) {
            for (let i = 0; i < inventory.length; i++) {
                const item = saved.inventory[i];
                inventory[i] = item && typeof item.name === "string"
                    ? {name: item.name, description: typeof item.description === "string" ? item.description : ""}
                    : null;
            }
        } else if (keyCollected && inventory.length) {
            inventory[0] = {name: "ACCESS KEY", description: "ECHO TERMINAL에서 인증된 보안구역 접근 키입니다."};
        }
        if (typeof saved.accessCode === "string" && /^\d{4}$/.test(saved.accessCode)) ACCESS_CODE = saved.accessCode;
        player.style.left = playerX + "%";
        player.style.top = playerY + "%";
        echoMessage.textContent = typeof saved.echoText === "string" ? saved.echoText : (messages[echoIndex] || "");
        typingDone = true; // iframe 재생성 후에는 현재 문장을 보존하고 타이핑 완료 상태로 복구
        echoNext.classList.add("ready");
        renderInventory();
        if (keyCollected) {
            const keyNode = document.getElementById("accessKey");
            if (keyNode) keyNode.classList.remove("visible");
        }
        return true;
    } catch (e) { return false; }
}

const tutorialWasRestored = restoreTutorialState();
const tutorialTransition = document.getElementById("tutorialTransition");
if (!tutorialWasRestored && tutorialTransition) {
    tutorialTransition.classList.add("show");
    window.setTimeout(() => tutorialTransition.classList.add("hide"), 2700);
    window.setTimeout(() => tutorialTransition.remove(), 3150);
}
if (!tutorialWasRestored) typeEcho(0);
setInterval(saveTutorialState, 250);
window.addEventListener("beforeunload", saveTutorialState);
window.addEventListener("pagehide", saveTutorialState);
document.addEventListener("visibilitychange", function () { if (document.visibilityState === "hidden") saveTutorialState(); });


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


/* Short, bright two-note card-acquired chime (no external audio asset required). */
function playCardAcquireSound() {
    try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        const now = ctx.currentTime;
        [[880, 0], [1320, 0.105]].forEach(([frequency, offset]) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = "sine";
            osc.frequency.setValueAtTime(frequency, now + offset);
            gain.gain.setValueAtTime(0.0001, now + offset);
            gain.gain.exponentialRampToValueAtTime(0.18, now + offset + 0.012);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + offset + 0.24);
            osc.connect(gain); gain.connect(ctx.destination);
            osc.start(now + offset); osc.stop(now + offset + 0.25);
        });
        window.setTimeout(() => ctx.close().catch(() => {}), 500);
    } catch (e) {}
}

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
        const itemNotice = document.getElementById("itemAcquiredNotice");
        playCardAcquireSound();
        if (itemNotice) {
            let noticeDismissed = false;
            itemNotice.classList.add("show");
            const dismissItemNotice = () => {
                if (noticeDismissed) return;
                noticeDismissed = true;
                itemNotice.classList.remove("show");
                // ECHO speaks only after the acquisition notice has disappeared.
                window.setTimeout(() => typeEcho(5), 180);
            };
            itemNotice.onclick = dismissItemNotice;
            itemNotice.onkeydown = (event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); dismissItemNotice(); } };
            window.setTimeout(dismissItemNotice, 6500);
        } else {
            typeEcho(5);
        }


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
        !keyCollected || cardConsumed
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

        // 카드키는 일회용: 인벤토리에서 제거하고 리더기를 녹색으로 변경한다.
        inventory[0] = null;
        keyCollected = false;
        cardConsumed = true;
        renderInventory();
        if (readerLight) readerLight.classList.add("green");
        cardStatus.textContent = "ACCESS GRANTED // CARD CONSUMED";

        // 짧은 문 개방 효과음(Web Audio, 별도 파일 불필요)
        try {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            if (AudioContextClass) {
                const audio = new AudioContextClass();
                const now = audio.currentTime;
                [440, 660, 880].forEach((frequency, index) => {
                    const oscillator = audio.createOscillator();
                    const gain = audio.createGain();
                    oscillator.type = "square";
                    oscillator.frequency.value = frequency;
                    gain.gain.setValueAtTime(0.0001, now + index * 0.12);
                    gain.gain.exponentialRampToValueAtTime(0.08, now + index * 0.12 + 0.02);
                    gain.gain.exponentialRampToValueAtTime(0.0001, now + index * 0.12 + 0.18);
                    oscillator.connect(gain);
                    gain.connect(audio.destination);
                    oscillator.start(now + index * 0.12);
                    oscillator.stop(now + index * 0.12 + 0.2);
                });
                setTimeout(() => audio.close(), 900);
            }
        } catch (error) {}

        setTimeout(function () {
            closeCardAccess();
            clearTimeout(typingTimer);
            echoMessage.textContent = "이제 다음 스테이지로 넘어가도록 합시다.";
            typingDone = true;
            echoNext.classList.add("ready");
            setTimeout(function () {
                const fadeMessage = document.getElementById("fadeMessage");
                if (fadeMessage) fadeMessage.innerHTML = '<span class="fade-stage">STAGE 01</span><span class="fade-room">:ARCHIVE ACCESS</span>';
                if (fadeScreen) fadeScreen.classList.add("active");
                // Leave the black screen and flickering stage sign visible for 3 seconds.
                setTimeout(function () { parentAction("stage01"); }, 3000);
            }, 1000);
        }, 700);

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

function parentAction(action) {
    // components.html is sandboxed: top-level navigation can be rejected after a timer.
    // If same-origin access is available, update the Streamlit page URL and reload it;
    // the page's Python action handler then performs st.switch_page().
    try {
        const parentWindow = window.parent;
        const targetUrl = new URL(parentWindow.location.href);
        targetUrl.search = "";
        targetUrl.hash = "";
        targetUrl.searchParams.set("action", action);
        parentWindow.history.replaceState({}, "", targetUrl.toString());
        parentWindow.location.reload();
        return;
    } catch (error) {}

    // User-triggered pause actions are also real target=_top links, so this fallback
    // is only reached if the timed transition is blocked by the iframe sandbox.
    const statusNode = document.getElementById("status");
    if (statusNode) {
        statusNode.textContent = "NAVIGATION BLOCKED // browser sandbox prevented automatic transition.";
    }
}


// Route pause-menu navigation through the Streamlit page URL handler.
// This avoids broken relative links inside the embedded components.html frame.
const restartButton = document.getElementById("restartButton");
const titleButton = document.getElementById("titleButton");
if (restartButton) restartButton.addEventListener("click", function (event) { event.preventDefault(); event.stopPropagation(); parentAction("restart"); });
if (titleButton) titleButton.addEventListener("click", function (event) { event.preventDefault(); event.stopPropagation(); parentAction("title"); });


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

pauseToggle.textContent = paused ? "▶" : "Ⅱ";
if (paused) {
    pauseOverlay.style.display = "flex";
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
html = html.replace("__CARD_IMAGE_BASE64__", "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")


html = html.replace(
    "__PAUSED__",
    "true"
    if paused
    else "false",
)

html = html.replace("__RESET_TUTORIAL_SAVE__", "true" if st.session_state.pop("tutorial_reset_save", False) else "false")


# =========================================================
# RENDER
# =========================================================

components.html(
    html,
    height=1000,
    scrolling=False,
)

