import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PROJECT : LOGIC // HOW TO PLAY",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


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
       BACK TO TITLE
       ===================================================== */

    .st-key-back_to_title {{
        position: fixed !important;

        right: 32px !important;
        bottom: 28px !important;

        width: 190px !important;
        height: 50px !important;

        margin: 0 !important;
        padding: 0 !important;

        z-index: 999999 !important;
    }}


    .st-key-back_to_title button {{
        width: 190px !important;
        height: 50px !important;

        margin: 0 !important;
        padding: 0 !important;

        border: 1px solid #777777 !important;
        border-radius: 0 !important;

        background: rgba(5, 5, 5, 0.96) !important;

        color: #ffffff !important;

        font-family: "NeoDungGeunMo", monospace !important;

        font-size: 16px !important;

        box-shadow: none !important;

        cursor: pointer !important;

        transition:
            background 0.15s ease,
            color 0.15s ease,
            border-color 0.15s ease !important;
    }}


    .st-key-back_to_title button:hover {{
        background: #ffffff !important;

        color: #000000 !important;

        border-color: #ffffff !important;
    }}


    .st-key-back_to_title button:focus {{
        background: rgba(5, 5, 5, 0.96) !important;

        color: #ffffff !important;

        border-color: #777777 !important;

        box-shadow: none !important;
    }}


    .st-key-back_to_title button:focus:hover {{
        background: #ffffff !important;

        color: #000000 !important;

        border-color: #ffffff !important;
    }}


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 700px) {{

        .st-key-back_to_title {{
            right: 20px !important;
            bottom: 20px !important;

            width: 170px !important;
            height: 46px !important;
        }}

        .st-key-back_to_title button {{
            width: 170px !important;
            height: 46px !important;

            font-size: 14px !important;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HOW TO PLAY
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
    min-height: 100%;

    background: #000000;

    font-family: "NeoDungGeunMo", monospace;
}}


/* =====================================================
   PAGE
   ===================================================== */

body {{
    color: #ffffff;

    overflow-x: hidden;
    overflow-y: auto;
}}


.screen {{
    width: 100%;

    min-height: 100vh;

    background: #000000;

    padding-bottom: 150px;
}}


/* =====================================================
   HEADER
   ===================================================== */

.header {{
    width: calc(100% - 100px);

    margin: 0 auto;

    padding-top: 32px;

    display: flex;

    justify-content: space-between;
    align-items: center;

    font-size: 15px;

    letter-spacing: 1px;
}}


.header-right {{
    color: #666666;
}}


/* =====================================================
   TITLE
   ===================================================== */

.title-area {{
    width: calc(100% - 100px);

    margin: 65px auto 0;

    max-width: 1000px;
}}


.main-title {{
    font-size: clamp(32px, 4vw, 48px);

    letter-spacing: 2px;

    margin-bottom: 14px;
}}


.subtitle {{
    color: #777777;

    font-size: 15px;

    letter-spacing: 1px;
}}


/* =====================================================
   CONTENT
   ===================================================== */

.content {{
    width: calc(100% - 100px);

    max-width: 1000px;

    margin: 70px auto 0;

    display: grid;

    grid-template-columns: repeat(2, minmax(280px, 1fr));

    gap: 18px;
}}


/* =====================================================
   CARD
   ===================================================== */

.card {{
    min-height: 145px;

    border: 1px solid #333333;

    background: #050505;

    padding: 20px;

    transition:
        border-color 0.15s ease,
        background 0.15s ease;
}}


.card:hover {{
    border-color: #ffffff;

    background: #0b0b0b;
}}


.card-header {{
    display: flex;

    align-items: center;

    gap: 12px;

    margin-bottom: 17px;
}}


.number {{
    color: #666666;

    font-size: 13px;
}}


.card-title {{
    color: #ffffff;

    font-size: 19px;

    letter-spacing: 1px;
}}


/* =====================================================
   KEY
   ===================================================== */

.key {{
    display: inline-flex;

    align-items: center;
    justify-content: center;

    min-width: 58px;
    height: 32px;

    padding: 0 10px;

    margin-right: 7px;

    border: 1px solid #777777;

    background: #111111;

    color: #ffffff;

    font-size: 14px;

    vertical-align: middle;
}}


/* =====================================================
   DESCRIPTION
   ===================================================== */

.description {{
    color: #999999;

    font-size: 14px;

    line-height: 1.9;
}}


/* =====================================================
   IMPORTANT
   ===================================================== */

.important {{
    grid-column: 1 / -1;

    border: 1px solid #555555;

    background: #030303;

    padding: 24px;

    margin-top: 5px;

    min-height: 150px;
}}


.important-title {{
    color: #ffffff;

    font-size: 17px;

    margin-bottom: 14px;

    letter-spacing: 1px;
}}


.important-text {{
    color: #888888;

    font-size: 14px;

    line-height: 2;
}}


.warning {{
    color: #ffffff;
}}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {{
    width: calc(100% - 100px);

    max-width: 1000px;

    margin: 55px auto 0;

    color: #444444;

    font-size: 11px;

    letter-spacing: 1px;
}}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {{

    .header {{
        width: calc(100% - 50px);

        font-size: 12px;
    }}

    .title-area {{
        width: calc(100% - 50px);

        margin-top: 60px;
    }}

    .content {{
        width: calc(100% - 50px);

        margin-top: 55px;

        grid-template-columns: 1fr;
    }}

    .important {{
        grid-column: auto;
    }}

    .footer {{
        width: calc(100% - 50px);
    }}

}}

</style>

</head>


<body>


<div class="screen">


    <!-- =================================================
         HEADER
         ================================================= -->

    <div class="header">

        <div>
            PROJECT : LOGIC
        </div>

        <div class="header-right">
            SYSTEM MANUAL // 01
        </div>

    </div>


    <!-- =================================================
         TITLE
         ================================================= -->

    <div class="title-area">

        <div class="main-title">
            HOW TO PLAY
        </div>

        <div class="subtitle">
            BASIC OPERATING INSTRUCTIONS
        </div>

    </div>


    <!-- =================================================
         CONTENT
         ================================================= -->

    <div class="content">


        <!-- 01 MOVEMENT -->

        <div class="card">

            <div class="card-header">

                <span class="number">
                    01
                </span>

                <span class="card-title">
                    MOVEMENT
                </span>

            </div>

            <div class="description">

                <span class="key">W</span>
                <span class="key">A</span>
                <span class="key">S</span>
                <span class="key">D</span>

                <br>

                연구시설 내부를 이동합니다.

            </div>

        </div>


        <!-- 02 INTERACTION -->

        <div class="card">

            <div class="card-header">

                <span class="number">
                    02
                </span>

                <span class="card-title">
                    INTERACTION
                </span>

            </div>

            <div class="description">

                <span class="key">E</span>

                주변의 물체를 조사하거나

                <br>

                아이템을 획득합니다.

            </div>

        </div>


        <!-- 03 INVENTORY -->

        <div class="card">

            <div class="card-header">

                <span class="number">
                    03
                </span>

                <span class="card-title">
                    INVENTORY
                </span>

            </div>

            <div class="description">

                <span class="key">I</span>

                보유한 아이템과 단서를 확인합니다.

                <br>

                <span class="key">ESC</span>

                인벤토리 또는 메뉴를 닫습니다.

            </div>

        </div>


        <!-- 04 SYSTEM MESSAGE -->

        <div class="card">

            <div class="card-header">

                <span class="number">
                    04
                </span>

                <span class="card-title">
                    SYSTEM MESSAGE
                </span>

            </div>

            <div class="description">

                <span class="key">SPACE</span>

                대화와 시스템 메시지를 진행합니다.

                <br>

                중요한 정보가 표시될 수 있습니다.

            </div>

        </div>


        <!-- =================================================
             IMPORTANT
             ================================================= -->

        <div class="important">

            <div class="important-title">
                IMPORTANT
            </div>

            <div class="important-text">

                주변의 물체와 기록을 자세히 조사하십시오.

                <br>

                <span class="warning">
                    ECHO가 제공하는 모든 정보가 사실이라고 가정하지 마십시오.
                </span>

                <br>

                서로 모순되는 단서가 발견될 수 있습니다.

                <br>

                무엇을 믿을 것인지는 당신의 판단에 달려 있습니다.

            </div>

        </div>


    </div>


    <!-- =================================================
         FOOTER
         ================================================= -->

    <div class="footer">

        ECHO SYSTEM // INFORMATION IS NOT ALWAYS TRUE

    </div>


</div>


</body>

</html>
"""


# =========================================================
# RENDER
# =========================================================

components.html(
    html,
    height=1000,
    scrolling=True,
)


# =========================================================
# BACK TO TITLE
# =========================================================

with st.container(key="back_to_title"):

    back_clicked = st.button(
        "BACK TO TITLE",
        key="back_title_button",
    )


# =========================================================
# PAGE NAVIGATION
# =========================================================

if back_clicked:

    st.switch_page("main.py")
