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

st.markdown(
    """
    <style>
    #MainMenu,header,footer,[data-testid="stSidebar"]{visibility:hidden;display:none}
    .stApp{background:#000!important;color:#fff!important}
    .block-container{padding:0!important;max-width:100%!important}
    iframe{border:0!important}
    </style>
    """,
    unsafe_allow_html=True,
)

html = r"""
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<style>
__TUTORIAL_CSS__
/* Stage-specific additions. Page 2's base scene styles are used above. */
.stage01-timer{position:absolute;top:28px;right:72px;z-index:22;color:#777;font-size:11px;letter-spacing:1px}
.stage01-pause{position:absolute;top:18px;right:18px;z-index:160;width:34px;height:34px;padding:0;border:0;background:#000;color:#fff;font-size:20px;line-height:1}
.stage01-pause:hover{background:#fff;color:#000}
.stage01-object{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;width:15%;height:10%;min-width:90px;padding:8px!important;background:#090909}
.stage01-object .main-label{font-size:12px;color:#ddd;line-height:1.4}
.stage01-object .sub-label{font-size:9px;color:#666;line-height:1.4}
.stage01-object.near{border-color:#eee;color:#fff;box-shadow:0 0 0 1px #ffffff22}
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
.save-gear{position:fixed;right:18px;bottom:18px;z-index:99999;display:none;align-items:center;gap:8px;padding:8px 11px;background:#050505;border:1px solid #666;color:#ddd;font-size:11px;letter-spacing:1px}
.save-gear.show{display:flex}
.save-gear .gear{display:inline-block;font-size:20px;animation:gearSpin .8s linear infinite}
@keyframes gearSpin{to{transform:rotate(360deg)}}
.computer-overlay.show{display:flex}
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
</style></head><body>
<div class="game" id="gameRoot" tabindex="0">
  <div class="project-title">PROJECT : LOGIC</div>
  <div class="stage-title">STAGE 01 // ARCHIVE ACCESS</div>
  <div class="stage01-timer" id="timer">12:00</div>
  <button class="stage01-pause" id="pauseBtn" type="button" aria-label="Pause">Ⅱ</button>

  <div class="game-area" id="gameArea">
    <div class="mobile-controls" id="mobileControls">
      <button class="control-button control-up" data-direction="w" type="button">▲</button>
      <button class="control-button control-left" data-direction="a" type="button">◀</button>
      <button class="control-button control-right" data-direction="d" type="button">▶</button>
      <button class="control-button control-down" data-direction="s" type="button">▼</button>
    </div>

    <div class="room" id="room">
      <div class="room-line-horizontal"></div>
      <div class="room-line-vertical"></div>

      <div class="object stage01-object stage01-a" id="objectA" data-id="A"><span class="main-label">SECTOR A</span><span class="sub-label" id="stateA">DATA SEALED</span></div>
      <div class="object stage01-object stage01-b" id="objectB" data-id="B"><span class="main-label">COMPUTER / B</span><span class="sub-label" id="stateB">DATA SEALED</span></div>
      <div class="object stage01-object stage01-c" id="objectC" data-id="C"><span class="main-label">SECTOR C</span><span class="sub-label" id="stateC">DATA SEALED</span></div>
      <div class="object stage01-object stage01-archive" id="objectArchive" data-id="ARCHIVE"><span class="main-label">ARCHIVE NOTE</span><span class="sub-label" id="stateArchive">UNREAD</span></div>
      <div class="object stage01-object stage01-panel" id="objectPanel" aria-hidden="true"><span class="reader-light" id="panelLight"></span><span class="main-label">EXIT ACCESS</span><span class="sub-label" id="statePanel">LOCKED</span></div>

      <div class="exit-wall" id="exitDoor" data-id="EXIT"><span class="reader-light" id="exitLight" aria-label="Exit access indicator"></span><span class="exit-reader-label">E<br>ACCESS</span></div>
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

  <div class="pause-overlay" id="pauseOverlay">
    <div><div class="pause-title">GAME PAUSED</div><div class="pause-sub">PRESS Ⅱ TO CONTINUE</div><div class="pause-actions"><button class="code-button" id="resumeBtn" type="button">RESUME</button><button class="code-button" id="restartBtn" type="button">RESTART</button><button class="code-button" id="saveTitleBtn" type="button">SAVE &amp; TITLE</button><a class="code-button" id="titleBtn" href="?action=title" target="_top" rel="noopener" style="display:flex;align-items:center;justify-content:center;box-sizing:border-box;text-decoration:none">TITLE</a></div></div>
  </div>
<div class="save-gear" id="saveGear" aria-live="polite"><span class="gear">⚙</span><span id="saveGearText">SAVING...</span></div>
</div>

<script>
(function(){
'use strict';
const $=id=>document.getElementById(id);
const root=$('gameRoot'), room=$('room'), player=$('player'), interactionMessage=$('interactionMessage');
const inventoryOverlay=$('inventoryOverlay'), helpOverlay=$('helpOverlay'), dataOverlay=$('dataOverlay'), codeOverlay=$('codeOverlay'), pauseOverlay=$('pauseOverlay');
const echoMessage=$('echoMessage'), echoNext=$('echoNext'), status=$('status'), timerNode=$('timer');
let playerX=50, playerY=43, seconds=720, paused=false, finished=false, codeSolved=false, nearby=null;
let helpOpen=false, inventoryOpen=false, dataOpen=false, codeOpen=false, typingDone=false, typingTimer=null, echoIndex=0, pinBuffer='';
let timerLast=Date.now();
const STAGE_SAVE_KEY='project_logic_stage01_save_v1';
if(__RESET_STAGE_SAVE__){try{localStorage.removeItem(STAGE_SAVE_KEY)}catch(e){}}
let audioContext=null;
function playTone(freq=880,duration=0.07,volume=0.045){try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!audioContext)audioContext=new AC();if(audioContext.state==='suspended')audioContext.resume();const osc=audioContext.createOscillator(),gain=audioContext.createGain();osc.type='square';osc.frequency.value=freq;gain.gain.setValueAtTime(0.0001,audioContext.currentTime);gain.gain.exponentialRampToValueAtTime(volume,audioContext.currentTime+0.008);gain.gain.exponentialRampToValueAtTime(0.0001,audioContext.currentTime+duration);osc.connect(gain);gain.connect(audioContext.destination);osc.start();osc.stop(audioContext.currentTime+duration+0.01)}catch(e){}}
function playDoorOpen(){try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!audioContext)audioContext=new AC();if(audioContext.state==='suspended')audioContext.resume();const now=audioContext.currentTime;[440,660,880].forEach((frequency,index)=>{const osc=audioContext.createOscillator(),gain=audioContext.createGain();osc.type='square';osc.frequency.value=frequency;gain.gain.setValueAtTime(0.0001,now+index*.12);gain.gain.exponentialRampToValueAtTime(.08,now+index*.12+.02);gain.gain.exponentialRampToValueAtTime(.0001,now+index*.12+.18);osc.connect(gain);gain.connect(audioContext.destination);osc.start(now+index*.12);osc.stop(now+index*.12+.2)});}catch(e){}}
const keys={w:false,a:false,s:false,d:false};
const inventory=Array(8).fill(null);
const items=[];
const messages=[
 '연결이 확인되었습니다. 저는 ECHO입니다. 7년 전 이 시설에서 발생한 사고 기록은 아직 완전히 복구되지 않았습니다.',
 '사고 직전, 관리자는 세 구역의 로그를 따로 저장했습니다. 누군가 기록을 지우려 했기 때문에 하나의 파일로 보관하지 않았습니다.',
 '복구된 숫자는 접근 코드 자체가 아닙니다. ARCHIVE NOTE의 규칙으로 숫자를 변환해야 보안 시스템이 이를 받아들입니다.',
 '마지막 로그에는 이상한 명령이 남아 있습니다. “기록을 복구하지 말 것.” 발신자 식별란은 ECHO의 내부 인증값으로 덮여 있습니다.',
 '출구의 인증 장치에 네 자리 코드를 입력하면 잠금이 해제됩니다. 제한 시간은 12분입니다. 남은 기록을 대조하고 사고 당시의 명령을 확인하십시오.'
];
const puzzleCandidates=[];
for(let a=2;a<=9;a++)for(let b=1;b<a;b++)for(let c=a+1;c<=Math.min(9,a+b-1);c++)puzzleCandidates.push({A:a,B:b,C:c});
let puzzle=puzzleCandidates[Math.floor(Math.random()*puzzleCandidates.length)];
let expectedCode=makeExpectedCode();
function makeExpectedCode(){const checksum=(puzzle.A+puzzle.B+puzzle.C)%9||9;return String(puzzle.A-puzzle.B)+String(puzzle.C-puzzle.A)+String(puzzle.A+puzzle.B-puzzle.C)+String(checksum)}
const found={A:false,B:false,C:false,ARCHIVE:false};
const clues={};
function rebuildClues(){
 clues.A={title:'SECTOR A // ACCESS LOG',body:`출입 기록 04-A\n\n보안 담당자는 02:13에 서버실을 나갔다. 2분 뒤 중앙 로그에 삭제 명령이 기록되었다.\n\nA 기록값: ${puzzle.A}\nRECOVERED VALUE: ${puzzle.A}`};
 clues.B={title:'COMPUTER / SECTOR B',body:`시스템 진단 로그\n\n02:15:08 — ARCHIVE INDEX ACCESS\n02:15:11 — DELETE REQUEST REJECTED\n02:15:12 — REQUEST SOURCE: ECHO\n\nB 기록값: ${puzzle.B}\nRECOVERED VALUE: ${puzzle.B}`};
 clues.C={title:'SECTOR C // MAINTENANCE',body:`정비 기록 17-C\n\n출구 잠금은 원격 조작으로 전환되었다. 수동 해제는 인증 코드 복구 후에만 허용된다.\n\nC 기록값: ${puzzle.C}\nRECOVERED VALUE: ${puzzle.C}`};
}
rebuildClues();
const objects=[
 {id:'A',name:'SECTOR A',x:11,y:17,w:15,h:10,el:$('objectA')},
 {id:'B',name:'COMPUTER / SECTOR B',x:42,y:13,w:16,h:13,el:$('objectB')},
 {id:'C',name:'SECTOR C',x:77,y:18,w:15,h:10,el:$('objectC')},
 {id:'ARCHIVE',name:'ARCHIVE NOTE',x:15,y:73,w:18,h:10,el:$('objectArchive')},
 {id:'EXIT',name:'EXIT',x:92,y:35,w:8,h:30,el:$('exitDoor')}
];
const obstacles=objects.map(o=>({x:o.x,y:o.y,w:o.w,h:o.h}));
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
function renderInventory(){document.querySelectorAll('.inventory-slot').forEach((slot,i)=>{const item=inventory[i];slot.innerHTML=item?`<div class="slot-number">${String(i+1).padStart(2,'0')}</div><div class="item-name">${item.name}</div>`:`<div class="slot-number">${String(i+1).padStart(2,'0')}</div><div class="empty-text">EMPTY</div>`;slot.classList.remove('selected')})}
function openInventory(){if(dataOpen||codeOpen||paused||finished)return;if(inventoryOpen){inventoryOpen=false;inventoryOverlay.style.display='none';root.focus();return}helpOpen=false;helpOverlay.style.display='none';inventoryOpen=true;inventoryOverlay.style.display='flex';$('itemDescription').innerHTML='ITEM DESCRIPTION<br><br>기록을 선택하면 설명이 표시됩니다.';renderInventory();clearKeys()}
function openHelp(){if(dataOpen||codeOpen||paused||finished)return;if(helpOpen){helpOpen=false;helpOverlay.style.display='none';root.focus();return}inventoryOpen=false;inventoryOverlay.style.display='none';helpOpen=true;helpOverlay.style.display='flex';clearKeys()}
function addItem(id){if(items.some(item=>item.id===id))return;let item;if(id==='ARCHIVE'){item={id,name:'ARCHIVE NOTE',body:'ARCHIVE INCIDENT // FRAGMENT 04\n\n첫째 자리 = A − B.\n둘째 자리 = C − A.\n셋째 자리 = A + B − C.\n넷째 자리 = A + B + C를 9로 나눈 나머지. 나머지가 0이면 9로 기록한다.\n\n“ECHO에게 묻지 말 것. 이 명령은 기록을 삭제하라는 지시와 함께 저장되었다.”'}}else item={id,name:clues[id].title,body:clues[id].body};items.push(item);const slot=items.length-1;if(slot<inventory.length)inventory[slot]=item;renderInventory()}
function interact(){if(paused||finished||isOverlayOpen())return;if(!nearby){say('NO TARGET // 가까운 장치로 이동하십시오.');return}const id=nearby.id;if(clues[id]){if(!found[id]){found[id]=true;addItem(id);$('state'+id).textContent='DATA FOUND';say(id+' 기록을 확보했습니다. INVENTORY에서 다시 확인할 수 있습니다.')}showRecord(clues[id].title,clues[id].body);return}if(id==='ARCHIVE'){found.ARCHIVE=true;$('stateArchive').textContent='READ';addItem('ARCHIVE');say('ARCHIVE NOTE 확보 // 네 자리 인증식을 확인하십시오.');showRecord('ARCHIVE NOTE // FRAGMENT 04','ARCHIVE INCIDENT // PERSONAL NOTE\n\n첫째 자리 = A − B.\n둘째 자리 = C − A.\n셋째 자리 = A + B − C.\n넷째 자리 = A + B + C를 9로 나눈 나머지. 나머지가 0이면 9로 기록한다.\n\n“ECHO에게 묻지 말 것. 기록 삭제 명령은 사고 직전 ECHO의 내부 인증값으로 전송되었다.”');return}if(id==='EXIT'){if(!codeSolved){showCode();return}finishStage();return}}
function verify(){if(pinBuffer.length!==4){$('codeError').textContent='FOUR DIGITS REQUIRED // 네 자리 모두 입력하십시오.';return}if(pinBuffer===expectedCode){codeSolved=true;$('statePanel').textContent='UNLOCKED';$('panelLight').classList.add('green');$('exitLight').classList.add('green');$('pinLight').classList.add('green');$('pinStatus').textContent='ACCESS GRANTED // GREEN';$('codeError').textContent='ACCESS GRANTED // 출구 잠금 해제';playDoorOpen();saveStageState();say('인증 완료. 출구 표시등이 초록색으로 바뀌었습니다. 출구에서 E를 눌러 진입하십시오.');setTimeout(()=>{if(codeOpen)closeCode()},900)}else{$('pinLight').classList.remove('green');$('codeError').textContent='INVALID CODE // 기록의 규칙을 다시 확인하십시오.';$('pinStatus').textContent='ACCESS DENIED // RED';say('인증 실패 // 보안 표시등이 빨간색입니다. 기록과 계산 순서를 다시 대조하십시오.')}}
function addRestartAndTitleButtons(title,sub,copy){helpOpen=false;inventoryOpen=false;dataOpen=true;codeOpen=false;helpOverlay.style.display='none';inventoryOverlay.style.display='none';codeOverlay.style.display='none';pauseOverlay.style.display='none';$('closeRecord').style.display='none';$('windowTitle').textContent=title;$('windowSub').textContent=sub;$('windowBody').innerHTML=copy+'<div class="stage01-window-actions"><button class="code-button" id="clearRestart" type="button">RESTART</button><a class="code-button" href="?action=title" target="_top" rel="noopener" style="display:inline-flex;align-items:center;text-decoration:none">TITLE</a></div>';const b=$('clearRestart');if(b)b.onclick=restartStage;dataOpen=true;dataOverlay.style.display='flex'}
function finishStage(){finished=true;clearKeys();pauseOverlay.style.display='none';addRestartAndTitleButtons('STAGE 01 CLEAR','ARCHIVE ACCESS // COMPLETE','<p>ACCESS GRANTED</p><p>ARCHIVE ACCESS가 완료되었습니다.</p>');say('STAGE 01 CLEAR // 다음 구역의 신호가 감지되었습니다.')}
function expireGame(){if(finished)return;finished=true;clearKeys();addRestartAndTitleButtons('TIME EXPIRED','SYSTEM LOCKDOWN','<p>제한 시간이 종료되었습니다.</p>');say('TIME EXPIRED // RESTART를 선택하십시오.')}
function syncTimer(){const now=Date.now();if(!paused&&!finished){const elapsed=(now-timerLast)/1000;if(elapsed>=1){const spent=Math.floor(elapsed);seconds=Math.max(0,seconds-spent);timerLast+=spent*1000;updateTimer();if(seconds===0)expireGame()}}else timerLast=now}
function getDistance(obj){return Math.hypot(playerX-(obj.x+obj.w/2),playerY-(obj.y+obj.h/2))}
function checkInteraction(){nearby=null;let best=Infinity;objects.forEach(obj=>{const d=getDistance(obj);obj.el.classList.remove('near');if(d<12&&d<best){best=d;nearby=obj}});if(nearby&&!paused&&!isOverlayOpen()){nearby.el.classList.add('near');interactionMessage.textContent='E  //  '+nearby.name;interactionMessage.classList.add('visible')}else interactionMessage.classList.remove('visible')}
function circleHitsRect(cx,cy,r,o){const dx=Math.max(o.x,Math.min(cx,o.x+o.w));const dy=Math.max(o.y,Math.min(cy,o.y+o.h));return Math.hypot(cx-dx,cy-dy)<r}
function blocked(x,y){if(x<3||x>97||y<3||y>96)return true;return obstacles.some(o=>circleHitsRect(x,y,1.3,o))}
function updateMovement(){if(paused||isOverlayOpen())return;let dx=(keys.d?1:0)-(keys.a?1:0),dy=(keys.s?1:0)-(keys.w?1:0);if(!dx&&!dy)return;const len=Math.hypot(dx,dy);dx=dx/len*.48;dy=dy/len*.48;if(!blocked(playerX+dx,playerY))playerX+=dx;if(!blocked(playerX,playerY+dy))playerY+=dy;player.style.left=playerX+'%';player.style.top=playerY+'%';checkInteraction()}
function typeEcho(index){echoIndex=index;clearTimeout(typingTimer);const text=messages[index]||'';echoMessage.textContent='';typingDone=false;echoNext.classList.remove('ready');let i=0;function tick(){if(i<text.length){echoMessage.textContent+=text[i++];typingTimer=setTimeout(tick,24)}else{typingDone=true;echoNext.classList.add('ready')}}tick()}
function nextEcho(){if(!typingDone){clearTimeout(typingTimer);echoMessage.textContent=messages[echoIndex]||'';typingDone=true;echoNext.classList.add('ready');return}if(echoIndex<messages.length-1)typeEcho(echoIndex+1)}
function saveStageState(){
  try{
    localStorage.setItem(STAGE_SAVE_KEY,JSON.stringify({version:1,playerX,playerY,seconds,codeSolved,puzzle,found,items,inventory,echoIndex,echoText:echoMessage.textContent,typingDone,updatedAt:Date.now()}));
    return true;
  }catch(e){return false}
}
function restoreStageState(){
  try{
    const saved=JSON.parse(localStorage.getItem(STAGE_SAVE_KEY)||'null');
    if(!saved||saved.version!==1||!saved.puzzle||!Number.isFinite(saved.seconds))return false;
    playerX=Number.isFinite(saved.playerX)?saved.playerX:50;playerY=Number.isFinite(saved.playerY)?saved.playerY:43;
    seconds=Math.max(0,Math.min(720,Math.floor(saved.seconds)));codeSolved=!!saved.codeSolved;
    if(Number.isFinite(saved.puzzle.A)&&Number.isFinite(saved.puzzle.B)&&Number.isFinite(saved.puzzle.C)){puzzle=saved.puzzle;expectedCode=makeExpectedCode();rebuildClues()}
    Object.keys(found).forEach(k=>found[k]=!!(saved.found&&saved.found[k]));
    items.length=0;(Array.isArray(saved.items)?saved.items:[]).forEach(item=>{if(item&&item.id&&item.name)items.push(item)});
    inventory.fill(null);(Array.isArray(saved.inventory)?saved.inventory:[]).slice(0,inventory.length).forEach((item,i)=>inventory[i]=item);
    ['A','B','C'].forEach(k=>{const el=$('state'+k);if(el)el.textContent=found[k]?'DATA FOUND':'DATA SEALED'});
    $('stateArchive').textContent=found.ARCHIVE?'READ':'UNREAD';
    if(codeSolved){$('statePanel').textContent='UNLOCKED';$('panelLight').classList.add('green');$('exitLight').classList.add('green');$('pinLight').classList.add('green')}
    echoIndex=Number.isFinite(saved.echoIndex)?Math.max(0,Math.min(messages.length-1,saved.echoIndex)):0;
    player.style.left=playerX+'%';player.style.top=playerY+'%';renderInventory();updateTimer();
    if(typeof saved.echoText==='string'){echoMessage.textContent=saved.echoText;typingDone=true;echoNext.classList.add('ready')}else typeEcho(echoIndex);
    return true;
  }catch(e){return false}
}
function navigateToTitle(){try{const parentWindow=window.parent;const targetUrl=new URL(parentWindow.location.href);targetUrl.search='';targetUrl.hash='';targetUrl.searchParams.set('action','title');parentWindow.history.replaceState({},'',targetUrl.toString());parentWindow.location.reload();return}catch(e){}try{window.top.location.href='?action=title'}catch(e){say('TITLE NAVIGATION BLOCKED // 새로고침 후 CONTINUE를 선택하십시오.')}}
function saveAndReturnToTitle(){
  paused=true;clearKeys();const gear=$('saveGear'),label=$('saveGearText');gear.classList.add('show');label.textContent='SAVING...';
  const ok=saveStageState();
  setTimeout(()=>{label.textContent=ok?'SAVED // RETURNING':'SAVE FAILED';setTimeout(navigateToTitle,350)},650);
}
function restartStage(){try{localStorage.removeItem(STAGE_SAVE_KEY)}catch(e){}paused=false;finished=false;codeSolved=false;seconds=720;timerLast=Date.now();playerX=50;playerY=43;nearby=null;helpOpen=inventoryOpen=dataOpen=codeOpen=false;[inventoryOverlay,helpOverlay,dataOverlay,codeOverlay,pauseOverlay].forEach(el=>el.style.display='none');Object.keys(found).forEach(k=>found[k]=false);items.length=0;inventory.fill(null);$('stateA').textContent=$('stateB').textContent=$('stateC').textContent='DATA SEALED';$('stateArchive').textContent='UNREAD';$('statePanel').textContent='LOCKED';$('panelLight').classList.remove('green');$('exitLight').classList.remove('green');$('pinLight').classList.remove('green');pinBuffer='';renderPin();puzzle=puzzleCandidates[Math.floor(Math.random()*puzzleCandidates.length)];expectedCode=makeExpectedCode();rebuildClues();$('panelLight').classList.remove('green');$('exitLight').classList.remove('green');$('pinLight').classList.remove('green');clearPin();renderInventory();updateTimer();player.style.left=playerX+'%';player.style.top=playerY+'%';echoIndex=0;typeEcho(0);say('SYSTEM READY // 접근 가능한 장치 가까이 이동하십시오.');clearKeys();checkInteraction();root.focus()}
function resume(){paused=false;pauseOverlay.style.display='none';timerLast=Date.now();root.focus();clearKeys()}
function focusGame(){try{root.focus({preventScroll:true})}catch(e){root.focus()}}

$('pauseBtn').addEventListener('click',()=>{if(finished)return;if(!paused&&(helpOpen||inventoryOpen||dataOpen||codeOpen))return;paused=!paused;timerLast=Date.now();pauseOverlay.style.display=paused?'flex':'none';clearKeys();if(!paused)focusGame()});
$('resumeBtn').addEventListener('click',resume);$('restartBtn').addEventListener('click',restartStage);$('saveTitleBtn').addEventListener('click',saveAndReturnToTitle);$('titleBtn').addEventListener('click',e=>{e.preventDefault();saveAndReturnToTitle()});
$('closeRecord').addEventListener('click',closeRecord);$('closeCode').addEventListener('click',closeCode);$('verifyBtn').addEventListener('click',verify);
document.querySelectorAll('[data-pin]').forEach(btn=>btn.addEventListener('click',()=>{const action=btn.dataset.pin;if(action==='clear')clearPin();else if(action==='back')backspacePin();else appendPinDigit(action)}));
document.querySelectorAll('[data-direction]').forEach(btn=>{const k=btn.dataset.direction;const down=e=>{e.preventDefault();keys[k]=true;focusGame()};const up=e=>{e.preventDefault();keys[k]=false};btn.addEventListener('pointerdown',down);['pointerup','pointercancel','lostpointercapture'].forEach(ev=>btn.addEventListener(ev,up))});
document.querySelectorAll('.inventory-slot').forEach((slot,i)=>slot.addEventListener('click',()=>{document.querySelectorAll('.inventory-slot').forEach(s=>s.classList.remove('selected'));slot.classList.add('selected');const item=inventory[i];$('itemDescription').innerHTML=item?`<strong>${item.name}</strong><br><br>${item.body.replace(/\n/g,'<br>')}`:'ITEM DESCRIPTION<br><br>비어 있는 슬롯입니다.'}));
document.addEventListener('keydown',e=>{const key=e.key.toLowerCase();if(codeOpen){if(/^[0-9]$/.test(e.key)){e.preventDefault();appendPinDigit(e.key);return}if(key==='backspace'){e.preventDefault();backspacePin();return}if(key==='enter'){e.preventDefault();verify();return}if(key==='escape'){e.preventDefault();closeCode();return}return}if(e.repeat&&['e','h','i','escape'].includes(key))return;if(e.code==='Space'){e.preventDefault();if(!paused&&!isOverlayOpen())nextEcho();return}if(key==='escape'){if(codeOpen){closeCode();return}if(dataOpen){closeRecord();return}if(helpOpen){openHelp();return}if(inventoryOpen){openInventory();return}if(paused){resume();return}return}if(key==='h'){e.preventDefault();openHelp();return}if(key==='i'){e.preventDefault();openInventory();return}if(key==='e'){e.preventDefault();interact();return}if(['w','a','s','d'].includes(key)&&!paused&&!isOverlayOpen()){keys[key]=true;e.preventDefault()}});
document.addEventListener('keyup',e=>{const key=e.key.toLowerCase();if(key in keys){keys[key]=false;e.preventDefault()}});window.addEventListener('blur',clearKeys);root.addEventListener('pointerdown',focusGame);
function loop(){updateMovement();checkInteraction();requestAnimationFrame(loop)}
const restored=restoreStageState();if(!restored){player.style.left=playerX+'%';player.style.top=playerY+'%';renderInventory();updateTimer();typeEcho(0)}checkInteraction();focusGame();setInterval(syncTimer,250);setInterval(saveStageState,1000);requestAnimationFrame(loop);
})();
</script></body></html>
"""

html = html.replace("__TUTORIAL_CSS__", tutorial_css)
html = html.replace("__RESET_STAGE_SAVE__", "true" if st.session_state.pop("stage01_reset_save", False) else "false")
components.html(html, height=1000, scrolling=False)
