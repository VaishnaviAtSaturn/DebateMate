import os
import streamlit as st
from dotenv import load_dotenv

from topics import get_all_topics, get_random_topic
from scorer import score_argument
from report import generate_report
from ai_opponent import DebateOpponent

# ─────────────────────────────────────────────
#  Load environment variables
# ─────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────
#  Page config (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DebateMate — AI Debate Coach",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  Comprehensive CSS — Neo-Brutalist + fixed
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;900&family=IBM+Plex+Mono:wght@400;700&display=swap');

/* ── Reset & base ─────────────────────────── */
*, *::before, *::after {
    font-family: 'Space Grotesk', sans-serif !important;
    box-sizing: border-box !important;
}

.stApp {
    background-color: #FFFBE6 !important;
}

/* Remove Streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
    padding-top: 2rem !important;
    max-width: 860px !important;
}

/* ── Typography ───────────────────────────── */
h1 {
    font-size: 72px !important;
    font-weight: 900 !important;
    letter-spacing: -3px !important;
    color: #000 !important;
    line-height: 1 !important;
    margin-bottom: 4px !important;
}
h2 {
    font-size: 22px !important;
    font-weight: 900 !important;
    color: #000 !important;
    border-bottom: 4px solid #000 !important;
    padding-bottom: 6px !important;
    margin-top: 28px !important;
    letter-spacing: 1px !important;
}
h3 {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #000 !important;
}
p, li, span, label, div {
    color: #000 !important;
}

/* ── Buttons ──────────────────────────────── */
.stButton > button {
    background-color: #FFD600 !important;
    color: #000 !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    box-shadow: 4px 4px 0px #000 !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    padding: 10px 22px !important;
    transition: all 0.08s ease !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
}
.stButton > button:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px #000 !important;
    background-color: #FFE033 !important;
}
.stButton > button:active {
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0px #000 !important;
}

/* ── Text inputs ──────────────────────────── */
.stTextInput > div > div > input {
    background-color: #fff !important;
    color: #000 !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    box-shadow: 3px 3px 0px #000 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input::placeholder {
    color: #888 !important;
}
.stTextInput > div > div > input:focus {
    outline: none !important;
    border-color: #000 !important;
    box-shadow: 5px 5px 0px #000 !important;
}
.stTextInput label {
    font-weight: 700 !important;
    font-size: 14px !important;
    color: #000 !important;
}

/* ── Textarea ──────────────────────────────── */
.stTextArea > div > div > textarea {
    background-color: #fff !important;
    color: #000 !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    box-shadow: 3px 3px 0px #000 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px !important;
    padding: 12px 14px !important;
    resize: vertical !important;
}
.stTextArea > div > div > textarea::placeholder {
    color: #888 !important;
}
.stTextArea label {
    font-weight: 700 !important;
    color: #000 !important;
}

/* ── Selectbox — force white bg + black text ── */
.stSelectbox > label {
    font-weight: 700 !important;
    font-size: 14px !important;
    color: #000 !important;
}

/* Outer wrapper */
.stSelectbox > div > div,
.stSelectbox > div > div > div {
    background-color: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    box-shadow: 3px 3px 0px #000 !important;
    color: #000 !important;
}

/* Every BaseWeb select layer */
[data-baseweb="select"],
[data-baseweb="select"] > div,
[data-baseweb="select"] > div > div,
[data-baseweb="select"] > div > div > div {
    background-color: #fff !important;
    background: #fff !important;
    color: #000 !important;
    border-radius: 0 !important;
}

/* The actual displayed value text */
[data-baseweb="select"] span {
    color: #000 !important;
    background-color: transparent !important;
}

/* Every div/span/input inside select */
[data-baseweb="select"] div,
[data-baseweb="select"] input,
[data-baseweb="select"] * {
    background-color: #fff !important;
    color: #000 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px !important;
    border-radius: 0 !important;
}

/* Arrow SVG */
[data-baseweb="select"] svg,
[data-baseweb="select"] svg path {
    fill: #000 !important;
    color: #000 !important;
}

/* Dropdown popover panel */
[data-baseweb="popover"],
[data-baseweb="popover"] > div {
    background-color: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    box-shadow: 6px 6px 0px #000 !important;
}

