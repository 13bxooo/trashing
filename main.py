import base64
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="PROJECT : LOGIC",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "assets"
BACKGROUND_PATH = ASSET_DIR / "title_background.jpeg"
FONT_CANDIDATES = (ROOT / "neodgm.ttf", ROOT / "neodgm(2).ttf")

# The title reference image is used as the actual background. Its original
# embedded menu is covered by the custom two-button menu below.
if not BACKGROUND_PATH.exists():
    # Backward-compatible fallback for projects that have not copied the new asset yet.
    BACKGROUND_PATH = ASSET_DIR / "lab_background.jpeg"
background_data = base64.b64encode(BACKGROUND_PATH.read_bytes()).decode("ascii")
font_data = ""
for candidate in FONT_CANDIDATES:
    if candidate.exists():
        font_data = base64.b64encode(candidate.read_bytes()).decode("ascii")
        break

# Resolve navigation requests before rendering the title page.
action = st.query_params.get("action", "")
if action:
    st.query_params.clear()
    if action == "title":
        st.session_state.game_paused = False
        st.session_state.start_open = False
        st.session_state.error_popup = False
        st.session_state.warning_popup = False
        st.rerun()
    elif action == "stage01":
        st.session_state.stage01_started = True
        st.session_state.game_started = True
        st.session_state.game_paused = False
        st.switch_page("pages/3_Stage_01.py")
    elif action == "tutorial":
        st.session_state.game_started = True
        st.session_state.game_paused = False
        st.session_state.tutorial_complete = False
        st.session_state.stage01_started = False
        st.session_state.stage02_started = False
        st.switch_page("pages/2_Game.py")

