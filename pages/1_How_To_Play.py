import base64
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="PROJECT : LOGIC // HOW TO PLAY", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")
font_data = ""
root = Path(__file__).resolve().parent.parent
for candidate in (root / "neodgm.ttf", root / "neodgm(2).ttf", Path("neodgm.ttf"), Path("neodgm(2).ttf")):
    if candidate.exists():
        font_data = base64.b64encode(candidate.read_bytes()).decode("ascii")
        break

st.markdown(f"""
<style>
@font-face{{font-family:NeoDungGeunMo;src:url(data:font/ttf;base64,{font_data}) format('truetype');font-weight:normal;font-style:normal}}
#MainMenu,header,footer,[data-testid="stSidebar"],[data-testid="stToolbar"],[data-testid="stDecoration"]{{display:none!important}}
html,body,[data-testid="stAppViewContainer"],.stApp{{background:#000!important;color:#fff!important;font-family:NeoDungGeunMo,monospace!important}}
html,body,[data-testid="stAppViewContainer"] *,.stApp *{{font-family:NeoDungGeunMo,monospace!important}}
.block-container{{max-width:1080px!important;padding:clamp(24px,6vh,70px) clamp(18px,4vw,48px) 120px!important}}
.manual-head{{border:3px double #26d9f5;padding:24px clamp(18px,4vw,40px);position:relative;background:#000;box-shadow:0 0 18px #00dfff18;margin-bottom:20px}}
.manual-kicker{{color:#42eaff;letter-spacing:3px;font-size:12px;margin-bottom:14px}}
.manual-title{{font-size:clamp(27px,4vw,44px);letter-spacing:2px;line-height:1.4;margin:0;color:#fff}}
.manual-subtitle{{color:#a8eafa;letter-spacing:1px;margin-top:10px;font-size:clamp(12px,1.8vw,16px)}}
.manual-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:18px 0 22px}}
.manual-card{{border:2px solid #147b94;background:#020609;padding:18px 20px;min-height:105px;box-shadow:inset 0 0 18px #00cfff08}}
.manual-card .num{{color:#38eaff;font-size:12px;letter-spacing:2px;margin-bottom:10px}}
.manual-card .label{{font-size:17px;color:#fff;margin-bottom:8px}}
.manual-card .detail{{font-size:13px;line-height:1.9;color:#c8e7ef}}
.manual-note{{border:2px solid #25bcd7;background:#02090e;padding:16px 20px;color:#d9f7ff;line-height:1.9;font-size:13px;margin:16px 0 22px}}
.st-key-menu_fixed{{position:fixed!important;right:24px!important;bottom:22px!important;z-index:999999!important;background:#000;border:2px solid #28dfff;padding:7px;box-shadow:0 0 18px #00dfff25;width:min(260px,calc(100vw - 32px))}}
.st-key-menu_fixed [data-testid="stButton"]{{margin:0!important}}
.st-key-menu_fixed button{{width:100%!important;min-height:48px!important;border:1px solid #fff!important;border-radius:0!important;background:#fff!important;color:#000!important;font-size:14px!important}}
.st-key-menu_fixed button:hover{{background:#28dfff!important;border-color:#28dfff!important;color:#000!important}}
@media(max-width:650px){{.manual-grid{{grid-template-columns:1fr}}.manual-head{{padding:22px 18px}}.manual-card{{min-height:0}}.st-key-menu_fixed{{right:12px!important;bottom:12px!important;width:210px!important}}}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<section class="manual-head">
  <div class="manual-kicker">PROJECT : LOGIC // SYSTEM MANUAL</div>
  <h1 class="manual-title">HOW TO PLAY</h1>
  <div class="manual-subtitle">INFORMATION IS NOT ALWAYS TRUE</div>
</section>
<div class="manual-grid">
  <div class="manual-card"><div class="num">01 // MOVEMENT</div><div class="label">이동</div><div class="detail">키보드의 W A S D 또는 화면에 표시되는 방향 버튼으로 이동합니다.</div></div>
  <div class="manual-card"><div class="num">02 // INTERACTION</div><div class="label">조사 / 상호작용</div><div class="detail">E 키 또는 화면의 INTERACT 버튼으로 주변 장치와 기록을 조사합니다.</div></div>
  <div class="manual-card"><div class="num">03 // DIALOGUE</div><div class="label">대사 진행</div><div class="detail">SPACE를 누르면 현재 출력 중인 문장을 완성합니다. 필수 행동은 건너뛸 수 없습니다.</div></div>
  <div class="manual-card"><div class="num">04 // INVENTORY</div><div class="label">인벤토리</div><div class="detail">I 키로 확보한 카드와 기록을 확인합니다. 아이템 설명에서 단서를 다시 읽을 수 있습니다.</div></div>
  <div class="manual-card"><div class="num">05 // SYSTEM MENU</div><div class="label">일시정지</div><div class="detail">화면 오른쪽 위의 Ⅱ 버튼을 눌러 RESUME, RESTART, TITLE 메뉴를 엽니다.</div></div>
  <div class="manual-card"><div class="num">06 // INVESTIGATION</div><div class="label">단서 분석</div><div class="detail">단말기 기록과 보관 기록의 단서를 모아 보안 패널 코드를 찾으세요.</div></div>
</div>
<div class="manual-note">SYSTEM NOTE // 모든 기록이 사실인 것은 아닙니다. 서로 다른 단서를 비교하고, 기록에 적힌 규칙을 확인한 뒤 행동하세요.</div>
""", unsafe_allow_html=True)

# Fixed popup-style navigation: it stays at the lower-right while the manual scrolls.
with st.container(key="menu_fixed"):
    if st.button("BACK TO MENU", key="back_to_menu", use_container_width=True):
        st.session_state.start_open = False
        st.session_state.show_title_warning = False
        st.switch_page("main.py")
