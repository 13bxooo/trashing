import base64
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="PROJECT : LOGIC", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")

# Navigation requests and persistent progress flags.
_page_action = st.query_params.get("action", "")
if _page_action == "title":
    st.query_params.clear()
    st.session_state.game_paused = False
    st.session_state.start_open = True
    st.session_state.show_title_warning = False
    st.rerun()
elif _page_action == "stage01":
    # The tutorial iframe requests the next Streamlit page via ?action=stage01.
    st.query_params.clear()
    st.session_state.stage01_started = True
    st.session_state.game_started = True
    st.session_state.game_paused = False
    st.session_state.start_open = False
    st.switch_page("pages/3_Stage_01.py")
elif _page_action == "restart":
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
    st.session_state.start_open = False
    st.switch_page("pages/2_Game.py")

for key, value in {
    "start_open": False,
    "game_started": False,
    "game_paused": False,
    "game_finished": False,
    "remaining_seconds": 15 * 60,
    "new_game_confirm": False,
    "show_title_warning": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

font_data = ""
for candidate in (Path("neodgm.ttf"), Path("neodgm(2).ttf")):
    if candidate.exists():
        font_data = base64.b64encode(candidate.read_bytes()).decode("utf-8")
        break

st.markdown(f"""
<style>
@font-face {{font-family:NeoDungGeunMo;src:url(data:font/ttf;base64,{font_data}) format('truetype');}}
#MainMenu,header,footer,[data-testid="stSidebar"]{{visibility:hidden;display:none}}
.stApp{{background:#000;color:#fff;font-family:NeoDungGeunMo,monospace}}
.block-container{{padding:0!important;max-width:100%!important}}
.project-title{{position:fixed;top:12vh;left:0;width:100%;text-align:center;color:#fff;font-family:NeoDungGeunMo,monospace;font-size:42px;letter-spacing:3px;z-index:10;text-shadow:0 0 3px #fff,0 0 10px #aaa;animation:titleFlicker 5.2s infinite steps(1,end)}}
.project-subtitle{{position:fixed;top:22vh;left:0;width:100%;text-align:center;color:#555;font-family:NeoDungGeunMo,monospace;font-size:13px;letter-spacing:2px;z-index:10}}
@keyframes titleFlicker{{0%,7%,9%,11%,44%,46%,48%,100%{{opacity:1;filter:brightness(1);text-shadow:0 0 3px #fff,0 0 10px #aaa}}8%,10%{{opacity:.35;filter:brightness(.65);text-shadow:none}}45%,47%{{opacity:.65;filter:brightness(.8);text-shadow:0 0 2px #fff}}72%{{opacity:.92}}73%{{opacity:.55}}74%{{opacity:1}}}}
@media(prefers-reduced-motion:reduce){{.project-title{{animation:none}}}}
.st-key-start_button,.st-key-how_to_play_button{{position:fixed!important;left:50%!important;transform:translateX(-50%)!important;margin:0!important;padding:0!important;z-index:100!important}}
.st-key-start_button{{top:51vh!important;width:170px!important;height:55px!important}}
.st-key-how_to_play_button{{top:65vh!important;width:220px!important;height:55px!important}}
.st-key-start_button button,.st-key-how_to_play_button button{{width:100%!important;height:55px!important;border:0!important;border-radius:0!important;background:#000!important;color:#fff!important;font-family:NeoDungGeunMo,monospace!important;font-size:19px!important;box-shadow:none!important}}
.st-key-start_button button:hover,.st-key-how_to_play_button button:hover{{background:#fff!important;color:#000!important}}
.st-key-popup{{position:fixed!important;top:calc(51vh - 3px)!important;left:calc(50% + 105px)!important;width:190px!important;margin:0!important;padding:6px!important;background:#000!important;border:1px solid #555!important;z-index:200!important}}
.st-key-confirm_modal{{position:fixed!important;inset:0!important;z-index:9999!important;display:flex!important;align-items:center!important;justify-content:center!important;padding:18px!important;background:rgba(0,0,0,.78)!important}}
.st-key-confirm_modal [data-testid="stVerticalBlockBorderWrapper"]{{width:min(430px,92vw)!important;max-width:430px!important;border:1px solid #aaa!important;background:#050505!important;box-shadow:0 0 0 1px #333,0 12px 40px #000!important;padding:22px 24px!important}}
.st-key-confirm_modal [data-testid="stMarkdownContainer"] p{{font-family:NeoDungGeunMo,monospace!important;font-size:13px!important;line-height:1.8!important;color:#ddd!important}}
.st-key-confirm_modal [data-testid="stButton"] button{{height:40px!important;border:1px solid #666!important;background:#050505!important;color:#fff!important;font-family:NeoDungGeunMo,monospace!important;border-radius:0!important}}
.st-key-confirm_modal [data-testid="stButton"] button:hover{{background:#fff!important;color:#000!important}}
.st-key-popup button{{width:100%!important;height:42px!important;margin:0 0 6px!important;padding:0!important;border:0!important;border-radius:0!important;background:#000!important;color:#fff!important;font-family:NeoDungGeunMo,monospace!important;font-size:14px!important}}
.st-key-popup button:last-child{{margin-bottom:0!important}}
.st-key-popup button:hover{{background:#fff!important;color:#000!important}}
[data-testid="stAlert"]{{position:fixed!important;top:calc(51vh + 115px)!important;left:50%!important;transform:translateX(-50%)!important;width:min(390px,85vw)!important;z-index:300!important;font-family:NeoDungGeunMo,monospace!important;font-size:13px!important}}
@media(max-width:700px){{.project-title{{top:15vh;font-size:30px;letter-spacing:2px}}.project-subtitle{{top:23vh;font-size:10px}}.st-key-start_button{{top:56vh!important;width:160px!important}}.st-key-how_to_play_button{{top:73vh!important;width:200px!important}}.st-key-popup{{top:59vh!important;left:50%!important;transform:translateX(-50%)!important;width:180px!important}}[data-testid="stAlert"]{{top:70vh!important}}}}
</style>
""", unsafe_allow_html=True)

# Returning from a game lands on the clean title screen; no overlapping banner is shown.
st.session_state.show_title_warning = False

st.markdown('<div class="project-title">PROJECT : LOGIC</div><div class="project-subtitle">FACILITY CONTROL SYSTEM</div>', unsafe_allow_html=True)
with st.container(key="start_button"):
    start_clicked = st.button("START", key="start", use_container_width=True)
if start_clicked:
    st.session_state.start_open = not st.session_state.start_open
with st.container(key="how_to_play_button"):
    how_clicked = st.button("HOW TO PLAY", key="how_to_play", use_container_width=True)
if how_clicked:
    st.switch_page("pages/1_How_To_Play.py")

if st.session_state.start_open:
    with st.container(key="popup"):
        continue_clicked = st.button("CONTINUE", key="continue", use_container_width=True)
        new_game_clicked = st.button("NEW GAME", key="new_game", use_container_width=True)

    if continue_clicked:
        st.session_state.start_open = False
        st.session_state.game_started = True
        st.session_state.game_paused = False
        # Session-state progress determines the page. If there is no progress flag
        # (e.g. a fresh session), CONTINUE opens the tutorial instead of doing nothing.
        if st.session_state.get("stage01_started", False):
            st.switch_page("pages/3_Stage_01.py")
        else:
            st.switch_page("pages/2_Game.py")

    if new_game_clicked:
        # A run exists if the tutorial/stage has ever been entered or any progress
        # marker has been set in this Streamlit session.
        progress_prefixes = ("s1_", "tutorial_", "stage01_")
        has_progress = bool(st.session_state.get("game_started", False)) or any(
            key.startswith(progress_prefixes) and bool(value)
            for key, value in st.session_state.items()
        ) or bool(st.session_state.get("stage01_started", False))

        if has_progress:
            st.session_state.new_game_confirm = True
            st.rerun()
        else:
            for _key in list(st.session_state.keys()):
                if _key.startswith(progress_prefixes):
                    del st.session_state[_key]
            st.session_state.tutorial_reset_save = True
            st.session_state.stage01_reset_save = True
            st.session_state.game_started = True
            st.session_state.game_paused = False
            st.session_state.game_finished = False
            st.session_state.tutorial_complete = False
            st.session_state.stage01_started = False
            st.session_state.remaining_seconds = 15 * 60
            st.session_state.new_game_confirm = False
            st.session_state.start_open = False
            st.switch_page("pages/2_Game.py")

if st.session_state.get("new_game_confirm", False):
    # Centered, compact system-dialog-style confirmation window.
    with st.container(key="confirm_modal", border=False):
        st.markdown("### SYSTEM CONFIRMATION")
        st.markdown("이전 플레이 기록이 존재합니다.\n\n기록을 초기화하고 새 게임을 시작하시겠습니까?")
        yes_col, no_col = st.columns(2, gap="small")
        with yes_col:
            yes_new_game = st.button("YES", key="confirm_new_game_yes", use_container_width=True)
        with no_col:
            no_new_game = st.button("NO", key="confirm_new_game_no", use_container_width=True)

    if yes_new_game:
        for _key in list(st.session_state.keys()):
            if _key.startswith(("s1_", "tutorial_", "stage01_")):
                del st.session_state[_key]
        st.session_state.tutorial_reset_save = True
        st.session_state.stage01_reset_save = True
        st.session_state.game_started = True
        st.session_state.game_paused = False
        st.session_state.game_finished = False
        st.session_state.remaining_seconds = 15 * 60
        st.session_state.tutorial_complete = False
        st.session_state.stage01_started = False
        st.session_state.new_game_confirm = False
        st.session_state.start_open = False
        st.switch_page("pages/2_Game.py")
    if no_new_game:
        st.session_state.new_game_confirm = False
        st.rerun()
