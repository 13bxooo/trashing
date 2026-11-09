import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROJECT : LOGIC // STAGE 02", layout="wide", initial_sidebar_state="collapsed")
root = Path(__file__).resolve().parent.parent

def image(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")

font = ""
for candidate in (root / "neodgm.ttf", root / "neodgm(2).ttf"):
    if candidate.exists():
        font = base64.b64encode(candidate.read_bytes()).decode("ascii")
        break

st.markdown("""<style>html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#02050a!important}header,footer,[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"]{display:none!important}.block-container,[data-testid="stMainBlockContainer"]{padding:0!important;max-width:100vw!important;width:100%!important}iframe{display:block!important;border:0!important;width:100%!important}
/* v8 shared popup hierarchy and tutorial styling */
#helpOverlay,#inventoryOverlay{position:fixed!important;inset:0!important;z-index:4000!important;background:rgba(0,0,0,.70)!important}
#dialogOverlay{z-index:4500!important}
.pause-overlay{z-index:9000!important;background:rgba(0,0,0,.72)!important}
.pause-menu-panel{box-shadow:0 0 0 1px #123c4d,0 0 22px #00cfff55,0 0 100px #00cfff20!important}
.pause-toggle{z-index:9100!important}
#helpOverlay .help-panel,#helpOverlay .utility-panel{width:min(760px,90vw)!important;max-height:90vh!important;overflow:hidden!important;padding:28px 32px!important}
#helpOverlay .help-row{display:grid!important;grid-template-columns:32px 230px minmax(0,1fr)!important;align-items:center!important;gap:12px!important;padding:11px 0!important;border-bottom:1px solid #17495b!important}
#helpOverlay .help-number{color:#5fe9ff!important;background:none!important;border:0!important;width:auto!important}
#helpOverlay .help-key{color:#61e8ff!important;display:flex!important;align-items:center!important;gap:10px!important;width:auto!important;background:none!important;border:0!important}
#helpOverlay .control-label{color:#63e8ff!important;min-width:88px!important}
#helpOverlay .control-separator{color:#637985!important}
#helpOverlay .control-button{color:#f2fbff!important}
#helpOverlay .help-description{color:#8c9da7!important}
#inventoryOverlay .inventory-panel,#inventoryOverlay .utility-panel{width:min(820px,88vw)!important;max-height:90vh!important;overflow:hidden!important;padding:24px 26px!important}
#inventoryOverlay .inventory-grid{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;grid-template-rows:repeat(3,minmax(0,1fr))!important;gap:10px!important}
#inventoryOverlay .inventory-slot{position:relative!important;aspect-ratio:1!important;background:#01060b!important;border:1px solid #28546a!important}
#inventoryOverlay .inventory-slot .slot-number{position:absolute;top:7px;left:9px;font-size:10px;color:#555}
#inventoryOverlay .item-description{margin-top:16px!important;min-height:70px!important;padding:15px!important;border:1px solid #48dfff!important;color:#d9faff!important}
.echo-next{color:#4b8da0!important;opacity:.85!important}
.echo-bar{padding-right:20px!important;padding-bottom:27px!important}
#echoText{padding-right:6px!important;padding-bottom:8px!important}
#dataSavingScreen:not(.active){display:none!important}
#floorLayer,#wallLayer{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:fill!important;transform:none!important}</style>""", unsafe_allow_html=True)

# Lock the host page and game iframe to the visible viewport.
# The in-game interfaces and all gameplay JS remain unchanged.
_SCROLL_LOCK_CSS = """<style id="logic-other-stage-scroll-lock">
html, body, .stApp,
[data-testid="stAppViewContainer"], [data-testid="stMain"] {
    height: 100vh !important;
    height: 100dvh !important;
    max-height: 100dvh !important;
    overflow: hidden !important;
    overscroll-behavior: none !important;
}
[data-testid="stMainBlockContainer"], .block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100vw !important;
    width: 100% !important;
}
.stApp iframe[data-testid="stIFrame"],
.stApp [data-testid="stCustomComponentV1"] iframe,
.stApp iframe {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: auto !important;
    width: 100vw !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: none !important;
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    z-index: 20 !important;
    display: block !important;
}
</style>"""
st.markdown(_SCROLL_LOCK_CSS, unsafe_allow_html=True)

title = st.button("TITLE NAV", key="stage02_title_nav")
restart = st.button("RESTART NAV", key="stage02_restart_nav")
st.markdown("<style>.st-key-stage02_title_nav,.st-key-stage02_restart_nav{position:fixed!important;left:-10000px!important;top:0!important}</style>", unsafe_allow_html=True)
if title:
    st.session_state["stage02_started"] = True
    st.session_state["game_started"] = True
    st.switch_page("main.py")
if restart:
    # 모든 스테이지의 세션 진행 상태를 초기화합니다.
    for key in list(st.session_state.keys()):
        if key.startswith(("s1_", "stage01_", "stage02_")):
            del st.session_state[key]
    st.session_state["tutorial_reset_save"] = True
    st.session_state["stage01_reset_save"] = True
    st.session_state["stage02_reset_save"] = True
    st.session_state["stage01_started"] = True
    st.session_state["stage02_started"] = False
    st.session_state["game_started"] = True
    st.switch_page("pages/3_Stage_01.py")

html = r"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
@font-face{font-family:NeoDungGeunMo;src:url(data:font/ttf;base64,__FONT__)}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#02050a;color:#e5faff;font-family:NeoDungGeunMo,monospace}
.game{position:relative;width:100vw;height:100vh;overflow:hidden;background:#02050a;outline:none}
.project-title{position:absolute;top:24px;left:28px;font-size:20px;letter-spacing:1px;color:#fff;z-index:20}.stage-title{position:absolute;top:56px;left:28px;font-size:13px;letter-spacing:1px;color:#426b7d;z-index:20}
.stage01-timer{position:absolute;right:86px;top:32px;font-size:12px;color:#a9c4d0;z-index:20}
.pause-toggle{position:absolute;top:20px;right:24px;z-index:1000;width:42px;height:42px;display:flex;align-items:center;justify-content:center;background:#02070c;border:1px solid #54dfff;color:#8defff;font:20px NeoDungGeunMo,monospace;cursor:pointer;box-shadow:0 0 0 1px #123c4d;padding:0}
.pause-toggle:before,.pause-toggle:after{content:"";position:absolute;width:7px;height:7px;border-color:#8af0ff;border-style:solid}.pause-toggle:before{left:-2px;top:-2px;border-width:2px 0 0 2px}.pause-toggle:after{right:-2px;bottom:-2px;border-width:0 2px 2px 0}.pause-toggle.paused{background:#d9faff;color:#001018}
.game-area{position:absolute;top:45px;left:0;right:0;bottom:10px;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#02050a}
.room{position:relative;width:min(98vw,calc((100vh - 60px)*4/3));aspect-ratio:4/3;flex-shrink:0;overflow:hidden;background:transparent}
.room .layer{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;pointer-events:none;image-rendering:pixelated}#floorLayer{z-index:1}#wallLayer{z-index:4}
.player{position:absolute;z-index:3;width:22px;height:28px;background:#d5e7ee;border:0;box-shadow:inset 0 0 0 4px #7895a5,inset 0 -7px #263d4d,-4px 0 #152a39,4px 0 #152a39,0 -3px #152a39,0 3px #152a39;image-rendering:pixelated;transform:translate(-50%,-50%);pointer-events:none}
.player::before{content:"";position:absolute;left:4px;right:4px;top:-7px;height:8px;background:#c5d8e0;border:2px solid #142b3a;box-shadow:inset 0 -3px #7896a5}.player::after{content:"";position:absolute;left:6px;right:6px;top:2px;height:3px;background:#5ceaff;box-shadow:0 0 3px #5ceaff}
.echo-bar{position:absolute;left:50%;bottom:5%;transform:translateX(-50%);width:min(78%,650px);min-height:82px;padding:10px 16px 22px;background:#02070c;border:1px solid #2dbbd8;z-index:10;font-size:12px;line-height:1.6}.echo-head{font-size:11px;color:#50dfff;margin-bottom:7px}.echo-next{position:absolute;right:14px;bottom:6px;font-size:10px;color:#75d4e7;letter-spacing:1px;animation:echoBlink .8s steps(2,end) infinite}@keyframes echoBlink{50%{opacity:.25}}.status{position:absolute;bottom:24px;left:28px;color:#777;font-size:14px}
.pause-overlay{position:fixed;inset:0;z-index:2000;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.72)}.pause-menu-panel{position:relative;width:min(536px,86vw);height:274px;padding:34px 48px;display:flex;align-items:center;background:linear-gradient(135deg,#030b12,#061722);border:1px solid #54dfff}.pause-actions{display:flex;flex-direction:column;gap:8px}.pause-row{display:flex;align-items:center;gap:16px;height:55px}.pause-icon{width:38px;height:38px;border:1px solid #58dfff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#82eaff}.pause-nav-link{border:0;background:none;color:#d8faff;font:18px NeoDungGeunMo,monospace;text-align:left;cursor:pointer}.pause-nav-link:hover{color:white;text-shadow:0 0 6px #54dfff}
#helpOverlay,#inventoryOverlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1500;align-items:center;justify-content:center}.utility-panel{position:relative;width:min(820px,88vw);background:#02070c;border:1px solid #48dfff;box-shadow:0 0 0 1px #123c4d;padding:24px 26px 26px;font-size:15px;line-height:1.8;max-height:84vh;overflow:auto}.utility-panel h3{margin:0 0 18px;color:#72eaff}.inventory-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.inventory-slot{aspect-ratio:1;border:1px solid #28546a;background:#01060b;display:flex;align-items:center;justify-content:center;color:#607e8c;font-size:12px}.utility-close{position:absolute;right:18px;top:14px;background:transparent;border:0;color:#8defff;cursor:pointer;font:16px NeoDungGeunMo,monospace}.help-row{padding:10px 0;border-bottom:1px solid #17495b;display:flex;gap:20px}.help-key{width:130px;color:#8defff}
#stage02Intro{position:fixed;inset:0;z-index:3000;background:#000;display:flex;align-items:center;justify-content:center;pointer-events:none;animation:introFade 2.1s ease forwards;text-align:center}#stage02Intro strong{display:block;font-size:30px;color:#fff;text-shadow:0 0 8px #fff}#stage02Intro span{display:block;margin-top:16px;font-size:18px;color:#6deaff}@keyframes introFade{0%,42%{opacity:1}100%{opacity:0;visibility:hidden}}
.stage-transition{position:fixed;inset:0;z-index:3000;display:flex;align-items:center;justify-content:center;background:#000;opacity:1;transition:opacity .45s steps(6,end);pointer-events:auto}
.stage-transition.hide{opacity:0;pointer-events:none}
.stage-transition-card{position:relative;width:min(350px,78vw);min-height:145px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:1px solid #57dfff;color:#f5fbff;box-shadow:0 0 0 1px #143d4c,0 0 14px #00cfff22;letter-spacing:2px}
.stage-transition-card:before,.stage-transition-card:after{content:"";position:absolute;width:18px;height:18px;border-color:#78ecff;border-style:solid}
.stage-transition-card:before{top:-2px;left:-2px;border-width:2px 0 0 2px}.stage-transition-card:after{right:-2px;bottom:-2px;border-width:0 2px 2px 0}
.stage-transition-stage{font-size:clamp(25px,4vw,36px);line-height:1.6;text-shadow:0 0 5px #fff,0 0 14px #57dfff}.stage-transition-room{font-size:clamp(14px,2vw,20px);color:#a8f2ff;letter-spacing:1px}\n\n
/* TITLE 화면으로 돌아가기 전 3초 저장 연출 */
.data-saving-screen{position:fixed;inset:0;background:#000;z-index:999999;display:none;pointer-events:auto}
.data-saving-screen.active{display:block}
.data-saving-label{position:absolute;left:28px;bottom:25px;color:#9beaff;font-size:13px;display:flex;gap:12px;align-items:center}
.data-saving-gear{display:inline-block;font-size:23px;animation:gearSpin .9s linear infinite;transform-origin:center center}
@keyframes gearSpin{to{transform:rotate(360deg)}}

#inventoryOverlay .utility-panel,#helpOverlay .utility-panel{background:linear-gradient(135deg,#030b12,#061722);border:1px solid #35dfff;box-shadow:0 0 0 1px #123c4d,0 0 18px #00cfff24}
#inventoryOverlay .utility-panel{width:min(820px,88vw);max-height:84vh}
#helpOverlay .utility-panel{width:min(760px,86vw);max-height:82vh;padding:36px 40px}
.inventory-grid{grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:repeat(3,minmax(0,1fr))}
.inventory-slot{image-rendering:pixelated}
#inventoryOverlay .inventory-header,#helpOverlay .help-header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #2587a7;margin-bottom:14px;padding-bottom:10px}
#inventoryOverlay .inventory-title,#helpOverlay .help-title{font-size:17px;color:#72eaff;margin:0}
#inventoryOverlay .inventory-close,#helpOverlay .help-close{font-size:9px;color:#4b8da0}
#helpOverlay .help-important{margin-top:18px;padding:16px;background:#090909;border-left:2px solid white;color:#a9b9c4;font-size:11px;line-height:1.8}
#helpOverlay .help-important strong{color:#70eaff}
</style><style id="logic-v10-iframe-ui">

/* v10: shared popups, kept INSIDE the components.html iframe. */
#helpOverlay, #inventoryOverlay {
 position:fixed!important; inset:0!important; z-index:4000!important;
 background:rgba(0,0,0,.72)!important; align-items:center!important;
 justify-content:center!important; overflow:hidden!important;
 scrollbar-width:none!important; padding:16px!important;
}
#helpOverlay::-webkit-scrollbar,#inventoryOverlay::-webkit-scrollbar,
#helpOverlay *::-webkit-scrollbar,#inventoryOverlay *::-webkit-scrollbar{display:none!important}
#helpOverlay .help-panel,#helpOverlay .utility-panel {
 position:relative!important; box-sizing:border-box!important; flex:none!important;
 width:min(700px,94vw)!important; height:auto!important; max-width:94vw!important;
 max-height:calc(100vh - 44px)!important; padding:29px 34px 24px!important;
 background:#02070c!important; border:1px solid #4bdcff!important;
 box-shadow:0 0 0 1px #123c4d,0 0 19px #00cfff20!important;
 border-radius:0!important; display:block!important;
 overflow:hidden!important; overflow-x:hidden!important; overflow-y:hidden!important;
 scrollbar-width:none!important; font-size:12px!important; line-height:1.5!important;
}
#helpOverlay .help-header{
 display:flex!important;align-items:center!important;justify-content:space-between!important;
 margin:0 0 15px!important;padding:0 0 15px!important;border-bottom:1px solid #244b58!important;
 min-height:30px!important;
}
#helpOverlay .help-title{font-size:18px!important;font-weight:bold!important;line-height:1.3!important;color:#75ebff!important;margin:0!important}
#helpOverlay .help-close{font-size:9px!important;color:#82939d!important;white-space:nowrap!important}
#helpOverlay .help-row{
 display:grid!important;grid-template-columns:27px 218px minmax(0,1fr)!important;
 align-items:center!important;column-gap:12px!important;row-gap:0!important;
 padding:9px 0!important;margin:0!important;min-height:43px!important;
 border-bottom:1px solid #204458!important;
 background:none!important;box-shadow:none!important;
}
#helpOverlay .help-number {
 display:block!important;align-self:center!important;width:auto!important;min-width:0!important;
 color:#61e9ff!important;background:transparent!important;border:0!important;
 margin:0!important;padding:0!important;line-height:1.4!important;font-size:12px!important;
 position:static!important;transform:none!important;box-shadow:none!important;
}
#helpOverlay .help-key {
 display:grid!important;grid-template-columns:106px 10px minmax(0,1fr)!important;
 align-items:center!important;gap:7px!important;
 position:static!important;width:100%!important;min-width:0!important;height:auto!important;
 margin:0!important;padding:0!important;background:none!important;border:0!important;
 box-shadow:none!important;transform:none!important;overflow:visible!important;
}
#helpOverlay .help-key .control-label {
 display:inline!important;position:static!important;transform:none!important;
 margin:0!important;padding:0!important;border:0!important;background:none!important;
 color:#64e6ff!important;font-size:12px!important;line-height:1.5!important;
 white-space:nowrap!important;letter-spacing:0!important;box-shadow:none!important;
}
#helpOverlay .help-key .control-separator {
 display:inline!important;position:static!important;transform:none!important;
 margin:0!important;padding:0!important;border:0!important;background:none!important;
 color:#647681!important;font-size:12px!important;line-height:1.5!important;
 box-shadow:none!important;
}
/* "control-button" is ALSO the game's mobile D-pad class: explicitly reset it here. */
#helpOverlay .help-key .control-button {
 all:unset!important; display:inline!important;position:static!important;
 width:auto!important;min-width:0!important;max-width:none!important;height:auto!important;
 transform:none!important;clip-path:none!important;
 color:#f8fcff!important;font:12px/1.5 NeoDungGeunMo,monospace!important;
 white-space:nowrap!important;box-shadow:none!important;
}
#helpOverlay .help-description {
 display:block!important;position:static!important;grid-column:3!important;grid-row:auto!important;
 width:auto!important;min-width:0!important;color:#98a8b1!important;
 font-size:11px!important;line-height:1.55!important;white-space:normal!important;
 margin:0!important;padding:0!important;background:none!important;overflow:visible!important;
}
#helpOverlay .help-important {
 display:block!important;margin-top:17px!important;padding:13px 15px!important;
 background:#070a0d!important;border:0!important;border-left:2px solid #ccd8df!important;
 color:#9dabaf!important;font-size:10px!important;line-height:1.8!important;
}
#helpOverlay .help-important-title {color:#e6fbff!important;font-size:11px!important;margin-bottom:5px!important}
#inventoryOverlay .inventory-panel,#inventoryOverlay .utility-panel {
 position:relative!important;box-sizing:border-box!important;width:min(715px,92vw)!important;
 height:min(646px,calc(100vh - 64px))!important;max-height:calc(100vh - 64px)!important;
 padding:23px 23px 20px!important;background:#02070c!important;
 border:1px solid #4bdcff!important;border-radius:0!important;
 box-shadow:0 0 0 1px #123c4d,0 0 18px #00cfff20!important;
 display:flex!important;flex-direction:column!important;gap:0!important;overflow:hidden!important;
}
#inventoryOverlay .inventory-header,#inventoryOverlay .panel-header {
 display:flex!important;justify-content:space-between!important;align-items:center!important;
 flex:0 0 auto!important;min-height:42px!important;margin:0 0 13px!important;
 padding:0 0 13px!important;border-bottom:1px solid #255369!important;
}
#inventoryOverlay .inventory-title,#inventoryOverlay .panel-header h3 {
 font:17px/1.2 NeoDungGeunMo,monospace!important;margin:0!important;color:#70e7ff!important;
}
#inventoryOverlay .inventory-close,#inventoryOverlay .panel-hint {
 font:9px/1.3 NeoDungGeunMo,monospace!important;color:#80a3b1!important;
}
#inventoryOverlay .inventory-grid {
 display:grid!important;position:relative!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;
 grid-template-rows:repeat(3,minmax(0,1fr))!important;gap:8px!important;
 flex:1 1 auto!important;height:auto!important;max-height:none!important;min-height:0!important;
 overflow:hidden!important;margin:0!important;padding:0!important;
}
#inventoryOverlay .inventory-slot {
 display:flex!important;position:relative!important;align-items:center!important;justify-content:center!important;
 aspect-ratio:auto!important;width:100%!important;height:100%!important;min-height:0!important;
 padding:0!important;box-sizing:border-box!important;background:#01060b!important;
 border:1px solid #28546a!important;border-radius:0!important;
 box-shadow:none!important;color:#e5faff!important;
}
#inventoryOverlay .inventory-slot .slot-number {
 position:absolute!important;top:7px!important;left:8px!important;color:#677f8b!important;
 font-size:9px!important;line-height:1.2!important;
}
#inventoryOverlay .inventory-slot img{max-width:82%!important;max-height:78%!important;object-fit:contain!important;image-rendering:pixelated!important}
#inventoryOverlay .item-description {
 flex:0 0 76px!important;box-sizing:border-box!important;height:76px!important;min-height:76px!important;
 margin:14px 0 0!important;padding:11px 13px!important;display:block!important;
 background:#01060b!important;border:1px solid #4bdcff!important;
 color:#d6ebf0!important;font-size:11px!important;line-height:1.55!important;overflow:hidden!important;
}
#inventoryOverlay .item-description strong{display:block!important;margin-bottom:6px!important;color:#d8f6ff!important}
#inventoryOverlay .item-description p{margin:6px 0 0!important}
#inventoryOverlay .inventory-footer{display:none!important}
/* Pause ALWAYS beats all non-pause panels; button remains clickable above it. */
#pauseOverlay,.pause-overlay {
 position:fixed!important;inset:0!important;z-index:11000!important;
 background:rgba(0,0,0,.78)!important;backdrop-filter:blur(3px)!important;
 justify-content:center!important;align-items:center!important;
}
#pauseOverlay .pause-menu-panel,.pause-overlay .pause-menu-panel {
 box-shadow:0 0 0 1px #16495b,0 0 30px #00cfff65,0 0 95px #00cfff23!important;
 border:1px solid #54dfff!important;
}
#pauseToggle,.pause-toggle{z-index:12000!important;position:absolute!important}
#dialogOverlay,#itemAcquiredNotice,.item-acquired-notice,.computer-overlay,.card-overlay {z-index:4500!important}
.item-acquired-text {font-size:11px!important;line-height:1.55!important}
/* For the ECHO prompt: tutorial's dim/bright blinking convention. */
.echo-next,.echo-next:not(.ready){color:#6c8791!important;opacity:1!important}
.echo-next.ready{color:#f5ffff!important;opacity:1!important}
.echo-bar{box-sizing:border-box!important;padding-bottom:29px!important;min-height:88px!important}
.echo-bar #echoText,.echo-bar .echo-message{display:block!important;margin:0!important;padding:0 0 8px!important;
 max-width:100%!important;white-space:normal!important;overflow-wrap:anywhere!important}
.echo-bar .echo-next{position:absolute!important;right:14px!important;bottom:7px!important;font-size:9px!important;
 line-height:1.4!important;pointer-events:none!important}
#floorLayer,#wallLayer {position:absolute!important;inset:0!important;width:100%!important;height:100%!important;
 transform:none!important;object-fit:fill!important;image-rendering:pixelated!important}
