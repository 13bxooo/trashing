import base64
from pathlib import Path
import re
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PROJECT : LOGIC // STAGE 01",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hidden host-page navigation controls. The iframe asks the parent Streamlit page
# to click these after its save/fade animation, avoiding sandboxed top-frame navigation.
st.markdown("<style>.st-key-host_title_nav,.st-key-host_restart_nav,.st-key-host_stage2_nav{position:fixed!important;left:-10000px!important;top:0!important;width:1px!important;height:1px!important;overflow:hidden!important;}</style>", unsafe_allow_html=True)
_host_title = st.button("TITLE NAV", key="host_title_nav")
_host_restart = st.button("RESTART NAV", key="host_restart_nav")
_host_stage2 = st.button("STAGE 02 NAV", key="host_stage2_nav")
if _host_title:
    st.session_state.game_paused = False
    st.session_state.start_open = False
    st.session_state.show_title_warning = False
    st.switch_page("main.py")
if _host_restart:
    st.session_state["stage01_reset_save"] = True
    st.session_state["stage02_reset_save"] = True
    st.session_state["stage01_started"] = True
    st.session_state["stage02_started"] = False
    st.session_state.game_started = True
    st.session_state.game_paused = False
    st.session_state.tutorial_complete = True
    st.rerun()
if _host_stage2:
    st.session_state["stage01_started"] = True
    st.session_state["stage02_started"] = True
    st.switch_page("pages/4_Stage_02.py")

# Stage 01 intentionally reuses page 2's original in-iframe stylesheet so the
# scene framing, room, player, ECHO bar, help and inventory panels stay consistent.
page_dir = Path(__file__).resolve().parent
project_root = page_dir.parent

font_data = ""
for candidate in (
    project_root / "neodgm.ttf",
    project_root / "neodgm(2).ttf",
    Path("neodgm.ttf"),
    Path("neodgm(2).ttf"),
):
    if candidate.exists():
        font_data = base64.b64encode(candidate.read_bytes()).decode("ascii")
        break

page2_source = (page_dir / "2_Game.py").read_text(encoding="utf-8")
page2_html_match = re.search(r'html\s*=\s*r"""(.*?)"""', page2_source, re.S)
if not page2_html_match:
    st.error("2페이지의 게임 템플릿을 찾지 못했습니다. pages/2_Game.py를 확인하세요.")
    st.stop()
style_match = re.search(r"<style>(.*?)</style>", page2_html_match.group(1), re.S)
if not style_match:
    st.error("2페이지의 스타일 템플릿을 읽지 못했습니다.")
    st.stop()
tutorial_css = style_match.group(1).replace("__FONT_BASE64__", font_data)

STAGE_ASSETS = project_root / "assets" / "stage01"
SPRITE_FILES = ["floor", "wall", "door_locked", "door_unlocked", "servers", "archive_shelf", "containment", "desk", "terminal", "lockers", "crates", "science_board", "vent"]
missing = [name for name in SPRITE_FILES if not (STAGE_ASSETS / (name + ".png")).is_file()]
if missing:
    st.error("STAGE 01 에셋 누락: " + ", ".join(missing))
    st.stop()
sprite_urls = {name: "data:image/png;base64," + base64.b64encode((STAGE_ASSETS / (name + ".png")).read_bytes()).decode("ascii") for name in SPRITE_FILES}

