# -*- coding: utf-8 -*-
"""
PROJECT : LOGIC / STAGE 01 — 한글 주석판

[전체 구조]
Python: Streamlit 페이지 설정, 이미지 로딩, 재시작 및 타이틀 이동
HTML: 게임 화면과 팝업의 구조
CSS: 캐릭터·방·오브제의 위치와 시각 효과
JavaScript: 이동, 충돌, 조사, 인벤토리, 퍼즐, 타이머, 문 개방

[게임 흐름]
터미널 A·B·C 조사 → 기록지 3장 수집 → NOTE 점멸 및 확인
→ 키패드 점멸 → 네 자리 인증번호 입력 → 열린 문 이미지로 교체

[수정 시 주의]
오브제 위치를 바꿀 때 CSS의 left/top과 JS objects의 x/y를 함께 바꾼다.
HTML·CSS·JS는 Python 삼중 따옴표 문자열에 포함되어 있다.
""" 
import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROJECT : LOGIC // STAGE 01",layout="wide",initial_sidebar_state="collapsed")
_action = st.query_params.get("action", "")
if _action in ("restart", "stage01_restart"):
    st.query_params.clear()
    for _key in list(st.session_state.keys()):
        if _key.startswith(("s1_", "stage01_")):
            del st.session_state[_key]
    st.session_state["stage01_started"] = True
    st.session_state["stage01_reset_save"] = True
    st.session_state["game_paused"] = False
    st.session_state["game_started"] = True
    st.rerun()
elif _action == "title":
    st.query_params.clear()
    st.switch_page("main.py")

root=Path(__file__).resolve().parent.parent
def data(path):
    return "data:image/png;base64,"+base64.b64encode(path.read_bytes()).decode("ascii")
font=""
for candidate in [root/"neodgm.ttf",root/"neodgm(2).ttf"]:
    if candidate.exists():
        font=base64.b64encode(candidate.read_bytes()).decode("ascii")
        break
st.markdown("""<style>
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#02050a!important}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stSidebarCollapsedControl"],footer{display:none!important}
.block-container,[data-testid="stMainBlockContainer"]{padding:0!important;max-width:100vw!important;width:100%!important}
iframe{display:block!important;border:0!important;width:100%!important}
/* Stage 01 viewport lock: prevent the 1000px components iframe from scrolling
   Streamlit's outer page on smaller screens. This CSS runs in the host page. */
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"] {
  height:100vh!important;
  height:100dvh!important;
  max-height:100dvh!important;
  overflow:hidden!important;
  overscroll-behavior:none!important;
}
.stApp iframe[data-testid="stIFrame"],
.stApp [data-testid="stCustomComponentV1"] iframe,
.stApp iframe {
  position:fixed!important;
  top:0!important;left:0!important;right:0!important;bottom:auto!important;
  width:100vw!important;height:100vh!important;height:100dvh!important;
  min-height:0!important;max-height:none!important;
  margin:0!important;padding:0!important;
  border:0!important;z-index:20!important;
  display:block!important;
}


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
#wallLayer{left:50%!important;top:50%!important;width:100%!important;height:100%!important;object-fit:fill!important;transform:translate(-50%,-50%)!important}</style>""",unsafe_allow_html=True)
a,b=st.columns(2)
with a:
    title=st.button("TITLE",key="stage01_title")
with b:
    restart=st.button("RESTART",key="stage01_restart")
    next_stage=st.button("STAGE 02",key="stage01_next")
    timeout_title=st.button("TIMEOUT TITLE",key="stage01_timeout_title")
if timeout_title:
    # 시간 초과 TITLE은 저장 연출 없이 모든 진행 기록을 초기화합니다.
    for _key in list(st.session_state.keys()):
        if _key.startswith(("s1_", "s2_", "tutorial_", "stage01_", "stage02_")) or _key in (
            "game_started", "game_finished", "game_paused", "remaining_seconds", "tutorial_step"
        ):
            del st.session_state[_key]
    st.session_state.update({
        "tutorial_reset_save": True,
        "stage01_reset_save": True,
        "stage02_reset_save": True,
        "tutorial_complete": False,
        "stage01_started": False,
        "stage02_started": False,
        "game_started": False,
        "game_finished": False,
        "game_paused": False,
        "remaining_seconds": 15 * 60,
        "start_open": False,
        "error_popup": False,
        "warning_popup": False,
    })
    st.switch_page("main.py")
if title:
    st.session_state["stage01_started"] = True
    st.session_state["game_started"] = True
    st.switch_page("main.py")
if next_stage:
    st.session_state["stage01_completed"] = True
    st.switch_page("pages/4_Stage_02.py")
if restart:
    for _key in list(st.session_state.keys()):
        if _key.startswith(("s1_", "stage01_")):
            del st.session_state[_key]
    st.session_state["stage01_started"] = True
    st.session_state["stage01_reset_save"] = True
    st.session_state["game_paused"] = False
    st.rerun()