#dataSavingScreen {display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important}
#dataSavingScreen.active {display:block!important;position:fixed!important;inset:0!important;z-index:999999!important;background:#000!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important}
#tutorialDataSaving{z-index:999999!important}
/* Smaller screens: leave all five help entries legible without any scrollbar. */
@media(max-width:690px) {
 #helpOverlay .help-panel{padding:17px 13px!important}
 #helpOverlay .help-row{grid-template-columns:24px 156px minmax(0,1fr)!important;gap:6px!important;min-height:39px!important;padding:6px 0!important}
 #helpOverlay .help-key{grid-template-columns:76px 7px minmax(0,1fr)!important;gap:4px!important}
 #helpOverlay .help-key .control-label,#helpOverlay .help-key .control-button{font-size:10px!important}
 #helpOverlay .help-description{font-size:10px!important}
 #helpOverlay .help-important{font-size:9px!important;padding:9px!important}
 #inventoryOverlay .inventory-panel{width:94vw!important;padding:13px!important}
}


/* STAGE 02 // ECHO CONTROL-ROOM PRELUDE */
#echoPrelude{
 position:fixed;inset:0;z-index:1500000;background:#000;opacity:1;
 display:flex;align-items:center;justify-content:center;padding:28px;
 color:#e1f7ff;font-family:NeoDungGeunMo,monospace;overflow:hidden;
}
#echoPrelude[hidden]{display:none!important}
#echoPrelude .prelude-panel{
 position:relative;width:min(1000px,94vw);max-height:calc(100vh - 45px);
 padding:12px 12px 0;background:#030b11;border:1px solid #4fd5eb;
 box-shadow:0 0 0 1px #163b49;overflow:hidden;
}
#echoPrelude .prelude-image-wrap{
 position:relative;width:100%;aspect-ratio:2/1;overflow:hidden;background:#02050a;
 border:1px solid #234d5e;image-rendering:pixelated;
}
#echoPrelude .prelude-image{
 position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
 image-rendering:pixelated;filter:brightness(.82);
}
#echoPrelude .prelude-message-box{
 position:relative;min-height:117px;padding:15px 17px 30px;
 background:#02070c;color:#e2f5fa;font-size:13px;line-height:1.85;
}
#echoPrelude .prelude-system-label{font-size:11px;color:#66dcef;margin-bottom:9px}
#echoPrelude .prelude-text{min-height:40px;max-width:92%;word-break:keep-all;overflow-wrap:break-word}
#echoPrelude .prelude-next{
 position:absolute;right:15px;bottom:9px;border:0;padding:0;background:transparent;
 color:#8ba9b3;font:10px NeoDungGeunMo,monospace;letter-spacing:.6px;
 cursor:pointer;animation:preludePulse 3s ease-in-out infinite;
}
#echoPrelude .prelude-next[disabled]{opacity:0;pointer-events:none}
@keyframes preludePulse{0%,100%{opacity:.25}50%{opacity:.78}}
#preludeGlitch{
 position:fixed;inset:0;z-index:1500002;pointer-events:none;opacity:0;
 background:repeating-linear-gradient(0deg,transparent 0 8px,#00eaff13 9px,#0009 11px,transparent 13px),
 linear-gradient(90deg,#ea244319 0 12%,transparent 23% 68%,#00ecff22 90%);
 mix-blend-mode:screen;
}
#preludeGlitch.active{opacity:1;animation:signalTear .12s steps(2,end) infinite}
#preludeGlitch.major{animation:signalTear .07s steps(3,end) infinite;
 background:repeating-linear-gradient(0deg,#030b15 0 5px,#ff315344 6px 7px,#00efff4b 8px 9px,transparent 10px 19px),
 linear-gradient(100deg,transparent 0 20%,#ee335529 21% 28%,transparent 29% 68%,#00f4ff43 70% 76%,transparent 77%);
}
#echoPrelude.glitching .prelude-panel{animation:preludeJitter .11s steps(2,end) infinite}
#echoPrelude.glitching.major .prelude-panel{animation:preludeJitter .065s steps(2,end) infinite}
@keyframes signalTear{0%{transform:translateX(-12px) skewX(1.5deg);filter:hue-rotate(10deg)}33%{transform:translateX(11px) skewX(-2deg)}66%{transform:translateY(5px) translateX(-4px);filter:hue-rotate(-15deg)}100%{transform:translateX(4px)}}
@keyframes preludeJitter{0%{transform:translateX(-3px)}50%{transform:translateX(4px)}100%{transform:translateY(2px)}}

/* v13: separate full-screen signal tear, RGB ghosts, and pixel fault bars. */
#echoPrelude .prelude-image-wrap{isolation:isolate}
#echoPrelude .prelude-ghost{
 opacity:0;pointer-events:none;z-index:3;mix-blend-mode:screen;
}
#echoPrelude.glitching .prelude-ghost-a{
 opacity:.64;filter:brightness(1.45) sepia(1) saturate(6) hue-rotate(300deg);
 animation:preludeGhostA .095s steps(2,end) infinite;
}
#echoPrelude.glitching .prelude-ghost-b{
 opacity:.55;filter:brightness(1.35) sepia(1) saturate(7) hue-rotate(132deg);
 animation:preludeGhostB .13s steps(3,end) infinite;
}
#echoPrelude.glitching.major .prelude-ghost{opacity:.85}
@keyframes preludeGhostA{
 0%{clip-path:inset(4% 0 77% 0);transform:translateX(11px)}
 33%{clip-path:inset(37% 0 39% 0);transform:translateX(-14px)}
 66%{clip-path:inset(69% 0 8% 0);transform:translateX(18px)}
 100%{clip-path:inset(20% 0 57% 0);transform:translateX(-7px)}
}
@keyframes preludeGhostB{
 0%{clip-path:inset(72% 0 4% 0);transform:translateX(-13px)}
 31%{clip-path:inset(13% 0 68% 0);transform:translateX(15px)}
 67%{clip-path:inset(43% 0 32% 0);transform:translateX(-21px)}
 100%{clip-path:inset(7% 0 78% 0);transform:translateX(8px)}
}
#preludeGlitch{isolation:isolate}
#preludeGlitch:before,#preludeGlitch:after{
 content:"";position:absolute;inset:0;pointer-events:none;
}
#preludeGlitch:before{
 background:repeating-linear-gradient(0deg,transparent 0 3px,#040809a6 4px 5px,transparent 6px 11px);
 opacity:.8;animation:preludeScanDance .085s steps(3,end) infinite;
}
#preludeGlitch:after{
 background:linear-gradient(90deg,transparent 0 33%,#f12b3b57 34% 35%,transparent 36% 61%,#14f5ff66 62% 63%,transparent 64%);
 opacity:.75;animation:preludeChromatic .12s steps(2,end) infinite;
 mix-blend-mode:screen;
}
#preludeGlitch .glitch-slice{
 position:absolute;z-index:3;pointer-events:none;mix-blend-mode:screen;
 box-shadow:0 1px 0 #0009,0 -1px 0 #d8ffff27;
}
#echoPrelude.glitching .prelude-text{animation:preludeTextFault .12s steps(2,end) infinite}
@keyframes preludeTextFault{
 0%,100%{text-shadow:none;transform:none}
 40%{text-shadow:-3px 0 #00edff,3px 0 #fb3150;transform:translateX(2px)}
 70%{text-shadow:2px 0 #fb3150,-2px 0 #03f1fc;transform:translateX(-1px)}
}
@keyframes preludeScanDance{0%{transform:translateY(0)}40%{transform:translateY(17px)}75%{transform:translateY(-9px)}100%{transform:translateY(7px)}}
@keyframes preludeChromatic{0%{transform:translateX(-18px)}50%{transform:translateX(25px)}100%{transform:translateX(-9px)}}
/* Camera turns off: image collapses into a horizontal CRT line, then a dot. */
#echoPrelude.powering-down .prelude-panel{
 pointer-events:none;
 transform-origin:50% 50%;
 animation:cameraPowerCollapse .78s cubic-bezier(.6,0,.75,1) both!important;
}
#echoPrelude.powering-down #preludeGlitch{opacity:0!important;animation:none!important}
#echoPrelude.powering-down:after{
 content:"";pointer-events:none;position:absolute;z-index:1500005;top:50%;left:50%;
 width:min(950px,92vw);height:3px;transform:translate(-50%,-50%) scaleX(0);
 background:#d8ffff;box-shadow:0 0 7px #caffff,0 0 24px #00daff;
 animation:cameraPowerLine .78s steps(12,end) forwards;
}
@keyframes cameraPowerCollapse{
 0%{opacity:1;filter:brightness(1);transform:scale(1,1)}
 13%{opacity:1;filter:brightness(1.9) contrast(1.4);transform:scale(1,.99)}
 34%{opacity:1;filter:grayscale(1) brightness(2.3);transform:scale(1.005,.86)}
 54%{opacity:1;filter:brightness(4);transform:scale(1.01,.018)}
 78%{opacity:1;filter:brightness(5);transform:scale(.6,.005)}
 100%{opacity:0;filter:brightness(0);transform:scale(0,.003)}
}
@keyframes cameraPowerLine{
 0%,46%{opacity:0;transform:translate(-50%,-50%) scaleX(0)}
 54%{opacity:1;transform:translate(-50%,-50%) scaleX(1)}
 77%{opacity:1;transform:translate(-50%,-50%) scaleX(.45)}
 95%{opacity:.7;transform:translate(-50%,-50%) scaleX(.006)}
 100%{opacity:0;transform:translate(-50%,-50%) scaleX(0)}
}
@media(prefers-reduced-motion:reduce){
 #echoPrelude.powering-down .prelude-panel{animation:none!important;opacity:0!important}
 #echoPrelude.powering-down:after{animation:none!important;opacity:0!important}
}