/* Menu list */
[data-baseweb="menu"],
[data-baseweb="menu"] > ul,
[data-baseweb="menu"] > div {
    background-color: #fff !important;
    border-radius: 0 !important;
}

/* Individual menu items */
[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"] {
    background-color: #fff !important;
    color: #000 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    border-radius: 0 !important;
}
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] [aria-selected="true"] {
    background-color: #FFD600 !important;
    color: #000 !important;
}

/* ── Form submit button ────────────────────── */
.stFormSubmitButton > button {
    background-color: #FFD600 !important;
    color: #000 !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    box-shadow: 4px 4px 0px #000 !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    padding: 10px 22px !important;
    width: 100% !important;
    transition: all 0.08s ease !important;
}
.stFormSubmitButton > button:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px #000 !important;
}

/* ── Download button ───────────────────────── */
.stDownloadButton > button {
    background-color: #000 !important;
    color: #FFD600 !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    box-shadow: 4px 4px 0px #555 !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    padding: 12px 22px !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background-color: #222 !important;
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0px #555 !important;
}

/* ── Progress bar ──────────────────────────── */
.stProgress > div > div > div > div {
    background-color: #000 !important;
    border-radius: 0 !important;
}
.stProgress > div > div {
    background-color: #ddd !important;
    border-radius: 0 !important;
    border: 2px solid #000 !important;
}

/* ── Horizontal divider ─────────────────────── */
hr {
    border: 2px solid #000 !important;
    margin: 20px 0 !important;
}

/* ── Alert / error messages ─────────────────── */
.stAlert {
    border-radius: 0 !important;
    border: 3px solid #000 !important;
    box-shadow: 4px 4px 0px #000 !important;
}

/* ── Spinner text ───────────────────────────── */
.stSpinner > div {
    color: #000 !important;
    font-weight: 700 !important;
}

/* ── Custom card components ─────────────────── */
.dm-card {
    background: #fff;
    border: 3px solid #000;
    box-shadow: 5px 5px 0px #000;
    padding: 18px 22px;
    margin: 10px 0;
}
.dm-green-card {
    background: #3BFF6E;
    border: 3px solid #000;
    box-shadow: 5px 5px 0px #000;
    padding: 18px 22px;
    margin: 10px 0;
    color: #000 !important;
    font-weight: 600;
    font-size: 15px;
}
.dm-red-card {
    background: #FF3F3F;
    border: 3px solid #000;
    box-shadow: 5px 5px 0px #000;
    padding: 18px 22px;
    margin: 10px 0;
    color: #fff !important;
    font-weight: 600;
    font-size: 15px;
}
.dm-yellow-card {
    background: #FFD600;
    border: 3px solid #000;
    box-shadow: 5px 5px 0px #000;
    padding: 18px 22px;
    margin: 10px 0;
    color: #000 !important;
    font-weight: 700;
    font-size: 16px;
}
.dm-black-card {
    background: #000;
    border: 3px solid #000;
    box-shadow: 5px 5px 0px #555;
    padding: 12px 22px;
    margin: 10px 0;
    color: #FFD600 !important;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 1px;
}

/* ── Chat bubbles ───────────────────────────── */
.user-bubble {
    background: #3BFF6E;
    border: 2px solid #000;
    border-left: 7px solid #000;
    box-shadow: 4px 4px 0px #000;
    padding: 14px 18px;
    margin: 10px 0 4px 0;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px;
    color: #000 !important;
    line-height: 1.5;
}
.ai-bubble {
    background: #FF3F3F;
    border: 2px solid #000;
    border-left: 7px solid #000;
    box-shadow: 4px 4px 0px #000;
    padding: 14px 18px;
    margin: 10px 0 16px 0;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px;
    color: #fff !important;
    line-height: 1.5;
}
.score-badge {
    background: #FFD600;
    border: 2px solid #000;
    padding: 4px 14px;
    font-weight: 800;
    font-size: 12px;
    display: inline-block;
    margin-bottom: 8px;
    font-family: 'IBM Plex Mono', monospace !important;
    color: #000 !important;
    letter-spacing: 0.5px;
}

