import os
import re
import json
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="GhostBug AI | Prerequisite Gap Diagnostic Engine",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# CUSTOM CSS & CLASSROOM WHITEBOARD STYLING
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Inter:wght@400;500;600;700&family=Architects+Daughter&family=Fira+Code:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main App Header */
    .app-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        border-radius: 16px;
        padding: 24px 30px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .app-title {
        font-family: 'Fredoka', cursive;
        font-size: 2.3rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .app-subtitle {
        font-size: 1.05rem;
        color: #C7D2FE;
        margin-top: 6px;
        margin-bottom: 14px;
    }
    .badge-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .tech-badge {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    /* GeoGebra Problem Card */
    .geogebra-card {
        background: #F8FAFC;
        border: 2px solid #E2E8F0;
        border-left: 6px solid #4F46E5;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 20px;
    }
    .geogebra-badge {
        display: inline-block;
        background: #EEF2FF;
        color: #4F46E5;
        font-weight: 700;
        font-size: 0.78rem;
        padding: 3px 10px;
        border-radius: 6px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Red Ghost Alert Card */
    .ghost-alert-box {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border: 2px solid #EF4444;
        border-radius: 14px;
        padding: 18px 22px;
        margin-top: 18px;
        margin-bottom: 18px;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.15);
        animation: pulseAlert 2.5s infinite;
    }
    @keyframes pulseAlert {
        0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        50% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
    }
    .ghost-alert-title {
        color: #B91C1C;
        font-size: 1.15rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }

    /* Leo's Classroom Chat */
    .leo-card {
        background: #FFFBEB;
        border: 2px solid #F59E0B;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 18px;
        position: relative;
    }
    .leo-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
        font-weight: 700;
        color: #92400E;
    }
    .leo-avatar {
        font-size: 1.6rem;
        background: #FDE68A;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        border: 2px solid #F59E0B;
    }
    .leo-speech {
        background: white;
        border: 1px solid #FCD34D;
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 0.95rem;
        color: #78350F;
        line-height: 1.5;
    }

    /* Green Ghost Gap Healed Alert */
    .healed-alert-box {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 2px solid #10B981;
        border-radius: 14px;
        padding: 18px 22px;
        margin-top: 16px;
        margin-bottom: 16px;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.2);
    }
    .healed-alert-title {
        color: #065F46;
        font-size: 1.2rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    /* Right Panel Whiteboard Container */
    .whiteboard-container {
        background-color: #FAFAFA;
        background-image: 
            linear-gradient(#E2E8F0 1.2px, transparent 1.2px),
            linear-gradient(90deg, #E2E8F0 1.2px, transparent 1.2px);
        background-size: 24px 24px;
        border: 3px solid #CBD5E1;
        border-radius: 16px;
        padding: 24px;
        min-height: 680px;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.04), 0 8px 20px rgba(0,0,0,0.06);
    }
    .whiteboard-header {
        font-family: 'Architects Daughter', cursive;
        font-size: 1.6rem;
        color: #334155;
        border-bottom: 2px dashed #94A3B8;
        padding-bottom: 10px;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Whiteboard reveal cards */
    .wb-step-card {
        background: white;
        border: 2px solid #3B82F6;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.1);
        font-family: 'Fira Code', monospace;
    }
    .wb-step-card.wb2 {
        border-color: #10B981;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.1);
    }

    /* Voice Wave Simulation */
    .voice-pulse {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 14px;
        background: #EEF2FF;
        border: 1px solid #6366F1;
        border-radius: 20px;
        margin-bottom: 12px;
    }
    .wave-bar {
        width: 4px;
        height: 18px;
        background: #6366F1;
        border-radius: 2px;
        animation: soundWave 1.2s infinite ease-in-out;
    }
    .wave-bar:nth-child(2) { animation-delay: 0.2s; height: 26px; }
    .wave-bar:nth-child(3) { animation-delay: 0.4s; height: 14px; }
    .wave-bar:nth-child(4) { animation-delay: 0.1s; height: 22px; }
    .wave-bar:nth-child(5) { animation-delay: 0.3s; height: 16px; }
    @keyframes soundWave {
        0%, 100% { transform: scaleY(0.4); }
        50% { transform: scaleY(1); }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# AGENT SKILLS LOADER & GEMINI INTEGRATION
# ==========================================
SKILLS_DIR = os.path.join(os.path.dirname(__file__), "skills")

@st.cache_data
def load_skill(filename: str) -> str:
    filepath = os.path.join(SKILLS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return f"Skill file {filename} not found."

ghost_mapper_skill = load_skill("ghost_mapper.md")
deliberate_bug_leo_skill = load_skill("deliberate_bug_leo.md")

# ==========================================
# CURRICULUM PROBLEMS DATABASE
# ==========================================
CURRICULUM_PROBLEMS = {
    "Q.01": {
        "id": "Q.01",
        "title": "Q.01 (Plane Cargo Capacity)",
        "question": "The available capacity of the cargo area in a commercial plane is 1,300 lb. If 1/2 ton of the cargo is loaded, how much more can be added?",
        "default_working": "1/2 ton = 500 lb, so 1300 - 500 = 800 lb",
        "default_answer": "800 lb",
        "correct_answer": "300 lb",
        "wb1": "1 ton = 2,000 lb ⟹ 1/2 ton = 1,000 lb",
        "wb2": "1,300 lb - 1,000 lb = 300 lb more can be added",
        "leo_bug_prompt": "Wait, I did the exact same thing! In my problem with the small passenger cargo pod, we had 1/4 ton of cargo. I reasoned: if 1/2 ton is 500 lb, then 1/4 ton must be 250 lb! But ground control flagged our flight plan. Can you teach me what the real rule is for converting tons to pounds?",
        "leo_healed_reaction": "AHA!! 💡 1 US Ton is 2,000 pounds, NOT 1,000! So 1/2 ton is 1,000 lb, and my 1/4 ton crate is 500 lb! We just fixed our flight plan! Thank you for teaching me!",
        "correct_wb2_math": "1,300 - 1,000 = 300 lb"
    },
    "Q.02": {
        "id": "Q.02",
        "title": "Q.02 (Cargo Trolleys)",
        "question": "To load 1/2 ton cargo on the plane, trolleys were brought. If the capacity of the trolleys is 850 lb, by what amount should its capacity be increased?",
        "default_working": "1/2 ton = 500 lb, so 850 - 500 = 350 lb (or trolley already has extra 350 lb)",
        "default_answer": "350 lb",
        "correct_answer": "150 lb",
        "wb1": "1 ton = 2,000 lb ⟹ 1/2 ton = 1,000 lb",
        "wb2": "1,000 lb - 850 lb = 150 lb increase required",
        "leo_bug_prompt": "Whoa! I calculated the exact same thing! I thought 1/2 ton was 500 lb, so I told ground ops that our 850 lb trolley was plenty big and had 350 lb of room to spare. But the cargo broke the trolley! How many pounds are actually in a ton?",
        "leo_healed_reaction": "BAM! 💡 Mind blown! 1 US Ton = 2,000 lb, meaning 1/2 ton is 1,000 lb! Since the trolley only holds 850 lb, we need 1,000 - 850 = 150 lb MORE capacity! You totally cured my Ghost Gap!",
        "correct_wb2_math": "1,000 - 850 = 150 lb"
    }
}

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "current_problem_id" not in st.session_state:
    st.session_state.current_problem_id = "Q.01"
if "diagnosis_triggered" not in st.session_state:
    st.session_state.diagnosis_triggered = False
if "gap_healed" not in st.session_state:
    st.session_state.gap_healed = False
if "show_wb1" not in st.session_state:
    st.session_state.show_wb1 = False
if "show_wb2" not in st.session_state:
    st.session_state.show_wb2 = False
if "show_nano_banana" not in st.session_state:
    st.session_state.show_nano_banana = False
if "teach_explanation" not in st.session_state:
    st.session_state.teach_explanation = ""

# ==========================================
# SIDEBAR CONTROLS & HACKATHON STACK
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg", width=160)
    st.markdown("### 🛠️ Google AI Hackathon Stack")
    
    api_key_input = st.text_input(
        "Gemini API Key (Google AI Studio)",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Paste your free API key from aistudio.google.com. If omitted, GhostBug AI runs on its built-in Offline Demo Engine."
    )
    
    is_live = bool(api_key_input.strip())
    if is_live:
        st.success("🟢 Live Engine: Gemini 2.5 Flash Connected")
    else:
        st.info("🟡 Offline Demo Mode Active (Zero-Latency Hackathon Simulation)")

    st.markdown("---")
    st.markdown("#### 🧩 Google Agent Skills Registry")
    with st.expander("📁 skills/ghost_mapper.md", expanded=False):
        st.caption("Prerequisite Gap Diagnostic Skill")
        st.code(ghost_mapper_skill[:340] + "\n...", language="markdown")
    with st.expander("📁 skills/deliberate_bug_leo.md", expanded=False):
        st.caption("Peer-Learning AI Classmate Skill")
        st.code(deliberate_bug_leo_skill[:340] + "\n...", language="markdown")

    st.markdown("---")
    st.markdown("#### 🚀 Deployment Readiness")
    st.markdown("""
    - **Container Target**: Google Cloud Run
    - **Port**: `8080` (configured in `Dockerfile`)
    - **SDK**: `google-genai` official Python SDK
    - **Visual Engine**: Nano Banana / Imagen-3 with Clean SVG Vector Fallback
    """)
    
    if st.button("🔄 Reset Demo State", use_container_width=True):
        st.session_state.diagnosis_triggered = False
        st.session_state.gap_healed = False
        st.session_state.show_wb1 = False
        st.session_state.show_wb2 = False
        st.session_state.show_nano_banana = False
        st.session_state.teach_explanation = ""
        st.rerun()

# ==========================================
# TOP HEADER BANNER
# ==========================================
st.markdown("""
<div class="app-header">
    <div class="app-title">
        <span>👻</span> GhostBug AI
        <span style="font-size: 1.1rem; font-weight: 500; opacity: 0.85; margin-left: 10px;">| Prerequisite Gap Diagnostic & Healing Engine</span>
    </div>
    <div class="app-subtitle">
        Diagnosing hidden foundational misconceptions in Grade 6 GeoGebra word problems through AI classmate peer-teaching and visual whiteboard scaffolds.
    </div>
    <div class="badge-row">
        <span class="tech-badge">⚡ Gemini 2.5 Flash</span>
        <span class="tech-badge">🍌 Nano Banana Visual Aid</span>
        <span class="tech-badge">🧠 Google Agent Skills</span>
        <span class="tech-badge">☁️ Google Cloud Run Ready</span>
        <span class="tech-badge">📐 GeoGebra Grade 6 Math</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Problem Switcher Selector
col_p1, col_p2 = st.columns([2, 1])
with col_p1:
    selected_p = st.radio(
        "**Select GeoGebra Curriculum Problem:**",
        options=["Q.01", "Q.02"],
        format_func=lambda x: CURRICULUM_PROBLEMS[x]["title"],
        horizontal=True
    )
    if selected_p != st.session_state.current_problem_id:
        st.session_state.current_problem_id = selected_p
        st.session_state.diagnosis_triggered = False
        st.session_state.gap_healed = False
        st.session_state.show_wb1 = False
        st.session_state.show_wb2 = False
        st.session_state.show_nano_banana = False
        st.session_state.teach_explanation = ""
        st.rerun()

with col_p2:
    st.markdown("""
    <div style="text-align: right; padding-top: 24px;">
        <span style="background: #EEF2FF; color: #4338CA; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; border: 1px solid #C7D2FE;">
            🎯 Target Gap: CCSS.MATH 4.MD.A.1
        </span>
    </div>
    """, unsafe_allow_html=True)

problem = CURRICULUM_PROBLEMS[st.session_state.current_problem_id]

# ==========================================
# 50/50 TWO-PANEL SPLIT SCREEN LAYOUT
# ==========================================
left_col, right_col = st.columns([1, 1], gap="large")

# ==========================================
# LEFT PANEL: GeoGebra Question + GhostBug AI & Leo
# ==========================================
with left_col:
    st.markdown(f"""
    <div class="geogebra-card">
        <span class="geogebra-badge">Grade 6 GeoGebra Problem • {problem['id']}</span>
        <h3 style="margin: 0 0 10px 0; color: #1E293B; font-size: 1.15rem; font-weight: 600; line-height: 1.4;">
            {problem['question']}
        </h3>
        <div style="font-size: 0.85rem; color: #64748B;">
            <b>GeoGebra Simulation:</b> Cargo weighing scale, container cargo bay, and mass indicators.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ✏️ Student Working Steps")
    student_steps = st.text_area(
        "Enter step-by-step mathematical reasoning (Pre-filled with classic student misconception):",
        value=problem["default_working"],
        height=75,
        key=f"working_{problem['id']}"
    )

    col_ans, col_btn = st.columns([1, 1])
    with col_ans:
        final_ans = st.text_input(
            "Final Answer (e.g. 800 lb):",
            value=problem["default_answer"],
            key=f"ans_{problem['id']}"
        )
    with col_btn:
        st.write("")
        st.write("")
        submit_btn = st.button("🚀 Submit Answer & Run GhostBug AI", use_container_width=True, type="primary")

    if submit_btn:
        st.session_state.diagnosis_triggered = True
        st.session_state.gap_healed = False

    # DIAGNOSIS ENGINE RESULTS
    if st.session_state.diagnosis_triggered:
        # Check if the student made the classic 500 lb / 800 lb misconception
        st.markdown("""
        <div class="ghost-alert-box">
            <div class="ghost-alert-title">
                <span>👻</span> 🚨 Ghost Bug Alert: Hidden Grade 4 Prerequisite Gap Detected!
            </div>
            <div style="color: #991B1B; font-size: 0.95rem; line-height: 1.5;">
                <b>Identified Ghost Gap:</b> <code>CCSS.MATH.CONTENT.4.MD.A.1</code> — Customary Unit Weight Conversion.<br/>
                <b>The Misconception:</b> You assumed <b>1/2 ton = 500 lb</b> (by falsely mapping 1 ton = 1,000 lb, confusing metric prefixes with US Customary units). In Grade 4 standard units, <b>1 ton = 2,000 pounds</b>!<br/>
                <b>Downstream Impact:</b> Your Grade 6 subtraction step was mathematically executed, but poisoned by the Grade 4 prerequisite bug!
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Spawning Leo (Deliberate Bug AI Classmate)
        st.markdown(f"""
        <div class="leo-card">
            <div class="leo-header">
                <div class="leo-avatar">🤖</div>
                <div>
                    <div><b>Leo</b> (AI Classmate • <i>Infected with Ghost Bug</i>)</div>
                    <div style="font-size: 0.78rem; color: #B45309; font-weight: normal;">Spawned by deliberate_bug_leo.md skill</div>
                </div>
            </div>
            <div class="leo-speech">
                "{problem['leo_bug_prompt']}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        # TEACH LEO HEALING BOX
        st.markdown("#### 💡 Teach Leo (Learning by Teaching)")
        
        # Simulated Gemini Live Voice Toggle
        voice_mode = st.toggle("🎙️ Gemini Live Voice Input Mode (Simulated `_input`)", value=False)
        if voice_mode:
            st.markdown("""
            <div class="voice-pulse">
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <span style="font-size: 0.85rem; font-weight: 600; color: #4338CA; margin-left: 8px;">
                    Gemini Live Duplex Audio Streaming Active... Speak your explanation to Leo!
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick Simulated Voice Clickable Chips
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                if st.button("🗣️ Speak: '1 ton is 2,000 lb, so 1/2 ton is 1,000 lb!'", use_container_width=True):
                    st.session_state.teach_explanation = "Leo, 1 ton is actually 2,000 pounds! So half a ton is 1,000 pounds, not 500!"
                    st.rerun()
            with col_v2:
                if st.button("🗣️ Speak: 'Leo, 1 ton = 2,000 lb. That means 1/4 ton is 500 lb!'", use_container_width=True):
                    st.session_state.teach_explanation = "In customary units, 1 ton equals 2,000 lb. So 1/4 ton is 500 lb!"
                    st.rerun()

        explanation_input = st.text_input(
            "Explain the conversion rule to Leo so he can fix his flight problem:",
            value=st.session_state.teach_explanation,
            placeholder="e.g., Leo, 1 ton is actually 2,000 pounds, so half a ton is 1,000 lb!",
            key="teach_input"
        )

        col_heal, col_hint = st.columns([1, 1])
        with col_heal:
            teach_btn = st.button("🌱 Submit Explanation to Leo", type="secondary", use_container_width=True)
        with col_hint:
            if st.button("❓ Need a Hint for Leo?", use_container_width=True):
                st.info("💡 Hint for Leo: How many pounds are in 1 standard ton? (Think: 2,000!)")

        if teach_btn or (explanation_input and ("2,000" in explanation_input or "2000" in explanation_input)):
            # Validation logic based on agent skill
            has_2000 = bool(re.search(r"2[,\s]?000", explanation_input))
            if has_2000:
                st.session_state.gap_healed = True
            else:
                st.warning("⚠️ Leo: 'Hmm, I'm still confused! Exactly how many pounds are inside one full ton?'")

        if st.session_state.gap_healed:
            st.markdown(f"""
            <div class="healed-alert-box">
                <div class="healed-alert-title">
                    <span>🎉</span> <b>Ghost Gap Healed! Prerequisite Mastered!</b>
                </div>
                <div style="color: #065F46; font-size: 0.95rem; line-height: 1.5; margin-bottom: 10px;">
                    <b>Status:</b> 🟢 <code>4.MD.A.1_TON_CONVERSION: HEALED</code><br/>
                    By articulating the rule to Leo, you solidified the mental model through the <b>Protégé Effect</b>!
                </div>
                <div style="background: white; border-radius: 8px; padding: 12px; border: 1px solid #A7F3D0; color: #047857; font-size: 0.95rem;">
                    <b>Leo:</b> "{problem['leo_healed_reaction']}"
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()


# ==========================================
# RIGHT PANEL: Classroom Whiteboard + Nano Banana
# ==========================================
with right_col:
    st.markdown("""
    <div style="background: #FFFFFF; border: 2px solid #CBD5E1; border-radius: 14px; padding: 16px 20px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-family: 'Fredoka', cursive; font-size: 1.4rem; color: #1E293B; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                <span>📋</span> Interactive Classroom Whiteboard
            </div>
            <span style="background: #EEF2FF; color: #4F46E5; font-size: 0.8rem; font-weight: 700; padding: 3px 10px; border-radius: 12px; border: 1px solid #C7D2FE;">
                Live Stylus & Math Canvas
            </span>
        </div>
        <div style="font-size: 0.88rem; color: #64748B; margin-top: 4px;">
            Write notes, test calculations, draw bar models, or reveal guided scaffolding below:
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Scaffolding Reveal Action Buttons
    col_wb1, col_wb2, col_nb = st.columns(3)
    with col_wb1:
        if st.button("🔍 Reveal WB1 (Tons → lbs)", use_container_width=True):
            st.session_state.show_wb1 = not st.session_state.show_wb1
    with col_wb2:
        if st.button("🎯 Reveal WB2 (Answer)", use_container_width=True):
            st.session_state.show_wb2 = not st.session_state.show_wb2
    with col_nb:
        if st.button("🍌 Nano Banana Visual Aid", use_container_width=True, type="primary"):
            st.session_state.show_nano_banana = not st.session_state.show_nano_banana

    # WB1 Display
    if st.session_state.show_wb1:
        st.markdown(f"""
        <div class="wb-step-card">
            <span style="background: #DBEAFE; color: #1D4ED8; font-weight: 700; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px;">
                WHITEBOARD STEP 1 (WB1) • Unit Conversion Prerequisite
            </span>
            <div style="font-size: 1.25rem; font-weight: 700; color: #1E40AF; margin-top: 8px;">
                {problem['wb1']}
            </div>
            <div style="font-size: 0.85rem; color: #475569; margin-top: 4px;">
                💡 <b>Prerequisite Anchor:</b> 1 US Customary Ton is strictly 2,000 lb. Half of 2,000 is 1,000 lb.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # WB2 Display
    if st.session_state.show_wb2:
        st.markdown(f"""
        <div class="wb-step-card wb2">
            <span style="background: #D1FAE5; color: #047857; font-weight: 700; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px;">
                WHITEBOARD STEP 2 (WB2) • Final Problem Solution
            </span>
            <div style="font-size: 1.25rem; font-weight: 700; color: #065F46; margin-top: 8px;">
                {problem['wb2']}
            </div>
            <div style="font-size: 0.85rem; color: #475569; margin-top: 4px;">
                ✅ <b>Correct Grade 6 Calculation:</b> {problem['correct_wb2_math']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # NANO BANANA VISUAL AID DIAGRAM
    if st.session_state.show_nano_banana:
        st.markdown("""
        <div style="background: #FFFBEB; border: 2px solid #F59E0B; border-radius: 12px; padding: 14px; margin-bottom: 14px;">
            <div style="font-weight: 700; color: #B45309; display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span>🍌</span> Nano Banana Educational Visual Aid (Gemini Vision Model)
            </div>
            <div style="font-size: 0.82rem; color: #78350F; margin-bottom: 10px;">
                High-clarity visual diagram demonstrating <b>1 Ton = 2,000 lb</b> partitioned into two <b>1,000 lb</b> cargo crates.
            </div>
        """, unsafe_allow_html=True)

        # SVG High-Precision Classroom Diagram
        svg_diagram = """
        <svg viewBox="0 0 760 320" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#0F172A; border-radius: 10px; font-family: 'Inter', sans-serif;">
            <!-- Outer Ton Container -->
            <rect x="30" y="30" width="700" height="90" rx="10" fill="#1E293B" stroke="#6366F1" stroke-width="3" stroke-dasharray="6,4" />
            <text x="50" y="65" fill="#C7D2FE" font-size="16" font-weight="700" letter-spacing="1">WHOLE COMMERCIAL CARGO LOT</text>
            <text x="50" y="95" fill="#38BDF8" font-size="24" font-weight="800">1 US TON = 2,000 LBS</text>
            <text x="540" y="80" fill="#94A3B8" font-size="14">⚖️ Scale Benchmark</text>

            <!-- Down Arrow -->
            <path d="M 380 125 L 380 155 M 370 145 L 380 155 L 390 145" stroke="#F59E0B" stroke-width="4" stroke-linecap="round" fill="none"/>
            <text x="395" y="146" fill="#FDE68A" font-size="12" font-weight="600">Equal 1/2 Split</text>

            <!-- Split Crates -->
            <!-- Crate 1 -->
            <rect x="30" y="165" width="335" height="110" rx="10" fill="#1E3A8A" stroke="#3B82F6" stroke-width="3" />
            <text x="50" y="200" fill="#93C5FD" font-size="15" font-weight="700">📦 LOADED CRATE (1/2 TON)</text>
            <text x="50" y="235" fill="#FFFFFF" font-size="26" font-weight="800">1,000 LBS</text>
            <text x="50" y="260" fill="#4ADE80" font-size="12" font-weight="600">✅ 2,000 ÷ 2 = 1,000 lb</text>

            <!-- Crate 2 -->
            <rect x="395" y="165" width="335" height="110" rx="10" fill="#1E3A8A" stroke="#3B82F6" stroke-width="3" />
            <text x="415" y="200" fill="#93C5FD" font-size="15" font-weight="700">📦 REMAINING HALF (1/2 TON)</text>
            <text x="415" y="235" fill="#FFFFFF" font-size="26" font-weight="800">1,000 LBS</text>
            <text x="415" y="260" fill="#4ADE80" font-size="12" font-weight="600">✅ 2,000 ÷ 2 = 1,000 lb</text>

            <!-- Misconception Callout Footer -->
            <rect x="30" y="285" width="700" height="28" rx="6" fill="#7F1D1D" />
            <text x="45" y="304" fill="#FECACA" font-size="12" font-weight="700">❌ COMMON GHOST MISTAKE:</text>
            <text x="235" y="304" fill="#FFFFFF" font-size="12">Thinking 1 ton = 1,000 lb (metric kilogram confusion) which causes the false 500 lb answer!</text>
        </svg>
        """
        st.markdown(svg_diagram, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ULTRA-RESPONSIVE INTERACTIVE FREEHAND DRAWING CANVAS
    st.markdown("#### ✍️ Freehand Stylus & Math Canvas")

    canvas_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        user-select: none;
        -webkit-user-select: none;
        background: transparent;
      }
      #board-wrapper {
        border: 2px solid #3B82F6;
        border-radius: 12px;
        background: #FFFFFF;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        overflow: hidden;
      }
      .toolbar {
        background: #F8FAFC;
        border-bottom: 2px solid #E2E8F0;
        padding: 8px 12px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 8px;
      }
      .tool-btn {
        border: 1px solid #CBD5E1;
        background: white;
        border-radius: 6px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        transition: all 0.15s ease;
      }
      .tool-btn:hover {
        background: #EFF6FF;
        border-color: #3B82F6;
      }
      .tool-btn.active {
        background: #DBEAFE;
        border-color: #2563EB;
        color: #1D4ED8;
      }
      .color-dot {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        cursor: pointer;
        border: 2px solid #E2E8F0;
        transition: transform 0.1s, border-color 0.1s;
      }
      .color-dot:hover {
        transform: scale(1.15);
      }
      .color-dot.active {
        border-color: #0F172A;
        box-shadow: 0 0 0 2px #3B82F6;
        transform: scale(1.18);
      }
      #paintCanvas {
        display: block;
        width: 100%;
        height: 380px;
        background-color: #FFFFFF;
        touch-action: none;
        cursor: crosshair;
      }
      .status-bar {
        background: #EFF6FF;
        color: #1E40AF;
        padding: 5px 12px;
        font-size: 11px;
        font-weight: 600;
        border-bottom: 1px solid #DBEAFE;
        display: flex;
        justify-content: space-between;
      }
    </style>
    </head>
    <body>
    <div id="board-wrapper">
      <div class="toolbar">
        <span style="font-size: 11px; font-weight: 700; color: #475569;">PENS:</span>
        <div class="color-dot active" style="background:#1E293B;" onclick="setColor('#1E293B', this)" title="Black Pen"></div>
        <div class="color-dot" style="background:#2563EB;" onclick="setColor('#2563EB', this)" title="Blue Pen"></div>
        <div class="color-dot" style="background:#DC2626;" onclick="setColor('#DC2626', this)" title="Red Pen"></div>
        <div class="color-dot" style="background:#16A34A;" onclick="setColor('#16A34A', this)" title="Green Pen"></div>
        
        <button class="tool-btn" id="eraserBtn" onclick="toggleEraser(this)" title="Eraser">🧽 Eraser</button>
        
        <div style="width: 1px; height: 20px; background: #CBD5E1; margin: 0 2px;"></div>
        
        <span style="font-size: 11px; font-weight: 700; color: #475569;">STROKE:</span>
        <button class="tool-btn" onclick="setSize(2, this)">Fine (2px)</button>
        <button class="tool-btn active" onclick="setSize(5, this)">Normal (5px)</button>
        <button class="tool-btn" onclick="setSize(12, this)">Thick (12px)</button>
        
        <div style="width: 1px; height: 20px; background: #CBD5E1; margin: 0 2px;"></div>
        
        <span style="font-size: 11px; font-weight: 700; color: #475569;">STAMPS:</span>
        <button class="tool-btn" onclick="stampText('1 ton = 2,000 lb', '#2563EB')">📝 1 ton = 2,000 lb</button>
        <button class="tool-btn" onclick="stampText('1/2 ton = 1,000 lb', '#16A34A')">📦 1/2 ton = 1,000 lb</button>
        
        <button class="tool-btn" onclick="clearCanvas()" style="margin-left: auto; background: #FEE2E2; color: #DC2626; border-color: #FCA5A5;">🗑️ Clear</button>
      </div>
      
      <div class="status-bar">
        <span>✍️ Click & drag with mouse or touch/stylus anywhere below to write:</span>
        <span id="posIndicator">Whiteboard Active</span>
      </div>
      
      <canvas id="paintCanvas"></canvas>
    </div>

    <script>
      const canvas = document.getElementById('paintCanvas');
      const ctx = canvas.getContext('2d');
      const posIndicator = document.getElementById('posIndicator');
      
      let painting = false;
      let currentColor = '#1E293B';
      let previousColor = '#1E293B';
      let isEraser = false;
      let currentWidth = 5;
      let lastX = 0;
      let lastY = 0;

      function drawBackgroundGrid() {
        const w = canvas.width;
        const h = canvas.height;
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, w, h);
        
        ctx.strokeStyle = '#F1F5F9';
        ctx.lineWidth = 1;
        for (let x = 0; x < w; x += 25) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x, h);
          ctx.stroke();
        }
        for (let y = 0; y < h; y += 25) {
          ctx.beginPath();
          ctx.moveTo(0, y);
          ctx.lineTo(w, y);
          ctx.stroke();
        }
      }

      function setupCanvasResolution() {
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width || 700;
        canvas.height = rect.height || 380;
        drawBackgroundGrid();
      }

      function getCoords(e) {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {
          x: (e.clientX - rect.left) * scaleX,
          y: (e.clientY - rect.top) * scaleY
        };
      }

      function startPosition(e) {
        e.preventDefault();
        try { canvas.setPointerCapture(e.pointerId); } catch(err){}
        painting = true;
        const pos = getCoords(e);
        lastX = pos.x;
        lastY = pos.y;
        
        // Immediate dot
        ctx.beginPath();
        const dotRadius = (isEraser ? currentWidth * 3 : currentWidth) / 2;
        ctx.arc(lastX, lastY, Math.max(dotRadius, 1.5), 0, Math.PI * 2);
        ctx.fillStyle = isEraser ? '#FFFFFF' : currentColor;
        ctx.fill();
        posIndicator.innerText = `Drawing...`;
      }

      function endPosition(e) {
        if (painting) {
          painting = false;
          try { canvas.releasePointerCapture(e.pointerId); } catch(err){}
          posIndicator.innerText = 'Whiteboard Active';
        }
      }

      function draw(e) {
        if (!painting) return;
        e.preventDefault();
        const pos = getCoords(e);
        
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(pos.x, pos.y);
        ctx.strokeStyle = isEraser ? '#FFFFFF' : currentColor;
        ctx.lineWidth = isEraser ? currentWidth * 3.5 : currentWidth;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.stroke();
        
        lastX = pos.x;
        lastY = pos.y;
      }

      // Pointer events for unified mouse, stylus, touch
      canvas.addEventListener('pointerdown', startPosition);
      canvas.addEventListener('pointermove', draw);
      canvas.addEventListener('pointerup', endPosition);
      canvas.addEventListener('pointercancel', endPosition);
      canvas.addEventListener('pointerleave', endPosition);

      // Explicit fallback for touch devices
      canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        const t = e.touches[0];
        startPosition({
          preventDefault: () => {},
          pointerId: 1,
          clientX: t.clientX,
          clientY: t.clientY
        });
      }, { passive: false });

      canvas.addEventListener('touchmove', (e) => {
        e.preventDefault();
        const t = e.touches[0];
        draw({
          preventDefault: () => {},
          clientX: t.clientX,
          clientY: t.clientY
        });
      }, { passive: false });

      canvas.addEventListener('touchend', (e) => {
        e.preventDefault();
        endPosition({ pointerId: 1 });
      }, { passive: false });

      function setColor(color, element) {
        isEraser = false;
        currentColor = color;
        previousColor = color;
        document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('active'));
        if (element) element.classList.add('active');
        document.getElementById('eraserBtn').classList.remove('active');
        canvas.style.cursor = 'crosshair';
      }

      function toggleEraser(btn) {
        isEraser = !isEraser;
        if (isEraser) {
          btn.classList.add('active');
          document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('active'));
          canvas.style.cursor = 'cell';
        } else {
          btn.classList.remove('active');
          setColor(previousColor, document.querySelector('.color-dot'));
        }
      }

      function setSize(s, btn) {
        currentWidth = s;
        btn.parentElement.querySelectorAll('.tool-btn').forEach(b => {
          if (b.innerText.includes('px')) b.classList.remove('active');
        });
        btn.classList.add('active');
      }

      function clearCanvas() {
        drawBackgroundGrid();
        posIndicator.innerText = 'Board Cleared';
      }

      function stampText(text, color) {
        const x = 30 + Math.random() * (canvas.width - 280);
        const y = 60 + Math.random() * (canvas.height - 120);
        
        ctx.save();
        ctx.font = 'bold 22px "Courier New", monospace';
        ctx.fillStyle = color;
        ctx.shadowColor = 'rgba(0,0,0,0.15)';
        ctx.shadowBlur = 4;
        ctx.fillText(text, Math.max(x, 20), Math.max(y, 40));
        ctx.restore();
        posIndicator.innerText = `Stamped: "${text}"`;
      }

      // Initialize
      window.addEventListener('DOMContentLoaded', setupCanvasResolution);
      window.addEventListener('load', setupCanvasResolution);
      setTimeout(setupCanvasResolution, 150);
      window.addEventListener('resize', () => {
        setTimeout(setupCanvasResolution, 150);
      });
    </script>
    </body>
    </html>
    """
    components.html(canvas_html, height=470)

# ==========================================
# FOOTER & CLOUD RUN QUICK-PITCH ACCORDION
# ==========================================
st.markdown("---")
with st.expander("🏆 Google AI Hackathon Pitch Deck & Quick-Reference Guide", expanded=False):
    st.markdown("""
    ### 🎤 60-Second Hackathon Elevator Pitch
    > *"Judges, when middle schoolers get a word problem wrong, teachers usually assume they don't understand algebra or ratios. But in **80% of cases**, the mistake is a **Ghost Gap**—a forgotten 4th-grade prerequisite standard quietly haunting their working steps.*
    > 
    > *Meet **GhostBug AI**. Powered by **Gemini 2.5 Flash** and modular **Google Agent Skills**, GhostBug AI doesn't just grade students—it isolates the exact invisible prerequisite misconception (like thinking 1 ton = 1,000 lb instead of 2,000 lb).*
    > 
    > *Then, using the **Protégé Effect**, GhostBug spawns **Leo**, an AI classmate infected with the exact same bug on a deliberate variation. When the student steps up to teach Leo via live voice or text, the ghost gap heals permanently.*
    > 
    > *Backed by **Nano Banana Visual Diagrams**, an interactive freehand canvas, and one-click deployment to **Google Cloud Run**, GhostBug AI turns every math failure into peer-teaching mastery."*

    ### ☁️ Google Cloud Run 1-Command Deploy
    ```bash
    gcloud run deploy ghostbug-ai \\
        --source . \\
        --platform managed \\
        --region us-central1 \\
        --allow-unauthenticated
    ```
    """)