html = r"""
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<style>
__TUTORIAL_CSS__

.pause-overlay{position:fixed!important;inset:0!important;z-index:1500000!important;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.78)!important;padding:18px;box-sizing:border-box}
.pause-overlay>div{width:min(390px,90vw)!important;box-sizing:border-box!important;background:#000!important;color:#fff!important;border:3px double #28dfff!important;padding:28px!important;box-shadow:0 0 0 1px #07566c,0 0 18px #00dfff22!important}
.pause-title{color:#fff!important;font-family:NeoDungGeunMo,monospace!important;text-align:center!important;font-size:clamp(22px,3vw,30px)!important;letter-spacing:1px!important}
.pause-sub{color:#8fdff0!important;font-family:NeoDungGeunMo,monospace!important;text-align:center!important}
.pause-actions{visibility:visible!important;pointer-events:auto!important;margin-top:24px!important;display:flex!important;flex-direction:column!important;gap:12px!important;align-items:stretch!important}
.pause-actions button,.pause-actions a{width:100%!important;min-height:44px!important;background:#fff!important;color:#000!important;border:1px solid #fff!important;border-radius:0!important;font-family:NeoDungGeunMo,monospace!important;display:flex!important;align-items:center!important;justify-content:center!important;text-decoration:none!important;cursor:pointer!important}
.pause-actions button:hover,.pause-actions a:hover{background:#28dfff!important;color:#000!important;border-color:#28dfff!important}
.game-area{background:#000!important;}
.room{background:rgba(0,0,0,.12)!important;}
.inventory-panel{background:#020609!important;color:#eefaff!important;border:2px solid #28dfff!important;box-shadow:0 0 0 2px #073c4b,0 0 18px #00dfff20!important}
.inventory-header{border-bottom:2px solid #147b94!important}
.inventory-title{color:#42eaff!important;text-shadow:0 0 6px #00dfff55!important}
.inventory-slot{background:#02090e!important;color:#fff!important;border:1px solid #147b94!important;box-shadow:inset 0 0 0 1px #00dfff0d!important}
.inventory-slot:hover,.inventory-slot.selected{background:#073040!important;color:#fff!important;border-color:#42eaff!important;box-shadow:0 0 0 1px #42eaff,0 0 10px #00dfff22!important}
.item-description{background:#02090e!important;color:#d9f7ff!important;border-top:2px solid #147b94!important}
/* Stage-specific additions. Page 2's base scene styles are used above. */
.stage01-timer{position:absolute;top:28px;right:72px;z-index:22;color:#777;font-size:11px;letter-spacing:1px}
.stage01-pause{position:absolute;top:18px;right:18px;z-index:160;width:34px;height:34px;padding:0;border:0;background:#000;color:#fff;font-size:20px;line-height:1}
.stage01-pause:hover{background:#fff;color:#000}
.stage01-object{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;width:15%;height:10%;min-width:90px;padding:8px!important;background:#090909}
.stage01-object .main-label{font-size:12px;color:#ddd;line-height:1.4}
.stage01-object .sub-label{font-size:9px;color:#666;line-height:1.4}
.stage01-object.near{border-color:#eee;color:#fff;box-shadow:0 0 0 1px #ffffff22}
.stage01-object{animation:standbySpark 3.1s infinite steps(2,end)}
.stage01-object:nth-of-type(2n){animation-delay:.8s}
@keyframes standbySpark{0%,88%,100%{filter:brightness(1);box-shadow:0 0 0 transparent}90%,94%{filter:brightness(1.7);box-shadow:0 0 12px #40f6ff55}}
.stage-transition{position:fixed;inset:0;z-index:999999;background:#000;display:flex;align-items:center;justify-content:center;flex-direction:column;color:#fff;opacity:1;transition:opacity .7s steps(8,end);pointer-events:auto;text-align:center}
.stage-transition.hide{opacity:0;pointer-events:none}
.stage-transition .stage-no{font-size:clamp(25px,4vw,48px);letter-spacing:3px;line-height:1.6;text-shadow:0 0 8px #dffaff}
.stage-transition .stage-room{font-size:clamp(15px,2vw,24px);color:#aaa;letter-spacing:2px}
.stage-transition .transition-line{width:0;height:2px;background:#28dfff;margin-top:24px;box-shadow:0 0 10px #28dfff;animation:lineScan 1.4s steps(10,end) forwards}
.stage-transition{background:#000!important}
.stage-transition .stage-card{width:min(540px,84vw);min-height:160px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:2px solid #147b94;outline:1px solid #28dfff;outline-offset:5px;background:#000;position:relative;z-index:1;padding:20px;box-sizing:border-box}
.stage-transition .loading-indicator{position:relative;z-index:1;margin-top:34px;width:min(360px,78vw);text-align:center;color:#bcefff;font-size:11px;letter-spacing:1px}
.stage-transition .loading-symbol{font-size:32px;color:#28dfff;text-shadow:0 0 12px #28dfff;animation:loadPulse 1.1s steps(2,end) infinite;margin-bottom:8px}
.stage-transition .loading-label{color:#bcefff;margin-bottom:12px}
.stage-transition .loading-track{height:7px;border:1px solid #147b94;background:#02090e;padding:1px;box-sizing:border-box;overflow:hidden}
.stage-transition .loading-track span{display:block;height:100%;width:0;background:#28dfff;box-shadow:0 0 9px #28dfff;animation:loadBar 2.5s steps(12,end) forwards}
.stage-transition .transition-gear{position:absolute;left:20px;bottom:18px;color:#9bbdc5;font-size:24px;animation:gearRotate 1.2s linear infinite;z-index:2}
@keyframes loadPulse{50%{opacity:.4;transform:scale(.92)}}
@keyframes loadBar{to{width:100%}}
@keyframes gearRotate{to{transform:rotate(360deg)}}

.stage-transition:before{content:"";position:absolute;width:min(540px,84vw);height:190px;border:2px solid #147b94;outline:1px solid #28dfff;outline-offset:5px;pointer-events:none}
.stage-transition .stage-no,.stage-transition .stage-room,.stage-transition .transition-line{position:relative;z-index:1}
.stage-transition .stage-room{color:#bcefff!important}
@keyframes lineScan{to{width:min(360px,70vw)}}
.stage01-a{left:11%;top:17%}
.stage01-b{left:42%;top:13%;width:16%;height:13%}
.stage01-c{right:12%;top:18%}
.stage01-archive{left:15%;bottom:17%;width:18%;height:10%}
.stage01-panel{display:none!important}
.stage01-object .object-label{bottom:-22px}
.stage01-window-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px;align-items:center}
.stage01-window-actions button,.stage01-window-actions a{min-width:150px;text-align:center;justify-content:center}
.pause-actions{visibility:visible;pointer-events:auto}
.pause-actions button,.pause-actions a{min-width:130px;text-align:center;justify-content:center;text-decoration:none}
.save-gear{position:fixed;left:18px;bottom:18px;z-index:99999;display:none;align-items:center;gap:8px;padding:8px 11px;background:#050505;border:1px solid #666;color:#ddd;font-size:11px;letter-spacing:1px}
.save-gear.show{display:flex}
.save-gear .gear{display:inline-block;font-size:20px;animation:gearSpin .8s linear infinite}
@keyframes gearSpin{to{transform:rotate(360deg)}}
.computer-overlay.show{display:flex}
.save-fade{position:fixed;inset:0;background:#000;opacity:0;pointer-events:none;z-index:100000;transition:opacity .35s ease}
.save-fade.active{opacity:1;pointer-events:auto}
.save-fade .fade-label{position:absolute;left:18px;bottom:22px;font-size:12px;color:#aaa;letter-spacing:2px}
.save-fade .fade-gear{display:inline-block;margin-right:8px;font-size:22px;animation:gearSpin .8s linear infinite}
.system-computer{width:150px;height:120px;margin:10px auto 18px;position:relative;image-rendering:pixelated}
.system-computer .screen{position:absolute;left:20px;top:8px;width:110px;height:72px;background:#0876d1;border:8px solid #171717;box-shadow:inset 0 0 0 3px #55baff}
.system-computer .screen:before{content:'>';position:absolute;left:12px;top:8px;color:#b9edff;font-size:22px;text-shadow:0 0 5px #fff}
.system-computer .neck{position:absolute;left:67px;top:80px;width:16px;height:15px;background:#777}
.system-computer .base{position:absolute;left:45px;top:94px;width:60px;height:10px;background:#aaa;border-bottom:4px solid #555}
@media(max-width:700px){
 .stage01-timer{top:49px;right:56px;font-size:10px}
 .stage01-pause{top:10px;right:10px}
 .stage01-object{min-width:56px;padding:4px!important}
 .stage01-object .main-label{font-size:9px}
 .stage01-object .sub-label{font-size:8px}
 .stage01-a{left:3%;top:16%}
 .stage01-b{left:36%;top:13%;width:20%;height:12%}
 .stage01-c{right:3%;top:17%}
 .stage01-archive{left:3%;bottom:16%;width:22%;height:10%}
 .stage01-panel{display:none!important}
 .stage01-window-actions button,.stage01-window-actions a{min-width:120px}
 .pin-panel{width:min(390px,90vw);padding:20px}
 .pin-slots{gap:7px}
 .pin-slot{height:46px;font-size:22px}
 .pin-keypad{gap:6px}
 .pin-keypad button{height:48px;font-size:20px}
}
.pin-panel{width:min(390px,88vw);max-height:92%;overflow-y:auto;padding:22px}
.pin-status-line{position:relative;padding:9px 28px 9px 10px;border:1px solid #292929;color:#777;font-size:10px;letter-spacing:1px;min-height:32px}
.pin-status-line .reader-light{top:10px;right:10px}
.pin-slots{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:14px 2px 16px}
.pin-slot{height:52px;display:flex;align-items:center;justify-content:center;border:1px solid #444;background:#090909;color:#fff;font-size:27px;letter-spacing:1px;box-shadow:inset 0 0 0 1px #ffffff05}
.pin-slot.filled{border-color:#aaa;color:#fff}
.pin-keypad{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.pin-keypad button{width:100%;height:52px;margin:0;padding:0;border:1px solid #444;border-radius:0;background:#080808;color:#eee;font-family:NeoDungGeunMo,monospace;font-size:22px;cursor:pointer}
.pin-keypad button:hover,.pin-keypad button:focus-visible{background:#fff;color:#000;outline:none}
.pin-keypad .pin-cancel{font-size:11px;color:#888}
.pin-keypad .pin-backspace{font-size:24px}
.pin-verify,.pin-close{width:100%;margin-top:10px}
.pin-verify{background:#fff;color:#000}
.pin-verify:hover{background:#bbb;color:#000}
.reader-light{width:9px;height:9px;border-radius:50%;background:#ff3333;box-shadow:0 0 8px #ff3333;transition:background .18s,box-shadow .18s}
.reader-light.green{background:#36ff76;box-shadow:0 0 12px #36ff76}
.stage01-panel .reader-light{top:8px;right:8px}
.stage01-panel{position:absolute}
#exitLight{top:8px;right:8px}
.exit-reader-label{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:9px;line-height:1.8;letter-spacing:1px;color:#666;text-align:center;white-space:nowrap}
#exitDoor.near .exit-reader-label{color:#fff}
/* Stage entrance uses the same minimal cyan chapter card as the tutorial. */
.stage-transition{background:#000!important;z-index:999999!important;transition:opacity .45s steps(7,end)!important}
.stage-transition:before{display:none!important}
.stage-transition .stage-card{width:min(355px,82vw)!important;min-height:148px!important;padding:22px!important;border:1px solid #2cddf7!important;outline:none!important;box-shadow:0 0 15px #00dfff25!important}
.stage-transition .stage-no{font-size:30px!important;letter-spacing:2px!important;color:#f3ffff!important}
.stage-transition .stage-room{font-size:16px!important;letter-spacing:0!important;color:#b5f5ff!important}
/* New archive: no JPEG backdrop; keep the tutorial's dark cyan room theme. */
.game-area{background:#000!important}
.room{background:linear-gradient(135deg,#111e30,#172a40 45%,#0c1726)!important;border:3px solid #368eac!important;box-shadow:inset 0 0 0 8px #09111e!important}
.room:before{content:"";position:absolute;inset:3%;pointer-events:none;background-image:linear-gradient(#6fa5c61e 1px,transparent 1px),linear-gradient(90deg,#6fa5c61e 1px,transparent 1px);background-size:11.1% 11.1%;z-index:0}
.stage01-object{background:#07121e!important;border:2px solid #29c6e3!important;box-shadow:0 0 10px #00dfff1b!important;z-index:2}
.stage01-object .main-label{color:#a9f4ff!important}
.stage01-object .sub-label{color:#7bacc0!important}

/* STAGE 01 pixel sprites — consistent with tutorial theme */
.room{background:linear-gradient(145deg,#182941,#263b55 52%,#111e32)!important;border:3px solid #397e9c!important}
.room:before{background-image:linear-gradient(#8ab1d022 1px,transparent 1px),linear-gradient(90deg,#8ab1d022 1px,transparent 1px)!important;background-size:12.5% 12.5%!important}
.stage01-object{background:transparent!important;border:0!important;box-shadow:none!important;animation:none!important;padding:0!important;min-width:0!important}
.stage01-object .main-label,.stage01-object .sub-label{display:none!important}
.stage01-object.near{filter:drop-shadow(0 0 7px #46eaff)!important}
.stage01-object img{width:100%;height:100%;object-fit:contain;image-rendering:pixelated;pointer-events:none}
.stage01-a{left:10%!important;top:15%!important;width:18%!important;height:17%!important}
.stage01-b{left:33%!important;top:13%!important;width:34%!important;height:23%!important}
.stage01-c{left:73%!important;top:15%!important;width:17%!important;height:18%!important}
.stage01-archive{left:12%!important;bottom:17%!important;width:23%!important;height:20%!important}
.exit-wall{left:42%!important;top:0!important;width:16%!important;height:17%!important;background:transparent!important;border:0!important;box-shadow:none!important}
.exit-wall:before,.exit-wall:after,.exit-sign{display:none!important}
.exit-wall img{width:100%;height:100%;object-fit:contain;image-rendering:pixelated}
.exit-reader-label{display:none!important}
#exitLight{display:none!important}
.stage01-decor{position:absolute;object-fit:contain;image-rendering:pixelated;pointer-events:none;z-index:1}
.stage01-object,.exit-wall{z-index:4!important}
.player{z-index:6!important}
.pause-overlay>div{width:min(390px,86vw)!important;padding:34px!important;background:#02070c!important;border:1px solid #54dfff!important;box-shadow:0 0 0 1px #123c4d,0 0 18px #00cfff22!important}
.pause-actions{display:flex!important;flex-direction:column!important;gap:12px!important}
.pause-row{display:flex;align-items:center;gap:12px}
.pause-icon{width:30px;color:#54dfff;text-align:center;font-size:22px}
.pause-nav-link{flex:1;display:flex;justify-content:center;align-items:center;min-height:44px;background:#fff!important;color:#000!important;border:1px solid #fff!important;text-decoration:none;font-family:NeoDungGeunMo,monospace;cursor:pointer}
.pause-nav-link:hover{background:#28dfff!important;color:#000!important}
#timeoutPanel{display:none}

/* Independent layers: floor -> wall -> objects -> player -> HUD */
.room{background:#020813!important;border:0!important;box-shadow:none!important;overflow:hidden!important}
.room:before,.room:after,.room-line-horizontal,.room-line-vertical{display:none!important}
.stage01-layer{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;pointer-events:none}
#floorLayer{z-index:0}#wallLayer{z-index:1}
.stage01-object,.stage01-decor,.exit-wall{opacity:1!important;filter:none!important;pointer-events:none!important;background:none!important;border:0!important;box-shadow:none!important}
.stage01-object .main-label,.stage01-object .sub-label,.exit-sign{display:none!important}
.stage01-object img,.stage01-decor img,.exit-wall img{display:block!important;width:100%;height:100%;object-fit:contain;image-rendering:pixelated}
.stage01-object{z-index:3!important}.stage01-decor{position:absolute;z-index:2;pointer-events:none}.exit-wall{z-index:3!important}
.player{z-index:5!important}.echo-bar,.interaction-message{z-index:8!important}
.stage01-a{left:14%!important;top:32%!important;width:14%!important;height:20%!important}
.stage01-b{left:36%!important;top:68%!important;width:28%!important;height:17%!important}
.stage01-c{left:72%!important;top:32%!important;width:17%!important;height:20%!important}
.stage01-archive{left:14%!important;top:15%!important;width:20%!important;height:19%!important}
.exit-wall{left:38%!important;top:5%!important;width:24%!important;height:25%!important}
.exit-wall:before,.exit-wall:after{display:none!important}
.stage01-pause{top:10px!important;right:13px!important;width:44px!important;height:44px!important;border:2px solid #36eaff!important;border-radius:5px!important;background:#000c15!important;color:#fff!important;box-shadow:none!important;font-size:23px!important}
.pause-overlay>div{width:min(390px,86vw)!important;min-height:0!important;padding:34px!important;background:#02070c!important;border:1px solid #54dfff!important;box-shadow:0 0 0 1px #123c4d,0 0 18px #00cfff22!important}

.stage01-pause{width:44px!important;height:44px!important;border:1px solid #55eaff!important;border-radius:0!important;background:#00050a!important;color:#baf7ff!important;box-shadow:none!important}
.stage01-pause.paused{background:#baf7ff!important;color:#06151b!important}
.pause-overlay>div{width:min(536px,88vw)!important;height:274px!important;padding:32px 44px!important;border:1px solid #5eddf5!important;background:#04121d!important;box-shadow:none!important}
.pause-actions{margin:0!important;gap:8px!important;align-items:flex-start!important}
.pause-row{height:56px!important;gap:14px!important}
.pause-icon{width:38px!important;height:38px!important;border:1px solid #5de9ff!important;border-radius:50%!important;display:flex!important;align-items:center!important;justify-content:center!important;font-size:14px!important}
.pause-actions button.pause-nav-link{width:250px!important;background:transparent!important;border:0!important;color:#e9fcff!important;justify-content:flex-start!important;font-size:18px!important}
.stage01-object:not(.collected){animation:archiveGlow 2s ease-in-out infinite!important}
.stage01-object.collected{animation:none!important}
@keyframes archiveGlow{0%,100%{filter:drop-shadow(0 0 2px #15c9d9)}50%{filter:drop-shadow(0 0 10px #47ffff) drop-shadow(0 0 4px #11dce9)}}
#terminalTarget{position:absolute;left:64%;top:13%;width:9%;height:12%;pointer-events:none;z-index:3;animation:archiveGlow 2s infinite}
#floorLayer{z-index:0!important}#wallLayer{z-index:1!important}
</style></head><body>
<div class="game" id="gameRoot" tabindex="0">
  <div class="project-title">PROJECT : LOGIC</div>
  <div class="stage-title">STAGE 01 // ARCHIVE ACCESS</div>
  <div class="stage01-timer" id="timer">10:00</div>
  <button class="stage01-pause" id="pauseBtn" type="button" aria-label="Pause">Ⅱ</button>

  <div class="game-area" id="gameArea">
    <div class="mobile-controls" id="mobileControls">
      <button class="control-button control-up" data-direction="w" type="button">▲</button>
      <button class="control-button control-left" data-direction="a" type="button">◀</button>
      <button class="control-button control-right" data-direction="d" type="button">▶</button>
      <button class="control-button control-down" data-direction="s" type="button">▼</button>
    </div>

    <div class="room" id="room"><img class="stage01-layer" id="floorLayer" src="__SPR_FLOOR__"><img class="stage01-layer" id="wallLayer" src="__SPR_WALL__">
      





<div class="stage01-decor" style="left:12%;top:57%;width:14%;height:20%"><img src="__SPR_CONTAINMENT__"></div>
<div class="stage01-decor" style="left:78%;top:65%;width:13%;height:17%"><img src="__SPR_LOCKERS__"></div>
<div class="stage01-decor" style="left:70%;top:17%;width:15%;height:12%"><img src="__SPR_CRATES__"></div>
<div class="stage01-decor" style="left:64%;top:13%;width:9%;height:12%"><img src="__SPR_TERMINAL__"></div>
<div class="stage01-decor" style="left:33%;top:57%;width:10%;height:8%"><img src="__SPR_VENT__"></div>
<div class="stage01-decor" style="left:66%;top:57%;width:10%;height:8%"><img src="__SPR_VENT__"></div>

      

      <div id="terminalTarget"></div><div class="object stage01-object stage01-a" id="objectA" data-id="A"><img src="__SPR_SERVERS__" alt="servers"><span class="sub-label" id="stateA">DATA SEALED</span></div>
      <div class="object stage01-object stage01-b" id="objectB" data-id="B"><img src="__SPR_DESK__" alt="desk"><span class="sub-label" id="stateB">DATA SEALED</span></div>
      <div class="object stage01-object stage01-c" id="objectC" data-id="C"><img src="__SPR_ARCHIVE_SHELF__" alt="archive_shelf"><span class="sub-label" id="stateC">DATA SEALED</span></div>
      <div class="object stage01-object stage01-archive" id="objectArchive" data-id="ARCHIVE"><img src="__SPR_SCIENCE_BOARD__" alt="science_board"><span class="sub-label" id="stateArchive">UNREAD</span></div>
      <div class="object stage01-object stage01-panel" id="objectPanel" aria-hidden="true"><span class="reader-light" id="panelLight"></span><span class="main-label">EXIT ACCESS</span><span class="sub-label" id="statePanel">LOCKED</span></div>

      <div class="exit-wall" id="exitDoor" data-id="EXIT"><img id="doorSprite" src="__SPR_DOOR_LOCKED__"><span class="reader-light" id="exitLight" aria-label="Exit access indicator"></span></div>
      <div class="exit-sign"><span class="exit-arrow">↓ ↑</span><br><span>[EXIT] ARCHIVE ACCESS</span></div>
      <div class="player" id="player"></div>
      <div class="interaction-message" id="interactionMessage">PRESS E</div>

      <div class="echo-bar">
        <div class="echo-name">ECHO // AI SYSTEM</div>
        <div class="echo-message" id="echoMessage"></div>
        <div class="echo-next" id="echoNext">SPACE // SKIP / NEXT</div>
      </div>
    </div>
  </div>

  <div class="status" id="status">ECHO SYSTEM // ONLINE</div>

  <div class="overlay" id="inventoryOverlay" style="display:none">
    <div class="inventory-panel">
      <div class="inventory-header"><div class="inventory-title">INVENTORY</div><div class="inventory-close">I / ESC TO CLOSE</div></div>
      <div class="inventory-grid">
        <div class="inventory-slot" data-slot="0"></div><div class="inventory-slot" data-slot="1"></div><div class="inventory-slot" data-slot="2"></div><div class="inventory-slot" data-slot="3"></div>
        <div class="inventory-slot" data-slot="4"></div><div class="inventory-slot" data-slot="5"></div><div class="inventory-slot" data-slot="6"></div><div class="inventory-slot" data-slot="7"></div>
      </div>
      <div class="item-description" id="itemDescription">ITEM DESCRIPTION<br><br>기록을 선택하면 내용이 표시됩니다.</div>
    </div>
  </div>

  <div class="overlay" id="helpOverlay" style="display:none">
    <div class="help-panel">
      <div class="help-header"><div class="help-title">HOW TO PLAY</div><div class="help-close">H / ESC TO CLOSE</div></div>
      <div class="help-row"><div class="help-number">01</div><div class="help-key">MOVEMENT<br>W A S D</div><div class="help-description">WASD 키로 시설 내부를 직접 이동합니다.</div></div>
      <div class="help-row"><div class="help-number">02</div><div class="help-key">INTERACTION<br>E</div><div class="help-description">가까이 있는 구역 기록, 보관 기록, 보안 패널을 조사합니다.</div></div>
      <div class="help-row"><div class="help-number">03</div><div class="help-key">INVENTORY<br>I</div><div class="help-description">획득한 기록을 확인합니다.</div></div>
      <div class="help-row"><div class="help-number">04</div><div class="help-key">SYSTEM<br>SPACE</div><div class="help-description">현재 대사를 완성하거나 다음 안내를 확인합니다.</div></div>
      <div class="help-row"><div class="help-number">05</div><div class="help-key">HELP<br>H</div><div class="help-description">조작 방법을 다시 확인합니다. ESC로 열린 창을 닫습니다.</div></div>
      <div style="margin-top:22px;padding:16px;background:#090909;border-left:2px solid #fff"><div style="margin-bottom:8px;font-size:13px">ARCHIVE ACCESS</div><div style="color:#888;font-size:11px;line-height:1.8">A·B·C 구역의 기록과 ARCHIVE NOTE를 대조해 무작위 네 자리 코드를 복원하십시오. 기록 속 삭제 명령의 출처를 확인하고, 초록색 표시등이 켜지면 EXIT에 접근할 수 있습니다.</div></div>
    </div>
  </div>

  <div class="computer-overlay" id="dataOverlay">
    <div class="computer-panel"><div class="computer-title" id="windowTitle">RECORD</div><div class="computer-sub" id="windowSub">ARCHIVE ACCESS // RECOVERED DATA</div><div id="windowBody"></div><button class="code-button" id="closeRecord" type="button">CLOSE / ESC</button></div>
  </div>

  <div class="computer-overlay" id="codeOverlay">
    <div class="computer-panel pin-panel">
      <div class="computer-title" id="codeTitle">EXIT ACCESS READER</div>
      <div class="computer-sub">AUTHENTICATION // FOUR DIGITS</div>
      <div class="pin-status-line"><span class="reader-light" id="pinLight" aria-label="Authentication status"></span><span id="pinStatus">ACCESS LOCKED // ENTER CODE</span></div>
      <div class="pin-slots" id="pinSlots" aria-label="입력한 네 자리 코드"><div class="pin-slot">—</div><div class="pin-slot">—</div><div class="pin-slot">—</div><div class="pin-slot">—</div></div>
      <div class="pin-keypad" id="pinKeypad">
        <button type="button" data-pin="1">1</button><button type="button" data-pin="2">2</button><button type="button" data-pin="3">3</button>
        <button type="button" data-pin="4">4</button><button type="button" data-pin="5">5</button><button type="button" data-pin="6">6</button>
        <button type="button" data-pin="7">7</button><button type="button" data-pin="8">8</button><button type="button" data-pin="9">9</button>
        <button type="button" class="pin-cancel" data-pin="clear">취소</button><button type="button" data-pin="0">0</button><button type="button" class="pin-backspace" data-pin="back" aria-label="마지막 숫자 지우기">⌫</button>
      </div>
      <button class="code-button pin-verify" id="verifyBtn" type="button">VERIFY CODE</button>
      <div class="code-error" id="codeError" aria-live="polite"></div>
      <button class="code-button pin-close" id="closeCode" type="button">CLOSE / ESC</button>
    </div>
  </div>

  <div class="stage-transition" id="stageTransition"><div class="stage-card"><div class="stage-no">STAGE 01</div><div class="stage-room">:ARCHIVE ACCESS</div></div></div>
  <div class="pause-overlay" id="pauseOverlay">
    <div class="pause-menu-panel"><div class="pause-actions">
<div class="pause-row"><span class="pause-icon">Ⅱ</span><button class="pause-nav-link" id="resumeBtn" type="button">RESUME</button></div>
<div class="pause-row"><span class="pause-icon">↻</span><button class="pause-nav-link" id="restartBtn" type="button">RESTART</button></div>
<div class="pause-row"><span class="pause-icon">⌂</span><button class="pause-nav-link" id="titleBtn" type="button">TITLE</button></div>
</div></div>
  </div>
<div class="save-fade" id="saveFade"><div class="fade-label"><span class="fade-gear">⚙</span>SAVING DATA...</div></div>
<div class="save-gear" id="saveGear" aria-live="polite"><span class="gear">⚙</span><span id="saveGearText">SAVING...</span></div>
</div>

<script>
(function(){
'use strict';
const $=id=>document.getElementById(id);
const root=$('gameRoot'), room=$('room'), player=$('player'), interactionMessage=$('interactionMessage');
const inventoryOverlay=$('inventoryOverlay'), helpOverlay=$('helpOverlay'), dataOverlay=$('dataOverlay'), codeOverlay=$('codeOverlay'), pauseOverlay=$('pauseOverlay');
const echoMessage=$('echoMessage'), echoNext=$('echoNext'), status=$('status'), timerNode=$('timer');
let playerX=50, playerY=55, seconds=600, paused=false, finished=false, codeSolved=false, nearby=null;
let helpOpen=false, inventoryOpen=false, dataOpen=false, codeOpen=false, typingDone=false, typingTimer=null, echoIndex=0, pinBuffer='';
let timerLast=Date.now();
const RUN_SAVE_KEY='project_logic_run_state_v1';
try{const run=JSON.parse(localStorage.getItem(RUN_SAVE_KEY)||'null');if(run&&Number.isFinite(run.seconds))seconds=Math.max(0,Math.min(600,Math.floor(run.seconds)))}catch(e){}
const STAGE_SAVE_KEY='project_logic_stage01_save_v1';
if(__RESET_STAGE_SAVE__){seconds=600;try{localStorage.removeItem(STAGE_SAVE_KEY);localStorage.removeItem('project_logic_stage02_save_v1');localStorage.removeItem('project_logic_run_state_v1')}catch(e){}}
let audioContext=null;
function playTone(freq=880,duration=0.07,volume=0.045){try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!audioContext)audioContext=new AC();if(audioContext.state==='suspended')audioContext.resume();const osc=audioContext.createOscillator(),gain=audioContext.createGain();osc.type='square';osc.frequency.value=freq;gain.gain.setValueAtTime(0.0001,audioContext.currentTime);gain.gain.exponentialRampToValueAtTime(volume,audioContext.currentTime+0.008);gain.gain.exponentialRampToValueAtTime(0.0001,audioContext.currentTime+duration);osc.connect(gain);gain.connect(audioContext.destination);osc.start();osc.stop(audioContext.currentTime+duration+0.01)}catch(e){}}
function playDoorOpen(){try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!audioContext)audioContext=new AC();if(audioContext.state==='suspended')audioContext.resume();const now=audioContext.currentTime;[440,660,880].forEach((frequency,index)=>{const osc=audioContext.createOscillator(),gain=audioContext.createGain();osc.type='square';osc.frequency.value=frequency;gain.gain.setValueAtTime(0.0001,now+index*.12);gain.gain.exponentialRampToValueAtTime(.08,now+index*.12+.02);gain.gain.exponentialRampToValueAtTime(.0001,now+index*.12+.18);osc.connect(gain);gain.connect(audioContext.destination);osc.start(now+index*.12);osc.stop(now+index*.12+.2)});}catch(e){}}
const keys={w:false,a:false,s:false,d:false};
const inventory=Array(8).fill(null);
const items=[];
const messages=[
'STAGE 01 // ARCHIVE ACCESS. 이곳은 연구소 사고의 기록을 보관하는 자료실입니다.',
'사고 이후 중앙 기록이 삭제되었지만, 서버와 연구원의 작업대, 보관함에 사본이 남아 있습니다.',
'세 곳을 조사해 A·B·C 기록값을 수집하십시오. 왼쪽 위 화이트보드에는 네 자리 암호의 복원 규칙이 있습니다.',
'복원한 암호를 문 오른쪽 보안 단말기에 입력하면 잠금이 해제됩니다. 이후 출입문에서 E키를 누르십시오.',
'다만 삭제 명령에 사용된 인증 정보가 제 시스템과 일치합니다. 그 이유를 밝혀야 합니다.'
];
const puzzleCandidates=[];
for(let a=2;a<=9;a++)for(let b=1;b<a;b++)for(let c=a+1;c<=Math.min(9,a+b-1);c++)puzzleCandidates.push({A:a,B:b,C:c});
let puzzle=puzzleCandidates[Math.floor(Math.random()*puzzleCandidates.length)];
let expectedCode=makeExpectedCode();
function makeExpectedCode(){const checksum=(puzzle.A+puzzle.B+puzzle.C)%9||9;return String(puzzle.A-puzzle.B)+String(puzzle.C-puzzle.A)+String(puzzle.A+puzzle.B-puzzle.C)+String(checksum)}
const found={A:false,B:false,C:false,ARCHIVE:false};
const clues={};
function rebuildClues(){
 clues.A={title:'SERVER A // 출입 기록',body:`출입 기록 04-A\n\n보안 담당자는 02:13에 서버실을 나갔다. 2분 뒤 중앙 로그에 삭제 명령이 기록되었다.\n\nA 기록값: ${puzzle.A}\nRECOVERED VALUE: ${puzzle.A}`};
 clues.B={title:'DESK B // 작업 기록',body:`시스템 진단 로그\n\n02:15:08 — ARCHIVE INDEX ACCESS\n02:15:11 — DELETE REQUEST REJECTED\n02:15:12 — REQUEST SOURCE: ECHO\n\nB 기록값: ${puzzle.B}\nRECOVERED VALUE: ${puzzle.B}`};
 clues.C={title:'ARCHIVE C // 보관 기록',body:`정비 기록 17-C\n\n출구 잠금은 원격 조작으로 전환되었다. 수동 해제는 인증 코드 복구 후에만 허용된다.\n\nC 기록값: ${puzzle.C}\nRECOVERED VALUE: ${puzzle.C}`};
}
rebuildClues();
const objects=[
 {id:'A',name:'SERVER LOG',x:13,y:30,w:14,h:20,el:$('objectA')},
 {id:'B',name:'DESK RECORDS',x:35,y:69,w:30,h:16,el:$('objectB')},
 {id:'C',name:'ARCHIVE SHELF',x:72,y:30,w:17,h:20,el:$('objectC')},
 {id:'ARCHIVE',name:'ARCHIVE NOTE',x:14,y:15,w:20,h:19,el:$('objectArchive')},
 {id:'TERMINAL',name:'SECURITY TERMINAL',x:64,y:13,w:9,h:12,el:$('terminalTarget')}, {id:'EXIT',name:'EXIT',x:38,y:5,w:24,h:25,el:$('exitDoor')}
];
const obstacles=objects.filter(o=>o.id!=='EXIT'&&o.id!=='TERMINAL').map(o=>({x:o.x,y:o.y,w:o.w,h:o.h}));
function say(t){status.textContent=t}
function updateTimer(){const m=Math.floor(seconds/60),s=seconds%60;timerNode.textContent=String(m).padStart(2,'0')+':'+String(s).padStart(2,'0')}
function clearKeys(){Object.keys(keys).forEach(k=>keys[k]=false)}
function isOverlayOpen(){return helpOpen||inventoryOpen||dataOpen||codeOpen||finished}
function showRecord(title,body){helpOpen=false;inventoryOpen=false;codeOpen=false;helpOverlay.style.display='none';inventoryOverlay.style.display='none';codeOverlay.style.display='none';$('closeRecord').style.display='inline-block';$('windowTitle').textContent=title;$('windowSub').textContent='ARCHIVE ACCESS // RECOVERED DATA';$('windowBody').innerHTML='<div style="margin:10px 0;color:#aaa;line-height:1.9;white-space:pre-line">'+body.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')+'</div>';dataOpen=true;dataOverlay.style.display='flex';clearKeys()}
function closeRecord(){if(finished)return;dataOpen=false;dataOverlay.style.display='none';root.focus()}
function renderPin(){const slots=$('pinSlots').querySelectorAll('.pin-slot');slots.forEach((el,i)=>{el.textContent=pinBuffer[i]||'—';el.classList.toggle('filled',Boolean(pinBuffer[i]))})}
function appendPinDigit(digit){if(!codeOpen||pinBuffer.length>=4)return;pinBuffer+=digit;playTone(880,.055,.035);renderPin();$('codeError').textContent='';$('pinStatus').textContent='AUTHENTICATION // '+pinBuffer.length+'/4'}
function clearPin(){pinBuffer='';renderPin();$('codeError').textContent='';$('pinStatus').textContent='ACCESS LOCKED // ENTER CODE'}
function backspacePin(){if(!codeOpen)return;pinBuffer=pinBuffer.slice(0,-1);renderPin();$('pinStatus').textContent='AUTHENTICATION // '+pinBuffer.length+'/4'}
function showCode(){if(!['A','B','C','ARCHIVE'].every(k=>found[k])){showRecord('EXIT // ACCESS LOCKED','ACCESS DENIED\n\n출구 인증을 시작하려면 A·B·C 구역 기록과 ARCHIVE NOTE를 먼저 모두 확보하십시오.');return}codeOpen=true;pinBuffer='';renderPin();codeOverlay.style.display='flex';$('codeTitle').textContent='EXIT ACCESS READER';$('codeError').textContent='';$('pinStatus').textContent='ACCESS LOCKED // ENTER CODE';$('pinLight').classList.remove('green');clearKeys()}
function closeCode(){codeOpen=false;codeOverlay.style.display='none';root.focus()}
const paperIcon='<svg viewBox="0 0 44 52" width="36" height="42"><path d="M5 2h25l9 9v39H5z" fill="#c7e8ef" stroke="#28d9ed" stroke-width="2"/><path d="M30 2v9h9M11 19h22M11 24h15M11 29h22M11 34h15" fill="none" stroke="#39788c" stroke-width="2"/><path d="M12 43l7-7 5 4 7-8" fill="none" stroke="#00a6bb" stroke-width="2"/></svg>';
function renderInventory(){document.querySelectorAll('.inventory-slot').forEach((slot,i)=>{const item=inventory[i];slot.innerHTML=item?`<div class="slot-number">${String(i+1).padStart(2,'0')}</div><div>${paperIcon}</div><div class="item-name">${item.name}</div>`:`<div class="slot-number">${String(i+1).padStart(2,'0')}</div><div class="empty-text">EMPTY</div>`;slot.classList.remove('selected')})}
function openInventory(){if(dataOpen||codeOpen||paused||finished)return;if(inventoryOpen){inventoryOpen=false;inventoryOverlay.style.display='none';root.focus();return}helpOpen=false;helpOverlay.style.display='none';inventoryOpen=true;inventoryOverlay.style.display='flex';$('itemDescription').innerHTML='ITEM DESCRIPTION<br><br>기록을 선택하면 설명이 표시됩니다.';renderInventory();clearKeys()}
function openHelp(){if(dataOpen||codeOpen||paused||finished)return;if(helpOpen){helpOpen=false;helpOverlay.style.display='none';root.focus();return}inventoryOpen=false;inventoryOverlay.style.display='none';helpOpen=true;helpOverlay.style.display='flex';clearKeys()}
function playWritingSound(){try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!audioContext)audioContext=new AC();audioContext.resume();const n=Math.floor(audioContext.sampleRate*.22),buf=audioContext.createBuffer(1,n,audioContext.sampleRate),a=buf.getChannelData(0);let v=0;for(let i=0;i<n;i++){v=v*.75+(Math.random()*2-1)*.25;a[i]=v*.23*(1-i/n)}const src=audioContext.createBufferSource(),filter=audioContext.createBiquadFilter();filter.type='highpass';filter.frequency.value=850;src.buffer=buf;src.connect(filter);filter.connect(audioContext.destination);src.start()}catch(e){}}
function addItem(id){if(items.some(item=>item.id===id))return;let item;if(id==='ARCHIVE'){item={id,name:'ARCHIVE NOTE',body:'ARCHIVE INCIDENT // FRAGMENT 04\n\n첫째 자리 = A − B.\n둘째 자리 = C − A.\n셋째 자리 = A + B − C.\n넷째 자리 = A + B + C를 9로 나눈 나머지. 나머지가 0이면 9로 기록한다.\n\n“ECHO에게 묻지 말 것. 이 명령은 기록을 삭제하라는 지시와 함께 저장되었다.”'}}else item={id,name:clues[id].title,body:clues[id].body};items.push(item);playWritingSound();const slot=items.length-1;if(slot<inventory.length)inventory[slot]=item;renderInventory()}
function interact(){if(paused||finished||isOverlayOpen())return;if(!nearby){say('NO TARGET // 가까운 장치로 이동하십시오.');return}const id=nearby.id;if(clues[id]){if(!found[id]){found[id]=true;addItem(id);nearby.el.classList.add('collected');$('state'+id).textContent='DATA FOUND';say(id+' 기록을 확보했습니다. INVENTORY에서 다시 확인할 수 있습니다.')}showRecord(clues[id].title,clues[id].body);return}if(id==='ARCHIVE'){found.ARCHIVE=true;nearby.el.classList.add('collected');$('stateArchive').textContent='READ';addItem('ARCHIVE');say('ARCHIVE NOTE 확보 // 네 자리 인증식을 확인하십시오.');showRecord('ARCHIVE NOTE // FRAGMENT 04','ARCHIVE INCIDENT // PERSONAL NOTE\n\n첫째 자리 = A − B.\n둘째 자리 = C − A.\n셋째 자리 = A + B − C.\n넷째 자리 = A + B + C를 9로 나눈 나머지. 나머지가 0이면 9로 기록한다.\n\n“ECHO에게 묻지 말 것. 기록 삭제 명령은 사고 직전 ECHO의 내부 인증값으로 전송되었다.”');return}if(id==='TERMINAL'){if(!codeSolved)showCode();else say('인증 완료. 출입문에서 E키를 누르십시오.');return}if(id==='EXIT'){if(!codeSolved){say('문 오른쪽 보안 단말기에 암호를 입력하십시오.');return}finishStage();return}}
function verify(){if(pinBuffer.length!==4){$('codeError').textContent='FOUR DIGITS REQUIRED // 네 자리 모두 입력하십시오.';return}if(pinBuffer===expectedCode){codeSolved=true;$('statePanel').textContent='UNLOCKED';$('panelLight').classList.add('green');$('exitLight').classList.add('green');$('room').classList.add('unlocked');$('doorSprite').src='__SPR_DOOR_UNLOCKED__';$('pinLight').classList.add('green');$('pinStatus').textContent='ACCESS GRANTED // GREEN';$('codeError').textContent='ACCESS GRANTED // 출구 잠금 해제';playDoorOpen();saveStageState();say('인증 완료. 출구 표시등이 초록색으로 바뀌었습니다. 출구에서 E를 눌러 진입하십시오.');setTimeout(()=>{if(codeOpen)closeCode()},900)}else{$('pinLight').classList.remove('green');$('codeError').textContent='INVALID CODE // 기록의 규칙을 다시 확인하십시오.';$('pinStatus').textContent='ACCESS DENIED // RED';say('인증 실패 // 보안 표시등이 빨간색입니다. 기록과 계산 순서를 다시 대조하십시오.')}}
function addRestartAndTitleButtons(title,sub,copy){helpOpen=false;inventoryOpen=false;dataOpen=true;codeOpen=false;helpOverlay.style.display='none';inventoryOverlay.style.display='none';codeOverlay.style.display='none';pauseOverlay.style.display='none';$('closeRecord').style.display='none';$('windowTitle').textContent=title;$('windowSub').textContent=sub;$('windowBody').innerHTML=copy+'<div class="pause-actions"><div class="pause-row"><span class="pause-icon">↻</span><button class="pause-nav-link" id="clearRestart" type="button">RESTART</button></div><div class="pause-row"><span class="pause-icon">⌂</span><button class="pause-nav-link" id="timeoutTitle" type="button">TITLE</button></div></div>';const b=$('clearRestart');if(b)b.onclick=restartViaHost;const tb=$('timeoutTitle');if(tb)tb.onclick=saveAndReturnToTitle;dataOpen=true;dataOverlay.style.display='flex'}
function finishStage(){finished=true;paused=true;timerLast=Date.now();clearKeys();pauseOverlay.style.display='none';helpOpen=false;inventoryOpen=false;codeOpen=false;dataOpen=true;helpOverlay.style.display='none';inventoryOverlay.style.display='none';codeOverlay.style.display='none';$('closeRecord').style.display='none';$('windowTitle').textContent='SYSTEM HANDOFF';$('windowSub').textContent='ARCHIVE ACCESS // NEXT SECTOR DETECTED';$('windowBody').innerHTML='<div class="system-computer" aria-label="blue pixel computer"><div class="screen"></div><div class="neck"></div><div class="base"></div></div><p> ECHO // 연결된 시스템에서 새로운 신호가 감지되었습니다.</p><p>“이 기록은 끝이 아닙니다. 서버 코어에 남아 있는 원본 로그를 확인해야 합니다.”</p><p>STAGE 02로 이동할 준비가 되었습니다.</p><div class="stage01-window-actions"><button class="code-button" id="continueStage2Btn" type="button">CONTINUE // STAGE 02</button><button class="code-button" id="stage1TitleBtn" type="button">TITLE</button></div>';$('continueStage2Btn').onclick=continueStage2;$('stage1TitleBtn').onclick=saveAndReturnToTitle;dataOverlay.style.display='flex';say('SYSTEM HANDOFF // 타이머 일시정지')}
function expireGame(){if(finished)return;finished=true;clearKeys();addRestartAndTitleButtons('TIME EXPIRED','SYSTEM LOCKDOWN','<p>제한 시간이 종료되었습니다.</p>');say('TIME EXPIRED // RESTART를 선택하십시오.')}
function introDialogueActive(){return !(echoIndex>=messages.length-1&&typingDone)}
function syncTimer(){const now=Date.now();if(introDialogueActive()){timerLast=now;return}if(!paused&&!finished){const elapsed=(now-timerLast)/1000;if(elapsed>=1){const spent=Math.floor(elapsed);seconds=Math.max(0,seconds-spent);timerLast+=spent*1000;updateTimer();if(seconds===0)expireGame()}}else timerLast=now}
function getDistance(obj){const nx=Math.max(obj.x,Math.min(playerX,obj.x+obj.w)),ny=Math.max(obj.y,Math.min(playerY,obj.y+obj.h));return Math.hypot(playerX-nx,playerY-ny)}
function checkInteraction(){nearby=null;let best=Infinity;objects.forEach(obj=>{const d=getDistance(obj);obj.el.classList.remove('near');if(d<7&&d<best){best=d;nearby=obj}});if(nearby&&!paused&&!isOverlayOpen()){nearby.el.classList.add('near');interactionMessage.textContent='E  //  '+nearby.name;interactionMessage.classList.add('visible')}else interactionMessage.classList.remove('visible')}
function circleHitsRect(cx,cy,r,o){const dx=Math.max(o.x,Math.min(cx,o.x+o.w));const dy=Math.max(o.y,Math.min(cy,o.y+o.h));return Math.hypot(cx-dx,cy-dy)<r}
// Independent walkable floor polygon; player's collision circle must stay inside.
const walkPolygon=[[9,30],[91,30],[91,82],[85,91],[15,91],[9,82]];
function insideFloor(x,y){let inside=false;for(let i=0,j=walkPolygon.length-1;i<walkPolygon.length;j=i++){
 const a=walkPolygon[i],b=walkPolygon[j];if(((a[1]>y)!=(b[1]>y))&&(x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]))inside=!inside;
}return inside}
const decorObstacles=[{x:12,y:57,w:14,h:20},{x:78,y:65,w:13,h:17},{x:70,y:17,w:15,h:12},{x:79,y:80,w:11,h:13}];
function blocked(x,y){const radius=1.4;for(const [dx,dy] of [[0,0],[-radius,0],[radius,0],[0,-radius],[0,radius]])if(!insideFloor(x+dx,y+dy))return true;
return obstacles.concat(decorObstacles).some(o=>circleHitsRect(x,y,radius,o))}

function updateMovement(){if(paused||isOverlayOpen())return;let dx=(keys.d?1:0)-(keys.a?1:0),dy=(keys.s?1:0)-(keys.w?1:0);if(!dx&&!dy)return;const len=Math.hypot(dx,dy);dx=dx/len*.48;dy=dy/len*.48;if(!blocked(playerX+dx,playerY))playerX+=dx;if(!blocked(playerX,playerY+dy))playerY+=dy;player.style.left=playerX+'%';player.style.top=playerY+'%';checkInteraction()}
function typeEcho(index){echoIndex=index;clearTimeout(typingTimer);const text=messages[index]||'';echoMessage.textContent='';typingDone=false;echoNext.classList.remove('ready');let i=0;function tick(){if(i<text.length){echoMessage.textContent+=text[i++];typingTimer=setTimeout(tick,24)}else{typingDone=true;echoNext.classList.add('ready')}}tick()}
function nextEcho(){if(!typingDone){clearTimeout(typingTimer);echoMessage.textContent=messages[echoIndex]||'';typingDone=true;echoNext.classList.add('ready');return}if(echoIndex<messages.length-1)typeEcho(echoIndex+1)}
function saveStageState(){
  try{
    localStorage.setItem(STAGE_SAVE_KEY,JSON.stringify({version:1,playerX,playerY,seconds,codeSolved,puzzle,found,items,inventory,echoIndex,echoText:echoMessage.textContent,typingDone,updatedAt:Date.now()}));
    localStorage.setItem(RUN_SAVE_KEY,JSON.stringify({seconds,stage:1,updatedAt:Date.now()}));
    return true;
  }catch(e){return false}
}
function restoreStageState(){
  try{
    const saved=JSON.parse(localStorage.getItem(STAGE_SAVE_KEY)||'null');
    if(!saved||saved.version!==1||!saved.puzzle||!Number.isFinite(saved.seconds))return false;
    playerX=Number.isFinite(saved.playerX)?saved.playerX:50;playerY=Number.isFinite(saved.playerY)?saved.playerY:85;
    seconds=Math.max(0,Math.min(600,Math.floor(saved.seconds)));codeSolved=!!saved.codeSolved;
    if(Number.isFinite(saved.puzzle.A)&&Number.isFinite(saved.puzzle.B)&&Number.isFinite(saved.puzzle.C)){puzzle=saved.puzzle;expectedCode=makeExpectedCode();rebuildClues()}
    Object.keys(found).forEach(k=>found[k]=!!(saved.found&&saved.found[k]));
    items.length=0;(Array.isArray(saved.items)?saved.items:[]).forEach(item=>{if(item&&item.id&&item.name)items.push(item)});
    inventory.fill(null);(Array.isArray(saved.inventory)?saved.inventory:[]).slice(0,inventory.length).forEach((item,i)=>inventory[i]=item);
    ['A','B','C'].forEach(k=>{const el=$('state'+k);if(el)el.textContent=found[k]?'DATA FOUND':'DATA SEALED'});
    $('stateArchive').textContent=found.ARCHIVE?'READ':'UNREAD';
    if(codeSolved){$('statePanel').textContent='UNLOCKED';$('panelLight').classList.add('green');$('exitLight').classList.add('green');$('room').classList.add('unlocked');$('doorSprite').src='__SPR_DOOR_UNLOCKED__';$('pinLight').classList.add('green')}
    echoIndex=Number.isFinite(saved.echoIndex)?Math.max(0,Math.min(messages.length-1,saved.echoIndex)):0;
    player.style.left=playerX+'%';player.style.top=playerY+'%';renderInventory();updateTimer();
    if(typeof saved.echoText==='string'){echoMessage.textContent=saved.echoText;typingDone=true;echoNext.classList.add('ready')}else typeEcho(echoIndex);
    return true;
  }catch(e){return false}
}
function clickHostControl(className){try{const btn=window.parent.document.querySelector('.st-key-'+className+' button');if(btn){btn.click();return true}}catch(e){}return false}
function navigateToTitle(){if(!clickHostControl('host_title_nav')){try{window.top.location.assign(new URL('?action=title',window.top.location.href).toString())}catch(e){say('TITLE NAVIGATION BLOCKED')}}}
function saveAndReturnToTitle(){
  paused=true;timerLast=Date.now();clearKeys();const gear=$('saveGear'),label=$('saveGearText'),fade=$('saveFade');gear.classList.add('show');label.textContent='SAVING...';fade.classList.add('active');
  const ok=saveStageState();
  label.textContent=ok?'SAVED':'SAVE FAILED';
  setTimeout(()=>{if(!clickHostControl('host_title_nav'))navigateToTitle()},3000);
}
function restartViaHost(){paused=true;clearKeys();try{localStorage.removeItem(STAGE_SAVE_KEY);localStorage.removeItem(RUN_SAVE_KEY)}catch(e){}if(!clickHostControl('host_restart_nav'))restartStage()}
function continueStage2(){paused=true;timerLast=Date.now();clearKeys();saveStageState();try{localStorage.removeItem('project_logic_stage02_save_v1');localStorage.setItem(RUN_SAVE_KEY,JSON.stringify({seconds,stage:2,updatedAt:Date.now()}))}catch(e){}if(!clickHostControl('host_stage2_nav')){try{window.top.location.assign(new URL('pages/4_Stage_02.py',window.top.location.href).toString())}catch(e){say('STAGE 02 NAVIGATION BLOCKED')}}}
function restartStage(){try{localStorage.removeItem(STAGE_SAVE_KEY);localStorage.removeItem('project_logic_stage02_save_v1');localStorage.setItem(RUN_SAVE_KEY,JSON.stringify({seconds:600,stage:1,updatedAt:Date.now()}))}catch(e){}paused=false;finished=false;codeSolved=false;seconds=600;timerLast=Date.now();playerX=50;playerY=55;nearby=null;helpOpen=inventoryOpen=dataOpen=codeOpen=false;[inventoryOverlay,helpOverlay,dataOverlay,codeOverlay,pauseOverlay].forEach(el=>el.style.display='none');Object.keys(found).forEach(k=>found[k]=false);items.length=0;inventory.fill(null);$('stateA').textContent=$('stateB').textContent=$('stateC').textContent='DATA SEALED';$('stateArchive').textContent='UNREAD';$('statePanel').textContent='LOCKED';$('panelLight').classList.remove('green');$('exitLight').classList.remove('green');$('room').classList.remove('unlocked');$('doorSprite').src='__SPR_DOOR_LOCKED__';$('pinLight').classList.remove('green');pinBuffer='';renderPin();puzzle=puzzleCandidates[Math.floor(Math.random()*puzzleCandidates.length)];expectedCode=makeExpectedCode();rebuildClues();$('panelLight').classList.remove('green');$('exitLight').classList.remove('green');$('room').classList.remove('unlocked');$('doorSprite').src='__SPR_DOOR_LOCKED__';$('pinLight').classList.remove('green');clearPin();renderInventory();updateTimer();player.style.left=playerX+'%';player.style.top=playerY+'%';echoIndex=0;typeEcho(0);say('SYSTEM READY // 접근 가능한 장치 가까이 이동하십시오.');clearKeys();checkInteraction();root.focus()}
function resume(){$('pauseBtn').classList.remove('paused');$('pauseBtn').textContent='Ⅱ';paused=false;pauseOverlay.style.display='none';timerLast=Date.now();root.focus();clearKeys()}
function focusGame(){try{root.focus({preventScroll:true})}catch(e){root.focus()}}

$('pauseBtn').addEventListener('click',()=>{if(finished)return;if(!paused&&(helpOpen||inventoryOpen||dataOpen||codeOpen))return;paused=!paused;$('pauseBtn').classList.toggle('paused',paused);$('pauseBtn').textContent=paused?'▶':'Ⅱ';timerLast=Date.now();pauseOverlay.style.display=paused?'flex':'none';clearKeys();if(!paused)focusGame()});
$('resumeBtn').addEventListener('click',resume);$('restartBtn').addEventListener('click',restartViaHost);$('titleBtn').addEventListener('click',e=>{e.preventDefault();saveAndReturnToTitle()});
$('closeRecord').addEventListener('click',closeRecord);$('closeCode').addEventListener('click',closeCode);$('verifyBtn').addEventListener('click',verify);
document.querySelectorAll('[data-pin]').forEach(btn=>btn.addEventListener('click',()=>{const action=btn.dataset.pin;if(action==='clear')clearPin();else if(action==='back')backspacePin();else appendPinDigit(action)}));
document.querySelectorAll('[data-direction]').forEach(btn=>{const k=btn.dataset.direction;const down=e=>{e.preventDefault();keys[k]=true;focusGame()};const up=e=>{e.preventDefault();keys[k]=false};btn.addEventListener('pointerdown',down);['pointerup','pointercancel','lostpointercapture'].forEach(ev=>btn.addEventListener(ev,up))});
document.querySelectorAll('.inventory-slot').forEach((slot,i)=>slot.addEventListener('click',()=>{document.querySelectorAll('.inventory-slot').forEach(s=>s.classList.remove('selected'));slot.classList.add('selected');const item=inventory[i];$('itemDescription').innerHTML=item?`<strong>${item.name}</strong><br><br>${item.body.replace(/\n/g,'<br>')}`:'ITEM DESCRIPTION<br><br>비어 있는 슬롯입니다.'}));
document.addEventListener('keydown',e=>{const key=e.key.toLowerCase();if(codeOpen){if(/^[0-9]$/.test(e.key)){e.preventDefault();appendPinDigit(e.key);return}if(key==='backspace'){e.preventDefault();backspacePin();return}if(key==='enter'){e.preventDefault();verify();return}if(key==='escape'){e.preventDefault();closeCode();return}return}if(e.repeat&&['e','h','i','escape'].includes(key))return;if(e.code==='Space'){e.preventDefault();if(!paused&&!isOverlayOpen())nextEcho();return}if(key==='escape'){if(codeOpen){closeCode();return}if(dataOpen){closeRecord();return}if(helpOpen){openHelp();return}if(inventoryOpen){openInventory();return}if(paused){resume();return}return}if(key==='h'){e.preventDefault();openHelp();return}if(key==='i'){e.preventDefault();openInventory();return}if(key==='e'){e.preventDefault();interact();return}if(['w','a','s','d'].includes(key)&&!paused&&!isOverlayOpen()){keys[key]=true;e.preventDefault()}});
document.addEventListener('keyup',e=>{const key=e.key.toLowerCase();if(key in keys){keys[key]=false;e.preventDefault()}});window.addEventListener('blur',clearKeys);root.addEventListener('pointerdown',focusGame);
function loop(){updateMovement();checkInteraction();requestAnimationFrame(loop)}
const restored=restoreStageState();if(!restored){player.style.left=playerX+'%';player.style.top=playerY+'%';renderInventory();updateTimer();typeEcho(0)}const stageTransition=$('stageTransition');if(stageTransition){if(restored){stageTransition.remove()}else{setTimeout(()=>stageTransition.classList.add('hide'),2700);setTimeout(()=>stageTransition.remove(),3150)}}checkInteraction();focusGame();setInterval(syncTimer,250);setInterval(saveStageState,1000);requestAnimationFrame(loop);
})();
</script></body></html>
"""

html = html.replace("__TUTORIAL_CSS__", tutorial_css)
for name, url in sprite_urls.items():
    html = html.replace("__SPR_" + name.upper() + "__", url)



html = html.replace("__RESET_STAGE_SAVE__", "true" if st.session_state.pop("stage01_reset_save", False) else "false")
components.html(html, height=1000, scrolling=False)