/* ── Topic bar ──────────────────────────────── */
.topic-bar {
    background: #000;
    color: #FFD600 !important;
    padding: 12px 22px;
    font-weight: 800;
    font-size: 15px;
    margin-bottom: 20px;
    letter-spacing: 0.5px;
    border: 3px solid #000;
    box-shadow: 4px 4px 0px #555;
}

/* ── Big score display ──────────────────────── */
.big-score-wrap {
    text-align: center;
    padding: 30px;
    background: #000;
    border: 3px solid #000;
    box-shadow: 6px 6px 0px #555;
    margin: 16px 0;
}
.big-score-num {
    font-size: 100px;
    font-weight: 900;
    line-height: 1;
    display: block;
}
.big-score-label {
    font-size: 22px;
    font-weight: 700;
    color: #FFD600 !important;
    letter-spacing: 2px;
}

/* ── Stance / Difficulty pill ───────────────── */
.stance-pill {
    display: inline-block;
    padding: 8px 20px;
    font-weight: 900;
    font-size: 16px;
    border: 3px solid #000;
    box-shadow: 4px 4px 0px #000;
    margin-top: 10px;
    letter-spacing: 1px;
}

/* ── Tagline ─────────────────────────────────── */
.tagline {
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #000 !important;
    margin-top: -8px;
    margin-bottom: 24px;
    text-transform: uppercase;
}

