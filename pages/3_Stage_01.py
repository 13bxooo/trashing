import streamlit as st
import base64
import json
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(page_title="STAGE 01 | ARCHIVE ACCESS", layout="wide", initial_sidebar_state="collapsed")
ROOT = Path(__file__).resolve().parent.parent
ASSET = ROOT / "assets" / "stage01"

NAMES = ["floor", "wall_locked", "wall_unlocked", "servers", "archive_shelf",
         "console", "containment", "desk", "lockers", "terminal", "crates"]
missing = [name for name in NAMES if not (ASSET / (name + ".png")).exists()]
if missing:
    st.error("Stage 01 이미지 누락: " + ", ".join(missing) + "\nassets/stage01 폴더에 PNG 파일을 넣어주세요.")
    st.stop()
images = {
    name: "data:image/png;base64," + base64.b64encode((ASSET / (name + ".png")).read_bytes()).decode("ascii")
    for name in NAMES
}
positions = {'servers': (162, 171, 330, 345), 'archive_shelf': (165, 361, 403, 568), 'console': (450, 353, 862, 628), 'containment': (158, 627, 335, 867), 'desk': (469, 724, 833, 883), 'lockers': (986, 650, 1180, 839), 'terminal': (896, 867, 1019, 1019), 'crates': (948, 213, 1151, 332)}
html = r"""
<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>
*{box-sizing:border-box}html,body{margin:0;background:#00040b;color:#c5f8ff;font-family:monospace;overflow:hidden}
#wrap{width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}
#game{position:relative;width:min(94vw,calc(85vh * 1317 / 1194));aspect-ratio:1317/1194;background:#01040b;overflow:hidden;outline:0}
.layer,.sprite{position:absolute;pointer-events:none;image-rendering:auto}
.layer{width:100%;height:100%;left:0;top:0}
.sprite{z-index:3}
#player{position:absolute;width:2.1%;height:3.3%;z-index:5;background:linear-gradient(90deg,#293a50 20%,#c2e5e9 25%,#9fc8ce 75%,#293a50 80%);border:2px solid #0c2537;box-shadow:0 3px #122d3c}
#wall{z-index:4}
#hud{position:absolute;z-index:10;bottom:2%;left:5%;width:90%;background:#020c16ee;border:1px solid #14d9f4;padding:10px 15px;min-height:64px;font-size:clamp(10px,1.15vw,15px)}
#prompt{position:absolute;z-index:9;left:30%;top:64%;color:#b4faff;text-shadow:0 0 5px cyan}
#overlay{position:absolute;inset:0;z-index:30;background:#000b;display:none;align-items:center;justify-content:center}
#overlay.show{display:flex}
#panel{background:#020d17;border:2px solid #20d9f6;width:min(560px,85%);padding:24px;box-shadow:0 0 18px #087b89}
button,input{font:inherit;background:#091d2a;color:#d5faff;border:1px solid #19c9e7;padding:10px;margin:5px}
button{cursor:pointer}button:hover{background:#134456}
#intro{position:absolute;inset:0;z-index:50;background:#000;display:flex;align-items:center;justify-content:center;animation:vanish 0.7s 2.7s forwards}
#intro div{border:1px solid #14d9f4;padding:30px 65px;text-align:center;box-shadow:0 0 14px #0088a566}
#intro h1{letter-spacing:4px;margin:0;color:white;text-shadow:0 0 10px #d7fbff}
#intro p{color:#45dff0}
@keyframes vanish{to{opacity:0;visibility:hidden}}
small{color:#83aebd}
</style></head><body><div id="wrap"><div id="game" tabindex="0">
<img class="layer" src="__FLOOR__" style="z-index:1">
<div id="sprites"></div>
<img class="layer" id="wall" src="__WALL_LOCKED__">
<div id="player"></div><div id="prompt"></div>
<div id="hud"><b>ECHO // ARCHIVE ACCESS</b><div id="message" style="padding-top:8px"></div><small>WASD 이동 · E 상호작용 · I 인벤토리 · ESC 닫기</small></div>
<div id="overlay"><div id="panel"><h3 id="panelTitle"></h3><div id="panelBody"></div><div id="panelButtons"></div></div></div>
<div id="intro"><div><h1>STAGE 01</h1><p>:ARCHIVE ACCESS</p></div></div>
</div></div>
<script>
const game=document.getElementById('game'), player=document.getElementById('player');
const msg=document.getElementById('message'), prompt=document.getElementById('prompt');
const overlay=document.getElementById('overlay'), body=document.getElementById('panelBody'), buttons=document.getElementById('panelButtons');
const positions=__POSITIONS__;
const sprites=document.getElementById('sprites');
const rects=[];
for(const [name,r] of Object.entries(positions)){
 const im=document.createElement('img');im.className='sprite';im.src=window.ASSETS[name];
 im.style.left=(r[0]/1317*100)+'%';im.style.top=(r[1]/1194*100)+'%';
 im.style.width=((r[2]-r[0])/1317*100)+'%';im.style.height=((r[3]-r[1])/1194*100)+'%';
 sprites.appendChild(im);
 rects.push({name,x:r[0],y:r[1],w:r[2]-r[0],h:r[3]-r[1]});
}
let x=650,y=985,unlocked=false,modal=false;
let clues={server:false,archive:false,console:false},code='';
const keys={};
const lines=[
"이 구역은 ARCHIVE ACCESS. 시설의 기록은 인공지능이 관리하고 있습니다.",
"주의하십시오. 중앙 시스템의 기록과 물리적 기록이 일치하지 않습니다.",
"세 단서를 대조하여 변조되지 않은 네 자리 출입 코드를 복원하십시오."
];
let line=0;msg.textContent=lines[0];
function say(t){msg.textContent=t}
function show(title,content,actions=[]){
 modal=true;overlay.classList.add('show');document.getElementById('panelTitle').textContent=title;
 body.innerHTML=content;buttons.innerHTML='';
 for(const [label,fn] of actions){let b=document.createElement('button');b.textContent=label;b.onclick=fn;buttons.appendChild(b)}
 let close=document.createElement('button');close.textContent='닫기 [ESC]';close.onclick=hide;buttons.appendChild(close);
}
function hide(){modal=false;overlay.classList.remove('show');game.focus()}
function collide(nx,ny){
 const pad=13;
 if(nx<100||nx>1200||ny<280||ny>1035)return true;
 for(const r of rects){
  if(['terminal','servers','archive_shelf','console','containment','desk','lockers','crates'].includes(r.name)){
   if(nx+pad>r.x+8&&nx-pad<r.x+r.w-8&&ny+pad>r.y+8&&ny-pad<r.y+r.h-8)return true;
  }
 }
 return false;
}
function near(r){let cx=Math.max(r.x,Math.min(x,r.x+r.w)),cy=Math.max(r.y,Math.min(y,r.y+r.h));return Math.hypot(x-cx,y-cy)<95}
function interact(){
 if(modal)return;
 if(y<355&&x>520&&x<800){if(unlocked){show('출입 승인','보안 인증 완료. 다음 구역으로 이동합니다.',[['STAGE 02',()=>{window.parent.postMessage({type:'streamlit:setComponentValue',value:'stage02'},'*');say('STAGE 02 이동 요청이 전송되었습니다.');hide()}]])}else say('출입구 잠김. 우측 보안 단말기에서 코드를 입력하십시오.');return}
 const r=rects.filter(near).sort((a,b)=>Math.hypot(x-(a.x+a.w/2),y-(a.y+a.h/2))-Math.hypot(x-(b.x+b.w/2),y-(b.y+b.h/2)))[0];
 if(!r){say('상호작용 가능한 장비가 가까이 없습니다.');return}
 switch(r.name){
 case 'servers':clues.server=true;show('서버 로그','<p>AI 동기화 로그: 02:40 / 03:10 / 04:20</p><p>주의: 03:10 항목은 원본 서명 불일치.</p>');break;
 case 'archive_shelf':clues.archive=true;show('원본 보관함','<p>서면 기록: 승인된 출입 시각은 02:40.</p><p>원본 문서 번호: 6 — 2</p>');break;
 case 'console':clues.console=true;show('중앙 AI 단말','<p>AI 주장: 마지막 승인 시각은 03:10.</p><p>백업 로그: 02:40에만 정상 서명 존재.</p><p>백업 문서 번호: 8 — 4</p>');break;
 case 'terminal':show('SECURITY // CODE',`<p>서버의 위조 항목을 배제하고 원본 문서 번호를 순서대로 연결하십시오.</p><input id="pin" maxlength="4" inputmode="numeric" placeholder="4자리 코드">`,[['인증',()=>{
 const input=document.getElementById('pin').value.trim();
 if(!Object.values(clues).every(Boolean)){say('먼저 서버, 보관함, 중앙 단말을 모두 조사하십시오.');hide();return}
 if(input==='6284'){unlocked=true;document.getElementById('wall').src=window.ASSETS.wall_unlocked;say('ACCESS GRANTED // 출입구의 표시등이 청록색으로 전환되었습니다. 출입구에서 E키를 누르십시오.')}
 else say('ACCESS DENIED // 원본과 백업 문서 번호를 다시 확인하십시오.');
 hide();
 }]]);break;
 default:show('조사',`<p>${r.name} — 오래된 장비입니다. 현재 퍼즐과 직접 관련된 기록은 없습니다.</p>`);
 }
}
document.addEventListener('keydown',e=>{
 if(['w','a','s','d','e','i','Escape',' '].includes(e.key.toLowerCase()))e.preventDefault();
 const k=e.key.toLowerCase();
 if(k==='escape'){hide();return}
 if(k==='e'&&!e.repeat){interact();return}
 if(k==='i'&&!e.repeat){show('INVENTORY',`<p>서버 로그: ${clues.server?'획득':'미확인'}</p><p>원본 기록: ${clues.archive?'획득':'미확인'}</p><p>백업 로그: ${clues.console?'획득':'미확인'}</p>`);return}
 keys[k]=true;
});
document.addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);
window.addEventListener('blur',()=>{for(const k in keys)keys[k]=false});
let last=performance.now();
function tick(t){
 let dt=Math.min((t-last)/1000,.05);last=t;
 if(!modal&&t>3300){
  let dx=(keys.d?1:0)-(keys.a?1:0),dy=(keys.s?1:0)-(keys.w?1:0);
  let d=Math.hypot(dx,dy)||1,nx=x+dx/d*210*dt,ny=y+dy/d*210*dt;
  if(!collide(nx,y))x=nx;if(!collide(x,ny))y=ny;
 }
 player.style.left=(x/1317*100)+'%';player.style.top=(y/1194*100)+'%';
 prompt.textContent=(y<355&&x>520&&x<800)?'[E] 출입구':(rects.some(near)?'[E] 조사':'');
 requestAnimationFrame(tick)
}
requestAnimationFrame(tick);setTimeout(()=>{say(lines.join('  '));game.focus()},3300);
</script></body></html>
"""
# Inline asset mapping before the gameplay script
asset_script = '<script>window.ASSETS=__ASSET_JSON__;</script>'
html=html.replace('<script>\nconst game=',asset_script+'\n<script>\nconst game=')
for name, data in images.items():
    html=html.replace('__'+name.upper()+'__',data)
html=html.replace('__ASSET_JSON__',json.dumps(images,ensure_ascii=False))
html=html.replace('__POSITIONS__',json.dumps(positions))
components.html(html,height=900,scrolling=False)