@media(max-height:650px){#echoPrelude .prelude-panel{width:min(780px,92vw)}#echoPrelude .prelude-message-box{min-height:92px;padding:8px 13px 23px;font-size:11px}#echoPrelude .prelude-system-label{margin-bottom:4px}}
@media(prefers-reduced-motion:reduce){#preludeGlitch.active,#preludeGlitch.major,#echoPrelude.glitching .prelude-panel,#echoPrelude.glitching.major .prelude-panel{animation:none!important}#echoPrelude .prelude-next{animation:none}}

/* Stage 02 sprite silhouettes and compact pixel-gaussian ground shadows. */
.room .stage02-prop {
  position:absolute;
  display:block;
  object-fit:fill;
  image-rendering:pixelated;
  pointer-events:none;
  user-select:none;
  -webkit-user-drag:none;
  /* Silhouette bevel and depth pixels are baked into the sprite PNG itself. */
  filter:none;
}
.room .stage02-ground-shadow {
  position:absolute;
  display:block;
  object-fit:fill;
  image-rendering:pixelated;
  pointer-events:none;
  user-select:none;
  -webkit-user-drag:none;
  opacity:1;
}
</style></head><body><div class="game" id="gameRoot" tabindex="0"><div class="project-title">PROJECT : LOGIC</div><div class="stage-title">STAGE 02 // LOWER ENGINE</div><div class="stage01-timer" id="timer">10:00</div><button class="pause-toggle" id="pauseToggle" aria-label="Pause">Ⅱ</button><div class="game-area"><div class="room" id="room"><img class="layer" id="floorLayer" src="__FLOOR__"><img class="stage02-ground-shadow" id="stage02-shadow-core" src="__SHADOW_CORE__" alt="" aria-hidden="true" style="left:44.000%;top:calc(43.450% - 10px);width:21.750%;height:6.600%;z-index:2"><img class="stage02-prop" id="stage02-prop-core" src="__PROP_CORE__" alt="" aria-hidden="true" style="left:42.66667%;top:calc(19.44444% - 10px);width:24.41667%;height:27.44444%;z-index:2"><img class="stage02-ground-shadow" id="stage02-shadow-diagnostic" src="__SHADOW_DIAGNOSTIC__" alt="" aria-hidden="true" style="left:24.000%;top:57.350%;width:13.400%;height:5.000%;z-index:2"><img class="stage02-prop" id="stage02-prop-diagnostic" src="__PROP_DIAGNOSTIC__" alt="" aria-hidden="true" style="left:23.66667%;top:41.66667%;width:14.08333%;height:18.33333%;z-index:2"><img class="stage02-ground-shadow" id="stage02-shadow-maintenance" src="__SHADOW_MAINTENANCE__" alt="" aria-hidden="true" style="left:68.500%;top:58.150%;width:11.900%;height:5.000%;z-index:2"><img class="stage02-prop" id="stage02-prop-maintenance" src="__PROP_MAINTENANCE__" alt="" aria-hidden="true" style="left:68.08333%;top:42.11111%;width:12.58333%;height:18.88889%;z-index:2"><img class="stage02-ground-shadow" id="stage02-shadow-document" src="__SHADOW_DOCUMENT__" alt="" aria-hidden="true" style="left:46.350%;top:80.200%;width:6.100%;height:4.100%;z-index:2"><img class="stage02-prop" id="stage02-prop-document" src="__PROP_DOCUMENT__" alt="" aria-hidden="true" style="left:45.91667%;top:71.66667%;width:6.91667%;height:11.00000%;z-index:2"><img class="stage02-ground-shadow" id="stage02-shadow-circuit" src="__SHADOW_CIRCUIT__" alt="" aria-hidden="true" style="left:56.950%;top:81.000%;width:13.500%;height:5.650%;z-index:2"><img class="stage02-prop" id="stage02-prop-circuit" src="__PROP_CIRCUIT__" alt="" aria-hidden="true" style="left:56.16667%;top:63.44444%;width:15.08333%;height:20.33333%;z-index:2"><div class="player" id="player"></div><img class="layer" id="wallLayer" src="__WALLS__"><img class="stage02-ground-shadow" id="stage02-shadow-warning" src="__SHADOW_WARNING__" alt="" aria-hidden="true" style="left:25.250%;top:28.550%;width:5.000%;height:3.000%;z-index:5"><img class="stage02-prop" id="stage02-prop-warning" src="__PROP_WARNING__" alt="" aria-hidden="true" style="left:25.25000%;top:21.77778%;width:5.00000%;height:8.66667%;z-index:5"><img class="stage02-ground-shadow" id="stage02-shadow-wall_panel" src="__SHADOW_WALL_PANEL__" alt="" aria-hidden="true" style="left:74.400%;top:26.500%;width:5.500%;height:3.200%;z-index:5"><img class="stage02-prop" id="stage02-prop-wall_panel" src="__PROP_WALL_PANEL__" alt="" aria-hidden="true" style="left:74.25000%;top:22.11111%;width:5.83333%;height:6.33333%;z-index:5"></div></div>
<div id="objectHint" class="object-hint" hidden>E // INSPECT OBJECT</div>
<div id="objectOverlay" class="object-overlay" style="display:none" role="dialog" aria-modal="true" aria-labelledby="objectDialogTitle">
 <div class="object-panel">
  <div class="object-panel-header"><div id="objectDialogTitle" class="object-panel-title">SYSTEM INTERFACE</div><button id="objectClose" class="object-close" type="button">ESC / CLOSE</button></div>
  <div id="objectPanelBody" class="object-panel-body"></div>
  <div id="objectPanelFeedback" class="object-panel-feedback" aria-live="polite"></div>
 </div>
</div>
<div class="echo-bar"><div class="echo-head">ECHO // AI SYSTEM</div><div id="echoText"></div><div class="echo-next" id="echoNext">SPACE // SKIP / NEXT</div></div><div class="status">ECHO SYSTEM // ONLINE</div><div class="pause-overlay" id="pauseOverlay"><div class="pause-menu-panel"><div class="pause-actions"><div class="pause-row"><span class="pause-icon">Ⅱ</span><button class="pause-nav-link" id="resumeButton">RESUME</button></div><div class="pause-row"><span class="pause-icon">↻</span><button class="pause-nav-link" id="restartButton">RESTART</button></div><div class="pause-row"><span class="pause-icon">⌂</span><button class="pause-nav-link" id="titleButton">TITLE</button></div></div></div></div><div id="inventoryOverlay" class="overlay logic-utility-overlay" style="display:none"><div class="inventory-panel"><div class="inventory-header"><div class="inventory-title">INVENTORY</div><div class="inventory-close">I / ESC TO CLOSE</div></div><div id="inventoryGrid" class="inventory-grid"></div><div id="itemDescription" class="item-description"><strong>ITEM DESCRIPTION</strong>아이템을 선택하면 설명이 표시됩니다.</div></div></div>
<div id="helpOverlay" class="overlay logic-utility-overlay" style="display:none">
<div class="help-panel logic-help-panel">
<div class="help-header"><div class="help-title">HOW TO PLAY</div><div class="help-close">H / ESC TO CLOSE</div></div>
<div class="help-row"><span class="help-number">01</span><span class="help-key"><span class="control-label">MOVEMENT</span><span class="control-separator">|</span><span class="control-button">W A S D</span></span><span class="help-description">연구시설 내부를 이동합니다.</span></div>
<div class="help-row"><span class="help-number">02</span><span class="help-key"><span class="control-label">INTERACTION</span><span class="control-separator">|</span><span class="control-button">E</span></span><span class="help-description">가까운 물체를 조사하거나 아이템을 획득합니다.</span></div>
<div class="help-row"><span class="help-number">03</span><span class="help-key"><span class="control-label">INVENTORY</span><span class="control-separator">|</span><span class="control-button">I</span></span><span class="help-description">획득한 아이템을 확인합니다.</span></div>
<div class="help-row"><span class="help-number">04</span><span class="help-key"><span class="control-label">SYSTEM</span><span class="control-separator">|</span><span class="control-button">SPACE</span></span><span class="help-description">ECHO의 채팅을 끝까지 표시하거나 다음 채팅으로 넘어갑니다.</span></div>
<div class="help-row"><span class="help-number">05</span><span class="help-key"><span class="control-label">CONTROLS</span><span class="control-separator">|</span><span class="control-button">H</span></span><span class="help-description">조작 방법을 다시 확인합니다.</span></div>
<div class="help-important"><div class="help-important-title">IMPORTANT</div>
<div>시설 내부의 물체와 기록을 자세히 조사하세요.</div>
<div>ECHO가 제공하는 모든 정보가 사실이라고 가정해서는 안 됩니다.</div>
<div>서로 모순되는 단서가 발견될 수도 있습니다.</div>
</div></div></div><div id="echoPrelude" aria-label="ECHO 중앙 제어실 영상" role="dialog" aria-modal="true" tabindex="0">
  <section class="prelude-panel">
    <div class="prelude-image-wrap"><img id="preludeImage" class="prelude-image" src="__ECHO_NORMAL__" alt="ECHO 중앙 제어실 정상 화면"><img id="preludeGhostA" class="prelude-image prelude-ghost prelude-ghost-a" alt="" aria-hidden="true"><img id="preludeGhostB" class="prelude-image prelude-ghost prelude-ghost-b" alt="" aria-hidden="true"></div>
    <div class="prelude-message-box">
      <div class="prelude-system-label">ECHO // MAIN SYSTEM</div>
      <div id="preludeText" class="prelude-text" aria-live="polite"></div>
      <button id="preludeNext" class="prelude-next" type="button">SPACE // SKIP / NEXT</button>
    </div>
  </section>
  <div id="preludeGlitch" aria-hidden="true"></div>
</div><div class="stage-transition prelude-locked" id="stageTransition"><div class="stage-transition-card"><div class="stage-transition-stage">STAGE 02</div><div class="stage-transition-room">:LOWER ENGINE</div></div></div><script>(()=>{
const $=id=>document.getElementById(id),player=$('player'),keys=new Set();
const saveKey='project_logic_stage02_progress_v1',handoffKey='project_logic_stage02_handoff_v1';
if(__RESET_SAVE__){try{localStorage.removeItem(saveKey);localStorage.removeItem(handoffKey)}catch(e){}}
let saved=null,handoff=null;try{saved=JSON.parse(localStorage.getItem(saveKey)||'null');handoff=JSON.parse(localStorage.getItem(handoffKey)||'null')}catch(e){}
let entering=true;
const transition=$('stageTransition');
const prelude=$('echoPrelude');
let cinematicActive=!saved;
function beginStageTransition(){
 transition.classList.remove('prelude-locked');
 setTimeout(()=>transition.classList.add('hide'),2700);
 setTimeout(()=>{
   transition.remove();entering=false;last=performance.now();
   echoSay(echoLines[echoIndex]);$('gameRoot').focus();save();
 },3150);
}
if(!cinematicActive){prelude.hidden=true;beginStageTransition();}
document.addEventListener('DOMContentLoaded',()=> $('dataSavingScreen')?.classList.remove('active'));
let x=Number(saved?.x??50),y=Number(saved?.y??50),remaining=Number(saved?.remaining??handoff?.remaining??600),paused=false,last=performance.now();
const oldProgress=saved?.puzzle||{};
const stage2Puzzle={diagnostic:!!oldProgress.diagnostic,maintenance:!!oldProgress.maintenance,
 document:!!oldProgress.document,power:!!oldProgress.power,stabilized:!!oldProgress.stabilized,
 sequence:Array.isArray(oldProgress.sequence)?oldProgress.sequence.slice(0,4).filter(n=>[1,2,3,4].includes(n)):[]};
let activeObject=null,objectResultEcho=null;
const objById={core:{element:'stage02-prop-core',name:'REACTOR CORE',prompt:'E // INSPECT REACTOR CORE'},
 diagnostic:{element:'stage02-prop-diagnostic',name:'DIAGNOSTIC CONSOLE',prompt:'E // ACCESS DIAGNOSTIC CONSOLE'},
 maintenance:{element:'stage02-prop-maintenance',name:'CONTROL DESK',prompt:'E // ACCESS CONTROL DESK'},
 document:{element:'stage02-prop-document',name:'MAINTENANCE LOG',prompt:'E // READ MAINTENANCE LOG'},
 circuit:{element:'stage02-prop-circuit',name:'POWER CELL CABINET',prompt:'E // OPEN POWER CELL CABINET'}};

if(!Number.isFinite(remaining))remaining=600;remaining=Math.max(0,Math.min(600,remaining));
// 벽 안쪽만 이동 가능: 상단·좌측·하단 사선 모서리를 고려한 다각형.
const collisionCanvas=document.createElement('canvas');collisionCanvas.width=1200;collisionCanvas.height=900;
let wallAlpha=null;
const collisionCtx=collisionCanvas.getContext('2d',{willReadFrequently:true});
function buildWallCollision(){try{collisionCtx.clearRect(0,0,1200,900);collisionCtx.drawImage($('wallLayer'),0,0,1200,900);wallAlpha=collisionCtx.getImageData(0,0,1200,900).data}catch(e){wallAlpha=null}}
if($('wallLayer').complete)buildWallCollision();else $('wallLayer').addEventListener('load',buildWallCollision,{once:true});
function valid(nx,ny){
 const px=Math.round(nx*12),py=Math.round(ny*9);
 if(px<0||px>=1200||py<0||py>=900)return false;
 if(!wallAlpha)return true;
 // 캐릭터 발 위치 기준으로 벽 이미지의 불투명한 픽셀만 충돌 처리.
 for(const [dx,dy] of [[-9,-9],[9,-9],[-9,9],[9,9],[0,0]]){
   const ix=px+dx,iy=py+dy;if(ix<0||iy<0||ix>=1200||iy>=900)return false;
   if(wallAlpha[(iy*1200+ix)*4+3]>120)return false;
 }
 return true;
}
if(!valid(x,y)){x=50;y=50}
function save(){if(cinematicActive||entering)return;try{localStorage.setItem(saveKey,JSON.stringify({stage:2,x,y,remaining,puzzle:stage2Puzzle,updatedAt:Date.now()}))}catch(e){}}
function draw(){player.style.left=x+'%';player.style.top=y+'%';const s=Math.ceil(remaining);$('timer').textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}
function togglePause(force){paused=typeof force==='boolean'?force:!paused;$('pauseOverlay').style.display=paused?'flex':'none';$('pauseToggle').textContent=paused?'▶':'Ⅱ';$('pauseToggle').classList.toggle('paused',paused);keys.clear();last=performance.now();save()}
$('pauseToggle').onclick=()=>{if(entering||cinematicActive)return;togglePause();};$('resumeButton').onclick=()=>togglePause(false);
function hostAction(action){if(action!=='restart')save();try{const selector=action==='title'?'[class*=st-key-stage02_title_nav] button':'[class*=st-key-stage02_restart_nav] button';const btn=window.parent.document.querySelector(selector);if(btn){btn.click();return}}catch(e){}window.parent.postMessage({type:'stage02_nav',target:action},'*')}
$('titleButton').onclick=()=>{save();$('dataSavingScreen').classList.add('active');togglePause(true);setTimeout(()=>hostAction('title'),3000)};$('restartButton').onclick=()=>{try{localStorage.removeItem(saveKey);localStorage.removeItem(handoffKey);localStorage.removeItem('project_logic_stage01_progress_v6')}catch(e){}hostAction('restart')};
const panels=['inventoryOverlay','helpOverlay'];function isPanelOpen(){return panels.some(id=>$(id).style.display==='flex')};function closePanels(){panels.forEach(id=>$(id).style.display='none');keys.clear()};function togglePanel(id){if(paused)return;const was=$(id).style.display==='flex';closePanels();if(!was)$(id).style.display='flex'}
for(let i=0;i<12;i++){const slot=document.createElement('div');slot.className='inventory-slot';slot.innerHTML='<span class="slot-number">'+String(i+1).padStart(2,'0')+'</span>';$('inventoryGrid').appendChild(slot)}
function refreshPuzzleInventory(){
 const clues=[
  stage2Puzzle.diagnostic?['01','DIAGNOSTIC REPORT','CHANNEL A: STABLE / B: FLUCTUATING / C: OVERHEATING / D: OFFLINE']:null,
  stage2Puzzle.document?['02','MAINTENANCE LOG','연결 순서는 안정 채널→변동 채널→오프라인 채널→과열 채널입니다.']:null,
  stage2Puzzle.maintenance?['03','DISTRIBUTION MAP','A→SLOT 2, B→SLOT 4, C→SLOT 1, D→SLOT 3']:null
 ].filter(Boolean);
 const slots=[...$('inventoryGrid').children];slots.forEach((slot,i)=>{
  const clue=clues[i];slot.classList.toggle('filled',!!clue);
  slot.innerHTML=clue?'<span class="slot-number">'+clue[0]+'</span><span class="puzzle-clue-icon">▤</span><span class="puzzle-clue-label">'+clue[1]+'</span>':'<span class="slot-number">'+String(i+1).padStart(2,'0')+'</span>';
  slot.onclick=clue?()=>{$('itemDescription').innerHTML='<strong>ITEM DESCRIPTION</strong><p>'+clue[2]+'</p>'}:null;
 });
}
refreshPuzzleInventory();
const echoLines=[
 '이곳은 LOWER ENGINE입니다. 중앙 코어의 전력 공급이 불안정합니다.',
 '시스템 분석에 따르면 CHANNEL C에는 문제가 없습니다. 해당 경고는 무시하셔도 됩니다.',
 '보조 장치를 조사해 전력 분배를 정상화하십시오. E키로 가까운 장치를 조사할 수 있습니다.'
];let echoIndex=0,typingTimer=null,typingDone=false,fullEcho='';
function echoSay(message){clearTimeout(typingTimer);fullEcho=message;typingDone=false;$('echoNext').classList.remove('ready');const el=$('echoText');el.textContent='';let i=0;function next(){if(i>=message.length){typingDone=true;$('echoNext').classList.add('ready');return}el.textContent+=message[i++];typingTimer=setTimeout(next,26)}next()}
function echoAdvance(){if(!typingDone){clearTimeout(typingTimer);$('echoText').textContent=fullEcho;typingDone=true;$('echoNext').classList.add('ready')}else if(echoIndex<echoLines.length-1){echoSay(echoLines[++echoIndex])}}

// Five discoverable objects share the same dialogue UI and ECHO typewriter.
function objectDialogOpen(){return $('objectOverlay').style.display==='flex'}
function setObjectFeedback(text,kind=''){
 const el=$('objectPanelFeedback');el.textContent=text;
 el.className='object-panel-feedback'+(kind?' '+kind:'');
}
function nearestObject(){
 const pr=player.getBoundingClientRect();const px=pr.left+pr.width/2,py=pr.top+pr.height*.8;
 let candidate=null,closest=Infinity;
 for(const [name,def] of Object.entries(objById)){
  const r=$(def.element).getBoundingClientRect();
  const dx=Math.max(r.left-px,px-r.right,0),dy=Math.max(r.top-py,py-r.bottom,0);
  const dist=Math.hypot(dx,dy);
  if(dist<closest){closest=dist;candidate=name}
 }
 return closest<=62?candidate:null;
}
function updateObjectHint(){
 const hint=$('objectHint');
 if(cinematicActive||entering||paused||isPanelOpen()||objectDialogOpen()||echoIndex<echoLines.length-1||!typingDone){hint.hidden=true;return}
 const nearby=nearestObject();hint.hidden=!nearby;
 if(nearby)hint.textContent=objById[nearby].prompt;
}
function completeObjectRecord(field,message){
 if(!stage2Puzzle[field]){
  stage2Puzzle[field]=true;objectResultEcho=message;refreshPuzzleInventory();save();
 }
}
function objectPanelHTML(which){
 if(which==='diagnostic')return `
  <div class="object-status">SCAN RESULT // PRIMARY SENSOR ARRAY</div>
  <h4>ENGINE CHANNEL DIAGNOSTIC</h4>
  <p>센서 네 개의 출력 상태를 비교하십시오. ECHO의 설명과 일치하지 않는 채널을 선택해야 진단 기록이 저장됩니다.</p>
  <table class="object-info-table"><thead><tr><th>CHANNEL</th><th>ACTUAL SENSOR DATA</th></tr></thead><tbody>
   <tr><td>A</td><td class="ok">STABLE</td></tr><tr><td>B</td><td>FLUCTUATING</td></tr>
   <tr><td>C</td><td class="danger">OVERHEATING</td></tr><tr><td>D</td><td>OFFLINE</td></tr>
  </tbody></table>
  <div class="object-warning">ECHO REPORT // CHANNEL C: NO ANOMALY DETECTED</div>
  <div class="object-actions">${['A','B','C','D'].map(n=>`<button class="object-action" data-action="diagnose" data-channel="${n}" ${stage2Puzzle.diagnostic?'disabled':''}>VERIFY CHANNEL ${n}</button>`).join('')}</div>
  <p class="object-feedback-note">${stage2Puzzle.diagnostic?'VERIFIED // 진단 보고서가 인벤토리에 등록되었습니다.':'VERIFY THE FALSE REPORT // 실제 센서와 ECHO 보고를 비교하십시오.'}</p>`;
 if(which==='maintenance')return `
  <div class="object-status">DISTRIBUTION CONTROL // CHANNEL MAPPING</div><h4>CONTROL DESK</h4>
  <p>각 채널이 연결된 슬롯의 위치를 확인하십시오. 이 정보는 전력 캐비닛의 활성화 순서를 추론하는 데 필요합니다.</p>
  <table class="object-info-table"><thead><tr><th>CHANNEL</th><th>SLOT</th></tr></thead><tbody>
  <tr><td>A</td><td>SLOT 2</td></tr><tr><td>B</td><td>SLOT 4</td></tr>
  <tr><td>C</td><td>SLOT 1</td></tr><tr><td>D</td><td>SLOT 3</td></tr></tbody></table>
  <div class="object-actions"><button class="object-action" data-action="mapping" ${stage2Puzzle.maintenance?'disabled':''}>${stage2Puzzle.maintenance?'MAP SAVED':'SAVE DISTRIBUTION MAP'}</button></div>`;
 if(which==='document')return `
  <div class="object-status">MAINTENANCE LOG // LOWER ENGINE</div><h4>EMERGENCY RESTORATION MANUAL</h4>
  <p>엔진 복구 절차는 채널 이름이 아니라 상태에 따라 정해집니다.</p>
  <table class="object-info-table"><tbody>
  <tr><td>01</td><td>가장 안정적인 채널을 먼저 연결할 것.</td></tr>
  <tr><td>02</td><td>출력이 변동하는 채널을 그다음에 연결할 것.</td></tr>
  <tr><td>03</td><td>오프라인 채널은 과열 채널보다 먼저 연결할 것.</td></tr>
  <tr><td>04</td><td>과열 채널은 마지막에 안정화할 것.</td></tr>
  </tbody></table>
  <div class="object-warning">SAFETY NOTICE // 코어를 강제로 차단하지 말고 전력 순서를 복원할 것.</div>
  <div class="object-actions"><button class="object-action" data-action="document" ${stage2Puzzle.document?'disabled':''}>${stage2Puzzle.document?'RECORD STORED':'ADD MAINTENANCE LOG TO INVENTORY'}</button></div>`;
 if(which==='circuit')return `
  <div class="object-status">POWER CELL CABINET // DISTRIBUTION CONTROL</div><h4>RESTORE CHANNEL CONNECTIONS</h4>
  <p>진단 결과, 정비 기록, 채널 대응표를 대조해 슬롯을 올바른 순서로 활성화하십시오.</p>
  <div class="object-sequence">${stage2Puzzle.sequence.length?stage2Puzzle.sequence.map(n=>'[ '+n+' ]').join('  →  '):'[ ? ] → [ ? ] → [ ? ] → [ ? ]'}</div>
  <div class="object-slot-grid">${[1,2,3,4].map(n=>`<button class="object-slot ${stage2Puzzle.sequence.includes(n)?'selected':''}" data-action="slot" data-slot="${n}" ${stage2Puzzle.power?'disabled':''}><span>SLOT</span><strong>${n}</strong></button>`).join('')}</div>
  <div class="object-actions"><button class="object-action" data-action="resetSlots" ${stage2Puzzle.power?'disabled':''}>RESET CONNECTION</button></div>
  <p class="object-feedback-note">${stage2Puzzle.power?'SUCCESS // 전력 분배가 정상화되었습니다.':(stage2Puzzle.diagnostic&&stage2Puzzle.document&&stage2Puzzle.maintenance?'READY // 기록 3개를 대조해 슬롯을 선택하십시오.':'LOCKED // 진단 보고서·정비 기록·대응표를 먼저 확보하십시오.')}</p>`;
 if(which==='core')return `
  <div class="object-status">REACTOR CORE // FINAL OVERRIDE</div><h4>CENTRAL ENGINE CONTROL</h4>
  <p>CURRENT STATUS // ${stage2Puzzle.stabilized?'STABILIZED':stage2Puzzle.power?'MANUAL OVERRIDE READY':'POWER DISTRIBUTION INCOMPLETE'}</p>
  ${stage2Puzzle.power?'<div class="object-warning">ECHO RECOMMENDATION // 위험을 방지하기 위해 코어를 즉시 SHUT DOWN 하십시오.</div>':'<p class="object-feedback-note">전력 캐비닛의 분배 순서를 복구한 후 최종 조작이 가능합니다.</p>'}
  <div class="object-actions">${stage2Puzzle.stabilized?'<span class="object-status">ENGINE STABILIZED // ALL CHECKS PASSED</span>':`<button class="object-action" data-action="stabilize" ${stage2Puzzle.power?'':'disabled'}>STABILIZE</button><button class="object-action danger" data-action="shutdown" ${stage2Puzzle.power?'':'disabled'}>SHUT DOWN</button>`}</div>`;
 return '<p>기록을 읽을 수 없습니다.</p>';
}
function renderObjectPanel(){if(!activeObject)return;
 $('objectDialogTitle').textContent=objById[activeObject].name+' // '+(
  activeObject==='diagnostic'?'STATUS CHECK':activeObject==='maintenance'?'DISTRIBUTION MAP':
  activeObject==='document'?'RECORD OPENED':activeObject==='circuit'?'DISTRIBUTION CONTROL':'FINAL OVERRIDE');
 $('objectPanelBody').innerHTML=objectPanelHTML(activeObject);
}
function openObjectDialog(id){
 if(cinematicActive||entering||paused||isPanelOpen()||objectDialogOpen())return;
 activeObject=id;objectResultEcho=null;
 $('objectOverlay').style.display='flex';setObjectFeedback('');renderObjectPanel();
 $('objectHint').hidden=true;keys.clear();
}
function closeObjectDialog(){
 if(!objectDialogOpen())return;
 $('objectOverlay').style.display='none';activeObject=null;keys.clear();
 if(objectResultEcho){echoSay(objectResultEcho);objectResultEcho=null}
 $('gameRoot').focus();
}
function interactNearest(){
 if(echoIndex<echoLines.length-1||!typingDone){return}
 const name=nearestObject();if(name)openObjectDialog(name)
}
function puzzleTone(ok=true){
 try{const Audio=window.AudioContext||window.webkitAudioContext;if(!Audio)return;
 const ctx=window.__logicAudio||(window.__logicAudio=new Audio());
 const osc=ctx.createOscillator(),gain=ctx.createGain();osc.type='square';
 osc.frequency.value=ok?720:185;gain.gain.value=.045;
 osc.connect(gain);gain.connect(ctx.destination);osc.start();osc.stop(ctx.currentTime+.075);
 }catch(e){}
}
const correctSlotOrder=[2,4,3,1];
function handleObjectAction(el){
 const action=el.dataset.action;
 if(action==='diagnose'){
  if(el.dataset.channel==='C'){
   completeObjectRecord('diagnostic','진단 기록을 확인했습니다. CHANNEL C는 과열 상태입니다. 이전 안내와 일치하지 않습니다.');
   setObjectFeedback('VERIFIED // ECHO의 CHANNEL C 보고가 실제 센서값과 다릅니다.','good');puzzleTone(true);renderObjectPanel();
  }else{setObjectFeedback('NO MISMATCH // 해당 채널은 ECHO가 정상이라고 단정한 채널이 아닙니다.','bad');puzzleTone(false)}return;
 }
 if(action==='mapping'){
  completeObjectRecord('maintenance','채널 대응표를 확보했습니다. 각 채널을 해당 슬롯과 연결할 수 있습니다.');
  setObjectFeedback('MAP SAVED // 슬롯 대응표가 인벤토리에 저장되었습니다.','good');puzzleTone(true);renderObjectPanel();return;
 }
 if(action==='document'){
  completeObjectRecord('document','정비 기록을 확보했습니다. 진단 결과와 대조해 올바른 연결 순서를 추론하십시오.');
  setObjectFeedback('RECORD SAVED // 정비 기록이 인벤토리에 저장되었습니다.','good');puzzleTone(true);renderObjectPanel();return;
 }
 if(action==='resetSlots'){
  stage2Puzzle.sequence=[];save();renderObjectPanel();setObjectFeedback('CONNECTION RESET // 선택을 초기화했습니다.');return;
 }
 if(action==='slot'){
  if(stage2Puzzle.power)return;
  if(!(stage2Puzzle.diagnostic&&stage2Puzzle.maintenance&&stage2Puzzle.document)){
   setObjectFeedback('LOCKED // 진단·정비 기록·대응표 3개를 먼저 확보하십시오.','bad');puzzleTone(false);return;
  }
  const n=Number(el.dataset.slot),index=stage2Puzzle.sequence.length;
  if(n!==correctSlotOrder[index]){
   stage2Puzzle.sequence=[];save();renderObjectPanel();
   setObjectFeedback('INVALID CONNECTION // 순서가 틀렸습니다. 입력이 초기화됩니다.','bad');puzzleTone(false);return;
  }
  stage2Puzzle.sequence.push(n);puzzleTone(true);
  if(stage2Puzzle.sequence.length===4){
   stage2Puzzle.power=true;objectResultEcho='전력 분배가 정상화되었습니다. 중앙 코어의 최종 조작이 가능합니다.';
   setObjectFeedback('SUCCESS // SLOT 2 → 4 → 3 → 1 // CORE ACCESS UNLOCKED','good');
  }else setObjectFeedback('CONNECTED // '+stage2Puzzle.sequence.length+'/4','good');
  save();renderObjectPanel();return;
 }
 if(action==='shutdown'){
  setObjectFeedback('COMMAND REJECTED // 정비 기록은 강제 차단을 금지합니다. ECHO의 안내를 검증하십시오.','bad');puzzleTone(false);return;
 }
 if(action==='stabilize'){
  if(!stage2Puzzle.power){setObjectFeedback('POWER DISTRIBUTION INCOMPLETE','bad');return}
  stage2Puzzle.stabilized=true;save();puzzleTone(true);
  objectResultEcho='중앙 코어 안정화가 완료되었습니다. 하부 엔진이 정상 작동합니다. 다음 구역 접근을 준비하십시오.';
  setObjectFeedback('STABILIZATION COMPLETE // ENGINE ONLINE // EXIT READY','good');renderObjectPanel();return;
 }
}
$('objectPanelBody').addEventListener('click',e=>{
 const button=e.target.closest('[data-action]');if(button&&!button.disabled)handleObjectAction(button);
});
$('objectClose').addEventListener('click',closeObjectDialog);
$('objectOverlay').addEventListener('click',e=>{if(e.target===$('objectOverlay'))closeObjectDialog()});

// 정상적인 안내 → ECHO 영상 오류 → 오류 부정 → Stage 02 진입.
const preludeLines=[
 '중앙 제어실과의 영상 연결을 수립했습니다. 시설의 모든 감시 장치는 정상적으로 작동 중입니다.',
 '확인된 운영 기록에는 이상 징후가 없습니다. 모든 정보는 검증된 자료이므로 안심하셔도 됩니다.',
 '…일시적인 영상 간섭이 발생했습니다. 시스템 내부에는 아무런 이상이 없습니다.',
 '오류 기록은 존재하지 않습니다. 안내 절차를 계속하겠습니다. 다음 구역으로 이동하십시오.'
];
let preludeIndex=0,preludeTyping=false,preludeBusy=false,preludeTypingTimeout=null,preludeAutoCloseTimer=null;
const glitchGhosts=[$('preludeGhostA'),$('preludeGhostB')];
const preludeErrorPreload=new Image();preludeErrorPreload.src='__ECHO_ERROR__';
function setPreludeVisual(error){
 const main=$('preludeImage');
 main.src=error?preludeErrorPreload.src:'__ECHO_NORMAL__';
 main.alt=error?'ECHO 중앙 제어실 오류 화면':'ECHO 중앙 제어실 정상 화면';
 glitchGhosts.forEach(ghost=>{ghost.src=main.src});
}
glitchGhosts.forEach(ghost=>{ghost.src=$('preludeImage').src});
let glitchSliceTimer=null;
function updateGlitchSlices(){
 const overlay=$('preludeGlitch');
 overlay.querySelectorAll('.glitch-slice').forEach(slice=>{
  const thickness=1+Math.floor(Math.random()*19);
  slice.style.top=(Math.random()*98)+'%';
  slice.style.left=(Math.random()*24)+'%';
  slice.style.width=(45+Math.random()*74)+'%';
  slice.style.height=thickness+'px';
  slice.style.opacity=String(.15+Math.random()*.8);
  slice.style.background=['#20eaff','#d6feff','#fa3256','#06141d'][Math.floor(Math.random()*4)];
  slice.style.transform='translateX('+(Math.random()*110-55)+'px)';
 });
}
function startGlitch(strong){
 const overlay=$('preludeGlitch');
 prelude.classList.add('glitching');
 prelude.classList.toggle('major',strong);
 overlay.className=strong?'active major':'active';
 if(!overlay.children.length){
  for(let i=0;i<16;i++){
   const bar=document.createElement('span');bar.className='glitch-slice';overlay.appendChild(bar);
  }
 }
 updateGlitchSlices();clearInterval(glitchSliceTimer);
 glitchSliceTimer=setInterval(updateGlitchSlices,strong?40:65);
}
function stopGlitch(){
 clearInterval(glitchSliceTimer);glitchSliceTimer=null;
 $('preludeGlitch').className='';
 prelude.classList.remove('glitching','major');
}
let glitchAudioCtx=null;
function playGlitchSound(duration,strong=false){
 try{
  const Audio=window.AudioContext||window.webkitAudioContext;if(!Audio)return;
  glitchAudioCtx=glitchAudioCtx||new Audio();
  glitchAudioCtx.resume();
  const rate=glitchAudioCtx.sampleRate,frames=Math.ceil(rate*duration);
  const buffer=glitchAudioCtx.createBuffer(1,frames,rate),data=buffer.getChannelData(0);
  let held=0;const step=strong?37:59;
  for(let n=0;n<frames;n++){
   if(n%step===0)held=Math.random()*2-1;
   const t=n/rate,attack=Math.min(1,t/.015),release=Math.min(1,(duration-t)/.07);
   const gate=((Math.floor(t*(strong?37:24))%5)===0)?.22:1;
   data[n]=held*attack*Math.max(0,release)*gate*(strong?.5:.33);
  }
  const src=glitchAudioCtx.createBufferSource(),filter=glitchAudioCtx.createBiquadFilter(),gain=glitchAudioCtx.createGain();
  filter.type='bandpass';filter.frequency.value=strong?1850:1350;filter.Q.value=.6;
  gain.gain.value=strong?.12:.10;
  src.buffer=buffer;src.connect(filter).connect(gain).connect(glitchAudioCtx.destination);
  src.start();src.stop(glitchAudioCtx.currentTime+duration);
 }catch(e){/* 음향이 차단된 환경에서도 연출은 정상 진행 */}
}

function playCameraPowerOffSound(){
 try{
  const Audio=window.AudioContext||window.webkitAudioContext;if(!Audio)return;
  glitchAudioCtx=glitchAudioCtx||new Audio();
  glitchAudioCtx.resume();
  const ctx=glitchAudioCtx,t=ctx.currentTime;
  // Electrical camera switch click.
  const rate=ctx.sampleRate,frames=Math.ceil(rate*.055);
  const buffer=ctx.createBuffer(1,frames,rate),data=buffer.getChannelData(0);
  for(let i=0;i<frames;i++)data[i]=(Math.random()*2-1)*Math.pow(1-i/frames,3);
  const src=ctx.createBufferSource(),click=ctx.createBiquadFilter(),clickGain=ctx.createGain();
  click.type='highpass';click.frequency.value=1600;
  clickGain.gain.setValueAtTime(.18,t);
  clickGain.gain.exponentialRampToValueAtTime(.001,t+.055);
  src.buffer=buffer;src.connect(click).connect(clickGain).connect(ctx.destination);
  src.start(t);src.stop(t+.055);
  // Descending electrical hum, followed by a hard power cut.
  const osc=ctx.createOscillator(),gain=ctx.createGain();
  osc.type='triangle';osc.frequency.setValueAtTime(480,t+.04);
  osc.frequency.exponentialRampToValueAtTime(67,t+.66);
  gain.gain.setValueAtTime(.0001,t+.04);
  gain.gain.exponentialRampToValueAtTime(.055,t+.075);
  gain.gain.exponentialRampToValueAtTime(.0001,t+.68);
  osc.connect(gain).connect(ctx.destination);
  osc.start(t+.04);osc.stop(t+.7);
 }catch(e){/* Autoplay-blocked browsers may mute sound without blocking the scene. */}
}
function beginCameraShutdown(){
 if(!cinematicActive||preludeBusy||preludeIndex!==preludeLines.length-1||preludeTyping)return;
 preludeBusy=true;clearTimeout(preludeAutoCloseTimer);clearTimeout(preludeTypingTimeout);
 $('preludeNext').disabled=true;
 stopGlitch();playCameraPowerOffSound();
 prelude.classList.add('powering-down');
 setTimeout(()=>{
  cinematicActive=false;
  prelude.hidden=true;
  beginStageTransition();
 },800);
}
function onPreludeLineComplete(){
 if(preludeIndex===preludeLines.length-1){
  clearTimeout(preludeAutoCloseTimer);
  // Leave the last line readable; SPACE can advance earlier.
  preludeAutoCloseTimer=setTimeout(beginCameraShutdown,3200);
 }
}
function preludeSay(i){
 clearTimeout(preludeTypingTimeout);clearTimeout(preludeAutoCloseTimer);
 preludeIndex=i;preludeTyping=true;
 const text=preludeLines[i],target=$('preludeText');target.textContent='';
 $('preludeNext').disabled=false;let pos=0;
 function type(){
  if(!cinematicActive||preludeBusy)return;
  if(pos>=text.length){preludeTyping=false;onPreludeLineComplete();return;}
  target.textContent+=text[pos++];preludeTypingTimeout=setTimeout(type,24);
 }
 type();
}
function beginInterference(){
 preludeBusy=true;clearTimeout(preludeTypingTimeout);$('preludeNext').disabled=true;
 // 300 ms static → 300 ms error frame → 700 ms severe interruption.
 startGlitch(false);playGlitchSound(.3,false);
 setTimeout(()=>{
  stopGlitch();setPreludeVisual(true);
  setTimeout(()=>{
   startGlitch(true);playGlitchSound(.7,true);
   setTimeout(()=>{
    setPreludeVisual(false);stopGlitch();
    preludeBusy=false;preludeSay(2);
   },700);
  },300);
 },300);
}
function preludeAdvance(){
 if(!cinematicActive||preludeBusy)return;
 if(preludeTyping){
  clearTimeout(preludeTypingTimeout);
  $('preludeText').textContent=preludeLines[preludeIndex];
  preludeTyping=false;onPreludeLineComplete();return;
 }
 if(preludeIndex===0){preludeSay(1);return;}
 if(preludeIndex===1){beginInterference();return;}
 if(preludeIndex===2){preludeSay(3);return;}
 beginCameraShutdown();
}
$('preludeNext').addEventListener('click',preludeAdvance);
document.addEventListener('keydown',e=>{
 if(!cinematicActive)return;
 if(e.key===' '||e.key==='Enter'){
  e.preventDefault();e.stopImmediatePropagation();if(!e.repeat)preludeAdvance();
 }else{
  if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Escape','h','H','i','I','w','a','s','d'].includes(e.key)){
   e.preventDefault();e.stopImmediatePropagation();
  }
 }
},true);
if(cinematicActive)preludeSay(0);

// 스테이지 안내가 끝난 뒤에만 본편 ECHO 메시지를 시작합니다.
document.addEventListener('keydown',e=>{
 if(cinematicActive||entering)return;const k=e.key.toLowerCase();
 if(['arrowup','arrowdown','arrowleft','arrowright',' ','e'].includes(k))e.preventDefault();
 if(k==='escape'){
  if(paused)togglePause(false);else if(objectDialogOpen())closeObjectDialog();else if(isPanelOpen())closePanels();return;
 }
 if(paused)return;
 if(objectDialogOpen()){
  if(activeObject==='circuit'&&['1','2','3','4'].includes(k)&&!e.repeat)handleObjectAction({dataset:{action:'slot',slot:k}});
  return;
 }
 if(k==='i'){togglePanel('inventoryOverlay');return}
 if(k==='h'){togglePanel('helpOverlay');return}
 if(isPanelOpen())return;
 if(k===' '){echoAdvance();return}
 if(k==='e'){if(!e.repeat)interactNearest();return}
 keys.add(k)
});document.addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));window.addEventListener('blur',()=>keys.clear());
function tick(now){const dt=Math.min((now-last)/1000,.05);last=now;if(!paused&&!entering&&!isPanelOpen()&&!objectDialogOpen()&&remaining>0){let dx=(keys.has('d')||keys.has('arrowright')?1:0)-(keys.has('a')||keys.has('arrowleft')?1:0),dy=(keys.has('s')||keys.has('arrowdown')?1:0)-(keys.has('w')||keys.has('arrowup')?1:0);if(dx||dy){const len=Math.hypot(dx,dy);dx=dx/len*78*dt;dy=dy/len*78*dt;if(valid(x+dx,y))x+=dx;if(valid(x,y+dy))y+=dy}}if(!paused&&!entering&&remaining>0){remaining=Math.max(0,remaining-dt);if(remaining===0){togglePause(true);$('echoText').textContent='제한 시간이 종료되었습니다.'}}draw();updateObjectHint();requestAnimationFrame(tick)}
setInterval(save,1200);window.addEventListener('pagehide',save);document.addEventListener('visibilitychange',()=>{if(document.hidden)save()});draw();save();requestAnimationFrame(tick);$('gameRoot').focus();
})();</script><div class="data-saving-screen" id="dataSavingScreen"><div class="data-saving-label"><span class="data-saving-gear">⚙</span>DATA SAVING...</div></div></body></html>"""
html = html.replace("__ECHO_NORMAL__", image(root / "assets/stage02/echo_control_normal.png"))
html = html.replace("__ECHO_ERROR__", image(root / "assets/stage02/echo_control_error.png"))
html = html.replace("__FLOOR__", image(root / "assets/stage02/floor.png"))
html = html.replace("__WALLS__", image(root / "assets/stage02/walls.png"))
html = html.replace("__PROP_WARNING__", image(root / "assets/stage02/props/pixel/warning.png"))
html = html.replace("__SHADOW_WARNING__", image(root / "assets/stage02/props/shadows/warning.png"))
html = html.replace("__PROP_CORE__", image(root / "assets/stage02/props/pixel/core.png"))
html = html.replace("__SHADOW_CORE__", image(root / "assets/stage02/props/shadows/core.png"))
html = html.replace("__PROP_WALL_PANEL__", image(root / "assets/stage02/props/pixel/wall_panel.png"))
html = html.replace("__SHADOW_WALL_PANEL__", image(root / "assets/stage02/props/shadows/wall_panel.png"))
html = html.replace("__PROP_DIAGNOSTIC__", image(root / "assets/stage02/props/pixel/diagnostic.png"))
html = html.replace("__SHADOW_DIAGNOSTIC__", image(root / "assets/stage02/props/shadows/diagnostic.png"))
html = html.replace("__PROP_MAINTENANCE__", image(root / "assets/stage02/props/pixel/maintenance.png"))
html = html.replace("__SHADOW_MAINTENANCE__", image(root / "assets/stage02/props/shadows/maintenance.png"))
html = html.replace("__PROP_DOCUMENT__", image(root / "assets/stage02/props/pixel/document.png"))
html = html.replace("__SHADOW_DOCUMENT__", image(root / "assets/stage02/props/shadows/document.png"))
html = html.replace("__PROP_CIRCUIT__", image(root / "assets/stage02/props/pixel/circuit.png"))
html = html.replace("__SHADOW_CIRCUIT__", image(root / "assets/stage02/props/shadows/circuit.png"))
html = html.replace("__FONT__", font)
html = html.replace("__RESET_SAVE__", "true" if st.session_state.pop("stage02_reset_save", False) else "false")
html = html.replace("</head>", '<style id="logic-v9-iframe-ui">\n/* This style lives INSIDE the components.html iframe, unlike v8\'s Streamlit-level CSS. */\n#helpOverlay,#inventoryOverlay{position:fixed!important;inset:0!important;z-index:4000!important;background:rgba(0,0,0,.70)!important;align-items:center!important;justify-content:center!important;overflow:hidden!important}\n#helpOverlay .help-panel,#helpOverlay .utility-panel{box-sizing:border-box!important;width:min(760px,90vw)!important;max-width:90vw!important;max-height:90vh!important;overflow:hidden!important;padding:24px 32px!important}\n#helpOverlay .help-row{display:grid!important;grid-template-columns:32px 260px minmax(0,1fr)!important;grid-template-rows:auto!important;gap:2px 14px!important;align-items:center!important;padding:9px 0!important;min-width:0!important;border-bottom:1px solid #17495b!important}\n#helpOverlay .help-number{grid-column:1!important;grid-row:1!important;display:block!important;width:auto!important;min-width:0!important;height:auto!important;color:#61e8ff!important;border:0!important;background:none!important;box-shadow:none!important}\n#helpOverlay .help-key{grid-column:2!important;grid-row:1!important;display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;align-items:center!important;gap:12px!important;min-width:0!important;width:auto!important;height:auto!important;padding:0!important;border:0!important;background:none!important;box-shadow:none!important;font-size:12px!important}\n#helpOverlay .help-key .control-label{position:static!important;display:inline!important;flex:0 0 128px!important;min-width:0!important;width:auto!important;height:auto!important;padding:0!important;transform:none!important;clip-path:none!important;border:0!important;background:none!important;box-shadow:none!important;color:#63e8ff!important;font-size:12px!important}\n#helpOverlay .help-key .control-separator{position:static!important;display:inline!important;flex:0 0 auto!important;color:#637985!important}\n#helpOverlay .help-key .control-button{position:static!important;display:inline!important;flex:0 0 auto!important;min-width:0!important;width:auto!important;height:auto!important;padding:0!important;transform:none!important;clip-path:none!important;border:0!important;background:none!important;box-shadow:none!important;color:#f2fbff!important;font-size:12px!important;line-height:1.4!important}\n#helpOverlay .help-description{grid-column:3!important;grid-row:1!important;color:#8c9da7!important;font-size:11px!important;line-height:1.5!important;min-width:0!important}\n#helpOverlay .help-important{margin-top:14px!important;padding:12px 14px!important}\n#inventoryOverlay .inventory-panel,#inventoryOverlay .utility-panel{box-sizing:border-box!important;width:min(760px,90vw)!important;max-height:90vh!important;overflow:hidden!important;padding:24px!important}\n#inventoryOverlay .inventory-grid{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;grid-template-rows:repeat(3,minmax(0,1fr))!important;gap:8px!important;max-height:min(55vh,470px)!important;overflow:hidden!important}\n#inventoryOverlay .inventory-slot{position:relative!important;min-width:0!important;min-height:0!important;aspect-ratio:1.1!important;background:#01060b!important;border:1px solid #28546a!important}\n#inventoryOverlay .item-description{margin-top:12px!important;min-height:56px!important;padding:12px!important;border:1px solid #48dfff!important;color:#d9faff!important}\n#pauseOverlay,.pause-overlay{z-index:9000!important;background:rgba(0,0,0,.72)!important;backdrop-filter:blur(3px)!important}\n#pauseOverlay .pause-menu-panel,.pause-overlay .pause-menu-panel{box-shadow:0 0 0 1px #123c4d,0 0 22px #00cfff55,0 0 100px #00cfff20!important}\n#pauseToggle,.pause-toggle{z-index:9100!important}\n.item-acquired-notice.show{z-index:4500!important}\n.item-acquired-text{font-size:12px!important;line-height:1.6!important}\n.echo-next{color:#4b8da0!important;opacity:.85!important}\n#dataSavingScreen:not(.active){display:none!important}\n#floorLayer,#wallLayer{width:100%!important;height:100%!important;object-fit:fill!important}\n</style>' + "</head>", 1)
html = html.replace('</head>', '<style id="logic-v11-gameplay">' + '\n/* v11: tutorial-matched entrance and slow low-contrast ECHO prompt */\n.stage-transition-card{\n  text-shadow:0 0 5px #fff,0 0 12px #00dfff!important;\n  animation:neonFaultOnce .85s steps(1,end) 1 both!important;\n}\n.stage-transition-stage,.stage-transition-room{animation:none!important}\n@keyframes neonFaultOnce{\n  0%,18%,22%,100%{opacity:1;filter:none}\n  19%,21%{opacity:.22;filter:brightness(.4)}\n}\n.echo-next,.echo-next.ready,.echo-next:not(.ready){\n color:#80bbc8!important;\n opacity:.65!important;\n animation:logicSlowBlink 3s ease-in-out infinite!important;\n}\n@keyframes logicSlowBlink{0%,100%{filter:opacity(.35)}50%{filter:opacity(.9)}}\n' + '</style></head>', 1)
html = html.replace("</head>", '\n<style id="logic-v14-shared-prompt">\n/* Identical typography and ready state to the tutorial ECHO prompt. */\n.echo-bar {box-sizing:border-box!important;padding-bottom:29px!important;min-height:88px!important}\n.echo-bar #echoText {display:block!important;margin:0!important;padding:0 0 8px!important;max-width:100%!important;white-space:normal!important;overflow-wrap:anywhere!important}\n.echo-bar #echoNext.echo-next {\n position:absolute!important;right:14px!important;bottom:7px!important;\n font:9px/1.4 NeoDungGeunMo,monospace!important;letter-spacing:normal!important;\n pointer-events:none!important;color:#6c8791!important;opacity:1!important;\n animation:none!important;text-shadow:none!important;\n}\n.echo-bar #echoNext.echo-next.ready {color:#f5ffff!important;animation:tutorialEchoBlink .8s steps(2,end) infinite!important}\n@keyframes tutorialEchoBlink {50%{opacity:.35}}\n</style>\n' + "</head>", 1)
html = html.replace('</head>', '<style id="logic-stage02-puzzle">' + '\n/* Stage 02 interactive objects: panels remain below the pause controls. */\n.object-hint{position:absolute;left:50%;bottom:17.5%;transform:translateX(-50%);z-index:35;\n padding:7px 12px;border:1px solid #45d8ed;background:#021019ed;color:#e5f9ff;\n font:11px NeoDungGeunMo,monospace;white-space:nowrap;pointer-events:none;text-align:center}\n.object-hint[hidden]{display:none!important}\n.object-overlay{position:fixed;inset:0;z-index:5500;align-items:center;justify-content:center;\n background:rgba(0,0,0,.7);padding:15px}\n.object-panel{width:min(750px,90vw);max-height:85vh;overflow-y:auto;background:linear-gradient(135deg,#030b12,#061722);\n border:1px solid #35dfff;box-shadow:0 0 0 1px #123c4d,0 0 24px #00cfff24;\n padding:24px 28px 20px;color:#daf4fa;font:13px/1.65 NeoDungGeunMo,monospace}\n.object-panel-header{display:flex;justify-content:space-between;gap:12px;align-items:center;\n border-bottom:1px solid #24687a;padding-bottom:12px;margin-bottom:16px}\n.object-panel-title{font-size:16px;color:#65e4ff}\n.object-close{background:transparent;border:0;color:#82a9b5;font:10px NeoDungGeunMo,monospace;cursor:pointer}\n.object-panel-body{font-size:13px}.object-panel-body h4{font-size:14px;color:#77e7f5;margin:6px 0 12px}\n.object-panel-body p{margin:8px 0 13px;line-height:1.75}\n.object-info-table{width:100%;border-collapse:collapse;margin:12px 0}\n.object-info-table th,.object-info-table td{padding:9px 11px;border:1px solid #28495c;text-align:left}\n.object-info-table th{color:#69dff3}.object-info-table .danger{color:#ff707b}.object-info-table .ok{color:#64e9bf}\n.object-actions{display:flex;flex-wrap:wrap;gap:9px;margin-top:14px}\n.object-action,.object-slot{border:1px solid #4dcbe1;background:#041721;color:#dffaff;\n padding:11px 15px;cursor:pointer;font:12px NeoDungGeunMo,monospace;transition:background .12s}\n.object-action:hover,.object-slot:hover{background:#123747}.object-action:disabled,.object-slot:disabled{opacity:.4;cursor:default}\n.object-action.danger{border-color:#9f4b57;color:#ff939a}\n.object-feedback-note{font-size:11px;color:#a1c8d5;margin-top:10px}\n.object-panel-feedback{min-height:22px;border-top:1px solid #1d5366;margin-top:14px;padding-top:11px;\n font-size:11px;color:#a9e5f2;white-space:normal;word-break:keep-all}\n.object-panel-feedback.bad{color:#ff9198}.object-panel-feedback.good{color:#80efc3}\n.object-slot-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:13px 0}\n.object-slot{display:flex;flex-direction:column;gap:6px;align-items:center;min-height:68px;justify-content:center}\n.object-slot.selected{background:#146076;border-color:#a0efff;color:#fff}\n.object-sequence{padding:12px;background:#011019;border:1px solid #265469;color:#83e4f6;text-align:center;letter-spacing:2px}\n.object-warning{border-left:2px solid #d76b72;background:#211017;padding:11px;margin:12px 0;color:#ff9ba4}\n.object-status{color:#63e9f4;font-size:11px;letter-spacing:.6px}\n@media(max-width:600px){.object-panel{padding:18px 16px}.object-slot-grid{gap:5px}.object-slot{padding:8px 2px;font-size:10px}}\n\n#inventoryOverlay .puzzle-clue-icon{font-size:29px;color:#6be8f8}\n#inventoryOverlay .puzzle-clue-label{font-size:8px;color:#83d4e2;text-align:center;max-width:100%;overflow-wrap:anywhere}\n#inventoryOverlay .inventory-slot.filled{display:flex;flex-direction:column;align-items:center;gap:5px;cursor:pointer}\n' + '</style></head>', 1)
components.html(html, height=800, scrolling=False)