st.markdown("<style>.st-key-stage01_title,.st-key-stage01_restart,.st-key-stage01_next,.st-key-stage01_timeout_title{position:fixed!important;left:-9999px!important;top:0!important}</style>",unsafe_allow_html=True)
reset_save = bool(st.session_state.pop("stage01_reset_save", False))
html = r"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@font-face{font-family:NeoDungGeunMo;src:url(data:font/ttf;base64,__FONT__)}
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#02050a;color:#e5faff;font-family:NeoDungGeunMo,monospace}
.game{position:relative;width:100vw;height:100vh;overflow:hidden;background:#02050a;outline:none}
.project-title{position:absolute;top:24px;left:28px;font-size:20px;letter-spacing:1px;color:#fff;z-index:20}
.stage-title{position:absolute;top:56px;left:28px;font-size:13px;letter-spacing:1px;color:#426b7d;z-index:20}
.pause-toggle{position:absolute;top:20px;right:24px;z-index:1000;width:42px;height:42px;display:flex;align-items:center;justify-content:center;background:#02070c;border:1px solid #54dfff;color:#8defff;font:20px NeoDungGeunMo,monospace;line-height:1;text-align:center;cursor:pointer;box-shadow:0 0 0 1px #123c4d;padding:0;line-height:1}
.pause-toggle:before,.pause-toggle:after{content:"";position:absolute;width:7px;height:7px;border-color:#8af0ff;border-style:solid}
.pause-toggle:before{left:-2px;top:-2px;border-width:2px 0 0 2px}.pause-toggle:after{right:-2px;bottom:-2px;border-width:0 2px 2px 0}
.pause-toggle.paused{background:#d9faff;color:#001018}
.stage01-timer{position:absolute;right:86px;top:32px;font-size:12px;color:#a9c4d0;z-index:20}
.game-area{position:absolute;top:45px;left:0;right:0;bottom:10px;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#02050a}
.room{position:relative;width:min(98vw,calc((100vh - 60px)*4/3));aspect-ratio:4/3;flex-shrink:0;overflow:hidden;background:transparent}
.room img.layer{position:absolute;left:50%;top:50%;width:100%;height:100%;min-width:100%;min-height:100%;transform:translate(-50%,-50%);object-fit:fill;pointer-events:none;image-rendering:pixelated;filter:none;backface-visibility:hidden}
#floorLayer{z-index:1;transform:translate(-50%,-50%);transform-origin:center center}#wallLayer{z-index:4;transform:translate(-50%,-50%);transform-origin:center center;clip-path:polygon(0 0,100% 0,100% 100%,0 100%)}
#wallOpenLayer{z-index:4}
.room.show-upper-player #wallLayer,.room.show-upper-player #wallOpenLayer{z-index:2}.room.show-upper-player .player{z-index:5}
.player{position:absolute;z-index:3;width:22px;height:28px;background:#d5e7ee;border:0;box-shadow:inset 0 0 0 4px #7895a5,inset 0 -7px #263d4d,-4px 0 #152a39,4px 0 #152a39,0 -3px #152a39,0 3px #152a39;image-rendering:pixelated;transform:translate(-50%,-50%);pointer-events:none}
.player::before{content:"";position:absolute;left:4px;right:4px;top:-7px;height:8px;background:#c5d8e0;border:2px solid #142b3a;box-shadow:inset 0 -3px #7896a5}
.player::after{content:"";position:absolute;left:6px;right:6px;top:2px;height:3px;background:#5ceaff;box-shadow:0 0 3px #5ceaff}
.status{position:absolute;bottom:24px;left:28px;color:#777;font-size:14px}
.pause-overlay{position:fixed;inset:0;z-index:2000;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.72)}
.pause-menu-panel{position:relative;width:min(536px,86vw);height:274px;padding:34px 48px;display:flex;align-items:center;background:linear-gradient(135deg,#030b12,#061722);border:1px solid #54dfff}
.pause-actions{display:flex;flex-direction:column;gap:8px}
.pause-row{display:flex;align-items:center;gap:16px;height:55px}
.pause-icon{width:38px;height:38px;flex:0 0 38px;border:1px solid #58dfff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#82eaff;font-size:14px}
.pause-nav-link{border:0;background:none;color:#d8faff;font:18px NeoDungGeunMo,monospace;text-align:left;cursor:pointer;text-decoration:none}
.pause-nav-link:hover{color:white;text-shadow:0 0 6px #54dfff}
.game.dialog-active .echo-bar{display:none}
.echo-bar{position:absolute;left:50%;bottom:5%;transform:translateX(-50%);width:min(78%,650px);min-height:78px;padding:14px 20px;background:rgba(1,12,19,.92);border:1px solid #2dbbd8;z-index:10;font-size:12px;line-height:1.6}
.echo-head{font-size:11px;color:#50dfff;margin-bottom:7px}
.echo-next{position:absolute;right:14px;bottom:6px;font-size:10px;color:#75d4e7;letter-spacing:1px;animation:echoBlink .8s steps(2,end) infinite}@keyframes echoBlink{50%{opacity:.25}}
#helpOverlay,#inventoryOverlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1500;align-items:center;justify-content:center}
.utility-panel{position:relative;width:min(820px,88vw);background:#02070c;border:1px solid #48dfff;box-shadow:0 0 0 1px #123c4d;padding:24px 26px 26px;font-size:15px;line-height:1.8;max-height:84vh;overflow:auto}
.utility-panel h3{color:#67eaff;margin:0 0 12px}.panel-header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #2587a7;padding-bottom:12px;margin-bottom:16px}.panel-hint{font-size:11px;color:#659caf}.inventory-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.inventory-slot{aspect-ratio:1;background:#01060b;border:1px solid #28546a;color:#c9f9ff;display:flex;align-items:center;justify-content:center;cursor:pointer}.inventory-slot img{width:80%;height:75%;object-fit:contain;image-rendering:pixelated}.help-row{display:grid;grid-template-columns:50px 145px 1fr;gap:15px;border-bottom:1px solid #17313d;padding:12px 4px}.help-number,.help-key{color:#7deaff}
.help-panel{width:min(760px,86vw);max-height:82vh;overflow-y:auto;padding:36px 40px;background:#02070c;border:1px solid #48dfff;box-shadow:0 0 0 1px #123c4d,0 0 14px #00cfff22}
.help-header{display:flex;justify-content:space-between;padding-bottom:18px;margin-bottom:20px;border-bottom:1px solid #333}
.help-title{font-size:24px;color:#d9faff}.help-close{font-size:12px;color:#888}
.help-panel .help-row{display:flex;gap:20px;padding:14px 0;border-bottom:1px solid #1f1f1f}
.help-panel .help-number{width:30px;flex:0 0 30px;color:#777}
.help-panel .help-key{width:145px;flex:0 0 145px;font-size:14px;color:#d9faff}
.help-panel .help-description{color:#aaa;font-size:12px;line-height:1.7}
.inventory-panel{width:min(820px,88vw);max-height:84vh;display:flex;flex-direction:column;overflow:hidden}
.inventory-panel #inventoryItems{overflow-y:auto;min-height:0;flex:1;grid-auto-rows:minmax(65px,1fr)}
.inventory-panel .item-description{flex-shrink:0;min-height:58px;max-height:100px;overflow-y:auto;margin:8px 0 0}
.inventory-panel .inventory-footer{display:flex;justify-content:flex-end;flex-shrink:0;padding-top:12px;background:#02070c}
.utility-panel button{background:transparent;color:#aaf5ff;border:1px solid #54dfff;padding:8px 16px;cursor:pointer;font:inherit}
.stage-transition{position:fixed;inset:0;z-index:3000;display:flex;align-items:center;justify-content:center;background:#000;opacity:1;transition:opacity .45s steps(6,end);pointer-events:auto}
.stage-transition.hide{opacity:0;pointer-events:none}
.stage-transition-card{position:relative;width:min(350px,78vw);min-height:145px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:1px solid #57dfff;color:#f5fbff;box-shadow:0 0 0 1px #143d4c,0 0 14px #00cfff22;letter-spacing:2px}
.stage-transition-card:before,.stage-transition-card:after{content:"";position:absolute;width:18px;height:18px;border-color:#78ecff;border-style:solid}
.stage-transition-card:before{top:-2px;left:-2px;border-width:2px 0 0 2px}.stage-transition-card:after{right:-2px;bottom:-2px;border-width:0 2px 2px 0}
.stage-transition-stage{font-size:clamp(25px,4vw,36px);line-height:1.6;text-shadow:0 0 5px #fff,0 0 14px #57dfff}.stage-transition-room{font-size:clamp(14px,2vw,20px);color:#a8f2ff;letter-spacing:1px}

/* 모든 오브제 이미지의 공통 크기·위치·그림자 스타일 */
.prop{position:absolute;z-index:2;transform:translate(-50%,-50%);object-fit:contain;cursor:pointer;image-rendering:pixelated;filter:drop-shadow(2px 2px 0 #02090e) drop-shadow(-2px -2px 0 #a4d9e3)}
/* 세 터미널의 정삼각형 배치 좌표. JS objects 좌표와 맞춰야 한다. */
#terminalA{left:34%;top:44%;width:13%}#terminalB{left:66%;top:44%;width:13%}#terminalC{left:50%;top:71.7%;width:13%}
#noteProp{left:calc(37% - 90px);top:calc(29% - 120px);width:3.5%;z-index:6}#keypadProp{left:calc(63% + 120px);top:calc(29% - 120px);width:3.5%;z-index:6}
/* 조사 단계에 따라 NOTE 또는 키패드에 적용되는 청록색 점멸 효과 */
.glow{animation:cyanPulse 2.2s ease-in-out infinite;filter:drop-shadow(0 0 5px #20f4ed) drop-shadow(0 0 11px #17bfc8)}
@keyframes cyanPulse{0%,100%{filter:drop-shadow(0 0 1px #1ec5cf)}50%{filter:drop-shadow(0 0 9px #54ffff) drop-shadow(0 0 15px #12b7bf)}}
.prop:hover{filter:drop-shadow(0 0 7px #3beaf4)}
#interactionHint{position:absolute;bottom:calc(5% + 92px);left:50%;transform:translateX(-50%);z-index:30;white-space:nowrap;background:#020a10dd;border:1px solid #3aabb8;padding:7px 14px;font-size:12px;display:none}
#dialogOverlay{position:fixed;inset:0;background:#000b;display:none;align-items:center;justify-content:center;z-index:1700}
.dialog{background:#07121b;border:1px solid #56dfff;width:min(600px,90vw);max-height:80vh;overflow:auto;padding:23px;color:#eafcff;font-size:14px;line-height:1.7}
.dialog h3{color:#68eaff;margin:0 0 12px}.dialog img{max-width:100%;max-height:210px;display:block;margin:10px auto}
.dialog button,.numkey{background:#071f2c;color:#dcffff;border:1px solid #51d5e6;font:inherit;padding:9px 14px;cursor:pointer;margin:4px}
#inventoryItems{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:repeat(3,minmax(0,1fr));gap:10px;margin:14px 0}.inventory-slot{position:relative;min-height:70px}.inventory-slot.selected{border-color:#7cecff;background:#06202b}.item-description{border:1px solid #28546a;min-height:66px;padding:12px;margin-top:12px;font-size:12px;color:#a7d8e6}
.invitem{border:1px solid #315566;background:#020a11;color:white;padding:6px;cursor:pointer;font:11px NeoDungGeunMo,monospace}
.invitem img{display:block;width:90%;height:68px;object-fit:contain;margin:auto}
#keypadDigits{letter-spacing:6px;font-size:23px;color:#7cf6ff;text-align:center;padding:10px;border:1px solid #376674}
.keygrid{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;max-width:240px;margin:10px auto}
.keygrid button{margin:0}

/* TITLE 화면으로 돌아가기 전 3초 저장 연출 */
.data-saving-screen{position:fixed;inset:0;background:#000;z-index:999999;display:none;pointer-events:auto}
.data-saving-screen.active{display:block}
.data-saving-label{position:absolute;left:28px;bottom:25px;color:#9beaff;font-size:13px;display:flex;gap:12px;align-items:center}
.data-saving-gear{display:inline-block;font-size:23px;animation:gearSpin .9s linear infinite;transform-origin:center center}
@keyframes gearSpin{to{transform:rotate(360deg)}}

/* 튜토리얼과 동일한 패널의 크기·슬롯·픽셀 테두리 */
#inventoryOverlay .inventory-panel{width:min(820px,88vw);max-height:84vh;background:linear-gradient(135deg,#030b12,#061722);border:1px solid #35dfff;box-shadow:0 0 0 1px #123c4d,0 0 18px #00cfff24}
#helpOverlay .help-panel{width:min(760px,86vw);max-height:82vh;background:linear-gradient(135deg,#030b12,#061722);border:1px solid #35dfff;box-shadow:0 0 0 1px #123c4d,0 0 18px #00cfff24}
.inventory-slot{image-rendering:pixelated}.inventory-slot.selected{border-color:#a5f6ff;box-shadow:inset 0 0 0 1px #66ddff}
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

</style></head><body>
<div class="stage-transition" id="stageTransition"><div class="stage-transition-card"><div class="stage-transition-stage">STAGE 01</div><div class="stage-transition-room">:ARCHIVE ACCESS</div></div></div>
<div class="game" id="gameRoot" tabindex="0">
<div class="project-title">PROJECT : LOGIC</div><div class="stage-title">STAGE 01 // ARCHIVE ACCESS</div>
<div class="stage01-timer" id="timer">10:00</div><button class="pause-toggle" id="pauseToggle" aria-label="Pause">Ⅱ</button>
<div class="game-area"><div class="room" id="room">
<img id="floorLayer" class="layer" src="__FLOOR__" alt="">
<img id="wallLayer" class="layer" src="__WALLS__" alt="">
 <img id="wallOpenLayer" class="layer" src="__WALLSOPEN__" alt="" aria-hidden="true" style="visibility:hidden">
<img class="prop" id="terminalA" src="__TERMINALA__" alt="Terminal A"><img class="prop" id="terminalB" src="__TERMINALB__" alt="Terminal B"><img class="prop" id="terminalC" src="__TERMINALC__" alt="Terminal C"><img class="prop" id="noteProp" src="__NOTE__" alt="NOTE"><img class="prop" id="keypadProp" src="__KEYPAD__" alt="Keypad"><div class="player" id="player"></div><div id="exitDoor" style="position:absolute;left:47%;top:19%;width:6%;height:10%;z-index:5;pointer-events:none"></div>
</div></div>
<div class="echo-bar"><div class="echo-head">ECHO // AI SYSTEM</div><span id="echoText">안녕하세요. 저는 안내 시스템 ECHO입니다. 이곳은 기록 보관실입니다. 터미널 세 대의 자료를 확인하면 출구를 열 수 있습니다. [SPACE]</span><div class="echo-next" id="echoNext">SPACE // SKIP / NEXT</div></div>
<div id="dialogOverlay"><div class="dialog" id="dialogContent"></div></div>
<div id="interactionHint">E : 조사하기</div><div class="status">ECHO SYSTEM // ONLINE</div>
<div class="pause-overlay" id="pauseOverlay"><div class="pause-menu-panel"><div class="pause-actions">
<div class="pause-row"><span class="pause-icon">Ⅱ</span><button class="pause-nav-link" id="resumeButton">RESUME</button></div>
<div class="pause-row"><span class="pause-icon">↻</span><button class="pause-nav-link" id="restartButton">RESTART</button></div>
<div class="pause-row"><span class="pause-icon">⌂</span><button class="pause-nav-link" id="titleButton">TITLE</button></div>
</div></div></div>
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
</div></div></div>
<div id="inventoryOverlay" class="overlay logic-utility-overlay" style="display:none"><div class="inventory-panel"><div class="inventory-header"><div class="inventory-title">INVENTORY</div><div class="inventory-close">I / ESC TO CLOSE</div></div><div id="inventoryItems" class="inventory-grid"></div><div id="itemDescription" class="item-description"><strong>ITEM DESCRIPTION</strong>기록지를 선택하면 설명이 표시됩니다.</div></div></div>
</div>
<script>
// 요소 선택용 축약 함수와 현재 누른 키 목록
const $=id=>document.getElementById(id),keys=new Set();
let paused=false,remaining=600,last=performance.now(),x=50,y=56;
const records={A:false,B:false,C:false};let noteRead=false,doorOpen=false,dialogOpen=false,enteredCode='';
let digits=Array.from({length:4},()=>Math.floor(Math.random()*10)).join('');
// STAGE 01에서는 ECHO가 정확한 정답을 알려준다. 이후 스테이지의 불신 서사와 대비된다.
const echoLines=['여기는 ARCHIVE ACCESS, 첫 번째 보안 구역입니다.','터미널 A·B·C에서 기록지를 수집하세요. 획득한 기록지는 I키로 확인할 수 있습니다.','세 기록을 확보하면 NOTE를 확인할 수 있습니다.','걱정하지 마십시오. 이번에는 제가 정확한 비밀번호를 안내하겠습니다.'];let echoIndex=0;
// 튜토리얼과 동일하게 SPACE 1회는 타이핑 완료, 다음 SPACE는 다음 대사.
let typingTimer=null,typingDone=true,fullEcho='',deferredEcho=null;
function echoSay(message){
 clearTimeout(typingTimer);fullEcho=message;typingDone=false;$('echoNext').classList.remove('ready');
 const el=$('echoText');el.textContent='';let i=0;
 function typeNext(){if(i>=fullEcho.length){typingDone=true;$('echoNext').classList.add('ready');return;}el.textContent+=fullEcho[i++];typingTimer=setTimeout(typeNext,25)}
 typeNext();
}
function nextEcho(){
 if(!typingDone){clearTimeout(typingTimer);$('echoText').textContent=fullEcho;typingDone=true;$('echoNext').classList.add('ready');return;}
 if(echoIndex<echoLines.length)echoSay(echoLines[echoIndex++]);
}
const recordImages={A:'__RECORDA__',B:'__RECORDB__',C:'__RECORDC__'};
// CSS의 px 이동량을 상호작용 좌표에도 반영한다.
const objects=[{id:'terminalA',x:34,y:44,k:'A'},{id:'terminalB',x:66,y:44,k:'B'},{id:'terminalC',x:50,y:71.7,k:'C'},{id:'noteProp',x:37,y:29,k:'NOTE'},{id:'keypadProp',x:63,y:29,k:'KEYPAD'},{id:'exitDoor',x:50,y:24,k:'EXIT'}];

// 저장된 Stage 01 진행 상태를 복원합니다.
const SAVE_KEY='project_logic_stage01_progress_v6';
let timedOut=false;
const resetSaved=__RESET_SAVE__;
if(resetSaved){try{localStorage.removeItem(SAVE_KEY)}catch(e){}}
function saveProgress(){
 if(timedOut)return;
 try{localStorage.setItem(SAVE_KEY,JSON.stringify({x,y,remaining,records:{...records},noteRead,doorOpen,digits,echoIndex}))}catch(e){}
}
if(!resetSaved){try{
 const saved=JSON.parse(localStorage.getItem(SAVE_KEY)||'null');
 if(saved&&Number.isFinite(saved.x)&&Number.isFinite(saved.y)){
  x=saved.x;y=saved.y;remaining=Math.max(0,Math.min(600,Number(saved.remaining)||0));
  for(const k of ['A','B','C'])records[k]=Boolean(saved.records?.[k]);
  noteRead=Boolean(saved.noteRead);doorOpen=Boolean(saved.doorOpen);
  if(/^[0-9]{4}$/.test(saved.digits))digits=saved.digits;
  echoIndex=Math.max(0,Math.min(echoLines.length,Number(saved.echoIndex)||0));
  if(doorOpen){$('wallLayer').style.visibility='hidden';$('wallOpenLayer').style.visibility='visible';}
 }
}catch(e){}}
if(echoIndex<echoLines.length) echoSay(echoLines[echoIndex++]);
else echoSay('기록 보관실의 조사 절차를 계속하십시오.');
checkGlow();
let leaving=false;
let entering=true;const transition=$('stageTransition');setTimeout(()=>transition.classList.add('hide'),2700);setTimeout(()=>{transition.remove();entering=false;last=performance.now();$('gameRoot').focus()},3150);
const player=$('player');
// 열린 벽 이미지를 미리 불러와 문 전환 시 크기 재계산을 방지합니다.
const openWallPreload=new Image();openWallPreload.src='__WALLSOPEN__';
function draw(){player.style.left=x+'%';player.style.top=y+'%';$('room').classList.toggle('show-upper-player',y<30&&(x<23||x>77))}
// The collision surface is derived from the rendered WALL image (not the floor).
// A flood fill from the room centre keeps movement inside the wall frame.
const wallHitCanvas=document.createElement('canvas');
wallHitCanvas.width=1200;wallHitCanvas.height=900;
const wallHitContext=wallHitCanvas.getContext('2d',{willReadFrequently:true});
let wallWalkable=null;
function rebuildWallWalkable(){
 const image=doorOpen?$('wallOpenLayer'):$('wallLayer');if(!image.complete||!image.naturalWidth)return;
 try{
  wallHitContext.clearRect(0,0,1200,900);
  wallHitContext.drawImage(image,doorOpen?(-8*1200/Math.max(1,$('room').clientWidth)):(-10*1200/Math.max(1,$('room').clientWidth)),0,1200,900);
  const rgba=wallHitContext.getImageData(0,0,1200,900).data;
  const width=300,height=225,occupied=new Uint8Array(width*height);
  for(let cy=0;cy<height;cy++)for(let cx=0;cx<width;cx++){
   let solid=false;
   for(let yy=0;yy<4&&!solid;yy++)for(let xx=0;xx<4;xx++){
    if(rgba[(((cy*4+yy)*1200)+(cx*4+xx))*4+3]>100){solid=true;break}
   }
   occupied[cy*width+cx]=solid?1:0;
  }
  const region=new Uint8Array(width*height);
  const queue=new Int32Array(width*height);let read=0,write=0;
  const start=112*width+150;
  if(!occupied[start]){region[start]=1;queue[write++]=start}
  while(read<write){
   const p=queue[read++],cx=p%width,cy=(p/width)|0;
   const neighbors=[cx>0?p-1:-1,cx<width-1?p+1:-1,cy>0?p-width:-1,cy<height-1?p+width:-1];
   for(const n of neighbors)if(n>=0&&!occupied[n]&&!region[n]){region[n]=1;queue[write++]=n}
  }
  wallWalkable=region;
 }catch(e){wallWalkable=null}
}
$('wallLayer').addEventListener('load',rebuildWallWalkable);$('wallOpenLayer').addEventListener('load',()=>{if(doorOpen)rebuildWallWalkable()}); if($('wallLayer').complete)rebuildWallWalkable();
function insideWall(nx,ny){
 const cx=Math.round(nx*3),cy=Math.round(ny*2.25);
 if(cx<0||cy<0||cx>=300||cy>=225||!wallWalkable)return false;
 for(const [dx,dy] of [[0,0],[-3,-4],[3,-4],[-3,4],[3,4]]){
  const ix=cx+dx,iy=cy+dy;
  if(ix<0||iy<0||ix>=300||iy>=225||!wallWalkable[iy*300+ix])return false;
 }
 return true;
}
// 충돌 영역은 이미지 요소의 실제 표시 크기를 기준으로 계산합니다.
function objectRect(o){
 const el=$(o.id),room=$('room').getBoundingClientRect(),r=el.getBoundingClientRect();
 return {cx:(r.left+r.width/2-room.left)/room.width*100,cy:(r.top+r.height/2-room.top)/room.height*100,
  hw:r.width/room.width*50,hh:r.height/room.height*50};
}
// 열린 문 벽의 안쪽 경계만 이동 제한으로 사용합니다.
function canMove(nx,ny){
 if(!insideWall(nx,ny))return false;
 // 터미널과 NOTE·키패드 이미지에만 충돌 판정을 적용합니다.
 for(const o of objects){
  if(o.k==='EXIT')continue;
  const r=objectRect(o),marginX=o.k==='NOTE'||o.k==='KEYPAD'?0.7:1.2;
  const marginY=o.k==='NOTE'||o.k==='KEYPAD'?0.7:1.5;
  if(Math.abs(nx-r.cx)<r.hw+marginX&&Math.abs(ny-r.cy)<r.hh+marginY)return false;
 }
 return true;
}
function togglePause(value){paused=value;$('pauseOverlay').style.display=paused?'flex':'none';$('pauseToggle').textContent=paused?'▶':'Ⅱ';$('pauseToggle').classList.toggle('paused',paused);keys.clear()}
function closePanels(){$('helpOverlay').style.display='none';$('inventoryOverlay').style.display='none';keys.clear()}
$('pauseToggle').onclick=()=>{if(!timedOut)togglePause(!paused)};$('resumeButton').onclick=()=>{if(!timedOut)togglePause(false)};
// 게임 안의 버튼 클릭을 Streamlit의 재시작·타이틀 버튼에 전달한다.
function hostAction(action){
 const selector=action==='timeout_title'?'[class*=st-key-stage01_timeout_title] button':action==='title'?'[class*=st-key-stage01_title] button':action==='next'?'[class*=st-key-stage01_next] button':'[class*=st-key-stage01_restart] button';
 try{window.parent.document.querySelector(selector)?.click()}catch(e){}
}
function clearAllGameStorage(){
 for(const owner of [window,window.parent]){
  for(const type of ['localStorage','sessionStorage']){
   try{const store=owner[type],keys=[];
    for(let i=0;i<store.length;i++){const key=store.key(i);if(key&&(key.startsWith('project_logic_')||key.startsWith('logic_tutorial_')))keys.push(key)}
    keys.forEach(key=>store.removeItem(key));
   }catch(e){}
  }
 }
}
function timeoutTitle(){
 leaving=true;keys.clear();clearAllGameStorage();hostAction('timeout_title');
}
$('restartButton').onclick=()=>{try{localStorage.removeItem(SAVE_KEY)}catch(e){}hostAction('restart')};$('titleButton').onclick=()=>{if(timedOut){timeoutTitle();return}saveProgress();const screen=$('dataSavingScreen');screen.classList.add('active');togglePause(true);setTimeout(()=>hostAction('title'),3000)};
document.addEventListener('keydown',e=>{const k=e.key.toLowerCase();if(timedOut){e.preventDefault();return}if(['arrowup','arrowdown','arrowleft','arrowright',' '].includes(k))e.preventDefault();if(e.repeat&&['escape','h','i'].includes(k))return;
if(k==='escape'){if(dialogOpen){closeDialog();return}if($('helpOverlay').style.display==='flex'||$('inventoryOverlay').style.display==='flex'){closePanels();return}togglePause(!paused);return}
if(k==='h'&&!paused&&!dialogOpen){const el=$('helpOverlay');const opening=el.style.display!=='flex';closePanels();if(opening)el.style.display='flex';return}
if(k==='i'&&!paused&&!dialogOpen){const el=$('inventoryOverlay');const opening=el.style.display!=='flex';closePanels();if(opening){renderInventory();el.style.display='flex'}return}
if(k==='e'&&!paused&&!entering&&!dialogOpen&&$('inventoryOverlay').style.display!=='flex'&&$('helpOverlay').style.display!=='flex'){interact();return}
if(k===' '&&dialogOpen){closeDialog();return}if(k===' '&&!dialogOpen&&!paused){nextEcho();return}
keys.add(k)});
// 포커스가 버튼으로 이동해도 이동키 입력을 유지한다.
$('gameRoot').addEventListener('pointerdown',()=>{$('gameRoot').focus()});
document.addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));
window.addEventListener('blur',()=>keys.clear());
// 프레임 간 시간차로 이동량과 10분 제한시간을 갱신한다.
function tick(now){let dt=Math.min((now-last)/1000,.05);last=now;if(!paused&&!entering&&!leaving&&!dialogOpen&&$('helpOverlay').style.display!=='flex'&&$('inventoryOverlay').style.display!=='flex'){let dx=0,dy=0;if(keys.has('a')||keys.has('arrowleft'))dx--;if(keys.has('d')||keys.has('arrowright'))dx++;if(keys.has('w')||keys.has('arrowup'))dy--;if(keys.has('s')||keys.has('arrowdown'))dy++;if(dx||dy){const l=Math.hypot(dx,dy);dx=dx/l*78*dt;dy=dy/l*78*dt;if(canMove(x+dx,y))x+=dx;if(canMove(x,y+dy))y+=dy;draw()}
}if(!paused&&!entering&&!leaving){remaining=Math.max(0,remaining-dt);}if(!paused&&!entering&&!leaving){const sec=Math.ceil(remaining);$('timer').textContent=String(Math.floor(sec/60)).padStart(2,'0')+':'+String(sec%60).padStart(2,'0');if(remaining===0&&!timedOut){timedOut=true;closePanels();$('dialogOverlay').style.display='none';dialogOpen=false;$('pauseOverlay').classList.add('timeout-mode');togglePause(true);$('echoText').textContent='제한 시간이 종료되었습니다.'}}
updateHint();requestAnimationFrame(tick)}draw();requestAnimationFrame(tick);
setInterval(()=>{if(!leaving)saveProgress()},1500);
window.addEventListener('pagehide',()=>{if(!leaving)saveProgress()});
// 상호작용 거리는 각 오브제 이미지의 가장자리에서 측정합니다.
function objectDistance(o){
 if(o.k==='EXIT')return Math.hypot((x-50)*.843,(y-24)*.619);
 const r=objectRect(o),dx=Math.max(0,Math.abs(x-r.cx)-r.hw),dy=Math.max(0,Math.abs(y-r.cy)-r.hh);
 return Math.hypot(dx*.843,dy*.619);
}
function nearest(){
 let best=null,dist=Infinity;
 for(const o of objects){if(o.k==='EXIT'&&!doorOpen)continue;const d=objectDistance(o);if(d<dist){best=o;dist=d}}
 return dist<(best?.k==='EXIT'?8:best?.k==='KEYPAD'?8.5:4.8)?best:null;
}
function updateHint(){const o=nearest();$('interactionHint').style.display=o&&!leaving&&!dialogOpen&&!paused?'block':'none';if(o)$('interactionHint').textContent=o.k==='NOTE'?'E // READ NOTE':o.k==='KEYPAD'?'E // ACCESS KEYPAD':o.k==='EXIT'?'E // EXIT':`E // INVESTIGATE TERMINAL ${o.k}`}
function openDialog(content){dialogOpen=true;$('gameRoot').classList.add('dialog-active');keys.clear();$('dialogContent').innerHTML=content+`<div style="text-align:right"><button onclick="closeDialog()">CLOSE [SPACE]</button></div>`;$('dialogOverlay').style.display='flex'}
function closeDialog(){dialogOpen=false;$('gameRoot').classList.remove('dialog-active');$('dialogOverlay').style.display='none';keys.clear();if(deferredEcho){const message=deferredEcho;deferredEcho=null;echoSay(message)}}
$('dialogOverlay').addEventListener('click',e=>{if(e.target===$('dialogOverlay'))closeDialog()});
let audioCtx;
function scribble(){
 try{
  const AC=window.AudioContext||window.webkitAudioContext;
  if(!AC)return;
  audioCtx=audioCtx||new AC();
  audioCtx.resume();const now=audioCtx.currentTime;
  for(let stroke=0;stroke<7;stroke++){
   const duration=.085+Math.random()*.06;
   const buffer=audioCtx.createBuffer(1,Math.ceil(audioCtx.sampleRate*duration),audioCtx.sampleRate);
   const data=buffer.getChannelData(0);
   let prev=0;
   for(let i=0;i<data.length;i++){
    const noise=Math.random()*2-1;
    prev=prev*.54+noise*.46;
    const env=Math.pow(Math.sin(Math.PI*i/data.length),.8);
    data[i]=prev*env*.48;
   }
   const src=audioCtx.createBufferSource();src.buffer=buffer;
   const filter=audioCtx.createBiquadFilter();filter.type='bandpass';
   filter.frequency.value=1250+Math.random()*950;filter.Q.value=.65;
   const gain=audioCtx.createGain();gain.gain.value=.16;
   src.connect(filter).connect(gain).connect(audioCtx.destination);
   src.start(now+stroke*.075);
  }
 }catch(e){}
}
function renderInventory(){const keys=Object.keys(records).filter(k=>records[k]);$('itemDescription').textContent='ITEM DESCRIPTION / 기록지를 선택하면 설명이 표시됩니다.';$('inventoryItems').innerHTML=Array.from({length:12},(_,i)=>keys[i]?`<button class="inventory-slot" onclick="showRecord('${keys[i]}')" title="기록지 ${keys[i]}"><img src="${recordImages[keys[i]]}" alt="기록지 ${keys[i]}"></button>`:`<div class="inventory-slot"><span class="slot-number">${String(i+1).padStart(2,'0')}</span></div>`).join('')}
function showRecord(k){$('inventoryItems').querySelectorAll('.inventory-slot').forEach(el=>el.classList.remove('selected'));const idx=Object.keys(records).filter(v=>records[v]).indexOf(k);$('inventoryItems').children[idx]?.classList.add('selected');$('itemDescription').textContent=`조사 기록지 ${k} / ${recordText(k)}`;}
function recordText(k){return k==='A'?`기록 A / 접근 인증값: ${digits[1]} — 순서 단서는 NOTE에 보관되어 있다.`:k==='B'?`기록 B / 접근 인증값: ${digits[2]} — 모든 기록을 대조해야 한다.`:`기록 C / 접근 인증값: ${digits[0]}${digits[3]} — 첫 번째와 마지막 자릿수이다.`}
function checkGlow(){if(Object.values(records).every(Boolean)&&!noteRead)$('noteProp').classList.add('glow');else $('noteProp').classList.remove('glow');$('keypadProp').classList.toggle('glow',noteRead&&!doorOpen)}
function interact(){if(paused||entering||!typingDone||echoIndex<echoLines.length)return;const o=nearest();if(!o||leaving)return;if(o.k==='EXIT'){leaveStage();return;}if('ABC'.includes(o.k)&&o.k.length===1){const first=!records[o.k];records[o.k]=true;if(first){scribble();}checkGlow();deferredEcho=`터미널 ${o.k}의 기록을 확보했습니다. 인벤토리(I)에 기록지가 저장되었습니다.`;openDialog(`<h3>TERMINAL ${o.k} // INVESTIGATION COMPLETE</h3><img src="${recordImages[o.k]}"><p>${recordText(o.k)}</p><p>${first?'기록지가 인벤토리에 추가되었습니다.':'이미 확보한 기록입니다.'}</p>`);return}
if(o.k==='NOTE'){if(!Object.values(records).every(Boolean)){openDialog('<h3>NOTE // 잠금</h3>세 터미널의 기록을 모두 수집한 뒤 확인할 수 있습니다.');return}scribble();noteRead=true;checkGlow();openDialog(`<h3>NOTE // 인증 절차</h3><img src="__NOTE__"><p>이 보관실은 세 단말기에 분산된 인증 기록을 복원해야 출구가 개방된다.</p><p>기록을 읽는 순서는 <strong>C → A → B</strong>이다. C에는 첫째·넷째 자리, A에는 둘째 자리, B에는 셋째 자리가 기록되어 있다.</p><p>수집한 네 자릿수를 순서대로 입력하면 출구 잠금이 해제된다.</p>`);deferredEcho=`기록 복원이 완료되었습니다. 키패드의 정답은 ${digits}입니다. 안내한 번호를 그대로 입력하십시오.`;return}
if(o.k==='KEYPAD'){if(!noteRead){openDialog('<h3>SECURITY // LOCKED</h3>NOTE를 확인하고 인증 절차를 복원해야 합니다.');return}if(doorOpen){openDialog('<h3>EXIT OPEN</h3>출구가 열렸습니다.');return}enteredCode='';showKeypad()}}
function showKeypad(){openDialog(`<h3>SECURITY // ACCESS CODE</h3><p>에코가 안내한 네 자리 인증번호: <strong>${digits}</strong></p><div id="keypadDigits">${enteredCode.padEnd(4,'_')}</div><div class="keygrid">${['1','2','3','4','5','6','7','8','9','←','0','OK'].map(v=>`<button onclick="keyInput('${v}')">${v}</button>`).join('')}</div>`)}
function beep(){try{audioCtx=audioCtx||new(window.AudioContext||window.webkitAudioContext)();audioCtx.resume();const o=audioCtx.createOscillator(),g=audioCtx.createGain();o.type='square';o.frequency.value=820;g.gain.setValueAtTime(.035,audioCtx.currentTime);g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+.085);o.connect(g).connect(audioCtx.destination);o.start();o.stop(audioCtx.currentTime+.09)}catch(e){}}
function keyInput(v){beep();if(v==='←')enteredCode=enteredCode.slice(0,-1);else if(v==='OK'){if(enteredCode===digits){doorOpen=true;$('wallLayer').style.visibility='hidden';$('wallOpenLayer').style.visibility='visible';rebuildWallWalkable();checkGlow();closeDialog();deferredEcho='인증 성공. 출구가 열렸습니다. 문 앞에서 E키를 누르면 다음 구역으로 이동합니다.';openDialog('<h3>ACCESS GRANTED</h3><p>보관실 출구의 잠금이 해제되었습니다. 문이 열렸습니다.</p>');return}else{enteredCode='';echoSay('인증 실패. 기록지를 다시 확인하십시오.')}}else if(enteredCode.length<4)enteredCode+=v;showKeypad()}
// 열린 출구에서 E키를 누르면 1초 암전 후 Stage 02로 이동합니다.
function leaveStage(){
 if(!doorOpen||leaving)return;
 try{localStorage.setItem("project_logic_stage02_handoff_v1",JSON.stringify({remaining,from:"stage01"}));localStorage.removeItem("project_logic_stage02_progress_v1");localStorage.removeItem(SAVE_KEY)}catch(e){}
 leaving=true;keys.clear();closeDialog();
 const fade=document.createElement('div');fade.id='exitFade';
 fade.style.cssText='position:fixed;inset:0;background:#000;opacity:0;z-index:4000;transition:opacity 1s linear;pointer-events:auto';
 document.body.appendChild(fade);requestAnimationFrame(()=>fade.style.opacity='1');
 setTimeout(()=>hostAction('next'),1000);
}
objects.filter(o=>o.k!=='EXIT').forEach(o=>$(o.id).addEventListener('click',()=>{if(!paused&&!entering&&typingDone&&echoIndex>=echoLines.length){const d=objectDistance(o);if(d<(o.k==='KEYPAD'?8.5:4.8)){interact();}else echoSay('오브제 가까이 이동한 후 E키로 조사하십시오.')}}));

</script><div class="data-saving-screen" id="dataSavingScreen"><div class="data-saving-label"><span class="data-saving-gear">⚙</span>DATA SAVING...</div></div></body></html>"""
for token,name in {"__FLOOR__":"floor.png","__WALLS__":"walls.png","__WALLSOPEN__":"walls_open.png","__TERMINALA__":"terminal_A.png","__TERMINALB__":"terminal_B.png","__TERMINALC__":"terminal_C.png","__NOTE__":"note.png","__KEYPAD__":"keypad.png","__RECORDA__":"record_A.png","__RECORDB__":"record_B.png","__RECORDC__":"record_C.png"}.items():
    html=html.replace(token,data(root/"assets/stage01"/name))
html=html.replace("__FONT__",font)
html=html.replace("__RESET_SAVE__", "true" if reset_save else "false")
html = html.replace("</head>", '<style id="logic-v9-iframe-ui">\n/* This style lives INSIDE the components.html iframe, unlike v8\'s Streamlit-level CSS. */\n#helpOverlay,#inventoryOverlay{position:fixed!important;inset:0!important;z-index:4000!important;background:rgba(0,0,0,.70)!important;align-items:center!important;justify-content:center!important;overflow:hidden!important}\n#helpOverlay .help-panel,#helpOverlay .utility-panel{box-sizing:border-box!important;width:min(760px,90vw)!important;max-width:90vw!important;max-height:90vh!important;overflow:hidden!important;padding:24px 32px!important}\n#helpOverlay .help-row{display:grid!important;grid-template-columns:32px 260px minmax(0,1fr)!important;grid-template-rows:auto!important;gap:2px 14px!important;align-items:center!important;padding:9px 0!important;min-width:0!important;border-bottom:1px solid #17495b!important}\n#helpOverlay .help-number{grid-column:1!important;grid-row:1!important;display:block!important;width:auto!important;min-width:0!important;height:auto!important;color:#61e8ff!important;border:0!important;background:none!important;box-shadow:none!important}\n#helpOverlay .help-key{grid-column:2!important;grid-row:1!important;display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;align-items:center!important;gap:12px!important;min-width:0!important;width:auto!important;height:auto!important;padding:0!important;border:0!important;background:none!important;box-shadow:none!important;font-size:12px!important}\n#helpOverlay .help-key .control-label{position:static!important;display:inline!important;flex:0 0 128px!important;min-width:0!important;width:auto!important;height:auto!important;padding:0!important;transform:none!important;clip-path:none!important;border:0!important;background:none!important;box-shadow:none!important;color:#63e8ff!important;font-size:12px!important}\n#helpOverlay .help-key .control-separator{position:static!important;display:inline!important;flex:0 0 auto!important;color:#637985!important}\n#helpOverlay .help-key .control-button{position:static!important;display:inline!important;flex:0 0 auto!important;min-width:0!important;width:auto!important;height:auto!important;padding:0!important;transform:none!important;clip-path:none!important;border:0!important;background:none!important;box-shadow:none!important;color:#f2fbff!important;font-size:12px!important;line-height:1.4!important}\n#helpOverlay .help-description{grid-column:3!important;grid-row:1!important;color:#8c9da7!important;font-size:11px!important;line-height:1.5!important;min-width:0!important}\n#helpOverlay .help-important{margin-top:14px!important;padding:12px 14px!important}\n#inventoryOverlay .inventory-panel,#inventoryOverlay .utility-panel{box-sizing:border-box!important;width:min(760px,90vw)!important;max-height:90vh!important;overflow:hidden!important;padding:24px!important}\n#inventoryOverlay .inventory-grid{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;grid-template-rows:repeat(3,minmax(0,1fr))!important;gap:8px!important;max-height:min(55vh,470px)!important;overflow:hidden!important}\n#inventoryOverlay .inventory-slot{position:relative!important;min-width:0!important;min-height:0!important;aspect-ratio:1.1!important;background:#01060b!important;border:1px solid #28546a!important}\n#inventoryOverlay .item-description{margin-top:12px!important;min-height:56px!important;padding:12px!important;border:1px solid #48dfff!important;color:#d9faff!important}\n#pauseOverlay,.pause-overlay{z-index:9000!important;background:rgba(0,0,0,.72)!important;backdrop-filter:blur(3px)!important}\n#pauseOverlay .pause-menu-panel,.pause-overlay .pause-menu-panel{box-shadow:0 0 0 1px #123c4d,0 0 22px #00cfff55,0 0 100px #00cfff20!important}\n#pauseToggle,.pause-toggle{z-index:9100!important}\n.item-acquired-notice.show{z-index:4500!important}\n.item-acquired-text{font-size:12px!important;line-height:1.6!important}\n.echo-next{color:#4b8da0!important;opacity:.85!important}\n#dataSavingScreen:not(.active){display:none!important}\n#floorLayer,#wallLayer{width:100%!important;height:100%!important;object-fit:fill!important}\n</style>' + "</head>", 1)
html = html.replace('</head>', '<style id="logic-v11-gameplay">' + '\n/* v11: tutorial-matched entrance and slow low-contrast ECHO prompt */\n.stage-transition-card{\n  text-shadow:0 0 5px #fff,0 0 12px #00dfff!important;\n  animation:neonFaultOnce .85s steps(1,end) 1 both!important;\n}\n.stage-transition-stage,.stage-transition-room{animation:none!important}\n@keyframes neonFaultOnce{\n  0%,18%,22%,100%{opacity:1;filter:none}\n  19%,21%{opacity:.22;filter:brightness(.4)}\n}\n.echo-next,.echo-next.ready,.echo-next:not(.ready){\n color:#80bbc8!important;\n opacity:.65!important;\n animation:logicSlowBlink 3s ease-in-out infinite!important;\n}\n@keyframes logicSlowBlink{0%,100%{filter:opacity(.35)}50%{filter:opacity(.9)}}\n\n/* v11: closed and open Stage 01 wall sprites share the SAME physical rectangle. */\n.room #floorLayer,.room #wallLayer{\n position:absolute!important;left:0!important;top:0!important;right:auto!important;bottom:auto!important;\n width:100%!important;height:100%!important;min-width:100%!important;min-height:100%!important;\n transform:none!important;object-fit:fill!important;transform-origin:center center!important;\n image-rendering:pixelated!important;\n}\n.room #wallLayer{clip-path:none!important}\n.game #interactionHint{bottom:calc(5% + 135px)!important;z-index:30!important}\n' + '</style></head>', 1)
html = html.replace("</head>", '<style id="logic-timeout-actions">#pauseOverlay.timeout-mode .pause-row:first-child{display:none!important}</style></head>', 1)
html = html.replace("</head>", '<style id="logic-v14-wall-sync">\n/* Preloaded full-canvas closed/open wall sprites. Keep precisely the same render box. */\n.room #wallLayer,.room #wallOpenLayer {\n position:absolute!important;left:0!important;top:0!important;right:auto!important;bottom:auto!important;\n width:100%!important;height:100%!important;min-width:100%!important;min-height:100%!important;\n margin:0!important;padding:0!important;max-width:none!important;max-height:none!important;\n transform:none!important;transform-origin:center center!important;object-fit:fill!important;\n image-rendering:pixelated!important;filter:none!important;clip-path:none!important;\n z-index:4!important;pointer-events:none!important;\n}\n.room.show-upper-player #wallLayer,.room.show-upper-player #wallOpenLayer{z-index:2!important}\n</style>' + "</head>", 1)
html = html.replace("</head>", '\n<style id="logic-v14-shared-prompt">\n/* Identical typography and ready state to the tutorial ECHO prompt. */\n.echo-bar {box-sizing:border-box!important;padding-bottom:29px!important;min-height:88px!important}\n.echo-bar #echoText {display:block!important;margin:0!important;padding:0 0 8px!important;max-width:100%!important;white-space:normal!important;overflow-wrap:anywhere!important}\n.echo-bar #echoNext.echo-next {\n position:absolute!important;right:14px!important;bottom:7px!important;\n font:9px/1.4 NeoDungGeunMo,monospace!important;letter-spacing:normal!important;\n pointer-events:none!important;color:#6c8791!important;opacity:1!important;\n animation:none!important;text-shadow:none!important;\n}\n.echo-bar #echoNext.echo-next.ready {color:#f5ffff!important;animation:tutorialEchoBlink .8s steps(2,end) infinite!important}\n@keyframes tutorialEchoBlink {50%{opacity:.35}}\n</style>\n' + "</head>", 1)
# 실제 표시 위치와 충돌 판정의 픽셀 이동값을 일치시킵니다.
html = html.replace('</head>', '<style id="stage01-wall-final-offset">.room #wallLayer{left:-10px!important}.room #wallOpenLayer{left:-8px!important;top:0!important;transform:none!important}</style></head>', 1)
components.html(html,height=800,scrolling=False)
