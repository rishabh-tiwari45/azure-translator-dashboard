import streamlit as st
import requests
import json
import time
import uuid
from datetime import datetime
from collections import Counter

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌐 AI Translator Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 3D Animated CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base & font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Animated gradient background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    background-size: 400% 400%;
    animation: bgShift 12s ease infinite;
}
@keyframes bgShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Floating 3D particle orbs ── */
.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 20% 20%, rgba(120,80,255,0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(0,200,255,0.10) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(255,80,180,0.08) 0%, transparent 60%);
    animation: orbFloat 20s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
@keyframes orbFloat {
    0%,100% { transform: translate(0,0) rotate(0deg); }
    33%     { transform: translate(3%,2%) rotate(120deg); }
    66%     { transform: translate(-2%,3%) rotate(240deg); }
}

/* ── 3D card base ── */
.card-3d {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4),
                0 0 0 1px rgba(255,255,255,0.05) inset,
                0 1px 0 rgba(255,255,255,0.15) inset;
    transform: perspective(1000px) rotateX(0deg);
    transition: all 0.4s cubic-bezier(0.175,0.885,0.32,1.275);
    position: relative;
    overflow: hidden;
}
.card-3d::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: shimmer 3s ease infinite;
}
@keyframes shimmer {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* ── Stat metric cards ── */
.metric-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3),
                0 1px 0 rgba(255,255,255,0.1) inset;
    animation: cardPop 0.6s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
    transform: translateY(20px);
    opacity: 0;
}
.metric-card:nth-child(1) { animation-delay: 0.1s; }
.metric-card:nth-child(2) { animation-delay: 0.2s; }
.metric-card:nth-child(3) { animation-delay: 0.3s; }
.metric-card:nth-child(4) { animation-delay: 0.4s; }
@keyframes cardPop {
    to { transform: translateY(0); opacity: 1; }
}
.metric-number {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 8px 0 4px;
}
.metric-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
}
.metric-icon {
    font-size: 1.6rem;
    margin-bottom: 4px;
}

/* ── Translation result box ── */
.result-box {
    background: linear-gradient(135deg, rgba(167,139,250,0.12), rgba(96,165,250,0.12));
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 16px;
    padding: 24px;
    margin-top: 16px;
    position: relative;
    overflow: hidden;
    animation: slideUp 0.5s cubic-bezier(0.175,0.885,0.32,1.275);
}
.result-box::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(167,139,250,0.05), transparent);
    pointer-events: none;
}
@keyframes slideUp {
    from { opacity:0; transform: translateY(16px) scale(0.98); }
    to   { opacity:1; transform: translateY(0) scale(1); }
}
.result-text {
    font-size: 1.5rem;
    font-weight: 600;
    color: #e2e8f0;
    line-height: 1.5;
    margin: 0;
}
.result-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #a78bfa;
    font-weight: 600;
    margin-bottom: 10px;
}
.detected-lang {
    display: inline-block;
    background: rgba(96,165,250,0.2);
    border: 1px solid rgba(96,165,250,0.4);
    color: #93c5fd;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 3px 12px;
    border-radius: 20px;
    margin-top: 12px;
    text-transform: uppercase;
}

/* ── History item ── */
.history-item {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    transition: all 0.3s ease;
    animation: fadeIn 0.4s ease;
}
@keyframes fadeIn {
    from { opacity:0; transform: translateX(-10px); }
    to   { opacity:1; transform: translateX(0); }
}
.history-langs {
    font-size: 0.68rem;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-bottom: 6px;
}
.history-original { font-size: 0.85rem; color: rgba(255,255,255,0.5); margin-bottom: 3px; }
.history-translated { font-size: 0.9rem; color: #e2e8f0; font-weight: 500; }

/* ── Header ── */
.main-header {
    text-align: center;
    padding: 32px 0 24px;
    animation: headerDrop 0.8s cubic-bezier(0.175,0.885,0.32,1.275);
}
@keyframes headerDrop {
    from { opacity:0; transform: translateY(-30px); }
    to   { opacity:1; transform: translateY(0); }
}
.main-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.main-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.45);
    margin-top: 8px;
    font-weight: 400;
}

/* ── Pulse dot for live status ── */
.status-live {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    color: #34d399;
    font-weight: 600;
    letter-spacing: 1px;
}
.pulse-dot {
    width: 8px; height: 8px;
    background: #34d399;
    border-radius: 50%;
    animation: pulse 1.5s ease infinite;
}
@keyframes pulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(52,211,153,0.6); }
    50%     { box-shadow: 0 0 0 6px rgba(52,211,153,0); }
}

/* ── Streamlit widget overrides ── */
.stTextArea textarea, .stSelectbox select, .stTextInput input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: rgba(167,139,250,0.6) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.5px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,58,237,0.6) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.8) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }

/* ── Section labels ── */
.section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: rgba(255,255,255,0.35);
    font-weight: 600;
    margin-bottom: 10px;
    margin-top: 20px;
}

