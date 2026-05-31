import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT

load_dotenv()

st.set_page_config(
    page_title="Hannah Wellsy — Career & Wellbeing Coach",
    page_icon="💙",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { font-family: 'Inter', sans-serif; box-sizing: border-box; }

#MainMenu, footer, header { visibility: hidden; }

/* ── Background ── */
.stApp {
    background: #0a0a12;
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed;
    top: -30%;
    left: -20%;
    width: 70%;
    height: 70%;
    background: radial-gradient(ellipse, rgba(99,102,241,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: '';
    position: fixed;
    bottom: -20%;
    right: -10%;
    width: 60%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(236,72,153,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── Container ── */
.main .block-container {
    max-width: 760px;
    padding: 0 1.25rem 2rem;
    position: relative;
    z-index: 1;
}

/* ── Header ── */
.header-wrap {
    padding: 2.2rem 0 1.4rem;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 0.5rem;
}

.avatar-ring {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
    padding: 2px;
    margin-bottom: 14px;
    box-shadow: 0 0 30px rgba(99,102,241,0.35), 0 0 60px rgba(168,85,247,0.15);
}

.avatar-inner {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: #13131f;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
}

.brand-name {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.6px;
    line-height: 1.2;
}

.brand-sub {
    font-size: 13px;
    color: #4b5563;
    margin-top: 5px;
    font-weight: 400;
    letter-spacing: 0.2px;
}

.status-row {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 12px;
    background: rgba(74,222,128,0.08);
    border: 1px solid rgba(74,222,128,0.15);
    border-radius: 20px;
    padding: 5px 12px;
}

.status-dot {
    width: 7px;
    height: 7px;
    background: #4ade80;
    border-radius: 50%;
    animation: pulse 2.2s ease-in-out infinite;
}

.status-label {
    font-size: 11.5px;
    color: #4ade80;
    font-weight: 500;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.45; transform: scale(0.85); }
}

/* ── Chips ── */
.chips-section {
    margin: 1.4rem 0 0.5rem;
}

.chips-label {
    font-size: 11px;
    color: #374151;
    text-align: center;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
}

.chip-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
}

.chip {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 7px 15px;
    font-size: 12.5px;
    color: #6b7280;
    cursor: default;
    transition: all 0.2s ease;
    backdrop-filter: blur(4px);
}

.chip:hover {
    background: rgba(99,102,241,0.12);
    border-color: rgba(99,102,241,0.35);
    color: #a5b4fc;
    transform: translateY(-1px);
}

/* ── Chat messages ── */
.stChatMessage {
    background: transparent !important;
    border: none !important;
    padding: 0.4rem 0 !important;
    margin: 0 !important;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stChatMessageContent {
    background: linear-gradient(135deg, #3730a3, #4f46e5) !important;
    border-radius: 20px 20px 5px 20px !important;
    color: #e0e7ff !important;
    padding: 13px 17px !important;
    max-width: 82% !important;
    margin-left: auto !important;
    box-shadow: 0 4px 20px rgba(79,70,229,0.3), 0 1px 4px rgba(0,0,0,0.3) !important;
    font-size: 14.5px !important;
    line-height: 1.6 !important;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stChatMessageContent {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px 20px 20px 5px !important;
    color: #d1d5db !important;
    padding: 13px 17px !important;
    max-width: 82% !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25) !important;
    font-size: 14.5px !important;
    line-height: 1.7 !important;
    backdrop-filter: blur(8px) !important;
}

/* Avatars */
[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #3730a3, #4f46e5) !important;
    border-radius: 50% !important;
    box-shadow: 0 2px 10px rgba(79,70,229,0.4) !important;
}

[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #6366f1, #a855f7) !important;
    border-radius: 50% !important;
    box-shadow: 0 2px 10px rgba(168,85,247,0.35) !important;
}

/* ── Chat input ── */
.stChatInputContainer {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 18px !important;
    padding: 4px 10px !important;
    backdrop-filter: blur(12px) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

.stChatInputContainer:focus-within {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

textarea {
    color: #e2e8f0 !important;
    background: transparent !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
}

textarea::placeholder {
    color: #374151 !important;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin: 1rem 0;
}

/* ── Info bar ── */
.info-bar {
    display: flex;
    gap: 12px;
    margin: 1.2rem 0;
    justify-content: center;
    flex-wrap: wrap;
}

.info-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 7px 13px;
    font-size: 12px;
    color: #4b5563;
}

.info-pill span.icon {
    font-size: 14px;
}

/* ── Disclaimer ── */
.disclaimer {
    text-align: center;
    font-size: 11px;
    color: #1f2937;
    margin-top: 1.2rem;
    padding: 10px 16px;
    border-top: 1px solid rgba(255,255,255,0.04);
    line-height: 1.6;
}

.disclaimer strong {
    color: #374151;
}

/* ── Spinner ── */
.stSpinner > div {
    border-color: #6366f1 transparent transparent transparent !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1f2937; border-radius: 2px; }

/* ── Misc ── */
p { margin: 0 0 0.5em; }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="header-wrap">
    <div class="avatar-ring">
        <div class="avatar-inner">🌸</div>
    </div>
    <div class="brand-name">Hannah Wellsy</div>
    <div class="brand-sub">Career &amp; Wellbeing Coach · Young Professionals</div>
    <div class="status-row">
        <div class="status-dot"></div>
        <span class="status-label">Online &mdash; here for you</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Init ──
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "Hey, I'm really glad you found your way here. 💙\n\n"
            "I'm Hannah — your career and wellbeing coach. "
            "Whether you're spiraling about a job search, feeling stuck in the wrong path, "
            "dealing with family pressure, or just carrying something heavy that you haven't been able to say out loud — "
            "this is a safe place.\n\n"
            "What's going on with you today?"
        )
    })

# ── Suggestion chips (only on fresh session) ──
if len(st.session_state.messages) == 1:
    st.markdown("""
    <div class="chips-section">
        <div class="chips-label">Where are you right now?</div>
        <div class="chip-grid">
            <div class="chip">😔 Hopeless about my job search</div>
            <div class="chip">🌀 Feeling lost and confused</div>
            <div class="chip">🔥 Completely burnt out</div>
            <div class="chip">😤 Drowning in family pressure</div>
            <div class="chip">📄 Resume never gets shortlisted</div>
            <div class="chip">💸 Financial stress & anxiety</div>
            <div class="chip">🧠 Can't stop overthinking</div>
            <div class="chip">😶 Feeling behind everyone else</div>
        </div>
    </div>
    <div class="info-bar">
        <div class="info-pill"><span class="icon">🔒</span> Private & confidential</div>
        <div class="info-pill"><span class="icon">🇮🇳</span> Built for Indian professionals</div>
        <div class="info-pill"><span class="icon">💬</span> No judgment, ever</div>
    </div>
    <hr class="section-divider">
    """, unsafe_allow_html=True)

# ── Chat history ──
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ── Input & response ──
if prompt := st.chat_input("Tell me what's on your mind..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages]
                ],
                max_tokens=1200,
                temperature=0.75
            )
            assistant_response = response.choices[0].message.content
            st.write(assistant_response)

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# ── Disclaimer ──
st.markdown("""
<div class="disclaimer">
    Hannah is an AI coach &mdash; not a substitute for professional mental health care.<br>
    In a crisis, please call <strong>iCall: 9152987821</strong> &nbsp;|&nbsp; Vandrevala Foundation: <strong>1860-2662-345</strong> (24/7)
</div>
""", unsafe_allow_html=True)