# Defaults used by the title screen. These flags are shared with the game pages.
defaults = {
    "start_open": False,
    "game_started": False,
    "game_paused": False,
    "game_finished": False,
    "tutorial_complete": False,
    "stage01_started": False,
    "stage02_started": False,
    "remaining_seconds": 15 * 60,
    "error_popup": False,
    "warning_popup": False,
    "settings_open": False,
    "sound_enabled": True,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Progress is inferred from the state maintained by the existing game pages.
# The pages' own localStorage saves are cleared when the reset flags below are consumed.
def has_saved_progress() -> bool:
    return bool(
        st.session_state.get("game_started", False)
        or st.session_state.get("tutorial_complete", False)
        or st.session_state.get("stage01_started", False)
        or st.session_state.get("stage02_started", False)
        or st.session_state.get("game_finished", False)
        or st.session_state.get("tutorial_step", 0)
        or st.session_state.get("s1_progress")
    )

st.markdown(
    f"""
<style>
@font-face {{
  font-family: NeoDungGeunMo;
  src: url(data:font/ttf;base64,{font_data}) format('truetype');
  font-weight: normal;
  font-style: normal;
}}
:root {{ color-scheme: dark; }}
#MainMenu, header, footer, [data-testid="stSidebar"] {{ display:none !important; visibility:hidden !important; }}
.stApp {{
  background:#000 url(data:image/jpeg;base64,{background_data}) center center / cover no-repeat fixed !important;
  color:#fff !important;
  font-family:NeoDungGeunMo, monospace !important;
  min-height:100vh;
}}
html, body, [class*="css"], button, input, textarea, [data-testid="stMarkdownContainer"] {{
  font-family:NeoDungGeunMo, monospace !important;
}}
.block-container {{ max-width:none !important; padding:0 !important; }}
/* Hide Streamlit's normal top spacing so the background fills the viewport. */
[data-testid="stAppViewContainer"] > .main {{ padding:0 !important; }}
[data-testid="stAppViewContainer"] > .main .block-container {{ padding:0 !important; }}
/* Explicit title and subtitle overlays ensure both remain visible even if the background asset lacks text. */
.title-overlay {{
  position:fixed !important; top:25vh !important; left:50% !important;
  transform:translateX(-50%) !important; width:max-content !important;
  max-width:94vw !important; z-index:10 !important;
  margin:0 !important; padding:0 !important; background:transparent !important;
  border:0 !important; box-shadow:none !important;
  color:#f2fbff !important; font-family:NeoDungGeunMo,monospace !important;
  font-size:clamp(28px,4.8vw,60px) !important; letter-spacing:0.04em !important;
  text-align:center !important;
  text-shadow:0 0 3px #fff, 0 0 8px #00dfff, 0 0 18px #00dfff, 0 0 32px #008cff !important;
  animation:title-neon-flicker 4.5s infinite !important;
  pointer-events:none !important; white-space:nowrap !important;
}}
@keyframes title-neon-flicker {{
  0%, 18%, 20%, 22%, 55%, 57%, 100% {{ opacity:1; filter:brightness(1); }}
  19%, 56% {{ opacity:0.78; filter:brightness(0.78); }}
  21% {{ opacity:0.92; filter:brightness(1.2); }}
}}
.subtitle-overlay {{
  position:fixed !important; top:36vh !important; left:50% !important;
  transform:translateX(-50%) !important; width:max-content !important;
  max-width:92vw !important; z-index:10 !important;
  margin:0 !important; padding:0 !important; background:transparent !important;
  border:0 !important; box-shadow:none !important;
  color:#eafaff !important; font-family:NeoDungGeunMo,monospace !important;
  font-size:clamp(10px,1.45vw,17px) !important; letter-spacing:0.12em !important;
  text-align:center !important; text-shadow:0 0 5px #00dfff, 0 0 12px #00dfff66 !important;
  pointer-events:none !important;
}}
@media(max-width:600px) {{
  .title-overlay {{ top:24vh !important; font-size:clamp(22px,6.5vw,34px) !important; }}
  .subtitle-overlay {{ top:34vh !important; font-size:10px !important; letter-spacing:0.04em !important; }}
}}
.st-key-start_button, .st-key-how_to_play_button {{
  position:fixed !important; left:50% !important; transform:translateX(-50%) !important;
  z-index:20 !important; margin:0 !important; padding:0 !important; width:min(240px,68vw) !important;
}}
.st-key-start_button {{ top:57vh !important; }}
.st-key-how_to_play_button {{ top:68vh !important; }}
.st-key-start_button button, .st-key-how_to_play_button button {{
  width:100% !important; height:43px !important; min-height:43px !important;
  border:1px solid #159db9 !important; border-radius:0 !important;
  background:#000 !important; color:#f4fcff !important;
  font-family:NeoDungGeunMo,monospace !important; font-size:17px !important;
  box-shadow:none !important; padding:0 12px !important;
}}
.st-key-start_button button:hover, .st-key-how_to_play_button button:hover {{
  background:#fff !important; color:#000 !important; border-color:#fff !important;
}}
/* Compact START submenu, with a close control in its top-right corner. */
.st-key-start_popup {{
  position:fixed !important; z-index:40 !important; top:54vh !important;
  left:calc(50% + 155px) !important; width:164px !important;
  margin:0 !important; padding:8px !important; box-sizing:border-box !important;
  border:1px solid #26d9f5 !important; background:#02070b !important;
  box-shadow:0 0 14px #00dfff20 !important;
}}
.st-key-start_popup button {{
  width:100% !important; height:32px !important; min-height:32px !important;
  margin:0 0 5px !important; border:1px solid #147b94 !important;
  border-radius:0 !important; background:#000 !important; color:#fff !important;
  font-family:NeoDungGeunMo,monospace !important; font-size:12px !important;
}}
.st-key-start_popup button:last-child {{ margin-bottom:0 !important; }}
.st-key-start_popup [data-testid="stHorizontalBlock"] {{ gap:0.25rem !important; }}
.st-key-start_popup [data-testid="stHorizontalBlock"] button {{ height:24px !important; min-height:24px !important; padding:0 !important; }}
.st-key-start_popup button:hover {{ background:#fff !important; color:#000 !important; }}
/* Error and warning cards are separate pop-ups beside the START submenu. */
.st-key-error_popup, .st-key-warning_popup {{
  position:fixed !important; z-index:60 !important; top:55.5vh !important;
  left:calc(50% + 370px) !important; width:min(300px,28vw) !important;
  min-width:240px !important; margin:0 !important; padding:12px 14px !important;
  border:1px solid #26d9f5 !important; background:#02070b !important;
  box-shadow:0 0 22px #00dfff28 !important; box-sizing:border-box !important;
}}
.st-key-error_popup [data-testid="stMarkdownContainer"],
.st-key-warning_popup [data-testid="stMarkdownContainer"] {{
  color:#f3faff !important; font-family:NeoDungGeunMo,monospace !important;
  font-size:13px !important; line-height:1.8 !important;
}}
.st-key-error_popup button, .st-key-warning_popup button {{
  border:1px solid #26d9f5 !important; border-radius:0 !important;
  background:#000 !important; color:#fff !important;
  font-family:NeoDungGeunMo,monospace !important;
}}
.st-key-error_popup button:hover, .st-key-warning_popup button:hover {{ background:#fff !important; color:#000 !important; }}
@media(max-width:1000px) {{
  .st-key-start_popup {{ left:calc(50% + 115px) !important; width:150px !important; }}
  .st-key-error_popup, .st-key-warning_popup {{ left:50% !important; top:83vh !important; transform:translateX(-50%) !important; width:min(360px,90vw) !important; }}
}}
@media(max-width:600px) {{
  .st-key-start_button {{ top:52vh !important; width:190px !important; }}
  .st-key-how_to_play_button {{ top:62vh !important; width:190px !important; }}
  .st-key-start_popup {{ top:73vh !important; left:50% !important; transform:translateX(-50%) !important; width:170px !important; }}
  .st-key-error_popup, .st-key-warning_popup {{ top:77vh !important; }}
}}
</style>
""",
    unsafe_allow_html=True,
)

# Keep the title and subtitle explicit so they remain visible independently of the background asset.
st.markdown(
    '<div class="title-overlay">PROJECT : LOGIC</div>'
    '<div class="subtitle-overlay">INFORMATION IS NOT ALWAYS TRUE</div>',
    unsafe_allow_html=True,
)

# Main title menu: exactly two buttons.
start_clicked = st.button("START", key="start_button")
how_clicked = st.button("HOW TO PLAY", key="how_to_play_button")

if start_clicked:
    st.session_state.start_open = not st.session_state.start_open
    st.session_state.error_popup = False
    st.session_state.warning_popup = False
    st.rerun()

if how_clicked:
    st.session_state.start_open = False
    st.session_state.error_popup = False
    st.session_state.warning_popup = False
    st.switch_page("pages/1_How_To_Play.py")

if st.session_state.start_open:
    with st.container(key="start_popup", border=True):
        popup_head, popup_close = st.columns([5, 1], gap="small")
        with popup_head:
            st.markdown("**SELECT MODE**")
        with popup_close:
            if st.button("×", key="close_start_popup", help="팝업 닫기"):
                st.session_state.start_open = False
                st.session_state.error_popup = False
                st.session_state.warning_popup = False
                st.rerun()
        continue_clicked = st.button("CONTINUE", key="start_continue", use_container_width=True)
        new_game_clicked = st.button("NEW GAME", key="start_new_game", use_container_width=True)

    if continue_clicked:
        st.session_state.start_open = True
        if not has_saved_progress():
            st.session_state.error_popup = True
            st.session_state.warning_popup = False
            st.rerun()
        st.session_state.game_paused = False
        if st.session_state.get("stage02_started", False):
            st.switch_page("pages/4_Stage_02.py")
        elif st.session_state.get("stage01_started", False):
            st.switch_page("pages/3_Stage_01.py")
        else:
            st.switch_page("pages/2_Game.py")

    if new_game_clicked:
        st.session_state.error_popup = False
        if has_saved_progress():
            st.session_state.warning_popup = True
            st.rerun()
        else:
            # No existing run: begin immediately at the tutorial.
            st.session_state.warning_popup = False
            for key in list(st.session_state.keys()):
                if key.startswith(("s1_", "tutorial_", "stage01_", "stage02_")):
                    del st.session_state[key]
            st.session_state.tutorial_reset_save = True
            st.session_state.stage01_reset_save = True
            st.session_state.stage02_reset_save = True
            st.session_state.game_started = True
            st.session_state.game_paused = False
            st.session_state.game_finished = False
            st.session_state.tutorial_complete = False
            st.session_state.stage01_started = False
            st.session_state.stage02_started = False
            st.session_state.remaining_seconds = 15 * 60
            st.session_state.start_open = False
            st.switch_page("pages/2_Game.py")

if st.session_state.error_popup:
    with st.container(key="error_popup", border=True):
        title_col, close_col = st.columns([7, 1], gap="small")
        with title_col:
            st.markdown("### ⚠ ERROR")
        with close_col:
            if st.button("×", key="close_error", help="팝업 닫기"):
                st.session_state.error_popup = False
                st.rerun()
        st.markdown("이전 플레이 기록이 존재하지 않습니다.")

if st.session_state.warning_popup:
    with st.container(key="warning_popup", border=True):
        title_col, close_col = st.columns([7, 1], gap="small")
        with title_col:
            st.markdown("### ⚠ WARNING")
        with close_col:
            if st.button("×", key="close_warning", help="팝업 닫기"):
                st.session_state.warning_popup = False
                st.rerun()
        st.markdown("이전 플레이 기록이 존재합니다.\n\n새 게임을 진행하시겠습니까?")
        yes_col, no_col = st.columns(2, gap="small")
        with yes_col:
            yes_clicked = st.button("YES", key="warning_yes", use_container_width=True)
        with no_col:
            no_clicked = st.button("NO", key="warning_no", use_container_width=True)

    if yes_clicked:
        # Clear Streamlit state and signal each game page to clear its browser save.
        for key in list(st.session_state.keys()):
            if key.startswith(("s1_", "tutorial_", "stage01_", "stage02_")):
                del st.session_state[key]
        st.session_state.tutorial_reset_save = True
        st.session_state.stage01_reset_save = True
        st.session_state.stage02_reset_save = True
        st.session_state.game_started = True
        st.session_state.game_paused = False
        st.session_state.game_finished = False
        st.session_state.tutorial_complete = False
        st.session_state.stage01_started = False
        st.session_state.stage02_started = False
        st.session_state.remaining_seconds = 15 * 60
        st.session_state.warning_popup = False
        st.session_state.error_popup = False
        st.session_state.start_open = False
        st.switch_page("pages/2_Game.py")

    if no_clicked:
        st.session_state.warning_popup = False
        st.rerun()
