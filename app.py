import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NovaMind · AI Research Agent",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #f0eaff;
}

.stApp {
    background: #0a0a12;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(168,85,247,0.16) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(124,58,237,0.12) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 90% 10%, rgba(192,132,252,0.10) 0%, transparent 60%);
    background-attachment: fixed;
    perspective: 1400px;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; position: relative; z-index: 1; }

/* ── Ambient floating 3D orbs ── */
.orb-field {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(2px);
    opacity: 0.55;
    transform-style: preserve-3d;
    animation: orbFloat 14s ease-in-out infinite;
}
.orb-1 {
    width: 140px; height: 140px; top: 8%; left: 6%;
    background: radial-gradient(circle at 35% 30%, #d8b4fe, #7c3aed 70%, transparent 100%);
    animation-duration: 16s;
}
.orb-2 {
    width: 90px; height: 90px; top: 65%; left: 88%;
    background: radial-gradient(circle at 35% 30%, #c084fc, #6d28d9 70%, transparent 100%);
    animation-duration: 12s;
    animation-delay: -4s;
}
.orb-3 {
    width: 60px; height: 60px; top: 20%; left: 92%;
    background: radial-gradient(circle at 35% 30%, #e9d5ff, #a855f7 70%, transparent 100%);
    animation-duration: 10s;
    animation-delay: -2s;
}
.orb-4 {
    width: 110px; height: 110px; top: 82%; left: 15%;
    background: radial-gradient(circle at 35% 30%, #c4b5fd, #7c3aed 70%, transparent 100%);
    animation-duration: 18s;
    animation-delay: -7s;
}
@keyframes orbFloat {
    0%   { transform: translate3d(0,0,0) rotateX(0deg) rotateY(0deg) scale(1); }
    25%  { transform: translate3d(20px,-30px,40px) rotateX(15deg) rotateY(20deg) scale(1.08); }
    50%  { transform: translate3d(-15px,-10px,-30px) rotateX(-10deg) rotateY(-15deg) scale(0.95); }
    75%  { transform: translate3d(-25px,20px,20px) rotateX(10deg) rotateY(-25deg) scale(1.05); }
    100% { transform: translate3d(0,0,0) rotateX(0deg) rotateY(0deg) scale(1); }
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c084fc;
    margin-bottom: 1rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #f4f0ff;
    margin: 0 0 1rem;
    text-shadow: 0 0 40px rgba(168,85,247,0.25);
    animation: heroDrift 8s ease-in-out infinite;
    transform-style: preserve-3d;
}
.hero h1 span {
    color: #a855f7;
    text-shadow: 0 0 30px rgba(168,85,247,0.5);
}
@keyframes heroDrift {
    0%, 100% { transform: translateZ(0) rotateX(0deg); }
    50%      { transform: translateZ(25px) rotateX(2deg); }
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #b8a8d8;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168,85,247,0.35), transparent);
    margin: 2rem 0;
}

/* ── Input card (3D tilt on hover) ── */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(168,85,247,0.18);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(8px);
    transform-style: preserve-3d;
    transition: transform 0.4s ease, box-shadow 0.4s ease, border-color 0.4s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.input-card:hover {
    transform: perspective(900px) rotateX(2deg) rotateY(-2deg) translateZ(10px);
    border-color: rgba(168,85,247,0.35);
    box-shadow: 0 25px 50px rgba(124,58,237,0.25), 0 0 0 1px rgba(168,85,247,0.15) inset;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(168,85,247,0.3) !important;
    border-radius: 10px !important;
    color: #f4f0ff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #a855f7 !important;
    box-shadow: 0 0 0 3px rgba(168,85,247,0.15) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #c084fc !important;
    font-weight: 500 !important;
}

/* ── Button (raised 3D press effect) ── */
.stButton > button {
    background: linear-gradient(135deg, #b866ff 0%, #7c3aed 100%) !important;
    color: #0a0a12 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 6px 0 #5b21b6, 0 10px 24px rgba(168,85,247,0.35) !important;
    width: 100%;
    transform: translateY(0) translateZ(0);
}
.stButton > button:hover {
    transform: translateY(-3px) translateZ(6px) !important;
    box-shadow: 0 9px 0 #5b21b6, 0 18px 32px rgba(168,85,247,0.45) !important;
    opacity: 0.97 !important;
}
.stButton > button:active {
    transform: translateY(3px) translateZ(0) !important;
    box-shadow: 0 2px 0 #5b21b6, 0 4px 12px rgba(168,85,247,0.3) !important;
}

/* ── Pipeline step cards (3D tilt + depth) ── */
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transform-style: preserve-3d;
    transition: transform 0.35s ease, border-color 0.3s, box-shadow 0.35s ease;
}
.step-card:hover {
    transform: perspective(700px) rotateX(3deg) rotateY(-3deg) translateZ(8px);
    box-shadow: 0 18px 34px rgba(124,58,237,0.18);
}
.step-card.active {
    border-color: rgba(168,85,247,0.45);
    background: rgba(168,85,247,0.05);
    animation: pulseGlow 2.2s ease-in-out infinite;
}
.step-card.done {
    border-color: rgba(80,200,120,0.3);
    background: rgba(80,200,120,0.03);
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 0 rgba(168,85,247,0); }
    50%      { box-shadow: 0 0 28px rgba(168,85,247,0.28); }
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: rgba(255,255,255,0.05);
    transition: background 0.3s;
}
.step-card.active::before { background: #a855f7; }
.step-card.done::before   { background: #50c878; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #c084fc;
    opacity: 0.75;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #f4f0ff;
}
.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
}
.status-waiting  { color: #605878; }
.status-running  { color: #c084fc; }
.status-done     { color: #50c878; }

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
    transform-style: preserve-3d;
    transition: transform 0.3s ease;
}
.result-panel:hover {
    transform: translateZ(6px);
}
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c084fc;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(168,85,247,0.18);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: #d8ceec;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
}

/* ── Report & feedback panels (3D lift on hover) ── */
.report-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(168,85,247,0.25);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
    transform-style: preserve-3d;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
    box-shadow: 0 12px 28px rgba(0,0,0,0.3);
}
.report-panel:hover {
    transform: perspective(1000px) rotateX(1deg) translateZ(10px);
    box-shadow: 0 24px 48px rgba(124,58,237,0.2);
}
.feedback-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(80,200,120,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
    transform-style: preserve-3d;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
    box-shadow: 0 12px 28px rgba(0,0,0,0.3);
}
.feedback-panel:hover {
    transform: perspective(1000px) rotateX(1deg) translateZ(10px);
    box-shadow: 0 24px 48px rgba(80,200,120,0.15);
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange {
    color: #c084fc;
    border-bottom: 1px solid rgba(168,85,247,0.18);
}
.panel-label.green {
    color: #50c878;
    border-bottom: 1px solid rgba(80,200,120,0.15);
}

/* ── Progress text ── */
.stSpinner > div { color: #c084fc !important; }

/* ── Expander ── */
details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #b8a8d8 !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f4f0ff;
    margin: 2rem 0 1rem;
}

/* ── Example chips (subtle 3D lift) ── */
.chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 0.25rem 0.7rem;
    font-size: 0.75rem;
    color: #b8a8d8;
    font-family: 'DM Sans', sans-serif;
    display: inline-block;
    transition: transform 0.25s ease, border-color 0.25s ease;
}
.chip:hover {
    transform: translateY(-2px) translateZ(4px);
    border-color: rgba(168,85,247,0.35);
    color: #f0eaff;
}

/* ── Toast-style notice ── */
.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #6a6080;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}
</style>

<div class="orb-field">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
</div>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#8a7fa8;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Nova<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#6a6080;letter-spacing:0.1em;">TRY →</span>
    """, unsafe_allow_html=True)
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f'<span class="chip">{ex}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        # figure out which steps are done
        if step in r:
            return "done"
        # which step is running now (first not in r)
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    NovaMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)