/* ── Section label ───────────────────────────── */
.section-num {
    display: inline-block;
    background: #000;
    color: #FFD600 !important;
    font-weight: 900;
    font-size: 13px;
    padding: 2px 10px;
    margin-right: 8px;
    vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Session State Initialisation
# ─────────────────────────────────────────────
if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "stance" not in st.session_state:
    st.session_state.stance = "FOR"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "INTERMEDIATE"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "scores" not in st.session_state:
    st.session_state.scores = []
if "arguments" not in st.session_state:
    st.session_state.arguments = []
if "round" not in st.session_state:
    st.session_state.round = 1
if "opponent" not in st.session_state:
    st.session_state.opponent = None
if "ai_counters" not in st.session_state:
    st.session_state.ai_counters = []


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def reset_all_state():
    st.session_state.screen = "home"
    st.session_state.topic = ""
    st.session_state.stance = "FOR"
    st.session_state.difficulty = "INTERMEDIATE"
    st.session_state.chat_history = []
    st.session_state.scores = []
    st.session_state.arguments = []
    st.session_state.round = 1
    st.session_state.opponent = None
    st.session_state.ai_counters = []


def build_transcript(report: dict) -> str:
    lines = [
        "================================",
        "DEBATEMATE SESSION TRANSCRIPT",
        "================================",
        f"Topic: {st.session_state.topic}",
        f"Your Stance: {st.session_state.stance}",
        f"Difficulty: {st.session_state.difficulty}",
        f"Total Rounds: {st.session_state.round - 1}",
        "================================\n",
    ]
    for i, (arg, score, ai_resp) in enumerate(
        zip(st.session_state.arguments, st.session_state.scores, st.session_state.ai_counters),
        start=1,
    ):
        lines += [
            f"ROUND {i}",
            f"YOU: {arg}",
            f"SCORE: Clarity {score['clarity']}/10 | Relevance {score['relevance']}/10 | Logic {score['logic']}/10",
            f"AI: {ai_resp}",
            "--------------------------------\n",
        ]
    lines += [
        "================================",
        "FINAL REPORT",
        "================================",
        f"Overall Score: {report['overall_score']}/100",
        f"Clarity: {report['avg_clarity']}/10",
        f"Relevance: {report['avg_relevance']}/10",
        f"Logic: {report['avg_logic']}/10\n",
        f"Best Argument: {report['best_argument']}",
        f"Worst Argument: {report['worst_argument']}",
        f"AI Verdict: {report['ai_verdict']}",
        f"Your Tip: {report['tip']}",
        "================================",
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  SCREEN 1 — HOME
# ═══════════════════════════════════════════════════════════════
if st.session_state.screen == "home":

    # Title
    st.markdown("<h1>DEBATE<br>MATE</h1>", unsafe_allow_html=True)
    st.markdown('<p class="tagline">⚡ argue better &nbsp;·&nbsp; think sharper</p>', unsafe_allow_html=True)

    # API key warning
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key.strip() == "your_key_here":
        st.error("⚠️  GROQ_API_KEY not set. Open .env and paste your free key from console.groq.com")

    st.markdown("---")

    # ── SECTION 1: Topic ──────────────────────────────────────
    st.markdown("## 🎯 PICK YOUR TOPIC")

    all_topics = get_all_topics()

    # Pre-select from random if set
    default_idx = 0
    if st.session_state.topic in all_topics:
        default_idx = all_topics.index(st.session_state.topic) + 1

    topic_option = st.selectbox(
        "Choose from 60+ debate topics:",
        options=["— select a topic —"] + all_topics,
        index=default_idx,
        key="topic_select",
    )

    st.markdown("<p style='text-align:center; font-weight:700; font-size:13px; color:#888; margin:4px 0;'>— OR —</p>", unsafe_allow_html=True)

    custom_topic = st.text_input(
        "Write your own topic:",
        placeholder="e.g. Social media does more harm than good",
        key="custom_topic_input",
        value="",
    )

    # Random button
    if st.button("🎲 Surprise Me — Random Topic", key="random_btn"):
        st.session_state.topic = get_random_topic()
        st.rerun()

    # Resolve active topic
    if custom_topic.strip():
        active_topic = custom_topic.strip()
    elif topic_option and topic_option != "— select a topic —":
        active_topic = topic_option
    elif st.session_state.topic:
        active_topic = st.session_state.topic
    else:
        active_topic = ""

    if active_topic:
        st.markdown(
            f'<div class="dm-card"><b>📌 Selected Topic:</b><br><span style="font-size:16px; font-weight:600;">{active_topic}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── SECTION 2: Stance ─────────────────────────────────────
    st.markdown("## ⚔️ YOUR STANCE")
    st.markdown("<p style='font-size:14px; color:#444; margin-bottom:12px;'>Are you arguing FOR or AGAINST this topic?</p>", unsafe_allow_html=True)

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        if st.button("👍  I'M FOR IT", key="for_btn"):
            st.session_state.stance = "FOR"
            st.rerun()
    with s_col2:
        if st.button("👎  I'M AGAINST IT", key="against_btn"):
            st.session_state.stance = "AGAINST"
            st.rerun()

    if st.session_state.stance == "FOR":
        pill_bg, pill_fg = "#3BFF6E", "#000"
    else:
        pill_bg, pill_fg = "#FF3F3F", "#fff"

    st.markdown(
        f'<div class="stance-pill" style="background:{pill_bg}; color:{pill_fg};">'
        f'You are arguing <b>{st.session_state.stance}</b> this topic</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── SECTION 3: Difficulty ─────────────────────────────────
    st.markdown("## 🔥 DIFFICULTY LEVEL")
    st.markdown("<p style='font-size:14px; color:#444; margin-bottom:12px;'>Choose how hard you want the AI to push back.</p>", unsafe_allow_html=True)

    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        if st.button("🟢  BEGINNER", key="beginner_btn"):
            st.session_state.difficulty = "BEGINNER"
            st.rerun()
    with d_col2:
        if st.button("🟡  INTERMEDIATE", key="intermediate_btn"):
            st.session_state.difficulty = "INTERMEDIATE"
            st.rerun()
    with d_col3:
        if st.button("🔴  EXPERT", key="expert_btn"):
            st.session_state.difficulty = "EXPERT"
            st.rerun()

    diff_style = {
        "BEGINNER":     ("#3BFF6E", "#000", "Gentle coaching, simple counters."),
        "INTERMEDIATE": ("#FFD600", "#000", "Logical, direct, fact-based opposition."),
        "EXPERT":       ("#FF3F3F", "#fff", "Brutal, data-driven, no mercy."),
    }
    dbg, dfg, ddesc = diff_style[st.session_state.difficulty]
    st.markdown(
        f'<div class="stance-pill" style="background:{dbg}; color:{dfg};">'
        f'<b>{st.session_state.difficulty}</b> — {ddesc}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── START BUTTON ──────────────────────────────────────────
    st.markdown("## 🚀 READY TO ARGUE?")
    if st.button("START DEBATE  →", key="start_btn"):
        if not active_topic:
            st.error("Select or type a topic first.")
        elif not api_key or api_key.strip() == "your_key_here":
            st.error("Add your GROQ_API_KEY to the .env file.")
        else:
            with st.spinner("⚙️  Initialising your AI opponent..."):
                try:
                    opponent = DebateOpponent(
                        topic=active_topic,
                        user_stance=st.session_state.stance,
                        difficulty=st.session_state.difficulty,
                    )
                    st.session_state.opponent = opponent
                    st.session_state.topic = active_topic
                    st.session_state.screen = "debate"
                    st.rerun()
                except ValueError as ve:
                    st.error(str(ve))
                except Exception as e:
                    st.error(f"Failed to start: {e}")


# ═══════════════════════════════════════════════════════════════
#  SCREEN 2 — DEBATE ARENA
# ═══════════════════════════════════════════════════════════════
elif st.session_state.screen == "debate":

    ai_stance = "AGAINST" if st.session_state.stance == "FOR" else "FOR"
    rounds_done = st.session_state.round - 1

    # Topic bar
    st.markdown(
        f'<div class="topic-bar">'
        f'🗣️ &nbsp;<b>{st.session_state.topic}</b>'
        f'&nbsp;&nbsp;|&nbsp;&nbsp;'
        f'Round <b>{st.session_state.round}</b>/10'
        f'&nbsp;&nbsp;|&nbsp;&nbsp;'
        f'You: <b>{st.session_state.stance}</b>'
        f'&nbsp;&nbsp;|&nbsp;&nbsp;'
        f'AI: <b>{ai_stance}</b>'
        f'&nbsp;&nbsp;|&nbsp;&nbsp;'
        f'<b>{st.session_state.difficulty}</b>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Chat history
    if not st.session_state.chat_history:
        st.markdown(
            '<div class="dm-card" style="text-align:center; padding:30px;">'
            '<span style="font-size:40px;">🎤</span><br>'
            '<b style="font-size:18px;">State your opening argument below!</b><br>'
            '<span style="font-size:14px; color:#444;">Be clear, logical and confident.</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        for entry in st.session_state.chat_history:
            if entry["role"] == "user":
                score = entry.get("score", {})
                st.markdown(
                    f'<div class="user-bubble"><b>YOU:</b> {entry["text"]}</div>'
                    f'<span class="score-badge">'
                    f'Clarity {score.get("clarity",0)}/10 &nbsp;·&nbsp; '
                    f'Relevance {score.get("relevance",0)}/10 &nbsp;·&nbsp; '
                    f'Logic {score.get("logic",0)}/10 &nbsp;·&nbsp; '
                    f'Overall {score.get("overall",0)}/10'
                    f'</span>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="ai-bubble"><b>🤖 AI:</b> {entry["text"]}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # Input form
    with st.form(key="argue_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your argument:",
            placeholder="Make your point clearly. Use evidence, logic, examples.",
            height=130,
        )
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            argue_clicked = st.form_submit_button("⚔️  ARGUE")
        with f_col2:
            end_clicked = st.form_submit_button("🏁  END DEBATE")

    # End debate
    if end_clicked:
        if not st.session_state.scores:
            st.error("Make at least one argument before ending.")
        else:
            st.session_state.screen = "report"
            st.rerun()

    # Process argument
    if argue_clicked:
        raw = (user_input or "").strip()
        if not raw:
            st.error("Type your argument before clicking ARGUE.")
        else:
            with st.spinner("⚡ Scoring your argument..."):
                try:
                    score = score_argument(raw)
                except Exception as e:
                    st.error(f"Scoring error: {e}")
                    score = {"clarity": 5.0, "relevance": 5.0, "logic": 5.0, "overall": 5.0}

            st.session_state.scores.append(score)
            st.session_state.arguments.append(raw)

            with st.spinner("🤖 AI is thinking..."):
                try:
                    counter = st.session_state.opponent.get_counter(raw)
                except Exception as e:
                    counter = f"Error: {e}"

            st.session_state.ai_counters.append(counter)
            st.session_state.chat_history.append({"role": "user", "text": raw, "score": score})
            st.session_state.chat_history.append({"role": "ai", "text": counter})
            st.session_state.round += 1

            if st.session_state.round > 10:
                st.session_state.screen = "report"
            st.rerun()


# ═══════════════════════════════════════════════════════════════
#  SCREEN 3 — REPORT
# ═══════════════════════════════════════════════════════════════
elif st.session_state.screen == "report":

    report = generate_report(
        scores_list=st.session_state.scores,
        arguments_list=st.session_state.arguments,
        topic=st.session_state.topic,
    )

    st.markdown("<h1>DEBATE<br>REPORT</h1>", unsafe_allow_html=True)
    st.markdown(
        f'<p style="font-size:15px; font-weight:600; color:#444;">📋 {st.session_state.topic}</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Overall score ──────────────────────────────────────────
    score_val = report["overall_score"]
    if score_val > 75:
        score_color = "#3BFF6E"
        score_label_color = "#000"
    elif score_val >= 50:
        score_color = "#FFD600"
        score_label_color = "#000"
    else:
        score_color = "#FF3F3F"
        score_label_color = "#fff"

    st.markdown(
        f'<div class="big-score-wrap">'
        f'<span class="big-score-num" style="color:{score_color};">{score_val}</span>'
        f'<span class="big-score-label">/ 100</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Metrics ────────────────────────────────────────────────
    st.markdown("## 📊 ARGUMENT METRICS")

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(
            f'<div class="dm-card" style="text-align:center;">'
            f'<div style="font-size:13px; font-weight:700; letter-spacing:1px; margin-bottom:4px;">CLARITY</div>'
            f'<div style="font-size:48px; font-weight:900; line-height:1;">{report["avg_clarity"]}</div>'
            f'<div style="font-size:13px; color:#666;">/ 10</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.progress(int(report["avg_clarity"] * 10))

    with m_col2:
        st.markdown(
            f'<div class="dm-card" style="text-align:center;">'
            f'<div style="font-size:13px; font-weight:700; letter-spacing:1px; margin-bottom:4px;">RELEVANCE</div>'
            f'<div style="font-size:48px; font-weight:900; line-height:1;">{report["avg_relevance"]}</div>'
            f'<div style="font-size:13px; color:#666;">/ 10</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.progress(int(report["avg_relevance"] * 10))

    with m_col3:
        st.markdown(
            f'<div class="dm-card" style="text-align:center;">'
            f'<div style="font-size:13px; font-weight:700; letter-spacing:1px; margin-bottom:4px;">LOGIC</div>'
            f'<div style="font-size:48px; font-weight:900; line-height:1;">{report["avg_logic"]}</div>'
            f'<div style="font-size:13px; color:#666;">/ 10</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.progress(int(report["avg_logic"] * 10))

    st.markdown("---")

    # ── Best / Worst ───────────────────────────────────────────
    st.markdown("## 💬 YOUR ARGUMENTS")

    st.markdown("**✅ Best Argument:**")
    st.markdown(
        f'<div class="dm-green-card">"{report["best_argument"]}"</div>',
        unsafe_allow_html=True,
    )

    st.markdown("**❌ Worst Argument:**")
    st.markdown(
        f'<div class="dm-red-card">"{report["worst_argument"]}"</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Verdict ────────────────────────────────────────────────
    st.markdown("## 🤖 AI VERDICT")
    st.markdown(
        f'<div class="dm-yellow-card">💬 &nbsp;{report["ai_verdict"]}</div>',
        unsafe_allow_html=True,
    )

    # ── Tip ────────────────────────────────────────────────────
    st.markdown("## 💡 YOUR COACHING TIP")
    st.markdown(
        f'<div class="dm-card" style="border-left: 7px solid #FFD600;">💡 &nbsp;<b>{report["tip"]}</b></div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Download / Reset ───────────────────────────────────────
    dl_col, reset_col = st.columns(2)
    with dl_col:
        transcript = build_transcript(report)
        st.download_button(
            label="📥  DOWNLOAD TRANSCRIPT",
            data=transcript,
            file_name="debatemate_transcript.txt",
            mime="text/plain",
            key="download_btn",
        )
    with reset_col:
        if st.button("🔄  DEBATE AGAIN", key="debate_again_btn"):
            reset_all_state()
            st.rerun()
