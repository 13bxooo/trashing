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
# 이미지 및 글꼴을 HTML에 삽입하기 위한 Base64 인코딩 모듈
import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지의 제목, 폭, 사이드바 상태를 설정한다.
st.set_page_config(page_title="PROJECT : LOGIC // STAGE 01",layout="wide",initial_sidebar_state="collapsed")
# Handle the Stage 01 restart on the Streamlit host, not only inside the iframe.
# URL 매개변수를 확인해 재시작 또는 타이틀 이동 요청을 처리한다.
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

# pages 폴더의 상위 폴더를 프로젝트 루트로 사용한다.
root=Path(__file__).resolve().parent.parent
# PNG를 브라우저에서 표시 가능한 data URL 문자열로 변환한다.
def data(path):
    return "data:image/png;base64,"+base64.b64encode(path.read_bytes()).decode("ascii")
# NeoDungGeunMo 글꼴 파일이 있으면 읽어 온다.
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
</style>""",unsafe_allow_html=True)
# Parent-host navigation buttons preserve Streamlit's page switching.
# iframe 내부의 버튼이 부모 Streamlit에 명령을 전달하도록 숨김 버튼을 둔다.
a,b=st.columns(2)
with a:
    title=st.button("TITLE",key="stage01_title")
with b:
    restart=st.button("RESTART",key="stage01_restart")
if title:st.switch_page("main.py")
if restart:
    for _key in list(st.session_state.keys()):
        if _key.startswith(("s1_", "stage01_")):
            del st.session_state[_key]
    st.session_state["stage01_started"] = True
    st.session_state["stage01_reset_save"] = True
    st.session_state["game_paused"] = False
    st.rerun()
st.markdown("<style>.st-key-stage01_title,.st-key-stage01_restart{position:fixed!important;left:-9999px!important;top:0!important}</style>",unsafe_allow_html=True)
# 아래 문자열은 실제 게임 화면의 HTML, CSS, JavaScript 전체를 포함한다.
html='''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n<style>\n@font-face{font-family:NeoDungGeunMo;src:url(data:font/ttf;base64,__FONT__)}\n*{box-sizing:border-box}\nhtml,body{margin:0;width:100%;height:100%;overflow:hidden;background:#02050a;color:#e5faff;font-family:NeoDungGeunMo,monospace}\n.game{position:relative;width:100vw;height:100vh;overflow:hidden;background:#02050a;outline:none}\n.project-title{position:absolute;top:24px;left:28px;font-size:20px;letter-spacing:1px;color:#fff;z-index:20}\n.stage-title{position:absolute;top:56px;left:28px;font-size:13px;letter-spacing:1px;color:#426b7d;z-index:20}\n.pause-toggle{position:absolute;top:20px;right:24px;z-index:1000;width:42px;height:42px;display:flex;align-items:center;justify-content:center;background:#02070c;border:1px solid #54dfff;color:#8defff;font:20px NeoDungGeunMo,monospace;line-height:1;text-align:center;cursor:pointer;box-shadow:0 0 0 1px #123c4d;padding:0;line-height:1}\n.pause-toggle:before,.pause-toggle:after{content:"";position:absolute;width:7px;height:7px;border-color:#8af0ff;border-style:solid}\n.pause-toggle:before{left:-2px;top:-2px;border-width:2px 0 0 2px}.pause-toggle:after{right:-2px;bottom:-2px;border-width:0 2px 2px 0}\n.pause-toggle.paused{background:#d9faff;color:#001018}\n.stage01-timer{position:absolute;right:86px;top:32px;font-size:12px;color:#a9c4d0;z-index:20}\n.game-area{position:absolute;top:45px;left:0;right:0;bottom:10px;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#02050a}\n.room{position:relative;width:min(98vw,calc((100vh - 60px)*4/3));aspect-ratio:4/3;flex-shrink:0;overflow:hidden;background:transparent}\n.room img.layer{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;pointer-events:none;image-rendering:pixelated;filter:none;backface-visibility:hidden}\n#floorLayer{z-index:1}#wallLayer{z-index:4;clip-path:polygon(0 0,100% 0,100% 100%,0 100%)}\n.room.show-upper-player #wallLayer{z-index:2}.room.show-upper-player .player{z-index:5}
.player{position:absolute;z-index:3;width:24px;height:24px;background:#d5e7ee;border:0;border-radius:0;box-shadow:inset 0 0 0 4px #7895a5,inset 0 -7px #263d4d,-4px 0 #152a39,4px 0 #152a39,0 -3px #152a39,0 3px #152a39;image-rendering:pixelated;transform:translate(-50%,-50%);pointer-events:none}\n.player:before{content:"";position:absolute;left:4px;right:4px;top:-7px;height:8px;background:#c5d8e0;border:2px solid #142b3a;box-shadow:inset 0 -3px #7896a5}.player:after{content:"";position:absolute;left:6px;right:6px;top:2px;height:3px;background:#5ceaff;box-shadow:0 0 3px #5ceaff}\n.status{position:absolute;bottom:24px;left:28px;color:#777;font-size:14px}\n.pause-overlay{position:fixed;inset:0;z-index:2000;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.72)}\n.pause-menu-panel{position:relative;width:min(536px,86vw);height:274px;padding:34px 48px;display:flex;align-items:center;background:linear-gradient(135deg,#030b12,#061722);border:1px solid #54dfff}\n.pause-actions{display:flex;flex-direction:column;gap:8px}\n.pause-row{display:flex;align-items:center;gap:16px;height:55px}\n.pause-icon{width:38px;height:38px;flex:0 0 38px;border:1px solid #58dfff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#82eaff;font-size:14px}\n.pause-nav-link{border:0;background:none;color:#d8faff;font:18px NeoDungGeunMo,monospace;text-align:left;cursor:pointer;text-decoration:none}\n.pause-nav-link:hover{color:white;text-shadow:0 0 6px #54dfff}\n.game.dialog-active .echo-bar{display:none}
.echo-bar{position:absolute;left:50%;bottom:5%;transform:translateX(-50%);width:min(78%,650px);min-height:78px;padding:14px 20px;background:rgba(1,12,19,.92);border:1px solid #2dbbd8;z-index:10;font-size:12px;line-height:1.6}\n.echo-head{font-size:11px;color:#50dfff;margin-bottom:7px}\n#helpOverlay,#inventoryOverlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1500;align-items:center;justify-content:center}\n.utility-panel{position:relative;width:min(820px,88vw);background:#02070c;border:1px solid #48dfff;box-shadow:0 0 0 1px #123c4d;padding:24px 26px 26px;font-size:15px;line-height:1.8;max-height:84vh;overflow:auto}\n.utility-panel h3{color:#67eaff;margin:0 0 12px}.panel-header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #2587a7;padding-bottom:12px;margin-bottom:16px}.panel-hint{font-size:11px;color:#659caf}.inventory-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.inventory-slot{aspect-ratio:1;background:#01060b;border:1px solid #28546a;color:#c9f9ff;display:flex;align-items:center;justify-content:center;cursor:pointer}.inventory-slot img{width:80%;height:75%;object-fit:contain;image-rendering:pixelated}.help-row{display:grid;grid-template-columns:50px 145px 1fr;gap:15px;border-bottom:1px solid #17313d;padding:12px 4px}.help-number,.help-key{color:#7deaff}\n.utility-panel button{background:transparent;color:#aaf5ff;border:1px solid #54dfff;padding:8px 16px;cursor:pointer;font:inherit}\n.stage-transition{position:fixed;inset:0;z-index:3000;display:flex;align-items:center;justify-content:center;background:#000;opacity:1;transition:opacity .45s steps(6,end);pointer-events:auto}\n.stage-transition.hide{opacity:0;pointer-events:none}\n.stage-transition-card{position:relative;width:min(350px,78vw);min-height:145px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:1px solid #57dfff;color:#f5fbff;box-shadow:0 0 0 1px #143d4c,0 0 14px #00cfff22;letter-spacing:2px}\n.stage-transition-card:before,.stage-transition-card:after{content:"";position:absolute;width:18px;height:18px;border-color:#78ecff;border-style:solid}\n.stage-transition-card:before{top:-2px;left:-2px;border-width:2px 0 0 2px}.stage-transition-card:after{right:-2px;bottom:-2px;border-width:0 2px 2px 0}\n.stage-transition-stage{font-size:clamp(25px,4vw,36px);line-height:1.6;text-shadow:0 0 5px #fff,0 0 14px #57dfff}.stage-transition-room{font-size:clamp(14px,2vw,20px);color:#a8f2ff;letter-spacing:1px}\n
/* 모든 오브제 이미지의 공통 크기·위치·그림자 스타일 */
.prop{position:absolute;z-index:2;transform:translate(-50%,-50%);object-fit:contain;cursor:pointer;image-rendering:pixelated;filter:drop-shadow(2px 2px 0 #02090e) drop-shadow(-2px -2px 0 #a4d9e3)}
/* 세 터미널의 정삼각형 배치 좌표. JS objects 좌표와 맞춰야 한다. */
#terminalA{left:34%;top:44%;width:13%}#terminalB{left:66%;top:44%;width:13%}#terminalC{left:50%;top:71.7%;width:13%}
#noteProp{left:41%;top:33%;width:7%;z-index:6}#keypadProp{left:59%;top:33%;width:7%;z-index:6}
/* 조사 단계에 따라 NOTE 또는 키패드에 적용되는 청록색 점멸 효과 */
.glow{animation:cyanPulse 2.2s ease-in-out infinite;filter:drop-shadow(0 0 5px #20f4ed) drop-shadow(0 0 11px #17bfc8)}
@keyframes cyanPulse{0%,100%{filter:drop-shadow(0 0 1px #1ec5cf)}50%{filter:drop-shadow(0 0 9px #54ffff) drop-shadow(0 0 15px #12b7bf)}}
.prop:hover{filter:drop-shadow(0 0 7px #3beaf4)}
#interactionHint{position:absolute;bottom:88px;left:50%;transform:translateX(-50%);z-index:30;background:#020a10dd;border:1px solid #3aabb8;padding:7px 14px;font-size:12px;display:none}
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
</style></head><body>\n<div class="stage-transition" id="stageTransition"><div class="stage-transition-card"><div class="stage-transition-stage">STAGE 01</div><div class="stage-transition-room">:ARCHIVE ACCESS</div></div></div>\n<div class="game" id="gameRoot" tabindex="0">\n<div class="project-title">PROJECT : LOGIC</div><div class="stage-title">STAGE 01 // ARCHIVE ACCESS</div>\n<div class="stage01-timer" id="timer">10:00</div><button class="pause-toggle" id="pauseToggle" aria-label="Pause">Ⅱ</button>\n<div class="game-area"><div class="room" id="room">\n<img id="floorLayer" class="layer" src="__FLOOR__" alt="">\n<img id="wallLayer" class="layer" src="__WALLS__" alt="">\n<img class="prop" id="terminalA" src="__TERMINALA__" alt="Terminal A"><img class="prop" id="terminalB" src="__TERMINALB__" alt="Terminal B"><img class="prop" id="terminalC" src="__TERMINALC__" alt="Terminal C"><img class="prop" id="noteProp" src="__NOTE__" alt="NOTE"><img class="prop" id="keypadProp" src="__KEYPAD__" alt="Keypad"><div class="player" id="player"></div>\n</div></div>\n<div class="echo-bar"><div class="echo-head">ECHO // AI SYSTEM</div><span id="echoText">안녕하세요. 저는 안내 시스템 ECHO입니다. 이곳은 기록 보관실이에요. 터미널 세 대의 자료를 확인하면 출구를 열 수 있습니다. [SPACE]</span></div>\n<div id="dialogOverlay"><div class="dialog" id="dialogContent"></div></div>\n<div id="interactionHint">E : 조사하기</div><div class="status">ECHO SYSTEM // ONLINE</div>\n<div class="pause-overlay" id="pauseOverlay"><div class="pause-menu-panel"><div class="pause-actions">\n<div class="pause-row"><span class="pause-icon">Ⅱ</span><button class="pause-nav-link" id="resumeButton">RESUME</button></div>\n<div class="pause-row"><span class="pause-icon">↻</span><button class="pause-nav-link" id="restartButton">RESTART</button></div>\n<div class="pause-row"><span class="pause-icon">⌂</span><button class="pause-nav-link" id="titleButton">TITLE</button></div>\n</div></div></div>\n<div id="helpOverlay"><div class="utility-panel"><div class="panel-header"><h3>HOW TO PLAY</h3><span class="panel-hint">H / ESC TO CLOSE</span></div><div class="help-row"><span class="help-number">01</span><span class="help-key">MOVEMENT<br>W A S D</span><span>캐릭터를 이동합니다.</span></div><div class="help-row"><span class="help-number">02</span><span class="help-key">INTERACTION<br>E</span><span>가까운 물체를 조사하거나 아이템을 획득합니다.</span></div><div class="help-row"><span class="help-number">03</span><span class="help-key">INVENTORY<br>I</span><span>획득한 기록지를 확인합니다.</span></div><div class="help-row"><span class="help-number">04</span><span class="help-key">SYSTEM<br>SPACE</span><span>대사를 넘기거나 조사창을 닫습니다.</span></div><div class="help-row"><span class="help-number">05</span><span class="help-key">CONTROLS<br>H</span><span>조작 방법을 다시 확인합니다.</span></div><button onclick="closePanels()">CLOSE</button></div></div>\n<div id="inventoryOverlay"><div class="utility-panel"><div class="panel-header"><h3>INVENTORY</h3><span class="panel-hint">I / ESC TO CLOSE</span></div><div id="inventoryItems" class="inventory-grid"></div><div id="itemDescription" class="item-description">ITEM DESCRIPTION<br>아이템을 선택하면 설명이 표시됩니다.</div><button onclick="closePanels()">CLOSE</button></div></div>\n</div>\n<script>\n// 요소 선택용 축약 함수와 현재 누른 키 목록
const $=id=>document.getElementById(id),keys=new Set();\nlet paused=false,remaining=600,last=performance.now(),x=50,y=56;
// 조사 완료 여부와 NOTE·출구의 상태를 보관한다.
const records={A:false,B:false,C:false};let noteRead=false,doorOpen=false,dialogOpen=false,enteredCode='';
// 매번 새롭게 생성하는 네 자리 비밀번호. 기록지의 단서도 이에 연동된다.
const digits=Array.from({length:4},()=>Math.floor(Math.random()*10)).join('');
// STAGE 01에서는 ECHO가 정확한 정답을 알려준다. 이후 스테이지의 불신 서사와 대비된다.
const echoLines=['여기는 ARCHIVE ACCESS, 첫 번째 보안 구역입니다.','터미널 A·B·C에서 기록지를 수집하세요. 획득한 기록지는 I키로 볼 수 있어요.','세 기록을 확보하면 NOTE를 확인할 수 있습니다.','걱정하지 마세요. 이번에는 제가 정확한 비밀번호를 알려드릴게요.'];let echoIndex=0;
function echoSay(message){$('echoText').textContent=message;}
function nextEcho(){if(echoIndex<echoLines.length)echoSay(echoLines[echoIndex++]);}
const recordImages={A:'__RECORDA__',B:'__RECORDB__',C:'__RECORDC__'};
// 오브제별 위치(백분율)와 상호작용 종류를 정의한다.
const objects=[{id:'terminalA',x:34,y:44,k:'A'},{id:'terminalB',x:66,y:44,k:'B'},{id:'terminalC',x:50,y:71.7,k:'C'},{id:'noteProp',x:41,y:33,k:'NOTE'},{id:'keypadProp',x:59,y:33,k:'KEYPAD'}];
\nlet entering=true;const transition=$('stageTransition');setTimeout(()=>transition.classList.add('hide'),2700);setTimeout(()=>{transition.remove();entering=false;last=performance.now();$('gameRoot').focus()},3150);\nconst player=$(\'player\');\nfunction draw(){player.style.left=x+\'%\';player.style.top=y+\'%\';$(\'room\').classList.toggle(\'show-upper-player\',y<30&&(x<23||x>77))}\n// Coordinates are expressed in the original 843×619 artwork. The red boundary\n// defines the traversable floor; walls are always rendered above the player.\n// 방 내부를 0~100% 좌표로 표현한다. 위쪽 문 및 네 모서리의 사선 벽을 반영한다.
const boundary=[[14,24],[86,24],[94,31],[94,83],[88,92],[12,92],[6,83],[6,31]];
function inPolygon(px,py){let inside=false;for(let i=0,j=boundary.length-1;i<boundary.length;j=i++){const a=boundary[i],b=boundary[j];if((a[1]>py)!=(b[1]>py)&&px<(b[0]-a[0])*(py-a[1])/(b[1]-a[1])+a[0])inside=!inside}return inside}
function canMove(nx,ny){if(![[-1.2,-1.8],[1.2,-1.8],[-1.2,1.8],[1.2,1.8]].every(([dx,dy])=>inPolygon(nx+dx,ny+dy)))return false;
 // 오브제의 중심에 겹쳐 들어가지 않도록 막되, E키 조사 거리는 확보한다.
 return !objects.some(o=>Math.hypot((nx-o.x)*.75,ny-o.y)<4.6)}
function togglePause(value){paused=value;$(\'pauseOverlay\').style.display=paused?\'flex\':\'none\';$(\'pauseToggle\').textContent=paused?\'▶\':\'Ⅱ\';$(\'pauseToggle\').classList.toggle(\'paused\',paused);keys.clear()}\nfunction closePanels(){$(\'helpOverlay\').style.display=\'none\';$(\'inventoryOverlay\').style.display=\'none\';keys.clear()}\n$(\'pauseToggle\').onclick=()=>togglePause(!paused);$(\'resumeButton\').onclick=()=>togglePause(false);\n// 게임 안의 버튼 클릭을 Streamlit의 재시작·타이틀 버튼에 전달한다.
function hostAction(action){window.parent.document.querySelector(action===\'title\'?\'[class*=st-key-stage01_title] button\':\'[class*=st-key-stage01_restart] button\')?.click()}\n$(\'restartButton\').onclick=()=>window.location.reload();$(\'titleButton\').onclick=()=>hostAction(\'title\');\ndocument.addEventListener(\'keydown\',e=>{const k=e.key.toLowerCase();if([\'arrowup\',\'arrowdown\',\'arrowleft\',\'arrowright\',\' \'].includes(k))e.preventDefault();if(e.repeat&&[\'escape\',\'h\',\'i\'].includes(k))return;\nif(k===\'escape\'){if(dialogOpen){closeDialog();return}if($(\'helpOverlay\').style.display===\'flex\'||$(\'inventoryOverlay\').style.display===\'flex\'){closePanels();return}togglePause(!paused);return}\nif(k===\'h\'&&!paused&&!dialogOpen){const el=$(\'helpOverlay\');const opening=el.style.display!==\'flex\';closePanels();if(opening)el.style.display=\'flex\';return}\nif(k===\'i\'&&!paused&&!dialogOpen){const el=$(\'inventoryOverlay\');const opening=el.style.display!==\'flex\';closePanels();if(opening){renderInventory();el.style.display=\'flex\'}return}\nif(k==='e'&&!paused&&!entering&&!dialogOpen&&$('inventoryOverlay').style.display!=='flex'&&$('helpOverlay').style.display!=='flex'){interact();return}
if(k===' '&&dialogOpen){closeDialog();return}if(k===' '&&!dialogOpen&&!paused){nextEcho();return}if(k===' '&&!dialogOpen&&!paused){nextEcho();return}
keys.add(k)});\ndocument.addEventListener(\'keyup\',e=>keys.delete(e.key.toLowerCase()));\nwindow.addEventListener(\'blur\',()=>keys.clear());\n// 프레임 간 시간차로 이동량과 10분 제한시간을 갱신한다.
function tick(now){let dt=Math.min((now-last)/1000,.05);last=now;if(!paused&&!entering&&!dialogOpen&&$('helpOverlay').style.display!=='flex'&&$('inventoryOverlay').style.display!=='flex'){let dx=0,dy=0;if(keys.has(\'a\')||keys.has(\'arrowleft\'))dx--;if(keys.has(\'d\')||keys.has(\'arrowright\'))dx++;if(keys.has(\'w\')||keys.has(\'arrowup\'))dy--;if(keys.has(\'s\')||keys.has(\'arrowdown\'))dy++;if(dx||dy){const l=Math.hypot(dx,dy);dx=dx/l*78*dt;dy=dy/l*78*dt;if(canMove(x+dx,y))x+=dx;if(canMove(x,y+dy))y+=dy;draw()}\nremaining=Math.max(0,remaining-dt);const sec=Math.ceil(remaining);$(\'timer\').textContent=String(Math.floor(sec/60)).padStart(2,\'0\')+\':\'+String(sec%60).padStart(2,\'0\');if(remaining===0){togglePause(true);$(\'echoText\').textContent=\'제한 시간이 종료되었습니다.\'}}\nupdateHint();requestAnimationFrame(tick)}draw();requestAnimationFrame(tick);
// 캐릭터와 가장 가까운 오브제를 찾아 상호작용 가능 거리를 판정한다.
function nearest(){let best=null,dist=999;for(const o of objects){const d=Math.hypot((x-o.x)*.843,(y-o.y)*.619);if(d<dist){best=o;dist=d}}return dist<17?best:null}
function updateHint(){const o=nearest();$('interactionHint').style.display=o&&!doorOpen?'block':'none';if(o)$('interactionHint').textContent='E : '+(o.k==='NOTE'?'NOTE 확인':o.k==='KEYPAD'?'보안 키패드':`터미널 ${o.k} 조사`)}
// 조사 결과나 퍼즐 안내를 공통 팝업에 표시한다.
function openDialog(content){dialogOpen=true;$('gameRoot').classList.add('dialog-active');keys.clear();$('dialogContent').innerHTML=content+`<div style="text-align:right"><button onclick="closeDialog()">CLOSE [SPACE]</button></div>`;$('dialogOverlay').style.display='flex'}
function closeDialog(){dialogOpen=false;$('gameRoot').classList.remove('dialog-active');$('dialogOverlay').style.display='none';keys.clear()}
$('dialogOverlay').addEventListener('click',e=>{if(e.target===$('dialogOverlay'))closeDialog()});
// Generated locally: short feather/quill-on-paper scratch, without an external audio file.
// 기록지 획득 시 종이에 글씨를 쓰는 듯한 짧은 합성 효과음을 재생한다.
let audioCtx;function scribble(){try{audioCtx=audioCtx||new(window.AudioContext||window.webkitAudioContext)();const ctx=audioCtx;ctx.resume();for(let j=0;j<5;j++){const buffer=ctx.createBuffer(1,Math.round(ctx.sampleRate*.12),ctx.sampleRate);const v=buffer.getChannelData(0);for(let i=0;i<v.length;i++)v[i]=(Math.random()*2-1)*(.15+.85*Math.abs(Math.sin(i*.012)))*(1-i/v.length);const src=ctx.createBufferSource();src.buffer=buffer;const filter=ctx.createBiquadFilter();filter.type='bandpass';filter.frequency.value=1150+j*240;filter.Q.value=.8;const gain=ctx.createGain();gain.gain.value=.14;src.connect(filter).connect(gain).connect(ctx.destination);src.start(ctx.currentTime+j*.105)}}catch(e){}}
// 조사 완료한 기록지들을 인벤토리에 이미지로 표시한다.
function renderInventory(){const keys=Object.keys(records).filter(k=>records[k]);$('itemDescription').textContent='ITEM DESCRIPTION / 기록지를 선택하면 내용을 다시 확인할 수 있습니다.';$('inventoryItems').innerHTML=Array.from({length:12},(_,i)=>keys[i]?`<button class="inventory-slot" onclick="showRecord('${keys[i]}')" title="기록지 ${keys[i]}"><img src="${recordImages[keys[i]]}" alt="기록지 ${keys[i]}"></button>`:`<div class="inventory-slot"></div>`).join('')}
// 인벤토리에서 선택한 기록지를 다시 펼쳐 볼 수 있게 한다.
function showRecord(k){closePanels();openDialog(`<h3>조사 기록지 ${k}</h3><img src="${recordImages[k]}"><p>${recordText(k)}</p>`)}
// 기록지 A/B/C에 대응하는 인증번호 단서를 구성한다.
function recordText(k){return k==='A'?`기록 A / 접근 인증값: ${digits[1]} — 순서 단서는 NOTE에 보관되어 있다.`:k==='B'?`기록 B / 접근 인증값: ${digits[2]} — 모든 기록을 대조해야 한다.`:`기록 C / 접근 인증값: ${digits[0]}${digits[3]} — 첫 번째와 마지막 자릿수이다.`}
// 세 기록 수집 후 NOTE 점멸, NOTE 확인 후 키패드 점멸을 제어한다.
function checkGlow(){if(Object.values(records).every(Boolean)&&!noteRead)$('noteProp').classList.add('glow');else $('noteProp').classList.remove('glow');$('keypadProp').classList.toggle('glow',noteRead&&!doorOpen)}
// E키 상호작용: 터미널 조사, NOTE 확인, 키패드 사용을 분기한다.
function interact(){const o=nearest();if(!o)return;if('ABC'.includes(o.k)&&o.k.length===1){const first=!records[o.k];records[o.k]=true;if(first){scribble();}checkGlow();echoSay(`터미널 ${o.k}의 기록을 확보했어요. 인벤토리(I)에 기록지가 저장됐습니다.`);openDialog(`<h3>TERMINAL ${o.k} // 조사 완료</h3><img src="${recordImages[o.k]}"><p>${recordText(o.k)}</p><p>${first?'기록지가 인벤토리에 추가되었습니다.':'이미 확보한 기록입니다.'}</p>`);return}
if(o.k==='NOTE'){if(!Object.values(records).every(Boolean)){openDialog('<h3>NOTE // 잠금</h3>세 터미널의 기록을 모두 수집한 뒤 확인할 수 있습니다.');return}noteRead=true;checkGlow();openDialog(`<h3>NOTE // 인증 절차</h3><img src="__NOTE__"><p>이 보관실은 세 단말기에 분산된 인증 기록을 복원해야 출구가 개방된다.</p><p>기록을 읽는 순서는 <strong>C → A → B</strong>이다. C에는 첫째·넷째 자리, A에는 둘째 자리, B에는 셋째 자리가 기록되어 있다.</p><p>수집한 네 자릿수를 순서대로 입력하면 출구 잠금이 해제된다.</p>`);echoSay(`기록 복원 완료! 키패드의 정답은 ${digits}입니다. 제가 알려드린 숫자를 그대로 입력하세요.`);return}
if(o.k==='KEYPAD'){if(!noteRead){openDialog('<h3>SECURITY // LOCKED</h3>NOTE를 확인하고 인증 절차를 복원해야 합니다.');return}if(doorOpen){openDialog('<h3>EXIT OPEN</h3>출구가 열렸습니다.');return}enteredCode='';showKeypad()}}
// 숫자 버튼이 포함된 비밀번호 입력 팝업을 표시한다.
function showKeypad(){openDialog(`<h3>SECURITY // ACCESS CODE</h3><p>에코가 안내한 네 자리 인증번호: <strong>${digits}</strong></p><div id="keypadDigits">${enteredCode.padEnd(4,'_')}</div><div class="keygrid">${['1','2','3','4','5','6','7','8','9','←','0','OK'].map(v=>`<button onclick="keyInput('${v}')">${v}</button>`).join('')}</div>`)}
// 버튼을 누를 때마다 Web Audio API로 짧은 삑 소리를 낸다.
function beep(){try{audioCtx=audioCtx||new(window.AudioContext||window.webkitAudioContext)();audioCtx.resume();const o=audioCtx.createOscillator(),g=audioCtx.createGain();o.type='square';o.frequency.value=820;g.gain.setValueAtTime(.035,audioCtx.currentTime);g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+.085);o.connect(g).connect(audioCtx.destination);o.start();o.stop(audioCtx.currentTime+.09)}catch(e){}}
// 숫자 입력과 삭제, 정답 검사, 열린 벽 이미지 교체를 처리한다.
function keyInput(v){beep();if(v==='←')enteredCode=enteredCode.slice(0,-1);else if(v==='OK'){if(enteredCode===digits){doorOpen=true;$('wallLayer').src='__WALLSOPEN__';checkGlow();closeDialog();$('echoText').textContent='인증 성공. 출구가 개방되었습니다. 다음 구역으로 이동할 수 있습니다.';openDialog('<h3>ACCESS GRANTED</h3><p>보관실 출구의 잠금이 해제되었습니다. 문이 열렸습니다.</p>');return}else{enteredCode='';$('echoText').textContent='인증 실패. 기록지를 다시 확인하십시오.'}}else if(enteredCode.length<4)enteredCode+=v;showKeypad()}
objects.forEach(o=>$(o.id).addEventListener('click',()=>{if(!paused&&!entering){const d=Math.hypot((x-o.x)*.843,(y-o.y)*.619);if(d<17){interact();}else $('echoText').textContent='오브제 가까이 이동한 후 E키로 조사하십시오.'}}));
\n</script></body></html>'''
# HTML의 이미지 자리표시자를 실제 PNG 데이터로 치환한다.
for token,name in {"__FLOOR__":"floor.png","__WALLS__":"walls.png","__WALLSOPEN__":"walls_open.png","__TERMINALA__":"terminal_A.png","__TERMINALB__":"terminal_B.png","__TERMINALC__":"terminal_C.png","__NOTE__":"note.png","__KEYPAD__":"keypad.png","__RECORDA__":"record_A.png","__RECORDB__":"record_B.png","__RECORDC__":"record_C.png"}.items():
    html=html.replace(token,data(root/"assets/stage01"/name))
html=html.replace("__FONT__",font)
components.html(html,height=1000,scrolling=False)
