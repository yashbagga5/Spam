"""
Will You Be My Valentine? 💖 — Cinematic Streamlit experience
Run: streamlit run streamlit_app.py
URL: http://localhost:8501/?name=HerName
Luxury theme: ?name=HerName&luxury=1
"""

import base64
import json
import os
import random
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

try:
    from streamlit_confetti import confetti
    HAS_CONFETTI = True
except Exception:
    HAS_CONFETTI = False

LOVE_MESSAGE = "YAYYY!!! ❤️ You Just Made Me The Happiest Person!"
NO_MESSAGES = ["Are you sure? 🥺", "Think again…", "I'll buy you chocolate 🍫", "Last chance 👀"]
MAX_NO_CLICKS = 5
# Intro: soft pink gradient only (no external image)

st.set_page_config(
    page_title="Will You Be My Valentine? 💖",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Theme: default playful pink vs luxury black/red/gold
try:
    luxury = st.query_params.get("luxury", "0") == "1" if hasattr(st.query_params, "get") else False
except Exception:
    luxury = False

if luxury:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Quicksand:wght@400;500&display=swap');
    .stApp { background: #0a0505 !important; min-height: 100vh; }
    .block-container { padding-top: 2rem; max-width: 900px; margin: 0 auto; }
    h1, h2 { font-family: 'Cormorant Garamond', serif !important; color: #c9a227 !important; }
    p, .stMarkdown { font-family: 'Quicksand', sans-serif !important; color: #e8d5d5 !important; }
    .glass { background: rgba(20,5,5,0.6); border: 1px solid rgba(201,162,39,0.4); color: #e8d5d5; }
    </style>
    """, unsafe_allow_html=True)
else:
    # 1️⃣ Global sparkle background (all pages) — 28 dots, slow elegant fade
    sparkle_spans = "".join(
        f'<span class="sparkle-dot" style="left:{random.randint(0,100)}%;top:{random.randint(0,100)}%;animation-delay:{random.uniform(0,5):.1f}s;"></span>'
        for _ in range(28)
    )
    st.markdown(f"""
    <div id="sparkle-bg" aria-hidden="true">{sparkle_spans}</div>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Pacifico&family=Quicksand:wght@400;500;600;700&family=Dancing+Script:wght@400;600&display=swap');
    .stApp {{ background: linear-gradient(135deg, #ffd6e8 0%, #ff99cc 40%, #ff4d88 80%, #ff99cc 100%); background-size: 400% 400%; animation: appGradient 10s ease infinite; min-height: 100vh; }}
    @keyframes appGradient {{ 0%{{background-position:0% 50%;}} 50%{{background-position:100% 50%;}} 100%{{background-position:0% 50%;}} }}
    #sparkle-bg {{
      position: fixed; inset: 0; width: 100vw; height: 100vh; z-index: -1; pointer-events: none; overflow: hidden;
    }}
    .sparkle-dot {{
      position: absolute; width: 5px; height: 5px; border-radius: 50%;
      background: radial-gradient(circle, rgba(255,255,255,0.95) 0%, rgba(255,182,193,0.5) 50%, transparent 70%);
      box-shadow: 0 0 12px rgba(255,255,255,0.5);
      animation: sparkleFloat 8s ease-in-out infinite;
    }}
    @keyframes sparkleFloat {{
      0%, 100% {{ opacity: 0.25; transform: scale(0.7); }}
      50% {{ opacity: 0.9; transform: scale(1.3); }}
    }}
    h1, h2, .big-title {{ font-family: 'Pacifico', cursive !important; color: white !important; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }}
    p, .font-cute, .stMarkdown {{ font-family: 'Quicksand', 'Nunito', sans-serif !important; }}
    .glass {{ background: rgba(255,255,255,0.25); backdrop-filter: blur(12px); border-radius: 1.5rem; padding: 1.5rem 2rem; border: 1px solid rgba(255,255,255,0.4); box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin: 1rem 0; }}
    .block-container {{ padding-top: 2rem; max-width: 900px; margin: 0 auto; }}
    </style>
    """, unsafe_allow_html=True)

# 2️⃣ Pink heart cursor trail (thin top strip only, so rest of page is clickable)
if not luxury:
    HEART_TRAIL_HTML = """
    <div id="heart-trail-layer" style="position:relative;width:100%;height:90px;margin:0;padding:0;overflow:visible;">
      <div id="heart-trail-capture" style="position:absolute;top:0;left:0;right:0;height:90px;pointer-events:auto;cursor:default;z-index:1;"></div>
      <div id="heart-trail-container" style="position:absolute;top:0;left:0;right:0;height:90px;pointer-events:none;z-index:2;"></div>
    </div>
    <style>
    .heart-trail-heart { position: absolute; font-size: 10px; pointer-events: none; animation: heartFloat 0.8s ease-out forwards; z-index: 3; }
    @keyframes heartFloat {
      0% { opacity: 1; transform: translateY(0) scale(1); }
      100% { opacity: 0; transform: translateY(-40px) scale(0.8); }
    }
    </style>
    <script>
    (function(){
      var container = document.getElementById('heart-trail-container');
      var capture = document.getElementById('heart-trail-capture');
      var colors = ['#ff4d88', '#ff66a3', '#ff85c1'];
      var last = 0;
      capture.addEventListener('mousemove', function(e) {
        if (Date.now() - last < 60) return;
        last = Date.now();
        var h = document.createElement('span');
        h.className = 'heart-trail-heart';
        h.textContent = '♥';
        h.style.left = (e.clientX - 6) + 'px';
        h.style.top = (e.clientY - 6) + 'px';
        h.style.color = colors[Math.floor(Math.random() * 3)];
        container.appendChild(h);
        setTimeout(function() { if (h.parentNode) h.parentNode.removeChild(h); }, 800);
      });
    })();
    </script>
    """
    components.html(HEART_TRAIL_HTML, height=90)

# Sync said_yes from URL (so HTML can redirect parent to ?said_yes=1)
try:
    if hasattr(st.query_params, "get") and st.query_params.get("said_yes") == "1":
        st.session_state.said_yes = True
except Exception:
    pass

if "stage" not in st.session_state:
    st.session_state.stage = "home"
if "no_clicks" not in st.session_state:
    st.session_state.no_clicks = 0
if "said_yes" not in st.session_state:
    st.session_state.said_yes = False
if "no_column" not in st.session_state:
    st.session_state.no_column = 1
if "run_scan" not in st.session_state:
    st.session_state.run_scan = False
if "scan_done" not in st.session_state:
    st.session_state.scan_done = False
if "love_meter_val" not in st.session_state:
    st.session_state.love_meter_val = 0

try:
    name = st.query_params.get("name", "You") if hasattr(st.query_params, "get") else "You"
    if not name or not str(name).strip():
        name = "You"
except Exception:
    name = "You"

def get_base64_image(path):
    """Load image from path and return base64 string for HTML embedding."""
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except (FileNotFoundError, OSError):
        # Placeholder: tiny pink pixel PNG if asset missing
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADBgGA/jT9CQAAAABJRU5ErkJggg=="


def load_photo_from_assets(assets_dir, name_no_ext):
    """Load photo trying .jpg, .jpeg, .png. Returns (base64_string, mime for data URL: 'jpeg' or 'png')."""
    for ext in (".jpg", ".jpeg", ".png"):
        path = os.path.join(assets_dir, name_no_ext + ext)
        if os.path.isfile(path):
            b64 = get_base64_image(path)
            mime = "jpeg" if ext in (".jpg", ".jpeg") else "png"
            return b64, mime
    return get_base64_image(os.path.join(assets_dir, "__missing__")), "png"

def get_next_valentines():
    now = datetime.now()
    next_v = datetime(now.year, 2, 14)
    if now >= next_v:
        next_v = datetime(now.year + 1, 2, 14)
    return next_v

def countdown_str():
    n = get_next_valentines()
    d = (n - datetime.now()).days
    return f"Next Valentine's Day in **{d}** days 💖"

# ----- CELEBRATION (after YES) — 6️⃣ Dynamic mood: zoom, red shift, shake, heartbeat, ring + 10️⃣ Our Future -----
if st.session_state.said_yes:
    # Full cinematic transformation overlay: zoom, deep red bg, camera shake, heartbeat, ring shine
    RING_HTML = """
    <div id="yes-overlay" style="position:fixed;inset:0;z-index:9999;overflow:hidden;">
      <div id="yes-bg" style="position:absolute;inset:0;background:linear-gradient(180deg, #fce7f3 0%, #ec4899 40%, #7f1d1d 80%, #450a0a 100%);opacity:0;animation:bgShift 2s ease 0.5s forwards;"></div>
      <div id="yes-zoom" style="position:absolute;inset:-10%;animation:screenZoom 1.2s ease 0.2s forwards;transform:scale(0.9);pointer-events:none;"></div>
      <div id="yes-shake" style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;animation:cameraShake 0.5s ease 0.3s;">
        <div id="ring-box" style="animation:ringZoom 2s ease-out 1s forwards;transform:scale(0);filter:drop-shadow(0 0 30px #ff6b9d);">
          <div style="font-size:90px;animation:ringShine 0.8s ease-in-out infinite 2s;">💍</div>
        </div>
        <p id="ring-text" style="margin-top:1rem;font-family:'Pacifico',cursive;color:#fff;font-size:1.8rem;text-shadow:0 0 20px rgba(255,255,255,0.8);opacity:0;animation:showText 0.8s 2.5s forwards;">It's official now 😌 You're Mine Forever.</p>
      </div>
      <div id="heart-rain"></div>
    </div>
    <style>
      @keyframes bgShift { to { opacity: 1; } }
      @keyframes screenZoom { to { transform: scale(1.1); } }
      @keyframes cameraShake { 0%,100%{transform:translateX(0);} 20%{transform:translateX(-12px);} 40%{transform:translateX(12px);} 60%{transform:translateX(-8px);} 80%{transform:translateX(8px);} }
      @keyframes ringZoom { 0%{transform:scale(0) rotate(-20deg);} 50%{transform:scale(1.25) rotate(5deg);} 100%{transform:scale(1) rotate(0);} }
      @keyframes ringShine { 0%,100%{filter:drop-shadow(0 0 25px #ff6b9d);} 50%{filter:drop-shadow(0 0 50px #fff);} }
      @keyframes showText { to { opacity: 1; } }
      @keyframes fall { to { transform: translateY(100vh) rotate(360deg); } }
      @keyframes confettiFall { to { transform: translateY(100vh) rotate(720deg); opacity: 0; } }
    </style>
    <script>
    (function(){
      function heartbeat(){
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var o = ctx.createOscillator(); var g = ctx.createGain();
        o.type = 'sine'; o.frequency.value = 60; g.gain.value = 0.2;
        o.connect(g); g.connect(ctx.destination);
        o.start(ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.15);
        setTimeout(function(){ o.frequency.value = 80; o.start(ctx.currentTime); g.gain.setValueAtTime(0.15, ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2); }, 180);
      }
      setTimeout(heartbeat, 800);
      var hr = document.getElementById('heart-rain');
      for(var i=0;i<60;i++){
        var h = document.createElement('span'); h.textContent = '💕'; h.style.cssText = 'position:fixed;left:'+Math.random()*100+'vw;top:-20px;font-size:'+(14+Math.random()*24)+'px;animation:fall '+(4+Math.random()*3)+'s linear '+(Math.random()*2)+'s infinite;pointer-events:none;z-index:10000;';
        document.body.appendChild(h);
      }
      setTimeout(function(){ for(var i=0;i<120;i++){ var c=document.createElement('div'); c.style.cssText='position:fixed;width:12px;height:12px;background:hsl('+Math.random()*360+',80%,60%);left:'+Math.random()*100+'vw;top:40vh;border-radius:50%;pointer-events:none;z-index:10001;'; c.style.animation = 'confettiFall '+(2.5+Math.random()*2)+'s ease-out forwards'; document.body.appendChild(c); } }, 600);
    })();
    </script>
    """
    components.html(RING_HTML, height=500)
    if HAS_CONFETTI:
        confetti()
    st.markdown(f"## {LOVE_MESSAGE}")
    st.markdown("I can't wait to celebrate with you! 💕")
    st.markdown("---")
    st.markdown('<div class="glass">**Date night?**  \nFeb 14 — You & Me 💖</div>', unsafe_allow_html=True)
    st.balloons()

    # 10️⃣ Post-YES Secret: Our Future
    st.markdown("---")
    st.markdown("## 👑 Our Future")
    st.markdown("A little preview of what we're building together…")
    n = get_next_valentines()
    days_v = (n - datetime.now()).days
    future_items = [
        ("Our First Trip ✈️", "Somewhere we've always talked about — just us."),
        ("Future House 🏠", "A place with a kitchen for your experiments and a couch for our movies."),
        ("Future Pet Name 🐾", "We'll argue over it and then pick something ridiculous. I can't wait."),
        ("Wedding Date Countdown 💒", f"Next Valentine's in **{days_v}** days — and every day after that."),
    ]
    for title, body in future_items:
        st.markdown(f'<div class="glass"><strong>{title}</strong><br>{body}</div>', unsafe_allow_html=True)
    st.stop()

# ----- Countdown + Share (only when not in intro/experience) -----
if st.session_state.stage not in ("intro", "experience"):
    c1, c2 = st.columns([2, 1])
    with c1:
        st.caption(countdown_str())
    with c2:
        if st.button("📋 Share link"):
            try:
                params = dict(st.query_params) if hasattr(st.query_params, "__iter__") else {}
                param_str = "&".join(f"{k}={v}" for k, v in params.items()) if params else "name=HerName"
                st.info(f"Copy URL with: ?{param_str}")
            except Exception:
                st.info("Use ?name=HerName in the URL to personalize!")
    st.markdown("---")

# ----- 3️⃣ HOMEPAGE — Full pink creative theme + 4️⃣ Special date (timeline) -----
if st.session_state.stage == "home" and luxury:
    st.session_state.stage = "intro"
    st.rerun()
if st.session_state.stage == "home" and not luxury:
    HOME_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
      <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600;700&family=Pacifico&family=Quicksand:wght@400;500&display=swap" rel="stylesheet">
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; font-family: Quicksand, sans-serif; overflow-x: hidden; }
        #home-bg {
          position: fixed; inset: 0; z-index: -1;
          background: linear-gradient(-45deg, #ffd6e8, #ff99cc, #ff4d88, #ff99cc, #ffd6e8);
          background-size: 400% 400%;
          animation: gradientShift 8s ease infinite;
        }
        @keyframes gradientShift {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        .home-content { position: relative; z-index: 1; padding: 2.5rem 2rem; max-width: 560px; }
        .home-title { font-family: Pacifico, cursive; font-size: clamp(2rem, 6vw, 3rem); color: #ffffff; font-weight: 600; text-shadow: 0 0 15px rgba(255,255,255,0.6), 0 0 40px rgba(255,182,193,0.4); margin-bottom: 0.75rem; letter-spacing: 0.02em; line-height: 1.3; }
        .home-hearts { font-size: 1.2rem; opacity: 0.95; margin-bottom: 2rem; }
        .date-section { margin: 2rem 0; }
        .date-main { font-family: Dancing Script, cursive; font-size: clamp(1.8rem, 5vw, 2.5rem); color: #ffffff; font-weight: 600; text-shadow: 0 0 15px rgba(255,255,255,0.6); position: relative; display: inline-block; padding-bottom: 0.4rem; }
        .date-main::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 2px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent); animation: underlinePulse 2s ease-in-out infinite; }
        @keyframes underlinePulse { 0%, 100% { opacity: 0.5; transform: scaleX(0.9); } 50% { opacity: 1; transform: scaleX(1); } }
        .date-sub { font-family: Quicksand, sans-serif; font-size: 1.05rem; color: #fff0f5; margin-top: 0.6rem; font-weight: 500; text-align: center; text-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .timeline { margin: 2.5rem 0; text-align: left; position: relative; padding-left: 2rem; }
        .timeline::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: linear-gradient(180deg, rgba(255,255,255,0.6), rgba(249,168,212,0.8)); border-radius: 3px; }
        .timeline-item { position: relative; margin-bottom: 1.5rem; padding: 0.8rem 1rem; background: rgba(255,255,255,0.15); border-radius: 12px; border-left: 4px solid rgba(255,255,255,0.6); box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .timeline-item::before { content: '❤'; position: absolute; left: -1.6rem; top: 0.6rem; font-size: 0.9rem; }
        .timeline-date { font-family: Dancing Script, cursive; font-size: 1.3rem; color: #fff; margin-bottom: 0.2rem; }
        .timeline-text { font-size: 0.95rem; color: #fff0f5; }
        .home-cta { margin-top: 2rem; }
        .home-cta .stButton { margin: 0 auto; }
      </style>
    </head>
    <body>
      <div id="home-bg"></div>
      <div class="home-content">
        <h1 class="home-title">Will You Be My Valentine? 💖</h1>
        <p class="home-hearts">❤️ 💕 ❤️ 💕 ❤️</p>
        <div class="date-section">
          <p class="date-main">Since 24 March 2025 ❤️</p>
          <p class="date-sub">The day my world changed forever.</p>
        </div>
        <div class="timeline">
          <div class="timeline-item">
            <div class="timeline-date">24 March 2025</div>
            <div class="timeline-text">The day we started our story — and every moment since has been magic.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-date">Our firsts</div>
            <div class="timeline-text">First laugh, first adventure, first “I don’t want this to end.”</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-date">Today & always</div>
            <div class="timeline-text">One question for you, with all my heart…</div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    components.html(HOME_HTML, height=620)
    st.markdown("<div class='home-cta' style='text-align:center;margin-top:0.5rem;'>", unsafe_allow_html=True)
    if st.button("Begin our story 💫", type="primary", key="home_enter"):
        st.session_state.stage = "intro"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ----- CINEMATIC OPENING -----
if st.session_state.stage == "intro":
    INTRO_HTML = """
    <div id="cinema-intro" style="position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Cormorant Garamond',Georgia,serif;overflow:hidden;">
      <div id="cinema-bg" style="position:absolute;inset:-20px;background:linear-gradient(-45deg, #ffd6e8, #ff99cc, #ff4d88, #ff99cc, #ffd6e8);background-size:400% 400%;animation:cinemaGradient 8s ease infinite;filter:blur(0);"></div>
      <div style="position:absolute;inset:0;background:rgba(255,255,255,0.12);backdrop-filter:blur(2px);"></div>
      <div id="cinema-text" style="position:relative;z-index:1;text-align:center;color:rgba(255,255,255,0.98);font-size:clamp(1.2rem,4vw,1.8rem);line-height:2;max-width:90%;"></div>
      <div id="cinema-name" style="position:relative;z-index:1;margin-top:2rem;font-size:clamp(2rem,8vw,4rem);color:transparent;opacity:0;text-shadow:0 0 40px rgba(255,255,255,0.7);background:linear-gradient(90deg,#ffd6e8,#fff,#ffd6e8);background-size:200% auto;-webkit-background-clip:text;background-clip:text;animation:nameGlow 3s ease 1s forwards;"></div>
      <div id="cinema-zoom" style="position:fixed;inset:0;background:radial-gradient(ellipse 80% 80% at 50% 50%, transparent 0%, rgba(255,182,193,0.15) 100%);pointer-events:none;opacity:0;animation:zoomIn 4s ease 2s forwards;"></div>
      <style>
        @keyframes cinemaGradient { 0%{background-position:0% 50%;} 50%{background-position:100% 50%;} 100%{background-position:0% 50%;} }
        @keyframes nameGlow { to { opacity: 1; } }
        @keyframes zoomIn { 0%{opacity:0;transform:scale(0.95);} 70%{opacity:0;} 100%{opacity:1;transform:scale(1.1);} }
      </style>
    </div>
    <script>
    (function(){
      var lines = ['In a world full of people…', 'There was one person…', 'Who changed everything.'];
      var el = document.getElementById('cinema-text');
      var nameEl = document.getElementById('cinema-name');
      var name = __NAME_JSON__;
      var typingSound = function(){
        try {
          var ctx = new (window.AudioContext || window.webkitAudioContext)();
          var o = ctx.createOscillator(); var g = ctx.createGain();
          o.type = 'sine'; o.frequency.value = 800; g.gain.value = 0.03;
          o.connect(g); g.connect(ctx.destination);
          o.start(ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.06);
        } catch(e){}
      };
      var lineIdx = 0;
      function typeLine(cb) {
        if (lineIdx >= lines.length) { nameEl.textContent = name; cb(); return; }
        var text = lines[lineIdx]; el.innerHTML = ''; var i = 0;
        function tick() {
          if (i <= text.length) {
            el.innerHTML = text.slice(0, i) + '<span style="opacity:0.5">|</span>';
            if (i > 0 && i % 2 === 0) typingSound();
            i++;
            setTimeout(tick, 90);
          } else {
            el.innerHTML = text;
            lineIdx++;
            setTimeout(function(){ typeLine(cb); }, 1200);
          }
        }
        tick();
      }
      setTimeout(function(){ typeLine(function(){}); }, 800);
    })();
    </script>
    """
    intro_html_final = INTRO_HTML.replace("__NAME_JSON__", json.dumps(name))
    components.html(intro_html_final, height=680)
    st.markdown("<div style='text-align:center;margin-top:1rem;'>", unsafe_allow_html=True)
    if st.button("Enter 💫", type="primary", key="enter_cinema"):
        st.session_state.stage = "fun"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ----- 2️⃣ IMMERSIVE EXPERIENCE (cursor reactive, 3D glass, catch-5-hearts, emotional build-up, time-stop proposal) -----
if st.session_state.stage == "experience":
    LUXURY_CSS = """
    #exp-bg { background: radial-gradient(ellipse at 50% 0%, #1a0505 0%, #0a0505 50%, #000 100%) !important; }
    .exp-card { background: rgba(20,5,5,0.7) !important; border: 1px solid rgba(201,162,39,0.3) !important; color: #e8d5d5 !important; }
    .exp-card:hover { box-shadow: 0 0 40px rgba(201,162,39,0.2) !important; }
    .exp-title { color: #c9a227 !important; font-family: Cormorant Garamond, serif !important; }
    .exp-heart { filter: drop-shadow(0 0 6px rgba(201,162,39,0.6)) !important; }
    #proposal-box { background: rgba(10,5,5,0.95) !important; border: 2px solid #c9a227 !important; }
    """ if luxury else ""
    EXP_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Pacifico&family=Quicksand:wght@400;500;600&display=swap" rel="stylesheet">
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Quicksand, sans-serif; overflow-x: hidden; min-height: 100vh; }
        #exp-bg { position: fixed; inset: 0; background: linear-gradient(180deg, #1a0a12 0%, #2d0a1a 30%, #4a0a24 60%, #2d0a1a 100%); z-index: 0; transition: transform 0.3s ease-out; }
        #exp-ripples { position: fixed; inset: 0; z-index: 1; pointer-events: none; }
        #exp-stars { position: fixed; inset: 0; z-index: 2; pointer-events: none; }
        #exp-content { position: relative; z-index: 3; padding: 2rem 1rem 4rem; max-width: 700px; margin: 0 auto; }
        .exp-card { background: rgba(255,255,255,0.08); backdrop-filter: blur(20px); border-radius: 24px; padding: 2rem; margin: 2rem 0; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 25px 50px rgba(0,0,0,0.3); transition: transform 0.4s ease, box-shadow 0.4s ease; }
        .exp-card:hover { transform: translateZ(20px) scale(1.02); box-shadow: 0 0 50px rgba(236,72,153,0.2); }
        .exp-title { font-family: Pacifico, cursive; font-size: 1.5rem; color: #fce7f3; margin-bottom: 0.75rem; }
        .exp-body { color: rgba(255,255,255,0.9); line-height: 1.7; }
        #game-section { text-align: center; padding: 3rem 1rem; }
        #game-title { font-family: Pacifico, cursive; font-size: 1.8rem; color: #fff; margin-bottom: 1rem; }
        #game-canvas { display: block; margin: 0 auto 1rem; border-radius: 16px; background: rgba(0,0,0,0.3); cursor: crosshair; }
        #game-score { font-size: 1.2rem; color: #f9a8d4; margin-bottom: 0.5rem; }
        #game-done { display: none; font-size: 1.5rem; color: #fff; animation: fadeIn 1s ease; }
        #build-up { padding: 3rem 1rem; text-align: center; }
        .build-line { font-family: Cormorant Garamond, serif; font-size: clamp(1.2rem,4vw,1.6rem); color: rgba(255,255,255,0.95); margin: 1rem 0; opacity: 0; animation: fadeInUp 1.2s ease forwards; }
        #proposal-wrap { position: fixed; inset: 0; z-index: 100; display: none; align-items: center; justify-content: center; background: rgba(0,0,0,0.7); backdrop-filter: blur(12px); }
        #proposal-wrap.active { display: flex; animation: fadeIn 0.6s ease; }
        #proposal-box { background: linear-gradient(145deg, rgba(80,20,40,0.95), rgba(40,5,25,0.98)); padding: 3rem; border-radius: 24px; text-align: center; border: 2px solid rgba(249,168,212,0.5); box-shadow: 0 0 60px rgba(236,72,153,0.3); }
        #proposal-q { font-family: Pacifico, cursive; font-size: clamp(1.5rem,5vw,2.2rem); color: #fff; margin-bottom: 1.5rem; }
        .proposal-btn { padding: 1rem 2.5rem; margin: 0 0.5rem; font-size: 1.2rem; border: none; border-radius: 50px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
        #btn-yes { background: linear-gradient(135deg, #ec4899, #be185d); color: #fff; }
        #btn-yes:hover { transform: scale(1.08); box-shadow: 0 0 30px rgba(236,72,153,0.6); }
        #btn-no { background: rgba(255,255,255,0.2); color: #fff; }
        @keyframes fadeIn { to { opacity: 1; } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        """ + LUXURY_CSS + """
      </style>
    </head>
    <body>
      <div id="exp-bg"></div>
      <canvas id="exp-ripples"></canvas>
      <div id="exp-stars"></div>
      <div id="exp-content">
        <div class="exp-card" data-tilt><div class="exp-title">The day we met ✨</div><div class="exp-body">Everything changed. You walked in and my world got a little brighter.</div></div>
        <div class="exp-card" data-tilt><div class="exp-title">You are my peace 🌙</div><div class="exp-body">Late talks, silly moments, and every second in between. I wouldn't trade them for anything.</div></div>
        <div class="exp-card" data-tilt><div class="exp-title">You make everything brighter ☀️</div><div class="exp-body">Your smile, your laugh, your presence. You're the best thing that ever happened to me.</div></div>

        <div id="game-section">
          <div id="game-title">Catch 5 falling hearts 💖</div>
          <div id="game-score">Hearts caught: <span id="score-num">0</span> / 5</div>
          <canvas id="game-canvas" width="400" height="300"></canvas>
          <div id="game-done">You caught my heart too. 💕</div>
          <button id="game-continue" style="display:none;margin-top:1rem;padding:0.8rem 2rem;background:linear-gradient(135deg,#ec4899,#be185d);color:#fff;border:none;border-radius:50px;font-size:1.1rem;cursor:pointer;">Continue →</button>
        </div>

        <div id="build-up" style="display:none;">
          <div class="build-line" style="animation-delay:0s">You're my comfort.</div>
          <div class="build-line" style="animation-delay:0.8s">My chaos.</div>
          <div class="build-line" style="animation-delay:1.6s">My peace.</div>
          <div class="build-line" style="animation-delay:2.4s">My forever.</div>
          <div class="build-line" style="animation-delay:3.5s; font-family:Pacifico,cursive; font-size:1.4rem;">And now…</div>
        </div>
      </div>

      <div id="proposal-wrap">
        <div id="proposal-box">
          <div id="proposal-q">Will You Be My Valentine? 💖</div>
          <button class="proposal-btn" id="btn-yes">YES 😍</button>
          <button class="proposal-btn" id="btn-no">NO 😢</button>
        </div>
      </div>

      <script>
      (function(){
        var luxury = __LUXURY_JS__;
        var name = __NAME_JSON__;

        // Cursor reactive bg
        var bg = document.getElementById('exp-bg');
        var mx = 0, my = 0;
        document.addEventListener('mousemove', function(e){ mx = (e.clientX / window.innerWidth - 0.5) * 20; my = (e.clientY / window.innerHeight - 0.5) * 20; });
        function tickBg(){ bg.style.transform = 'translate(' + mx + 'px, ' + my + 'px) scale(1.05)'; requestAnimationFrame(tickBg); }
        tickBg();

        // Ripples
        var rippleCanvas = document.getElementById('exp-ripples');
        rippleCanvas.width = window.innerWidth; rippleCanvas.height = window.innerHeight;
        var ripples = [];
        rippleCanvas.addEventListener('click', function(e){ ripples.push({ x: e.clientX, y: e.clientY, r: 0, max: 80 }); });
        function drawRipples(){
          var ctx = rippleCanvas.getContext('2d');
          ctx.clearRect(0,0,rippleCanvas.width,rippleCanvas.height);
          for(var i=ripples.length-1;i>=0;i--){
            var r = ripples[i]; r.r += 3;
            ctx.beginPath(); ctx.arc(r.x, r.y, r.r, 0, Math.PI*2);
            ctx.strokeStyle = 'rgba(249,168,212,0.4)'; ctx.lineWidth = 2; ctx.stroke();
            if(r.r > r.max) ripples.splice(i,1);
          }
          requestAnimationFrame(drawRipples);
        }
        drawRipples();

        // Stars
        var starsEl = document.getElementById('exp-stars');
        for(var i=0;i<80;i++){
          var s = document.createElement('div');
          s.style.cssText = 'position:absolute;left:'+Math.random()*100+'%;top:'+Math.random()*100+'%;width:'+(1+Math.random()*2)+'px;height:1px;background:rgba(255,255,255,'+(0.3+Math.random()*0.5)+');border-radius:50%;animation:twinkle '+(2+Math.random()*3)+'s ease-in-out infinite;';
          starsEl.appendChild(s);
        }
        var style = document.createElement('style');
        style.textContent = '@keyframes twinkle { 0%,100%{opacity:0.5;} 50%{opacity:1;} }';
        document.head.appendChild(style);

        // 3D tilt cards
        document.querySelectorAll('.exp-card[data-tilt]').forEach(function(card){
          card.addEventListener('mousemove', function(e){
            var rect = card.getBoundingClientRect();
            var x = (e.clientX - rect.left) / rect.width - 0.5;
            var y = (e.clientY - rect.top) / rect.height - 0.5;
            card.style.transform = 'perspective(800px) rotateX(' + (-y*8) + 'deg) rotateY(' + (x*8) + 'deg) translateZ(20px) scale(1.02)';
          });
          card.addEventListener('mouseleave', function(){ card.style.transform = ''; });
        });

        // Catch 5 hearts game
        var canvas = document.getElementById('game-canvas');
        var ctx = canvas.getContext('2d');
        var score = 0;
        var hearts = [];
        var heartImg = null;
        function spawnHeart(){
          hearts.push({ x: Math.random() * (canvas.width - 40), y: -30, vy: 0.5 + Math.random() * 0.5, caught: false });
        }
        function gameLoop(){
          ctx.clearRect(0,0,canvas.width,canvas.height);
          for(var i=hearts.length-1;i>=0;i--){
            var h = hearts[i];
            if(h.caught) continue;
            h.y += h.vy;
            ctx.font = '26px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.fillText('💖', h.x + 14, h.y + 14);
            if(h.y > canvas.height) hearts.splice(i,1);
          }
          if(hearts.length < 4 && Math.random() < 0.03) spawnHeart();
          requestAnimationFrame(gameLoop);
        }
        canvas.addEventListener('click', function(e){
          var rect = canvas.getBoundingClientRect();
          var x = e.clientX - rect.left, y = e.clientY - rect.top;
          hearts.forEach(function(h){
            if(h.caught) return;
            if(x >= h.x && x <= h.x+28 && y >= h.y && y <= h.y+28){ h.caught = true; score++; document.getElementById('score-num').textContent = score;
              if(score >= 5){ document.getElementById('game-done').style.display = 'block'; document.getElementById('game-continue').style.display = 'inline-block'; }
            }
          });
        });
        setInterval(spawnHeart, 900);
        gameLoop();

        // Continue -> build-up -> proposal
        document.getElementById('game-continue').onclick = function(){
          document.getElementById('game-section').style.display = 'none';
          document.getElementById('build-up').style.display = 'block';
          setTimeout(function(){
            document.getElementById('proposal-wrap').classList.add('active');
            document.body.style.overflow = 'hidden';
          }, 5000);
        };

        // NO button: hover = move away + shake + random text; click = more movement + shrink; after 5 = disable
        var noBtn = document.getElementById('btn-no');
        var noClicks = 0;
        var hoverTexts = ['Are you sure? 🥺', 'Think again 👀', 'Last chance 😏'];
        var proposalBox = document.getElementById('proposal-box');
        var noBtnLeft = 0, noBtnTop = 0;
        function getNoPos(){ var r = noBtn.getBoundingClientRect(); return { x: r.left + r.width/2, y: r.top + r.height/2 }; }
        noBtn.onmouseenter = function(e){
          if (noClicks >= 5) return;
          var pos = getNoPos();
          var dx = (e.clientX - pos.x) > 0 ? 1 : -1;
          var dy = (e.clientY - pos.y) > 0 ? 1 : -1;
          noBtnLeft += (20 + Math.random() * 12) * dx;
          noBtnTop += (12 + Math.random() * 8) * dy;
          noBtn.style.transform = 'translate(' + noBtnLeft + 'px, ' + noBtnTop + 'px)';
          noBtn.textContent = hoverTexts[Math.floor(Math.random() * 3)];
          noBtn.style.transition = 'none';
          noBtn.style.transform = 'translate(' + (noBtnLeft - 6) + 'px, ' + noBtnTop + 'px)';
          setTimeout(function(){ noBtn.style.transform = 'translate(' + (noBtnLeft + 6) + 'px, ' + noBtnTop + 'px)'; }, 40);
          setTimeout(function(){ noBtn.style.transform = 'translate(' + noBtnLeft + 'px, ' + noBtnTop + 'px)'; noBtn.style.transition = ''; }, 80);
        };
        noBtn.onclick = function(e){
          e.preventDefault();
          if (noClicks >= 5) return;
          noClicks++;
          noBtnLeft += (Math.random() * 60 - 30);
          noBtnTop += (Math.random() * 40 - 20);
          noBtn.style.transform = 'translate(' + noBtnLeft + 'px, ' + noBtnTop + 'px) scale(' + (1 - noClicks * 0.06) + ')';
          noBtn.textContent = hoverTexts[Math.floor(Math.random() * 3)];
          if (noClicks >= 5) {
            noBtn.textContent = 'Okay okay I give up 😭';
            noBtn.style.pointerEvents = 'none';
            noBtn.style.opacity = '0.6';
            noBtn.style.cursor = 'default';
          }
        };

        // YES -> redirect to set said_yes
        document.getElementById('btn-yes').onclick = function(){
          try {
            var url = (window.top.location.origin + window.top.location.pathname || '') + '?said_yes=1&name=' + encodeURIComponent(name);
            if(luxury) url += '&luxury=1';
            window.top.location.href = url;
          } catch(e) { window.location.href = '?said_yes=1'; }
        };
      })();
      </script>
    </body>
    </html>
    """
    exp_html_final = EXP_HTML.replace("__NAME_JSON__", json.dumps(name)).replace("__LUXURY_JS__", "true" if luxury else "false")
    components.html(exp_html_final, height=900, scrolling=True)
    st.stop()

# ----- FUN ZONE (Compatibility, Wheel, Secret, Love Meter) -----
elif st.session_state.stage == "fun":
    st.markdown("## 💖 Fun & surprises for you…")
    st.markdown("Try each one before we continue 💕")
    st.markdown("---")

    # 1️⃣ Love Compatibility Scanner
    st.markdown("### 💖 1. Love Compatibility Scanner")
    col_scan_btn, col_scan_result = st.columns([1, 2])
    with col_scan_btn:
        if st.button("Scan Our Love Compatibility 💕", type="primary", key="scan_btn"):
            st.session_state.run_scan = True
            st.rerun()
    if st.session_state.run_scan:
        SCAN_HTML = """
        <div id="scan-root" style="font-family:Quicksand,sans-serif;padding:1rem;border-radius:1rem;background:rgba(255,255,255,0.2);">
          <div id="scan-loading" style="text-align:center;">
            <div style="width:40px;height:40px;border:4px solid #f9a8d4;border-top-color:#ec4899;border-radius:50%;margin:0 auto 1rem;animation:spin 0.8s linear infinite;"></div>
            <p style="color:#831843;margin:0;">AI scanning compatibility…</p>
            <p id="scan-pct" style="font-size:2rem;font-weight:700;color:#be185d;margin:0.5rem 0;">0%</p>
          </div>
          <div id="scan-done" style="display:none;text-align:center;">
            <p id="scan-final" style="font-size:1.5rem;font-weight:700;color:#fff;text-shadow:0 0 20px #ff6b9d;animation:pulse 1s ease-in-out infinite;"></p>
            <p style="color:rgba(255,255,255,0.9);margin-top:0.5rem;">Soulmates Detected 💘</p>
          </div>
        </div>
        <style>
          @keyframes spin { to { transform: rotate(360deg); } }
          @keyframes pulse { 0%,100%{text-shadow:0 0 20px #ff6b9d;} 50%{text-shadow:0 0 40px #fff, 0 0 60px #ff6b9d;} }
        </style>
        <script>
        (function(){
          var loading = document.getElementById('scan-loading');
          var done = document.getElementById('scan-done');
          var pctEl = document.getElementById('scan-pct');
          var finalEl = document.getElementById('scan-final');
          function heartbeat(){
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            var o = ctx.createOscillator(); var g = ctx.createGain();
            o.connect(g); g.connect(ctx.destination); o.frequency.value = 120; g.gain.value = 0.15;
            o.start(); setTimeout(function(){ g.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1); }, 100);
            setTimeout(function(){ o.frequency.value = 140; o.start(ctx.currentTime); g.gain.setValueAtTime(0.15, ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.15); }, 200);
          }
          var n = 0;
          function tick(){
            n += Math.floor(Math.random() * 12) + 4;
            if (n >= 100) {
              pctEl.textContent = '100%';
              loading.style.display = 'none';
              finalEl.textContent = 'Compatibility: 999% – Soulmates Detected 💘';
              done.style.display = 'block';
              heartbeat();
              return;
            }
            pctEl.textContent = n + '%';
            setTimeout(tick, 80 + Math.random() * 60);
          }
          setTimeout(tick, 500);
        })();
        </script>
        """
        components.html(SCAN_HTML, height=180)
    st.markdown("---")

    # 2️⃣ Spin the Love Wheel
    st.markdown("### 🎰 2. Spin the Love Wheel")
    WHEEL_HTML = """
    <div style="font-family:Quicksand,sans-serif;text-align:center;">
      <div id="wheel-wrap" style="position:relative;width:200px;height:200px;margin:0 auto;">
        <canvas id="wheel" width="200" height="200"></canvas>
        <div id="wheel-pointer" style="position:absolute;top:-5px;left:50%;transform:translateX(-50%);font-size:24px;z-index:2;">▼</div>
      </div>
      <button id="spin-btn" style="margin-top:1rem;padding:0.6rem 1.5rem;background:linear-gradient(135deg,#ec4899,#be185d);color:white;border:none;border-radius:2rem;font-size:1rem;cursor:pointer;">Spin the Wheel 🎰</button>
      <div id="wheel-result" style="display:none;margin-top:1rem;padding:1rem;background:rgba(255,255,255,0.3);border-radius:1rem;font-size:1.2rem;font-weight:700;animation:popIn 0.5s ease;"></div>
    </div>
    <style>@keyframes popIn { 0%{transform:scale(0);} 70%{transform:scale(1.1);} 100%{transform:scale(1);} }</style>
    <script>
    (function(){
      var items = ['Hug Coupon 🤗','Movie Night 🎬','Unlimited Chocolates 🍫','Date Night 🌹','Forever Mine 💍'];
      var shortItems = ['Hug 🤗','Movie 🎬','Choco 🍫','Date 🌹','Forever 💍'];
      var colors = ['#f472b6','#ec4899','#db2777','#be185d','#9d174d'];
      var canvas = document.getElementById('wheel'); var ctx = canvas.getContext('2d');
      var resultEl = document.getElementById('wheel-result');
      var spinBtn = document.getElementById('spin-btn');
      var currentRotation = 0; var spinning = false;
      function drawWheel(rot){
        ctx.save();
        ctx.translate(100,100);
        ctx.rotate(rot);
        ctx.translate(-100,-100);
        var slice = (2*Math.PI)/items.length;
        for(var i=0;i<items.length;i++){
          ctx.beginPath(); ctx.moveTo(100,100);
          ctx.arc(100,100,95, i*slice, (i+1)*slice);
          ctx.fillStyle = colors[i]; ctx.fill(); ctx.stroke();
          ctx.save(); ctx.translate(100,100); ctx.rotate(i*slice+slice/2);
          ctx.fillStyle='#fff'; ctx.font='12px Quicksand'; ctx.textAlign='center';
          ctx.fillText(shortItems[i], 52, 5);
          ctx.restore();
        }
        ctx.restore();
      }
      drawWheel(0);
      spinBtn.onclick = function(){
        if(spinning) return;
        spinning = true;
        resultEl.style.display = 'none';
        var spins = 5 + Math.random()*3;
        var win = Math.floor(Math.random()*items.length);
        var slice = 2*Math.PI/items.length;
        var targetRot = spins*2*Math.PI - (win*slice + slice/2) - Math.PI/2;
        var start = currentRotation;
        var startT = Date.now();
        function animate(){
          var t = (Date.now()-startT)/3000;
          if(t>=1){ currentRotation = start + targetRot; spinning = false; drawWheel(currentRotation); resultEl.textContent = '🎉 You won: ' + items[win] + '!'; resultEl.style.display = 'block'; return; }
          var ease = 1 - Math.pow(1-t, 3);
          currentRotation = start + targetRot * ease;
          drawWheel(currentRotation);
          requestAnimationFrame(animate);
        }
        animate();
      };
    })();
    </script>
    """
    components.html(WHEEL_HTML, height=320)
    st.markdown("---")

    # 3️⃣ Unlockable Secret Message
    st.markdown("### 💌 3. Unlock the Secret Message")
    SECRET_HTML = """
    <div id="secret-container" style="font-family:Quicksand,sans-serif;">
      <div id="hearts-float" style="position:relative;height:80px;margin-bottom:1rem;"></div>
      <div id="secret-card" style="padding:1.5rem;border-radius:1rem;background:rgba(0,0,0,0.2);text-align:center;border:2px dashed rgba(255,255,255,0.5);">
        <p id="secret-locked" style="margin:0;color:rgba(255,255,255,0.8);">🔒 Secret Message — Click 5 floating hearts or scroll down to unlock!</p>
        <div id="secret-unlocked" style="display:none;">
          <p style="margin:0;font-size:1.2rem;color:#fff;text-shadow:0 0 20px #f9a8d4;animation:glow 1.5s ease-in-out infinite;">You are the most amazing person I've ever met. Every moment with you feels like magic. I love you forever. 💖✨</p>
        </div>
        <div id="scroll-zone" style="max-height:60px;overflow-y:auto;margin-top:0.5rem;">
          <div style="height:80px;"></div>
          <div id="scroll-trigger" style="height:1px;"></div>
        </div>
      </div>
    </div>
    <style>@keyframes glow { 0%,100%{text-shadow:0 0 20px #f9a8d4;} 50%{text-shadow:0 0 30px #fff, 0 0 40px #f9a8d4;} }</style>
    <script>
    (function(){
      var unlocked = false;
      function unlock(){
        if(unlocked) return;
        unlocked = true;
        document.getElementById('secret-locked').style.display = 'none';
        document.getElementById('secret-unlocked').style.display = 'block';
        document.getElementById('secret-card').style.background = 'rgba(236,72,153,0.3)';
        document.getElementById('secret-card').style.border = '2px solid rgba(255,255,255,0.8)';
        document.getElementById('secret-card').style.boxShadow = '0 0 30px rgba(249,168,212,0.8)';
      }
      var heartsDiv = document.getElementById('hearts-float');
      for(var i=0;i<8;i++){
        var h = document.createElement('span');
        h.textContent = '💕';
        h.style.cssText = 'position:absolute;left:'+(10+i*12)+'%;top:'+(10+Math.random()*60)+'px;font-size:'+(18+Math.random()*14)+'px;cursor:pointer;transition:transform 0.2s;';
        h.onmouseover = function(){ this.style.transform = 'scale(1.3)'; };
        h.onmouseout = function(){ this.style.transform = 'scale(1)'; };
        h.onclick = function(){ this.style.opacity = '0.5'; this.style.pointerEvents = 'none'; countClicks(); };
        heartsDiv.appendChild(h);
      }
      var clicks = 0;
      function countClicks(){ clicks++; if(clicks>=5) unlock(); }
      var trigger = document.getElementById('scroll-trigger');
      var obs = new IntersectionObserver(function(entries){ if(entries[0].isIntersecting) unlock(); }, { threshold: 0.5 });
      obs.observe(trigger);
    })();
    </script>
    """
    components.html(SECRET_HTML, height=280)
    st.markdown("---")

    # 4️⃣ Love Meter (0–100%)
    st.markdown("### 💘 4. How Much Do You Love Me?")
    love_val = st.slider("Drag to 100% for a surprise 💕", 0, 100, st.session_state.love_meter_val, key="love_meter")
    st.session_state.love_meter_val = love_val
    if love_val >= 100:
        METER_HTML = """
        <div id="meter-bang" style="padding:1rem;text-align:center;animation:meterShake 0.5s ease;">
          <p style="font-size:1.4rem;font-weight:700;color:#fff;text-shadow:0 0 15px rgba(255,255,255,0.6);">Maximum Love Achieved 💖</p>
          <div id="hearts-explode" style="position:relative;height:70px;"></div>
        </div>
        <style>
          @keyframes meterShake { 0%,100%{transform:translateX(0);} 20%{transform:translateX(-6px);} 40%{transform:translateX(6px);} 60%{transform:translateX(-4px);} 80%{transform:translateX(4px);} }
        </style>
        <script>
        (function(){
          var el = document.getElementById('hearts-explode');
          for(var i=0;i<16;i++){ var a=(i/16)*2*Math.PI; var dx=Math.cos(a)*50; var dy=Math.sin(a)*50;
            var h=document.createElement('span'); h.textContent='💖'; h.style.cssText='position:absolute;left:50%;top:50%;font-size:20px;margin-left:-10px;margin-top:-10px;animation:heartBurst'+i+' 0.9s ease-out forwards;';
            el.appendChild(h);
            var s=document.createElement('style'); s.textContent='@keyframes heartBurst'+i+' { to { transform: translate('+dx+'px,'+dy+'px) scale(0); opacity: 0; } }'; document.head.appendChild(s);
          }
        })();
        </script>
        """
        components.html(METER_HTML, height=110)
    st.markdown("---")

    # Our Memories ❤️ — Polaroid grid (6 images: assets/photo1 through photo6, .jpg / .jpeg / .png)
    ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    POLAROID_CAPTIONS = [
        "Our first moment ❤️",
        "Together forever 💕",
        "You & me 🌹",
        "My favorite smile 😊",
        "Adventure time ✨",
        "Us 💖",
    ]
    polaroid_data = [load_photo_from_assets(ASSETS_DIR, f"photo{i}") for i in range(1, 7)]
    POLAROID_CSS = """
    <style>
    .memories-section {
        background: linear-gradient(180deg, rgba(252,231,243,0.6) 0%, rgba(249,168,212,0.4) 50%, rgba(236,72,153,0.2) 100%);
        margin: 2rem -1rem;
        padding: 2rem 1rem 3rem;
        border-radius: 24px;
        animation: memoriesFadeIn 1s ease-out;
    }
    @keyframes memoriesFadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .memories-heading {
        font-family: 'Pacifico', cursive !important;
        font-size: 1.8rem !important;
        color: #831843 !important;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 10px rgba(255,255,255,0.5);
    }
    .polaroid-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 40px;
        padding: 20px 0 40px;
    }
    .polaroid {
        background: white;
        padding: 15px;
        padding-bottom: 40px;
        width: 220px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        transition: all 0.4s ease;
        text-align: center;
        font-family: cursive;
        animation: float 6s ease-in-out infinite;
    }
    .polaroid img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 6px;
    }
    .polaroid p {
        margin: 12px 0 0;
        font-size: 0.95rem;
        color: #831843;
    }
    .polaroid:hover {
        transform: rotate(var(--rotation)) scale(1.08);
        z-index: 10;
    }
    .polaroid.rotate1 { --rotation: -4deg; }
    .polaroid.rotate2 { --rotation: 3deg; }
    .polaroid.rotate3 { --rotation: -2deg; }
    .polaroid.rotate4 { --rotation: 5deg; }
    .polaroid.rotate5 { --rotation: -3deg; }
    .polaroid.rotate6 { --rotation: 2deg; }
    @keyframes float {
        0% { transform: translateY(0px) rotate(var(--rotation)); }
        50% { transform: translateY(-10px) rotate(var(--rotation)); }
        100% { transform: translateY(0px) rotate(var(--rotation)); }
    }
    .polaroid {
        animation: float 6s ease-in-out infinite;
    }
    @media (max-width: 768px) {
        .polaroid-container { flex-direction: column; align-items: center; gap: 30px; }
        .polaroid { width: 160px; padding-bottom: 32px; }
        .polaroid img { height: 130px; }
    }
    </style>
    """
    polaroid_cards_html = "".join(
        f'<div class="polaroid rotate{i}">'
        f'<img src="data:image/{polaroid_data[i-1][1]};base64,{polaroid_data[i-1][0]}" alt="Memory {i}">'
        f'<p>{POLAROID_CAPTIONS[i-1]}</p></div>'
        for i in range(1, 7)
    )
    st.markdown(
        POLAROID_CSS
        + '<div class="memories-section">'
        + '<p class="memories-heading">Our Beautiful Memories ❤️</p>'
        + '<div class="polaroid-container">'
        + polaroid_cards_html
        + "</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # 5️⃣ Little Things I Love About You ❤️
    LITTLE_THINGS = [
        "The way you smile when you're pretending not to laugh.",
        "How you make ordinary days feel special.",
        "Your dramatic reactions 😌",
        "That look you give when you're right.",
        "The way you exist so perfectly.",
    ]
    LITTLE_THINGS_HTML = """
    <style>
    .little-things-section { margin: 2.5rem 0; padding: 2rem 1rem; animation: littleFadeIn 1s ease-out; }
    @keyframes littleFadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    .little-things-title { font-family: 'Pacifico', cursive !important; font-size: 1.6rem !important; color: #831843 !important; text-align: center; margin-bottom: 1.5rem; text-shadow: 0 0 20px rgba(255,182,193,0.5); }
    .little-things-card { background: rgba(255,255,255,0.2); backdrop-filter: blur(14px); border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 0.75rem; border: 1px solid rgba(255,255,255,0.35); box-shadow: 0 8px 32px rgba(236,72,153,0.15); font-family: 'Dancing Script', cursive; font-size: 1.15rem; color: #5c2d4a; animation: littleFloat 4s ease-in-out infinite; }
    @keyframes littleFloat { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
    .little-things-divider { text-align: center; margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.8; }
    </style>
    <div class="little-things-section">
      <p class="little-things-title">Little Things I Love About You ❤️</p>
      """ + "".join(
        '<div class="little-things-card">' + c + "</div>"
        + ('<div class="little-things-divider">💕</div>' if i < len(LITTLE_THINGS) - 1 else '')
        for i, c in enumerate(LITTLE_THINGS)
    ) + """
    </div>
    """
    st.markdown(LITTLE_THINGS_HTML, unsafe_allow_html=True)
    st.markdown("---")

    if st.button("Continue to our story →", type="primary", use_container_width=True, key="fun_continue"):
        st.session_state.stage = "experience"
        st.rerun()

# ----- JOURNEY -----
elif st.session_state.stage == "journey":
    st.markdown("## The day we met… ✨")
    st.markdown("Everything changed. You walked in and my world got a little brighter.")
    st.markdown('<div class="glass"></div>', unsafe_allow_html=True)

    st.markdown("## Our favorite memories… 🌙")
    st.markdown("Late talks, silly moments, and every second in between. I wouldn't trade them for anything.")
    st.markdown('<div class="glass"></div>', unsafe_allow_html=True)

    st.markdown("## You make my world brighter… ☀️")
    st.markdown("Your smile, your laugh, your presence. You're the best thing that ever happened to me.")
    st.markdown('<div class="glass"></div>', unsafe_allow_html=True)

    st.markdown("## And now… 💖")
    st.markdown("I have one more question for you.")
    if st.button("Continue →", type="primary", use_container_width=True):
        st.session_state.stage = "proposal"
        st.rerun()

# ----- PROPOSAL -----
elif st.session_state.stage == "proposal":
    st.markdown("# Will You Be My Valentine? 💖")
    no_gone = st.session_state.no_clicks >= MAX_NO_CLICKS

    # YES always in first column; NO "runs away" by appearing in random column
    n_cols = 5
    cols = st.columns(n_cols)
    yes_col = 0
    if no_gone:
        no_col = -1
    else:
        no_col = st.session_state.no_column

    for i in range(n_cols):
        with cols[i]:
            if i == yes_col:
                if st.button("YES 😍", type="primary", key="yes_btn", use_container_width=True):
                    st.session_state.said_yes = True
                    st.rerun()
            elif i == no_col and not no_gone:
                if st.button("NO 😢", key="no_btn", use_container_width=True):
                    st.session_state.no_clicks += 1
                    if st.session_state.no_clicks >= MAX_NO_CLICKS:
                        st.rerun()
                    # Move NO to another random column (run away); keep out of column 0 (YES)
                    new_col = random.randint(1, n_cols - 1)
                    while new_col == no_col:
                        new_col = random.randint(1, n_cols - 1)
                    st.session_state.no_column = new_col
                    st.rerun()

    # 1st click -> "Are you sure?", 2nd -> "Think again?", ..., 4th -> "Last chance 👀"
    msg_idx = st.session_state.no_clicks - 1
    if 0 <= msg_idx < len(NO_MESSAGES) and NO_MESSAGES[msg_idx]:
        st.markdown(f"**{NO_MESSAGES[msg_idx]}**")

st.stop()
