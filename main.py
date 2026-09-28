import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PROJECT : LOGIC",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# QUERY ACTION
# =========================================================

action = st.query_params.get("action")

if action == "new_game":

    st.query_params.clear()

    st.switch_page("pages/1_Game.py")


elif action == "continue":

    st.query_params.clear()

    # -----------------------------------------
    # 아직 실제 저장 시스템이 없으므로
    # 현재는 저장 데이터가 없는 상태
    # -----------------------------------------

    st.warning(
        "이전 플레이 기록이 존재하지 않습니다. "
        "새 게임을 시작해주세요."
    )


elif action == "how_to_play":

    st.query_params.clear()

    st.switch_page("pages/2_How_to_Play.py")


# =========================================================
# STREAMLIT 기본 UI 제거
# =========================================================

st.markdown(
    """
    <style>

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

    [data-testid="stToolbar"] {
        display: none;
    }

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"] {

        margin: 0 !important;
        padding: 0 !important;

        background: #000000 !important;
    }

    .block-container {

        padding: 0 !important;
        margin: 0 !important;

        max-width: none !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# START SCREEN
# =========================================================

components.html(
    """
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <style>

            * {
                box-sizing: border-box;
            }


            html,
            body {

                margin: 0;
                padding: 0;

                width: 100%;
                height: 100%;

                overflow: hidden;

                background: #000000;
            }


            /* =========================================
               전체 화면
               ========================================= */

            .screen {

                position: relative;

                width: 100vw;
                height: 100vh;

                background: #000000;

                color: #ffffff;

                font-family:
                    "Courier New",
                    Consolas,
                    monospace;

                overflow: hidden;
            }


            /* =========================================
               PROJECT : LOGIC
               ========================================= */

            .title {

                position: absolute;

                top: 12vh;
                left: 50%;

                transform: translateX(-50%);

                color: #ffffff;

                font-size: clamp(32px, 4vw, 58px);

                font-weight: bold;

                letter-spacing: 0.12em;

                white-space: nowrap;

                text-align: center;

                text-shadow:
                    0 0 4px rgba(255,255,255,0.85),
                    0 0 12px rgba(255,255,255,0.25);

                animation:
                    title-flicker
                    4.2s
                    infinite;
            }


            /* =========================================
               SUBTITLE
               ========================================= */

            .subtitle {

                position: absolute;

                top: 22vh;
                left: 50%;

                transform: translateX(-50%);

                color: #9a9a9a;

                font-size: clamp(10px, 1.1vw, 15px);

                letter-spacing: 0.25em;

                white-space: nowrap;

                text-align: center;
            }


            /* =========================================
               메뉴 영역
               ========================================= */

            .menu-area {

                position: absolute;

                top: 51vh;
                left: 50%;

                transform: translateX(-50%);

                width: 500px;

                height: 180px;
            }


            /* =========================================
               START
               ========================================= */

            .start {

                position: absolute;

                top: 0;
                left: 0;

                width: 170px;
                height: 55px;

                display: flex;

                align-items: center;
                justify-content: center;

                color: #ffffff;

                font-size: 22px;

                letter-spacing: 0.12em;

                cursor: pointer;

                user-select: none;

                transition: none;
            }


            .start:hover {

                text-shadow:
                    0 0 5px rgba(255,255,255,0.5);
            }


            /* =========================================
               START 오른쪽 팝업
               ========================================= */

            .popup {

                position: absolute;

                top: -3px;
                left: 225px;

                width: 190px;

                padding: 7px 0;

                background: #080808;

                border: 1px solid #555555;

                box-shadow:
                    0 0 0 1px #111111,
                    0 0 12px rgba(255,255,255,0.08);

                display: none;

                animation:
                    popup-appear
                    0.12s
                    steps(2, end);
            }


            .popup.show {

                display: block;
            }


            /* =========================================
               팝업 버튼
               ========================================= */

            .popup-button {

                width: 100%;

                height: 42px;

                display: flex;

                align-items: center;

                padding-left: 18px;

                color: #ffffff;

                font-size: 14px;

                letter-spacing: 0.1em;

                cursor: pointer;

                user-select: none;
            }


            .popup-button + .popup-button {

                border-top: 1px solid #222222;
            }


            /* =========================================
               마우스 올리면 깜빡임
               ========================================= */

            .popup-button:hover {

                background: #ffffff;

                color: #000000;

                animation:
                    menu-flicker
                    0.55s
                    steps(1, end)
                    infinite;
            }


            /* =========================================
               HOW TO PLAY
               ========================================= */

            .how {

                position: absolute;

                top: 110px;
                left: -25px;

                width: 220px;
                height: 55px;

                display: flex;

                align-items: center;
                justify-content: center;

                color: #ffffff;

                font-size: 17px;

                letter-spacing: 0.12em;

                cursor: pointer;

                user-select: none;
            }


            .how:hover {

                text-shadow:
                    0 0 5px rgba(255,255,255,0.5);
            }


            /* =========================================
               TITLE FLICKER
               ========================================= */

            @keyframes title-flicker {

                0%,
                4% {
                    opacity: 1;
                }

                5% {
                    opacity: 0.45;
                }

                6% {
                    opacity: 1;
                }

                13% {
                    opacity: 1;
                }

                14% {
                    opacity: 0.2;
                }

                15% {
                    opacity: 0.85;
                }

                16% {
                    opacity: 1;
                }

                38% {
                    opacity: 1;
                }

                39% {
                    opacity: 0.4;
                }

                40% {
                    opacity: 0.1;
                }

                41% {
                    opacity: 0.9;
                }

                42% {
                    opacity: 1;
                }

                70% {
                    opacity: 1;
                }

                71% {
                    opacity: 0.3;
                }

                72% {
                    opacity: 1;
                }

                100% {
                    opacity: 1;
                }
            }


            /* =========================================
               MENU FLICKER
               ========================================= */

            @keyframes menu-flicker {

                0% {
                    opacity: 1;
                }

                18% {
                    opacity: 0.15;
                }

                19% {
                    opacity: 1;
                }

                38% {
                    opacity: 0.35;
                }

                39% {
                    opacity: 1;
                }

                60% {
                    opacity: 0.1;
                }

                61% {
                    opacity: 1;
                }

                80% {
                    opacity: 0.45;
                }

                81% {
                    opacity: 1;
                }

                100% {
                    opacity: 1;
                }
            }


            /* =========================================
               POPUP APPEAR
               ========================================= */

            @keyframes popup-appear {

                0% {

                    opacity: 0;

                    transform:
                        translateX(-7px);
                }

                100% {

                    opacity: 1;

                    transform:
                        translateX(0);
                }
            }


            /* =========================================
               작은 화면
               ========================================= */

            @media (max-width: 700px) {

                .title {

                    top: 12vh;

                    font-size: 30px;
                }


                .subtitle {

                    top: 21vh;

                    font-size: 9px;
                }


                .menu-area {

                    width: 100%;

                    left: 50%;
                }


                .start {

                    left: calc(50% - 85px);
                }


                .popup {

                    left: calc(50% + 105px);
                }


                .how {

                    left: calc(50% - 110px);
                }

            }

        </style>

    </head>


    <body>

        <div class="screen">


            <!-- =====================================
                 TITLE
                 ===================================== -->

            <div class="title">

                PROJECT : LOGIC

            </div>


            <div class="subtitle">

                INFORMATION IS NOT ALWAYS TRUE

            </div>


            <!-- =====================================
                 MENU
                 ===================================== -->

            <div class="menu-area">


                <!-- START -->

                <div
                    class="start"
                    id="start"
                >

                    START

                </div>


                <!-- START POPUP -->

                <div
                    class="popup"
                    id="popup"
                >

                    <div
                        class="popup-button"
                        id="continue"
                    >

                        CONTINUE

                    </div>


                    <div
                        class="popup-button"
                        id="new-game"
                    >

                        NEW GAME

                    </div>

                </div>


                <!-- HOW TO PLAY -->

                <div
                    class="how"
                    id="how"
                >

                    HOW TO PLAY

                </div>


            </div>


        </div>


        <script>

            /* =========================================
               START → POPUP
               ========================================= */

            const start =
                document.getElementById("start");

            const popup =
                document.getElementById("popup");


            start.addEventListener(
                "click",
                function() {

                    popup.classList.toggle("show");

                }
            );


            /* =========================================
               NEW GAME
               ========================================= */

            document
                .getElementById("new-game")
                .addEventListener(
                    "click",
                    function() {

                        window.parent.location.href =
                            "?action=new_game";

                    }
                );


            /* =========================================
               CONTINUE
               ========================================= */

            document
                .getElementById("continue")
                .addEventListener(
                    "click",
                    function() {

                        window.parent.location.href =
                            "?action=continue";

                    }
                );


            /* =========================================
               HOW TO PLAY
               ========================================= */

            document
                .getElementById("how")
                .addEventListener(
                    "click",
                    function() {

                        window.parent.location.href =
                            "?action=how_to_play";

                    }
                );

        </script>

    </body>

    </html>
    """,
    height=900,
    scrolling=False
)
