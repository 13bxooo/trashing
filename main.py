import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PROJECT : ECHO",
    page_icon="◈",
    layout="wide"
)

game_html = """
<!DOCTYPE html>
<html>
<head>

<style>

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #111820;
}

.game {
    position: relative;

    width: 100vw;
    height: 100vh;

    background:
        repeating-linear-gradient(
            0deg,
            #182631 0px,
            #182631 39px,
            #1c2c38 40px
        );

    font-family: monospace;
}


/* =========================
   PROJECT : ECHO
   ========================= */

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


/* =========================
   TIMER
   ========================= */

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


/* =========================
   ROOM
   ========================= */

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


/* =========================
   ECHO
   ========================= */

.echo {

    position: absolute;

    top: 20%;
    left: 50%;

    transform: translateX(-50%);

    color: #9db3c4;

    font-size: 14px;

    letter-spacing: 6px;
}


/* =========================
   CENTER
   ========================= */

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


/* =========================
   MESSAGE
   ========================= */

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

</style>

</head>


<body>

<div class="game">

    <!-- 제목 -->

    <div class="title">
        ☰ PROJECT : ECHO
    </div>


    <!-- 타이머 -->

    <div class="timer">
        TIME&nbsp;&nbsp;59:59
    </div>


    <!-- 게임 방 -->

    <div class="room">

        <div class="echo">
            E C H O
        </div>


        <div class="room-center">

            RESEARCH FACILITY
            <br>
            CONTROL ROOM

        </div>

    </div>


    <!-- 시스템 메시지 -->

    <div class="message">

        <div class="message-label">
            SYSTEM
        </div>


        <div class="message-text">

            시스템이 초기화되었습니다.
            <br>

            <b>ECHO</b> 연결을 확인하고 있습니다...

        </div>

    </div>

</div>

</body>
</html>
"""


components.html(
    game_html,
    height=800,
    scrolling=False
)
