import streamlit as st


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="PROJECT : LOGIC",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================
# SESSION STATE
# =========================================

if "continue_message" not in st.session_state:
    st.session_state.continue_message = ""


# =========================================
# QUERY ACTION
# =========================================

action = st.query_params.get("action")

if action == "new_game":
    st.query_params.clear()
    st.switch_page("pages/1_Game.py")

elif action == "continue":
    st.query_params.clear()

    # 지금은 저장 데이터가 없다고 가정
    # 나중에 실제 save.json 시스템으로 교체
    save_exists = False

    if save_exists:
        st.switch_page("pages/1_Game.py")
    else:
        st.session_state.continue_message = (
            "이전 플레이 기록이 존재하지 않습니다. "
            "새 게임을 시작해주세요."
        )

elif action == "how_to_play":
    st.query_params.clear()
    st.switch_page("pages/2_How_to_Play.py")


# =========================================
# GLOBAL CSS
# =========================================

st.markdown(
    """
    <style>

    /* -------------------------------------
       STREAMLIT UI 제거
    ------------------------------------- */

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

    .stApp {
        background: #000000;
    }

    [data-testid="stAppViewContainer"] {
        background: #000000;
    }

    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: none !important;
    }


    /* -------------------------------------
       전체 시작 화면
    ------------------------------------- */

    .logic-start-screen {
        position: fixed;
        inset: 0;

        width: 100vw;
        height: 100vh;

        background: #000000;

        overflow: hidden;

        font-family:
            "Courier New",
            "Consolas",
            monospace;

        color: #ffffff;
    }


    /* -------------------------------------
       PROJECT : LOGIC
    ------------------------------------- */

    .logic-title {
        position: fixed;

        top: 13vh;
        left: 50%;

        transform: translateX(-50%);

        color: #ffffff;

        font-size: clamp(32px, 4vw, 58px);
        font-weight: 700;

        letter-spacing: 0.14em;

        white-space: nowrap;

        text-align: center;

        /*
         * 형광등이 접촉 불량으로
         * 깜빡이는 듯한 효과
         */
        animation: title-flicker 4.2s infinite;

        text-shadow:
            0 0 4px rgba(255,255,255,0.8),
            0 0 12px rgba(255,255,255,0.25);
    }


    /* -------------------------------------
       SUBTITLE
    ------------------------------------- */

    .logic-subtitle {
        position: fixed;

        top: 23vh;
        left: 50%;

        transform: translateX(-50%);

        color: #9c9c9c;

        font-size: clamp(10px, 1.1vw, 15px);

        letter-spacing: 0.28em;

        white-space: nowrap;

        opacity: 0.85;
    }


    /* -------------------------------------
       START
    ------------------------------------- */

    .start-button {
        position: fixed;

        top: 54vh;
        left: 50%;

        transform: translateX(-50%);

        width: 170px;
        height: 52px;

        display: flex;
        align-items: center;
        justify-content: center;

        color: #ffffff;

        font-size: 22px;
        font-weight: bold;

        letter-spacing: 0.12em;

        text-decoration: none;

        cursor: pointer;

        transition: none;
    }

    .start-button:hover {
        color: #ffffff;

        text-shadow:
            0 0 4px #ffffff,
            0 0 10px rgba(255,255,255,0.45);
    }


    /* -------------------------------------
       HOW TO PLAY
    ------------------------------------- */

    .how-button {
        position: fixed;

        top: 67vh;
        left: 50%;

        transform: translateX(-50%);

        width: 220px;
        height: 52px;

        display: flex;
        align-items: center;
        justify-content: center;

        color: #ffffff;

        font-size: 17px;

        letter-spacing: 0.12em;

        text-decoration: none;

        cursor: pointer;
    }

    .how-button:hover {
        color: #ffffff;

        text-shadow:
            0 0 4px #ffffff,
            0 0 10px rgba(255,255,255,0.4);
    }


    /* -------------------------------------
       START 옆 메뉴
    ------------------------------------- */

    .start-menu {
        position: fixed;

        top: 51vh;
        left: calc(50% + 105px);

        width: 190px;

        padding: 10px 0;

        background: rgba(8, 8, 8, 0.96);

        border: 1px solid #777777;

        box-shadow:
            0 0 0 1px #111111,
            0 0 12px rgba(255,255,255,0.08);

        z-index: 20;

        animation: menu-appear 0.12s steps(2, end);
    }


    /* -------------------------------------
       CONTINUE / NEW GAME
    ------------------------------------- */

    .sub-menu-button {
        display: block;

        width: 100%;

        padding: 11px 18px;

        box-sizing: border-box;

        color: #ffffff;

        font-family:
            "Courier New",
            "Consolas",
            monospace;

        font-size: 14px;

        letter-spacing: 0.1em;

        text-decoration: none;

        cursor: pointer;

        background: transparent;

        border: none;
    }

    .sub-menu-button:hover {

        /*
         * 마우스를 올렸을 때
         * 전등이 불안정하게 깜빡이는 효과
         */
        animation:
            hover-flicker 0.55s infinite
            steps(1, end);

        background: #ffffff;

        color: #000000;

        text-shadow: none;
    }


    /* -------------------------------------
       CONTINUE 안내 메시지
    ------------------------------------- */

    .continue-message {
        position: fixed;

        left: 50%;
        top: 77vh;

        transform: translateX(-50%);

        width: min(520px, 80vw);

        padding: 12px 18px;

        box-sizing: border-box;

        color: #d0d0d0;

        background: #080808;

        border: 1px solid #444444;

        font-family:
            "Courier New",
            "Consolas",
            monospace;

        font-size: 12px;

        text-align: center;

        letter-spacing: 0.04em;

        animation: message-flicker 0.25s steps(2, end);
    }


    /* -------------------------------------
       애니메이션
    ------------------------------------- */

    @keyframes title-flicker {

        0% {
            opacity: 1;
        }

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
            opacity: 0.8;
        }

        16% {
            opacity: 1;
        }

        38% {
            opacity: 1;
        }

        39% {
            opacity: 0.55;
        }

        40% {
            opacity: 0.15;
        }

        41% {
            opacity: 0.95;
        }

        42% {
            opacity: 1;
        }

        70% {
            opacity: 1;
        }

        71% {
            opacity: 0.35;
        }

        72% {
            opacity: 1;
        }

        100% {
            opacity: 1;
        }
    }


    @keyframes hover-flicker {

        0% {
            opacity: 1;
        }

        20% {
            opacity: 0.2;
        }

        21% {
            opacity: 1;
        }

        42% {
            opacity: 0.35;
        }

        43% {
            opacity: 1;
        }

        65% {
            opacity: 0.15;
        }

        66% {
            opacity: 1;
        }

        83% {
            opacity: 0.5;
        }

        84% {
            opacity: 1;
        }

        100% {
            opacity: 1;
        }
    }


    @keyframes menu-appear {

        0% {
            opacity: 0;
            transform: translateX(-5px);
        }

        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }


    @keyframes message-flicker {

        0% {
            opacity: 0;
        }

        100% {
            opacity: 1;
        }
    }


    /* -------------------------------------
       작은 화면 대응
    ------------------------------------- */

    @media (max-width: 700px) {

        .logic-title {
            top: 12vh;
            font-size: 30px;
        }

        .logic-subtitle {
            top: 21vh;
            font-size: 9px;
        }

        .start-menu {
            left: 50%;
            top: 61vh;

            transform: translateX(-50%);
        }

        .start-button {
            top: 54vh;
        }

        .how-button {
            top: 73vh;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================
# START SCREEN
# =========================================

html = """
<div class="logic-start-screen">

    <div class="logic-title">
        PROJECT : LOGIC
    </div>

    <div class="logic-subtitle">
        INFORMATION IS NOT ALWAYS TRUE
    </div>


    <!-- START -->

    <a
        class="start-button"
        href="#"
        onclick="
            const menu = document.getElementById('start-menu');
            menu.style.display =
                menu.style.display === 'none'
                ? 'block'
                : 'none';
            return false;
        "
    >
        START
    </a>


    <!-- START SUB MENU -->

    <div
        id="start-menu"
        class="start-menu"
        style="display: none;"
    >

        <a
            class="sub-menu-button"
            href="?action=continue"
        >
            CONTINUE
        </a>

        <a
            class="sub-menu-button"
            href="?action=new_game"
        >
            NEW GAME
        </a>

    </div>


    <!-- HOW TO PLAY -->

    <a
        class="how-button"
        href="?action=how_to_play"
    >
        HOW TO PLAY
    </a>

</div>
"""

st.markdown(html, unsafe_allow_html=True)


# =========================================
# CONTINUE ERROR MESSAGE
# =========================================

if st.session_state.continue_message:

    st.markdown(
        f"""
        <div class="continue-message">
            {st.session_state.continue_message}
        </div>
        """,
        unsafe_allow_html=True
    )

    # 한 번 표시한 메시지는 다음 실행에서 제거
    st.session_state.continue_message = ""