/* ── Language badge ── */
.lang-badge {
    display: inline-block;
    background: rgba(124,58,237,0.25);
    border: 1px solid rgba(124,58,237,0.5);
    color: #c4b5fd;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    padding: 4px 14px;
    border-radius: 20px;
    text-transform: uppercase;
}
/* hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
for key, val in {
    "history": [],
    "total_chars": 0,
    "total_translations": 0,
    "api_ready": False,
    "az_key": "",
    "az_region": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Language map ──────────────────────────────────────────────────────────────
LANGUAGES = {
    "🔍 Auto-detect": "auto",
    "🇬🇧 English": "en",
    "🇫🇷 French": "fr",
    "🇩🇪 German": "de",
    "🇪🇸 Spanish": "es",
    "🇮🇳 Hindi": "hi",
    "🇮🇳 Tamil": "ta",
    "🇮🇳 Bengali": "bn",
    "🇮🇳 Telugu": "te",
    "🇵🇹 Portuguese": "pt",
    "🇷🇺 Russian": "ru",
    "🇨🇳 Chinese (Simplified)": "zh-Hans",
    "🇯🇵 Japanese": "ja",
    "🇰🇷 Korean": "ko",
    "🇸🇦 Arabic": "ar",
    "🇮🇹 Italian": "it",
    "🇳🇱 Dutch": "nl",
    "🇵🇱 Polish": "pl",
    "🇹🇷 Turkish": "tr",
    "🇸🇪 Swedish": "sv",
    "🇬🇷 Greek": "el",
    "🇮🇱 Hebrew": "he",
    "🇹🇭 Thai": "th",
    "🇻🇳 Vietnamese": "vi",
    "🇿🇦 Afrikaans": "af",
    "🇫🇮 Finnish": "fi",
    "🇩🇰 Danish": "da",
    "🇳🇴 Norwegian": "no",
    "🇺🇦 Ukrainian": "uk",
    "🇨🇿 Czech": "cs",
    "🇷🇴 Romanian": "ro",
    "🇭🇺 Hungarian": "hu",
    "🇮🇩 Indonesian": "id",
    "🇲🇾 Malay": "ms",
}

# ── Azure Translator call ─────────────────────────────────────────────────────
def translate_text(text: str, target_lang: str, source_lang: str, key: str, region: str):
    endpoint = "https://api.cognitive.microsofttranslator.com/translate"
    params = {"api-version": "3.0", "to": target_lang}
    if source_lang != "auto":
        params["from"] = source_lang
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }
    body = [{"text": text}]
    try:
        resp = requests.post(endpoint, params=params, headers=headers, json=body, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        translated = data[0]["translations"][0]["text"]
        detected = data[0].get("detectedLanguage", {}).get("language", source_lang)
        return {"success": True, "translation": translated, "detected": detected}
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response else "?"
        msg = {401: "Invalid API key.", 403: "Access denied — check your key and region.", 429: "Rate limit hit."}.get(code, str(e))
        return {"success": False, "error": f"HTTP {code}: {msg}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Network error — check your internet connection."}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
      <div style='font-size:2.5rem; margin-bottom:6px;'>🌐</div>
      <div style='font-size:1rem; font-weight:700; color:rgba(255,255,255,0.9);'>Translator Pro</div>
      <div style='font-size:0.72rem; color:rgba(255,255,255,0.35); letter-spacing:2px; text-transform:uppercase;'>Azure Powered</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown('<div class="section-label">🔑 API Credentials</div>', unsafe_allow_html=True)
    az_key    = st.text_input("Azure API Key", type="password", placeholder="Paste your key here…", value=st.session_state.az_key)
    az_region = st.text_input("Azure Region", placeholder="e.g. eastus, westeurope…", value=st.session_state.az_region)

    if st.button("✅  Connect API", use_container_width=True):
        if az_key and az_region:
            st.session_state.az_key    = az_key
            st.session_state.az_region = az_region
            st.session_state.api_ready = True
            st.success("Connected successfully!")
        else:
            st.error("Please fill in both fields.")

    if st.session_state.api_ready:
        st.markdown("""
        <div style='margin-top:10px;'>
          <span class='status-live'><span class='pulse-dot'></span>API CONNECTED</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="section-label">ℹ️ How to get credentials</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.78rem; color:rgba(255,255,255,0.45); line-height:1.8;'>
    1. Go to <b>portal.azure.com</b><br>
    2. Create a <b>Translator</b> resource<br>
    3. Copy <b>Key 1</b> and your <b>Region</b><br>
    4. Paste them above and hit Connect
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        st.divider()
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.total_chars = 0
            st.session_state.total_translations = 0
            st.rerun()

# ── Main header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='main-header'>
  <h1 class='main-title'>🌐 AI Translator Dashboard</h1>
  <p class='main-subtitle'>Powered by Azure Cognitive Services · 100+ Languages · Real-time</p>
</div>
""", unsafe_allow_html=True)

# ── Metrics row ───────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
top_pair = "—"
if st.session_state.history:
    pairs = [f"{h['from']} → {h['to']}" for h in st.session_state.history]
    top_pair = Counter(pairs).most_common(1)[0][0]

for col, icon, number, label in [
    (m1, "🔤", st.session_state.total_translations, "Translations"),
    (m2, "📝", f"{st.session_state.total_chars:,}", "Characters"),
    (m3, "🌍", len({h['to'] for h in st.session_state.history}) if st.session_state.history else 0, "Languages Used"),
    (m4, "🔥", top_pair, "Top Pair"),
]:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
          <div class='metric-icon'>{icon}</div>
          <div class='metric-number'>{number}</div>
          <div class='metric-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Translator panel ──────────────────────────────────────────────────────────
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown('<div class="card-3d">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">✍️ Input</div>', unsafe_allow_html=True)

    col_src, col_tgt = st.columns(2)
    with col_src:
        source_name = st.selectbox("From", list(LANGUAGES.keys()), index=0, key="src_lang")
    with col_tgt:
        target_options = [k for k in LANGUAGES if k != "🔍 Auto-detect"]
        target_name    = st.selectbox("To", target_options, index=0, key="tgt_lang")

    input_text = st.text_area(
        "Text to translate",
        height=180,
        placeholder="Type or paste your text here…",
        label_visibility="collapsed",
    )
    char_count = len(input_text)
    st.markdown(f'<div style="font-size:0.72rem;color:rgba(255,255,255,0.3);text-align:right;margin-top:-8px;">{char_count} characters</div>', unsafe_allow_html=True)

    translate_btn = st.button("🚀  Translate Now", use_container_width=True, disabled=not st.session_state.api_ready)

    if not st.session_state.api_ready:
        st.markdown('<div style="font-size:0.78rem;color:rgba(255,165,0,0.7);margin-top:8px;">⚠️ Connect your API key in the sidebar first.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card-3d">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">💬 Translation Output</div>', unsafe_allow_html=True)

    if translate_btn:
        if not input_text.strip():
            st.warning("Please enter some text to translate.")
        else:
            src_code = LANGUAGES[source_name]
            tgt_code = LANGUAGES[target_name]
            with st.spinner("Translating…"):
                result = translate_text(
                    input_text, tgt_code, src_code,
                    st.session_state.az_key, st.session_state.az_region
                )
            if result["success"]:
                detected = result["detected"]
                translation = result["translation"]

                st.markdown(f"""
                <div class='result-box'>
                  <div class='result-label'>Translated Text</div>
                  <p class='result-text'>{translation}</p>
                  <span class='detected-lang'>Detected: {detected.upper()}</span>
                </div>
                """, unsafe_allow_html=True)

                # Copy helper
                st.code(translation, language=None)

                # Save to history
                st.session_state.history.insert(0, {
                    "time": datetime.now().strftime("%H:%M"),
                    "from": detected.upper(),
                    "to": tgt_code.upper(),
                    "original": input_text[:60] + ("…" if len(input_text) > 60 else ""),
                    "translated": translation[:80] + ("…" if len(translation) > 80 else ""),
                })
                st.session_state.total_translations += 1
                st.session_state.total_chars += len(input_text)
                st.rerun()
            else:
                st.error(f"❌ {result['error']}")
    else:
        st.markdown("""
        <div style='display:flex; flex-direction:column; align-items:center; justify-content:center;
                    min-height:220px; text-align:center;'>
          <div style='font-size:3rem; margin-bottom:12px; opacity:0.4;'>🌍</div>
          <div style='color:rgba(255,255,255,0.3); font-size:0.85rem; max-width:200px; line-height:1.7;'>
            Your translated text will appear here
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Translation History ───────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">📜 Translation History</div>', unsafe_allow_html=True)

if not st.session_state.history:
    st.markdown("""
    <div style='text-align:center; padding:40px; color:rgba(255,255,255,0.2); font-size:0.9rem;'>
      No translations yet — start translating above!
    </div>
    """, unsafe_allow_html=True)
else:
    cols = st.columns(2)
    for i, item in enumerate(st.session_state.history[:10]):
        with cols[i % 2]:
            st.markdown(f"""
            <div class='history-item'>
              <div class='history-langs'>{item['time']}  ·  {item['from']} → {item['to']}</div>
              <div class='history-original'>"{item['original']}"</div>
              <div class='history-translated'>↳ {item['translated']}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:30px 0 10px; color:rgba(255,255,255,0.18); font-size:0.72rem; letter-spacing:1.5px;'>
  TRANSLATOR DASHBOARD  ·  AZURE COGNITIVE SERVICES  ·  BUILT WITH STREAMLIT
</div>
""", unsafe_allow_html=True)