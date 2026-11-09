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
.project-title{position:absolute;top:32px;left:24px;font-size:15px;color:#fff;z-index:20}.stage-title{position:absolute;top:56px;left:24px;font-size:12px;color:#426b7d;z-index:20}
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

</style></head><body><div class="game" id="gameRoot" tabindex="0"><div class="project-title">PROJECT : LOGIC</div><div class="stage-title">STAGE 02 // LOWER ENGINE</div><div class="stage01-timer" id="timer">10:00</div><button class="pause-toggle" id="pauseToggle" aria-label="Pause">Ⅱ</button><div class="game-area"><div class="room" id="room"><img class="layer" id="floorLayer" src="__FLOOR__"><div class="player" id="player"></div><img class="layer" id="wallLayer" src="__WALLS__"></div></div><div class="echo-bar"><div class="echo-head">ECHO // AI SYSTEM</div><div id="echoText"></div><div class="echo-next" id="echoNext">SPACE // SKIP / NEXT</div></div><div class="status">ECHO SYSTEM // ONLINE</div><div class="pause-overlay" id="pauseOverlay"><div class="pause-menu-panel"><div class="pause-actions"><div class="pause-row"><span class="pause-icon">Ⅱ</span><button class="pause-nav-link" id="resumeButton">RESUME</button></div><div class="pause-row"><span class="pause-icon">↻</span><button class="pause-nav-link" id="restartButton">RESTART</button></div><div class="pause-row"><span class="pause-icon">⌂</span><button class="pause-nav-link" id="titleButton">TITLE</button></div></div></div></div><div id="inventoryOverlay" class="overlay logic-utility-overlay" style="display:none"><div class="inventory-panel"><div class="inventory-header"><div class="inventory-title">INVENTORY</div><div class="inventory-close">I / ESC TO CLOSE</div></div><div id="inventoryGrid" class="inventory-grid"></div><div id="itemDescription" class="item-description"><strong>ITEM DESCRIPTION</strong>아이템을 선택하면 설명이 표시됩니다.</div></div></div>
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
</div></div></div><div class="stage-transition" id="stageTransition"><div class="stage-transition-card"><div class="stage-transition-stage">STAGE 02</div><div class="stage-transition-room">:LOWER ENGINE</div></div></div><script>(()=>{
const $=id=>document.getElementById(id),player=$('player'),keys=new Set();
const saveKey='project_logic_stage02_progress_v1',handoffKey='project_logic_stage02_handoff_v1';
if(__RESET_SAVE__){try{localStorage.removeItem(saveKey);localStorage.removeItem(handoffKey)}catch(e){}}
let saved=null,handoff=null;try{saved=JSON.parse(localStorage.getItem(saveKey)||'null');handoff=JSON.parse(localStorage.getItem(handoffKey)||'null')}catch(e){}
let entering=true;const transition=$('stageTransition');setTimeout(()=>transition.classList.add('hide'),2700);setTimeout(()=>{transition.remove();entering=false;last=performance.now();$('gameRoot').focus()},3150);
document.addEventListener('DOMContentLoaded',()=> $('dataSavingScreen')?.classList.remove('active'));
let x=Number(saved?.x??50),y=Number(saved?.y??50),remaining=Number(saved?.remaining??handoff?.remaining??600),paused=false,last=performance.now();
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
function save(){try{localStorage.setItem(saveKey,JSON.stringify({stage:2,x,y,remaining,updatedAt:Date.now()}))}catch(e){}}
function draw(){player.style.left=x+'%';player.style.top=y+'%';const s=Math.ceil(remaining);$('timer').textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}
function togglePause(force){paused=typeof force==='boolean'?force:!paused;$('pauseOverlay').style.display=paused?'flex':'none';$('pauseToggle').textContent=paused?'▶':'Ⅱ';$('pauseToggle').classList.toggle('paused',paused);keys.clear();last=performance.now();save()}
$('pauseToggle').onclick=()=>togglePause();$('resumeButton').onclick=()=>togglePause(false);
function hostAction(action){if(action!=='restart')save();try{const selector=action==='title'?'[class*=st-key-stage02_title_nav] button':'[class*=st-key-stage02_restart_nav] button';const btn=window.parent.document.querySelector(selector);if(btn){btn.click();return}}catch(e){}window.parent.postMessage({type:'stage02_nav',target:action},'*')}
$('titleButton').onclick=()=>{save();$('dataSavingScreen').classList.add('active');togglePause(true);setTimeout(()=>hostAction('title'),3000)};$('restartButton').onclick=()=>{try{localStorage.removeItem(saveKey);localStorage.removeItem(handoffKey);localStorage.removeItem('project_logic_stage01_progress_v6')}catch(e){}hostAction('restart')};
const panels=['inventoryOverlay','helpOverlay'];function isPanelOpen(){return panels.some(id=>$(id).style.display==='flex')};function closePanels(){panels.forEach(id=>$(id).style.display='none');keys.clear()};function togglePanel(id){if(paused)return;const was=$(id).style.display==='flex';closePanels();if(!was)$(id).style.display='flex'}
for(let i=0;i<12;i++){const slot=document.createElement('div');slot.className='inventory-slot';slot.innerHTML='<span class="slot-number">'+String(i+1).padStart(2,'0')+'</span>';$('inventoryGrid').appendChild(slot)}
const echoLines=['연결이 확인되었습니다. 저는 ECHO입니다. 이 시설에서의 첫 번째 절차를 안내하겠습니다.'];let echoIndex=0,typingTimer=null,typingDone=false,fullEcho='';
function echoSay(message){clearTimeout(typingTimer);fullEcho=message;typingDone=false;$('echoNext').classList.remove('ready');const el=$('echoText');el.textContent='';let i=0;function next(){if(i>=message.length){typingDone=true;$('echoNext').classList.add('ready');return}el.textContent+=message[i++];typingTimer=setTimeout(next,26)}next()}
function echoAdvance(){if(!typingDone){clearTimeout(typingTimer);$('echoText').textContent=fullEcho;typingDone=true;$('echoNext').classList.add('ready')}else if(echoIndex<echoLines.length-1){echoSay(echoLines[++echoIndex])}}
echoSay(echoLines[echoIndex]);
document.addEventListener('keydown',e=>{const k=e.key.toLowerCase();if(['arrowup','arrowdown','arrowleft','arrowright',' '].includes(k))e.preventDefault();if(k==='escape'){if(isPanelOpen())closePanels();else if(paused)togglePause(false);return}if(k==='i'){togglePanel('inventoryOverlay');return}if(k==='h'){togglePanel('helpOverlay');return}if(k===' '){if(!paused&&!isPanelOpen())echoAdvance();return}keys.add(k)});document.addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));window.addEventListener('blur',()=>keys.clear());
function tick(now){const dt=Math.min((now-last)/1000,.05);last=now;if(!paused&&!entering&&!isPanelOpen()&&remaining>0){let dx=(keys.has('d')||keys.has('arrowright')?1:0)-(keys.has('a')||keys.has('arrowleft')?1:0),dy=(keys.has('s')||keys.has('arrowdown')?1:0)-(keys.has('w')||keys.has('arrowup')?1:0);if(dx||dy){const len=Math.hypot(dx,dy);dx=dx/len*78*dt;dy=dy/len*78*dt;if(valid(x+dx,y))x+=dx;if(valid(x,y+dy))y+=dy}}if(!paused&&!entering&&remaining>0){remaining=Math.max(0,remaining-dt);if(remaining===0){togglePause(true);$('echoText').textContent='제한 시간이 종료되었습니다.'}}draw();requestAnimationFrame(tick)}
setInterval(save,1200);window.addEventListener('pagehide',save);document.addEventListener('visibilitychange',()=>{if(document.hidden)save()});draw();save();requestAnimationFrame(tick);$('gameRoot').focus();
})();</script><div class="data-saving-screen" id="dataSavingScreen"><div class="data-saving-label"><span class="data-saving-gear">⚙</span>DATA SAVING...</div></div></body></html>"""
html = html.replace("__FLOOR__", image(root / "assets/stage02/floor.png"))
html = html.replace("__WALLS__", image(root / "assets/stage02/walls.png"))
html = html.replace("__FONT__", font)
html = html.replace("__RESET_SAVE__", "true" if st.session_state.pop("stage02_reset_save", False) else "false")
html = html.replace("</head>", '<style id="logic-v9-iframe-ui">\n/* This style lives INSIDE the components.html iframe, unlike v8\'s Streamlit-level CSS. */\n#helpOverlay,#inventoryOverlay{position:fixed!important;inset:0!important;z-index:4000!important;background:rgba(0,0,0,.70)!important;align-items:center!important;justify-content:center!important;overflow:hidden!important}\n#helpOverlay .help-panel,#helpOverlay .utility-panel{box-sizing:border-box!important;width:min(760px,90vw)!important;max-width:90vw!important;max-height:90vh!important;overflow:hidden!important;padding:24px 32px!important}\n#helpOverlay .help-row{display:grid!important;grid-template-columns:32px 260px minmax(0,1fr)!important;grid-template-rows:auto!important;gap:2px 14px!important;align-items:center!important;padding:9px 0!important;min-width:0!important;border-bottom:1px solid #17495b!important}\n#helpOverlay .help-number{grid-column:1!important;grid-row:1!important;display:block!important;width:auto!important;min-width:0!important;height:auto!important;color:#61e8ff!important;border:0!important;background:none!important;box-shadow:none!important}\n#helpOverlay .help-key{grid-column:2!important;grid-row:1!important;display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;align-items:center!important;gap:12px!important;min-width:0!important;width:auto!important;height:auto!important;padding:0!important;border:0!important;background:none!important;box-shadow:none!important;font-size:12px!important}\n#helpOverlay .help-key .control-label{position:static!important;display:inline!important;flex:0 0 128px!important;min-width:0!important;width:auto!important;height:auto!important;padding:0!important;transform:none!important;clip-path:none!important;border:0!important;background:none!important;box-shadow:none!important;color:#63e8ff!important;font-size:12px!important}\n#helpOverlay .help-key .control-separator{position:static!important;display:inline!important;flex:0 0 auto!important;color:#637985!important}\n#helpOverlay .help-key .control-button{position:static!important;display:inline!important;flex:0 0 auto!important;min-width:0!important;width:auto!important;height:auto!important;padding:0!important;transform:none!important;clip-path:none!important;border:0!important;background:none!important;box-shadow:none!important;color:#f2fbff!important;font-size:12px!important;line-height:1.4!important}\n#helpOverlay .help-description{grid-column:3!important;grid-row:1!important;color:#8c9da7!important;font-size:11px!important;line-height:1.5!important;min-width:0!important}\n#helpOverlay .help-important{margin-top:14px!important;padding:12px 14px!important}\n#inventoryOverlay .inventory-panel,#inventoryOverlay .utility-panel{box-sizing:border-box!important;width:min(760px,90vw)!important;max-height:90vh!important;overflow:hidden!important;padding:24px!important}\n#inventoryOverlay .inventory-grid{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;grid-template-rows:repeat(3,minmax(0,1fr))!important;gap:8px!important;max-height:min(55vh,470px)!important;overflow:hidden!important}\n#inventoryOverlay .inventory-slot{position:relative!important;min-width:0!important;min-height:0!important;aspect-ratio:1.1!important;background:#01060b!important;border:1px solid #28546a!important}\n#inventoryOverlay .item-description{margin-top:12px!important;min-height:56px!important;padding:12px!important;border:1px solid #48dfff!important;color:#d9faff!important}\n#pauseOverlay,.pause-overlay{z-index:9000!important;background:rgba(0,0,0,.72)!important;backdrop-filter:blur(3px)!important}\n#pauseOverlay .pause-menu-panel,.pause-overlay .pause-menu-panel{box-shadow:0 0 0 1px #123c4d,0 0 22px #00cfff55,0 0 100px #00cfff20!important}\n#pauseToggle,.pause-toggle{z-index:9100!important}\n.item-acquired-notice.show{z-index:4500!important}\n.item-acquired-text{font-size:12px!important;line-height:1.6!important}\n.echo-next{color:#4b8da0!important;opacity:.85!important}\n#dataSavingScreen:not(.active){display:none!important}\n#floorLayer,#wallLayer{width:100%!important;height:100%!important;object-fit:fill!important}\n</style>' + "</head>", 1)
html = html.replace('</head>', '<style id="logic-v11-gameplay">' + '\n/* v11: tutorial-matched entrance and slow low-contrast ECHO prompt */\n.stage-transition-card{\n  text-shadow:0 0 5px #fff,0 0 12px #00dfff!important;\n  animation:neonFaultOnce .85s steps(1,end) 1 both!important;\n}\n.stage-transition-stage,.stage-transition-room{animation:none!important}\n@keyframes neonFaultOnce{\n  0%,18%,22%,100%{opacity:1;filter:none}\n  19%,21%{opacity:.22;filter:brightness(.4)}\n}\n.echo-next,.echo-next.ready,.echo-next:not(.ready){\n color:#80bbc8!important;\n opacity:.65!important;\n animation:logicSlowBlink 3s ease-in-out infinite!important;\n}\n@keyframes logicSlowBlink{0%,100%{filter:opacity(.35)}50%{filter:opacity(.9)}}\n' + '</style></head>', 1)
components.html(html, height=1000, scrolling=False)
