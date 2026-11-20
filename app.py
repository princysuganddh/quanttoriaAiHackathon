import os
import re
import json
import base64
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Quanttoria AI Maths | Adaptive Psychometric Quiz Engine",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# CUSTOM CSS & CLASSROOM WHITEBOARD STYLING
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main App Header */
    .app-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        border-radius: 16px;
        padding: 20px 28px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .app-title {
        font-family: 'Fredoka', cursive;
        font-size: 2.15rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
    }
    .app-subtitle {
        font-size: 0.98rem;
        color: #C7D2FE;
        margin-top: 6px;
        margin-bottom: 12px;
    }
    .badge-row {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .tech-badge {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    /* Quiz Progress Stepper */
    .quiz-stepper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        background: #F8FAFC;
        border: 2px solid #E2E8F0;
        border-radius: 14px;
        padding: 12px 18px;
        margin-bottom: 18px;
        flex-wrap: wrap;
    }
    .step-pill {
        flex: 1;
        min-width: 120px;
        text-align: center;
        padding: 8px 12px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 2px solid #E2E8F0;
        background: #FFFFFF;
        color: #64748B;
    }
    .step-pill.active {
        background: #EEF2FF;
        border-color: #4F46E5;
        color: #3730A3;
        box-shadow: 0 3px 10px rgba(79, 70, 229, 0.18);
    }
    .step-pill.solved {
        background: #ECFDF5;
        border-color: #10B981;
        color: #065F46;
    }

    /* Correct Toast Banner */
    .correct-banner {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 14px;
        font-weight: 700;
        font-size: 0.98rem;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.28);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Question Image Frame */
    .question-frame-header {
        background: #EEF2FF;
        border: 2px solid #C7D2FE;
        border-bottom: none;
        border-radius: 14px 14px 0 0;
        padding: 10px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 700;
        color: #3730A3;
        font-size: 0.9rem;
    }

    /* Red Ghost Alert Card */
    .ghost-alert-box {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border: 2px solid #EF4444;
        border-radius: 14px;
        padding: 16px 20px;
        margin-top: 14px;
        margin-bottom: 14px;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.15);
    }
    .ghost-alert-title {
        color: #B91C1C;
        font-size: 1.08rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    /* AI Psychometric Analysis Card */
    .psycho-card {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        border-radius: 16px;
        padding: 18px 22px;
        margin: 14px 0;
        color: white;
        border: 1px solid rgba(129, 140, 248, 0.45);
        box-shadow: 0 8px 24px rgba(49, 46, 129, 0.28);
    }
    .psycho-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #A5B4FC;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }
    .pattern-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        margin: 3px 4px 3px 0;
    }
    .pattern-primary { background: #EF4444; color: white; }
    .pattern-secondary { background: #F59E0B; color: white; }
    .pattern-recurring { background: #EC4899; color: white; }
    .confidence-bar-bg {
        background: rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        height: 9px;
        margin: 6px 0 4px 0;
        overflow: hidden;
    }
    .confidence-bar-fill {
        height: 100%;
        border-radius: 20px;
        background: linear-gradient(90deg, #38BDF8, #A855F7);
    }
    .insight-box {
        background: rgba(99, 102, 241, 0.18);
        border: 1px solid rgba(129, 140, 248, 0.35);
        border-radius: 10px;
        padding: 11px 14px;
        margin-top: 10px;
        font-size: 0.86rem;
        color: #E0E7FF;
        line-height: 1.55;
    }

    /* Warm Cognitive Coach Card (Child-Facing) */
    .coach-card {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border: 2px solid #0284C7;
        border-radius: 14px;
        padding: 15px 18px;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.12);
    }
    .coach-title {
        color: #0369A1;
        font-weight: 800;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }
    .memory-anchor {
        background: #FEF9C3;
        border: 1.5px dashed #CA8A04;
        border-radius: 10px;
        padding: 10px 14px;
        margin-top: 10px;
        color: #713F12;
        font-size: 0.88rem;
        font-weight: 600;
    }
    .domain-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(56, 189, 248, 0.2);
        border: 1px solid rgba(56, 189, 248, 0.45);
        color: #BAE6FD;
        padding: 3px 10px;
        border-radius: 14px;
        font-size: 0.76rem;
        font-weight: 700;
        margin: 4px 4px 4px 0;
    }

    /* Blinking Hint Highlight Overlay on Question Image */
    .q-img-wrap {
        position: relative;
        width: 100%;
        border: 2px solid #C7D2FE;
        border-top: none;
        border-radius: 0 0 14px 14px;
        overflow: hidden;
        background: #A5F3FC;
        margin-bottom: 12px;
    }
    .q-img-wrap img {
        width: 100%;
        height: auto;
        display: block;
    }
    @keyframes hintBlink {
        0%, 100% {
            opacity: 1;
            transform: scale(1);
            box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.85), 0 0 22px 6px rgba(250, 204, 21, 0.95);
            background: rgba(250, 204, 21, 0.34);
        }
        50% {
            opacity: 0.28;
            transform: scale(1.03);
            box-shadow: 0 0 0 8px rgba(250, 204, 21, 0.35), 0 0 6px 2px rgba(239, 68, 68, 0.2);
            background: rgba(250, 204, 21, 0.08);
        }
    }
    .hint-blink-box {
        position: absolute;
        border: 4px solid #EF4444;
        border-radius: 10px;
        pointer-events: none;
        animation: hintBlink 0.9s infinite ease-in-out;
        z-index: 10;
    }
    .hint-blink-tag {
        position: absolute;
        top: -26px;
        left: 0;
        background: #DC2626;
        color: #FEF08A;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 8px;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(0,0,0,0.28);
        letter-spacing: 0.3px;
    }

    /* Funny 2-Liner Student Cue Box */
    .funny-cue-box {
        background: linear-gradient(135deg, #FEF9C3 0%, #FDE047 100%);
        border: 2.5px solid #EA580C;
        border-left: 8px solid #DC2626;
        border-radius: 14px;
        padding: 14px 18px;
        margin: 12px 0;
        box-shadow: 0 6px 18px rgba(234, 88, 12, 0.22);
        animation: cuePop 0.35s ease-out;
    }
    @keyframes cuePop {
        0% { transform: scale(0.97); opacity: 0.6; }
        100% { transform: scale(1); opacity: 1; }
    }
    .funny-cue-title {
        color: #9A3412;
        font-family: 'Fredoka', cursive;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .funny-cue-text {
        color: #431407;
        font-size: 0.96rem;
        font-weight: 600;
        line-height: 1.55;
    }

    /* Cute Cartoon Mascot Bounce + Child-Friendly Celebration */
    @keyframes pipBounce {
        0%, 100% { transform: translateY(0) rotate(-3deg); }
        50% { transform: translateY(-7px) rotate(4deg); }
    }
    .pip-mascot {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: #FEF08A;
        border: 3px solid #F59E0B;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);
        animation: pipBounce 1.1s infinite ease-in-out;
        flex-shrink: 0;
    }
    .usp-compact-card {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        border: 1.5px solid rgba(129, 140, 248, 0.5);
        border-radius: 14px;
        padding: 16px 20px;
        margin-top: 14px;
        color: white;
        box-shadow: 0 6px 20px rgba(49, 46, 129, 0.22);
    }

    /* Cognitive Cue Reminder & Worked Example Cards */
    .cue-card {
        background: linear-gradient(135deg, #FEFCE8 0%, #FEF08A 100%);
        border: 2px solid #EAB308;
        border-left: 7px solid #CA8A04;
        border-radius: 14px;
        padding: 14px 18px;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(234, 179, 8, 0.16);
    }
    .worked-example-card {
        background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
        border: 2px solid #8B5CF6;
        border-left: 7px solid #6D28D9;
        border-radius: 14px;
        padding: 15px 18px;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.14);
    }
    .observer-card {
        background: linear-gradient(135deg, #ECFEFF 0%, #CFFAFE 100%);
        border: 2px solid #06B6D4;
        border-left: 7px solid #0891B2;
        border-radius: 14px;
        padding: 15px 18px;
        margin: 12px 0;
    }

    /* AI Similar-Concept Practice Card */
    .practice-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        border-radius: 14px;
        padding: 14px 18px;
        margin: 14px 0 10px 0;
        color: white;
        border: 1px solid #3B82F6;
    }
    .practice-card {
        background: #FFFFFF;
        border: 2px solid #6366F1;
        border-radius: 12px;
        padding: 15px 18px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
    }
    .difficulty-badge {
        display: inline-block;
        font-size: 0.76rem;
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 10px;
        background: #EEF2FF;
        color: #4338CA;
        margin-bottom: 8px;
    }

    /* Leo's Classroom Chat */
    .leo-card {
        background: #FFFBEB;
        border: 2px solid #F59E0B;
        border-radius: 14px;
        padding: 14px 18px;
        margin: 14px 0;
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
        font-size: 1.5rem;
        background: #FDE68A;
        width: 38px;
        height: 38px;
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
        padding: 10px 14px;
        font-size: 0.92rem;
        color: #78350F;
        line-height: 1.5;
    }

    /* Green Healed / Mastery Card */
    .healed-alert-box {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 2px solid #10B981;
        border-radius: 14px;
        padding: 16px 20px;
        margin: 14px 0;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.18);
    }
    .healed-alert-title {
        color: #065F46;
        font-size: 1.12rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    /* Whiteboard reveal cards */
    .wb-step-card {
        background: white;
        border: 2px solid #3B82F6;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
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
        margin-bottom: 10px;
    }
    .wave-bar {
        width: 4px;
        height: 16px;
        background: #6366F1;
        border-radius: 2px;
        animation: soundWave 1.2s infinite ease-in-out;
    }
    .wave-bar:nth-child(2) { animation-delay: 0.2s; height: 24px; }
    .wave-bar:nth-child(3) { animation-delay: 0.4s; height: 12px; }
    .wave-bar:nth-child(4) { animation-delay: 0.1s; height: 20px; }
    .wave-bar:nth-child(5) { animation-delay: 0.3s; height: 14px; }
    @keyframes soundWave {
        0%, 100% { transform: scaleY(0.4); }
        50% { transform: scaleY(1); }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DIRECTORIES & AGENT SKILLS LOADER
# ==========================================
SKILLS_DIR = os.path.join(os.path.dirname(__file__), "skills")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


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
# 4-QUESTION QUIZ CURRICULUM DATABASE
# ==========================================
QUIZ_ORDER = ["Q1", "Q2", "Q3", "Q4"]

QUIZ_QUESTIONS = {
    "Q1": {
        "id": "Q1",
        "num": 1,
        "short_label": "Q1 · Hangar Fuel",
        "topic": "Liquid Volume Conversion (Gallons ↔ Quarts)",
        "question_text": "The hangar needs to have fuel. 16 quarts of fuel costs the same as 4 gallons of fuel. Which is the better deal in terms of quantity?",
        "image_file": os.path.join(ASSETS_DIR, "q1_hangar_fuel.jpg"),
        "solution_image_file": os.path.join(ASSETS_DIR, "hangar_fuel_solution.png"),
        "input_type": "mcq",
        "options": [
            "A) 16 quarts of fuel",
            "B) 4 gallons of fuel",
            "C) Both the options are equally viable",
        ],
        "correct_option": "C) Both the options are equally viable",
        "correct_answer_display": "C) Both the options are equally viable (16 quarts = 4 gallons)",
        "unit_label": "",
        "concept_rule": "1 gallon = 4 quarts",
        "cue_reminder": "🔔 CUE REMINDER: 'QUART' sounds like 'QUARTER' (1/4)! There are 4 quarts in every 1 gallon. Always convert BOTH options into quarts before comparing!",
        "funny_two_liner_cue": (
            "Whoa there, Speedy Gonzales! 🏎️💨 Look at those blinking **`1 gal`** jugs — remember **1 gallon = 4 quarts** (just like 4 quarters make a dollar!).<br/>"
            "Slow down and count how many quarts are hiding inside all **4 blinking jugs** before picking your answer! 👀"
        ),
        "blink_boxes": [
            {"top": 47, "left": 21, "width": 16, "height": 11, "label": "👀 16 quarts"},
            {"top": 19, "left": 51, "width": 31, "height": 42, "label": "✨ LOOK HERE! 4 × 1 gal"},
        ],
        "worked_example": {
            "title": "AI Worked Example (Same Concept — Milk Jugs vs Cartons)",
            "problem": "A school cafeteria is offered 12 quarts of milk OR 3 gallons of milk for the same price. Which gives more milk?",
            "step1": "Convert gallons into quarts using 1 gallon = 4 quarts → 3 gallons × 4 = 12 quarts.",
            "step2": "Compare both in quarts → 12 quarts = 12 quarts (neither is bigger!).",
            "answer": "Both options give the exact same quantity of milk!",
        },
        "guided_observer": {
            "prompt": "Now YOU try a quick guided problem so AI can observe your steps: Compare 20 quarts of juice vs 5 gallons of juice. Which has more?",
            "step1_label": "Step 1 — Convert 5 gallons into quarts (show your multiplication):",
            "step1_placeholder": "e.g., 5 × 4 = 20 quarts",
            "step1_regex": r"(4|20)",
            "step2_label": "Step 2 — Compare both quantities in quarts:",
            "step2_placeholder": "e.g., 20 quarts = 20 quarts, so both are equal",
            "step2_regex": r"(equal|same|20\s*=\s*20|both)",
            "expected_summary": "5 × 4 = 20 quarts → 20 quarts = 20 quarts (Both are equal!)",
        },
        "target_gap_name": "Liquid Volume Conversion: 1 Gallon = 4 Quarts",
        "wb1": "1 gallon = 4 quarts ⟹ 4 gallons = 4 × 4 = 16 quarts",
        "wb2": "16 quarts = 16 quarts ⟹ Both the options are equally viable!",
        "correct_wb2_math": "4 gallons × 4 quarts/gal = 16 quarts (Equal deal)",
        "leo_bug_prompt": "Wait! I picked 16 quarts too! I thought 1 gallon was only 2 quarts (like a 2-liter soda bottle), so 4 gallons would only be 8 quarts. How many quarts are actually in 1 gallon?",
        "leo_healed_reaction": "AHA!! 💡 1 gallon = 4 quarts, NOT 2! So 4 gallons = 4 × 4 = 16 quarts! Both fuel deals give the exact same quantity. Thank you for teaching me!",
        "heal_regex": r"(4|four|equal|same)",
        "sample_rule": "1 gallon = 4 quarts, so 4 gallons = 16 quarts (both are equal)!",
        "default_psychometric": {
            "primary_pattern": "Metric-Imperial Crosswire",
            "secondary_pattern": "Partial Fact Recall",
            "confidence": 92,
            "cognitive_domain_impact": "Unit Attention",
            "affective_signal": "Systematic Schema Retrieval (Low Math Anxiety — High Curiosity)",
            "child_coach_message": "Hey, great effort! Your brain wasn't guessing wildly—it just compared the numbers quickly before converting them into the same unit. Let's snap one super easy memory picture into place so quarts and gallons never trick you again!",
            "memory_anchor_trick": "QUART sounds like QUARTER! Just like 4 quarters make 1 dollar, 4 quarts make 1 gallon (4 gal × 4 = 16 qt)!",
            "parent_teacher_tip": "Avoid drilling raw conversion tables in isolation; pair 'quart' etymologically with 'quarter (1/4)' and ask the child to convert both sides to the smaller unit before comparing.",
            "root_cause": "The child mapped 'gallon' onto a familiar 2-unit schema (like 1 pint = 2 cups or a 2-liter bottle), assuming 1 gallon = 2 quarts, or compared raw numbers (16 vs 4) without converting to a common unit.",
            "cognitive_load": "LOW — Single-step conversion blocked by an overlearned wrong anchor fact.",
            "intervention_type": "Visual Quart-Grouping + Etymological Memory Anchor",
            "error_tags": ["metric-imperial-crosswire", "unit-blindness", "partial-fact-recall"],
            "gemini_insight": "Confusing quarts and gallons is a classic 'confident wrong schema' signature. Even when children know the word 'quart' sounds like 'quarter' (1/4), under quiz pressure they often compare the raw numbers (16 > 4) instead of converting both sides into the same unit first.",
        },
        "practice_questions": [
            {
                "q": "A chef needs 8 quarts of soup stock. How many gallons is that? (Remember: 1 gallon = 4 quarts)",
                "correct_regex": r"\b2\b|two",
                "correct_answer": "2 gallons",
                "explanation": "1 gallon = 4 quarts, so 8 quarts ÷ 4 = 2 gallons.",
                "difficulty": "🟢 Easy · Memorize the Rule",
            },
            {
                "q": "A school picnic buys 3 gallons of orange juice. How many quarts of orange juice did they buy in total?",
                "correct_regex": r"\b12\b|twelve",
                "correct_answer": "12 quarts",
                "explanation": "3 gallons × 4 quarts per gallon = 12 quarts.",
                "difficulty": "🟡 Medium · Apply Forward",
            },
            {
                "q": "Tank A holds 20 quarts of water. Tank B holds 6 gallons of water. Which tank holds MORE water, and by how many quarts? (Write the extra quarts, e.g., '4')",
                "correct_regex": r"\b4\b|tank\s*b|four",
                "correct_answer": "Tank B holds 4 more quarts (6 gal = 24 quarts; 24 - 20 = 4 quarts)",
                "explanation": "Convert Tank B: 6 × 4 = 24 quarts. Compare: 24 − 20 = 4 more quarts in Tank B.",
                "difficulty": "🔴 Challenge · Compare Deals",
            },
        ],
        "possible_mistakes": [
            {
                "id": "q1_pick_16qt",
                "title": "Choosing 'A) 16 quarts of fuel' (Raw-Number Magnitude Bias)",
                "student_trap": "Comparing raw numbers (16 > 4) without converting both to the same unit, OR assuming 1 gallon = 2 quarts (4 × 2 = 8 qt < 16 qt).",
                "pattern": "Perceptual Magnitude Bias (Unit Blindness)",
                "domain": "Unit Attention",
                "cognitive_reason": "Under visual comparison load, children default to whole-number bias (16 looks much larger than 4) or retrieve a familiar 2-unit schema (like 1 pint = 2 cups).",
                "match_type": "contains",
                "match_value": "16 quarts",
            },
            {
                "id": "q1_pick_4gal",
                "title": "Choosing 'B) 4 gallons of fuel' (Unit-Size Overcompensation)",
                "student_trap": "Knowing gallons are larger containers than quarts and guessing 4 gallons is bigger without multiplying 4 × 4 = 16 quarts.",
                "pattern": "Unit-Size Overcompensation (Qualitative Guessing)",
                "domain": "Number Sense",
                "cognitive_reason": "The child avoids whole-number bias by noticing the bigger unit, but stops at qualitative intuition instead of verifying the exact ×4 conversion.",
                "match_type": "contains",
                "match_value": "4 gallons",
            },
        ],
    },
    "Q2": {
        "id": "Q2",
        "num": 2,
        "short_label": "Q2 · Fire Sand",
        "topic": "Weight Conversion & Equal Sharing (Pounds → Ounces)",
        "question_text": "Sand needs to be kept for fire emergencies. A sack of 20 lbs sand needs to be put in 8 small buckets. How many ounces of sand will each small bucket hold?",
        "image_file": os.path.join(ASSETS_DIR, "q2_fire_sand.jpg"),
        "solution_image_file": None,
        "input_type": "numeric",
        "correct_numeric": 40.0,
        "correct_answer_display": "40 oz",
        "unit_label": "oz",
        "concept_rule": "1 lb = 16 oz",
        "cue_reminder": "🔔 CUE REMINDER: Think 'SWEET 16 Ounces = 1 Pound'! Use 2 boxes: Box 1 = Multiply pounds × 16 to get total ounces. Box 2 = Divide total ounces equally across the buckets!",
        "funny_two_liner_cue": (
            "Hold your horses, Fire Chief! 🚒🔥 Peek at the blinking **`20 lbs`** and that sneaky **`oz`** at the bottom — they're NOT on the same team (**1 lb = 16 oz**, Sweet 16!).<br/>"
            "Turn all **20 lbs** into ounces first, then share them fairly across the **8 blinking buckets** — no rushing! 🪣✨"
        ),
        "blink_boxes": [
            {"top": 50, "left": 22, "width": 14, "height": 10, "label": "👀 20 lbs (×16!)"},
            {"top": 30, "left": 45, "width": 42, "height": 37, "label": "🪣 Share into 8!"},
            {"top": 83, "left": 66, "width": 9, "height": 9, "label": "⚠️ SNEAKY oz!"},
        ],
        "worked_example": {
            "title": "AI Worked Example (Same Concept — Sharing Rice into Bowls)",
            "problem": "A 10 lb bag of rice is shared equally into 4 big bowls. How many ounces of rice go in each bowl?",
            "step1": "Convert pounds into ounces using 1 lb = 16 oz → 10 lbs × 16 = 160 oz total.",
            "step2": "Divide equally into 4 bowls → 160 oz ÷ 4 = 40 oz per bowl.",
            "answer": "40 oz of rice in each bowl!",
        },
        "guided_observer": {
            "prompt": "Now YOU try a quick guided problem so AI can observe your steps: A 4 lb bag of flour is poured equally into 8 small jars. How many ounces go in each jar?",
            "step1_label": "Step 1 — Convert 4 lbs into ounces (1 lb = 16 oz):",
            "step1_placeholder": "e.g., 4 × 16 = 64 oz",
            "step1_regex": r"(16|64)",
            "step2_label": "Step 2 — Divide total ounces equally into 8 jars:",
            "step2_placeholder": "e.g., 64 ÷ 8 = 8 oz per jar",
            "step2_regex": r"\b8\b",
            "expected_summary": "4 × 16 = 64 oz → 64 ÷ 8 = 8 oz per jar!",
        },
        "target_gap_name": "Weight Conversion & Division: 1 lb = 16 oz, then divide by 8 buckets",
        "wb1": "1 lb = 16 oz ⟹ 20 lbs = 20 × 16 = 320 oz",
        "wb2": "320 oz ÷ 8 buckets = 40 oz in each bucket",
        "correct_wb2_math": "(20 × 16) ÷ 8 = 320 ÷ 8 = 40 oz",
        "leo_bug_prompt": "Whoa, I got stuck on the fire sand buckets! I assumed 1 pound was 10 ounces (just like metric units!) so I did 20 × 10 = 200 oz, then 200 ÷ 8 = 25 oz. Or wait—do we even need to convert pounds first? How many ounces are in 1 pound?",
        "leo_healed_reaction": "OH!! 💡 1 pound = 16 ounces (NOT 10 or 12)! So 20 lbs = 20 × 16 = 320 oz, and splitting 320 oz across 8 buckets gives 320 ÷ 8 = 40 oz per bucket! That makes total sense now!",
        "heal_regex": r"(16|sixteen|320|40)",
        "sample_rule": "1 lb = 16 oz, so 20 lbs = 320 oz, and 320 ÷ 8 = 40 oz per bucket!",
        "default_psychometric": {
            "primary_pattern": "Multi-Step Working Memory Overload",
            "secondary_pattern": "Base-10 Overgeneralization",
            "confidence": 90,
            "cognitive_domain_impact": "Working Memory",
            "affective_signal": "Elevated Executive Load — Use 2-Step Chunking to Keep Confidence High",
            "child_coach_message": "This was a tough 2-step puzzle, so don't worry at all! Your brain had to juggle TWO jobs at once: switching pounds into ounces AND sharing into 8 buckets. Let's split it into two tiny, stress-free steps!",
            "memory_anchor_trick": "Think 'SWEET 16 Ounces = 1 Pound'! Step 1: Multiply lbs × 16 to get ounces. Step 2: Divide into the buckets!",
            "parent_teacher_tip": "Encourage externalizing Step 1 on the whiteboard (writing 'Step 1: 320 oz') before attempting Step 2. Offloading working memory prevents premature stopping and reduces calculation anxiety.",
            "root_cause": "This problem requires holding TWO steps in working memory: (1) convert 20 lbs into ounces using 1 lb = 16 oz, and (2) divide equally across 8 buckets. Children commonly either skip unit conversion (20 ÷ 8 = 2.5), forget to divide (stopping at 320), or substitute 1 lb = 10 oz / 12 oz.",
            "cognitive_load": "HIGH — Two-stage problem (unit conversion + equal-share division).",
            "intervention_type": "2-Step Executive Chunking + 'Sweet 16' Anchor Drill",
            "error_tags": ["working-memory-overload", "base-10-overgeneralization", "multi-step-drop"],
            "gemini_insight": "When a child must switch from a non-decimal customary factor (×16) straight into division (÷8), cognitive load spikes. Anchoring '1 lb = 16 oz' first and offloading Step 1 onto the whiteboard drastically reduces anxiety and builds lasting mastery.",
        },
        "practice_questions": [
            {
                "q": "A bag of flour weighs 2 lbs. How many ounces of flour is that? (Anchor rule: 1 lb = 16 oz)",
                "correct_regex": r"\b32\b",
                "correct_answer": "32 oz",
                "explanation": "1 lb = 16 oz, so 2 lbs = 2 × 16 = 32 oz.",
                "difficulty": "🟢 Easy · Memorize 1 lb = 16 oz",
            },
            {
                "q": "A 5 lb box of clay is divided equally among 4 art students. How many ounces of clay does each student get?",
                "correct_regex": r"\b20\b",
                "correct_answer": "20 oz",
                "explanation": "Step 1: 5 lbs × 16 = 80 oz. Step 2: 80 oz ÷ 4 students = 20 oz each.",
                "difficulty": "🟡 Medium · Convert Then Share",
            },
            {
                "q": "A baker has a 10 lb sack of sugar and packs it equally into 8 jars. How many ounces of sugar go into each jar?",
                "correct_regex": r"\b20\b",
                "correct_answer": "20 oz",
                "explanation": "Step 1: 10 lbs × 16 = 160 oz. Step 2: 160 oz ÷ 8 jars = 20 oz per jar.",
                "difficulty": "🔴 Challenge · Same Pattern as Fire Sand",
            },
        ],
        "possible_mistakes": [
            {
                "id": "q2_2_5",
                "title": "Answering 2.5 (Skipped Pounds → Ounces Conversion)",
                "student_trap": "Dividing 20 lbs ÷ 8 buckets = 2.5 directly while missing that the question asks for OUNCES.",
                "pattern": "Unit Blindness (Skipped Conversion)",
                "domain": "Unit Attention",
                "cognitive_reason": "Strong equal-sharing division instinct, but unit-switch blindness at the end of the prompt caused the student to leave the answer in pounds.",
                "match_type": "num",
                "match_value": 2.5,
            },
            {
                "id": "q2_320",
                "title": "Answering 320 (Stopped After Step 1 Conversion)",
                "student_trap": "Correctly calculating 20 lbs × 16 = 320 oz total, but forgetting to divide by the 8 buckets.",
                "pattern": "Working Memory Overload (Goal-Completion Illusion)",
                "domain": "Working Memory",
                "cognitive_reason": "After completing a demanding multiplication (20 × 16), executive working memory signals 'done' and drops the second goal (÷ 8 buckets).",
                "match_type": "num",
                "match_value": 320.0,
            },
            {
                "id": "q2_25",
                "title": "Answering 25 (Assumed 1 lb = 10 oz)",
                "student_trap": "Using a decimal base-10 anchor (1 lb = 10 oz → 20 × 10 ÷ 8 = 25 oz).",
                "pattern": "Base-10 Metric Overgeneralization",
                "domain": "Schema Encoding",
                "cognitive_reason": "The student imported the metric base-10 system into US customary weight. Their 2-step strategy is intact; only the conversion fact (16 oz) is missing.",
                "match_type": "num",
                "match_value": 25.0,
            },
            {
                "id": "q2_30",
                "title": "Answering 30 (Confused 12 in/ft with 16 oz/lb)",
                "student_trap": "Multiplying by 12 instead of 16 (20 × 12 ÷ 8 = 30 oz).",
                "pattern": "Cross-Unit Anchor Confusion (12 vs 16)",
                "domain": "Schema Encoding",
                "cognitive_reason": "Retrieval interference between two customary units: the child pulled '12' from 1 foot = 12 inches instead of '16' for 1 pound = 16 ounces.",
                "match_type": "num",
                "match_value": 30.0,
            },
            {
                "id": "q2_160",
                "title": "Answering 160 (Multiplied 20 × 8 Instead of Converting & Dividing)",
                "student_trap": "Multiplying the two visible numbers (20 × 8 = 160) instead of converting lbs → oz and dividing equally.",
                "pattern": "Keyword/Number-Grabbing Heuristic",
                "domain": "Number Sense",
                "cognitive_reason": "When cognitive load feels high, students sometimes fall back on multiplying visible numbers without modeling the physical sharing of sand into buckets.",
                "match_type": "num",
                "match_value": 160.0,
            },
        ],
    },
    "Q3": {
        "id": "Q3",
        "num": 3,
        "short_label": "Q3 · Hangar Depth",
        "topic": "Fractions of Kilometers to Meters (km → m)",
        "question_text": "The depth of a hangar is 5/10 km. 100 m from the end wall is used to keep the equipment. What is the depth available for the planes? Write your answer in meters.",
        "image_file": os.path.join(ASSETS_DIR, "q3_hangar_depth.png"),
        "solution_image_file": None,
        "input_type": "numeric",
        "correct_numeric": 400.0,
        "correct_answer_display": "400 m",
        "unit_label": "m",
        "concept_rule": "1 km = 1,000 m",
        "cue_reminder": "🔔 CUE REMINDER: 'KILO' means '1K' = 1,000! So 1 km = 1,000 m. Step 1: Convert the fraction of 1,000 m. Step 2: Subtract the equipment area to find what's left!",
        "funny_two_liner_cue": (
            "Pump the brakes, Captain Jet! ✈️🛑 Look at that blinking **`5/10 km`** — **Kilo = 1K = 1,000 meters**, so `5/10` is HALF a kilometer!<br/>"
            "And don't park the plane on the blinking yellow **Maintenance Area (`100 m`)** — subtract that chunk before answering! 🚧😂"
        ),
        "blink_boxes": [
            {"top": 0, "left": 49, "width": 25, "height": 12, "label": "👀 5/10 km & 100 m!"},
            {"top": 61, "left": 28, "width": 48, "height": 11, "label": "🚧 Subtract 100 m!"},
        ],
        "worked_example": {
            "title": "AI Worked Example (Same Concept — Painted Bridge Length)",
            "problem": "A bridge is 6/10 km long. 150 m from one end is closed for painting. How many meters of bridge are open?",
            "step1": "Convert km to meters using 1 km = 1,000 m → (6/10) × 1,000 = 600 m total.",
            "step2": "Subtract the closed section → 600 m − 150 m = 450 m open.",
            "answer": "450 m of bridge remain open!",
        },
        "guided_observer": {
            "prompt": "Now YOU try a quick guided problem so AI can observe your steps: A runway is 8/10 km long. 250 m is used for lights. How many meters remain for takeoff?",
            "step1_label": "Step 1 — Convert 8/10 km into meters (1 km = 1,000 m):",
            "step1_placeholder": "e.g., (8/10) × 1000 = 800 m",
            "step1_regex": r"(1[,\s]?000|800)",
            "step2_label": "Step 2 — Subtract the 250 m light zone from Step 1:",
            "step2_placeholder": "e.g., 800 − 250 = 550 m",
            "step2_regex": r"\b550\b",
            "expected_summary": "(8/10) × 1,000 = 800 m → 800 − 250 = 550 m!",
        },
        "target_gap_name": "Fraction + Metric Length Conversion: 1 km = 1,000 m (5/10 km = 500 m)",
        "wb1": "1 km = 1,000 m ⟹ (5/10) km = (5/10) × 1,000 = 500 m",
        "wb2": "500 m − 100 m (equipment area) = 400 m available for planes",
        "correct_wb2_math": "500 m − 100 m = 400 m",
        "leo_bug_prompt": "Uh oh! I saw 5/10 km and thought 1 km was 100 meters (like centimeters in a meter!), so I got 50 meters—which wasn't even big enough to subtract 100 m! How many meters are really in 1 kilometer?",
        "leo_healed_reaction": "BINGO!! 💡 'Kilo' means 1,000! So 1 km = 1,000 m, which means 5/10 km (half a km!) = 500 m. Subtract 100 m for equipment and we have 400 m left for the planes!",
        "heal_regex": r"(1[,\s]?000|thousand|500|400)",
        "sample_rule": "1 km = 1,000 m, so 5/10 km = 500 m, and 500 − 100 = 400 m!",
        "default_psychometric": {
            "primary_pattern": "Place Value & Prefix Drift (kilo vs centi)",
            "secondary_pattern": "Fraction-to-Unit Conversion Friction",
            "confidence": 91,
            "cognitive_domain_impact": "Schema Encoding",
            "affective_signal": "Dual-Representation Friction (Fraction + Metric Prefix Combined)",
            "child_coach_message": "Fractions plus kilometers in one question can trick almost anyone! Notice that 5/10 is simply HALF — once you picture half of 1,000 meters, the rest becomes super fast subtraction!",
            "memory_anchor_trick": "'KILO' = '1K' (like 1K likes = 1,000)! So 1 km = 1,000 m, and 5/10 km (half of 1K) = 500 m!",
            "parent_teacher_tip": "Bridge metric prefixes to real-world digital literacy ('1K = 1,000') and prompt the child to simplify fractions like 5/10 → 1/2 before scaling, cutting cognitive load in half.",
            "root_cause": "The child struggled with combining a fraction (5/10) and a metric prefix ('kilo' = 1,000). A very common slip is mapping 1 km = 100 m (confusing 'kilo' with 'centi') or stopping right after finding 500 m without subtracting the 100 m maintenance zone.",
            "cognitive_load": "MEDIUM — Requires fraction simplification (5/10 = 1/2), ×1,000 scaling, and subtraction.",
            "intervention_type": "Prefix Meaning Anchor ('Kilo' = 1K = 1,000) + Number-Line Subtraction",
            "error_tags": ["place-value-drift", "prefix-confusion", "fraction-unit-conversion"],
            "gemini_insight": "Mixing fractions like 5/10 with unit conversion triggers 'dual-representation friction': the student can compute 5/10 of 100 easily, or recall 1 km = 1,000 m alone, but combining both causes a place-value slip by a factor of 10.",
        },
        "practice_questions": [
            {
                "q": "A jogging track is 3/10 km long. How many meters long is the track? (Remember: 1 km = 1,000 m)",
                "correct_regex": r"\b300\b",
                "correct_answer": "300 m",
                "explanation": "1 km = 1,000 m, so (3/10) × 1,000 = 300 m.",
                "difficulty": "🟢 Easy · Fraction of 1 km",
            },
            {
                "q": "A runway is 7/10 km long. If 200 m is closed for repairs, how many meters of runway are still open?",
                "correct_regex": r"\b500\b",
                "correct_answer": "500 m",
                "explanation": "(7/10) km = 700 m. Subtract 200 m → 700 − 200 = 500 m open.",
                "difficulty": "🟡 Medium · Convert Then Subtract",
            },
            {
                "q": "A tunnel is 9/10 km long. A train has already traveled 350 m inside the tunnel. How many meters does it still have left?",
                "correct_regex": r"\b550\b",
                "correct_answer": "550 m",
                "explanation": "(9/10) km = 900 m. Remaining distance = 900 − 350 = 550 m.",
                "difficulty": "🔴 Challenge · Hangar Depth Twin",
            },
        ],
        "possible_mistakes": [
            {
                "id": "q3_500",
                "title": "Answering 500 (Stopped After Step 1 km → m Conversion)",
                "student_trap": "Accurately finding 5/10 km = 500 m, but forgetting to subtract the 100 m equipment area.",
                "pattern": "Working Memory Overload (Goal-Completion Illusion)",
                "domain": "Working Memory",
                "cognitive_reason": "Converting a fraction of a kilometer consumes working memory, leading the student to submit the total depth (500 m) instead of the remaining plane depth.",
                "match_type": "num",
                "match_value": 500.0,
            },
            {
                "id": "q3_600",
                "title": "Answering 600 (Added 100 m Instead of Subtracting)",
                "student_trap": "Converting 5/10 km = 500 m accurately, then adding 500 + 100 = 600 m.",
                "pattern": "Operation Reversal Error (+ instead of −)",
                "domain": "Number Sense",
                "cognitive_reason": "Reading-comprehension load caused the student to combine the two distances rather than removing the equipment zone from the available hangar depth.",
                "match_type": "num",
                "match_value": 600.0,
            },
            {
                "id": "q3_50",
                "title": "Answering 50 or -50 (Confused 1 km = 100 m)",
                "student_trap": "Mapping 1 km = 100 m (mixing 'kilo' with 'centi') to get 5/10 km = 50 m.",
                "pattern": "Place Value & Prefix Drift (kilo vs centi)",
                "domain": "Schema Encoding",
                "cognitive_reason": "Prefix interference between centimeter (100) and kilometer (1,000) causes a factor-of-10 place-value slip when paired with a fraction (5/10).",
                "match_type": "num",
                "match_value": 50.0,
            },
            {
                "id": "q3_95",
                "title": "Answering 95 or 99.5 (Mixed-Unit Subtraction Without Converting)",
                "student_trap": "Subtracting 100 − 5 or 100 − 0.5 directly without converting kilometers to meters first.",
                "pattern": "Unit Blindness (Mixed-Unit Operation)",
                "domain": "Unit Attention",
                "cognitive_reason": "Operating on incompatible units (m and km) shows the student skipped the mandatory unit-standardization step before subtracting.",
                "match_type": "num",
                "match_value": 95.0,
            },
        ],
    },
    "Q4": {
        "id": "Q4",
        "num": 4,
        "short_label": "Q4 · Plane Cargo",
        "topic": "Heavy Weight Conversion (Tons → Pounds)",
        "question_text": "The available capacity of the cargo area in a commercial plane is 1,300 lb. If 1/2 ton of the cargo is loaded, how much more can be added?",
        "image_file": os.path.join(ASSETS_DIR, "q4_plane_cargo.png"),
        "solution_image_file": None,
        "input_type": "numeric",
        "correct_numeric": 300.0,
        "correct_answer_display": "300 lb",
        "unit_label": "lb",
        "concept_rule": "1 US ton = 2,000 lb",
        "cue_reminder": "🔔 CUE REMINDER: 1 US Ton = 2,000 lb (DOUBLE the metric thousand!). Step 1: Convert 1/2 ton into pounds. Step 2: Subtract the loaded weight from the plane's max capacity!",
        "funny_two_liner_cue": (
            "Easy there, Turbo Pilot! 🛫😄 Look at that blinking **`1/2 ton`** crate — 1 US Ton is a chunky **2,000 lb** (NOT 1,000, nice try metric brain!).<br/>"
            "Take half of **2,000 lb** first, then see how much space is left in the blinking **`1,300 lb`** cargo hold! 📦⚡"
        ),
        "blink_boxes": [
            {"top": 45, "left": 63, "width": 23, "height": 15, "label": "👀 1/2 of 2,000 lb!"},
            {"top": 46, "left": 18, "width": 22, "height": 12, "label": "✈️ Subtract from 1,300 lb!"},
        ],
        "worked_example": {
            "title": "AI Worked Example (Same Concept — Delivery Truck Space)",
            "problem": "A delivery truck can hold 1,450 lb. If 1/2 ton of boxes is already loaded, how many more pounds can be added?",
            "step1": "Convert 1/2 ton to pounds using 1 ton = 2,000 lb → 1/2 × 2,000 = 1,000 lb loaded.",
            "step2": "Subtract loaded weight from capacity → 1,450 lb − 1,000 lb = 450 lb left.",
            "answer": "450 lb more cargo can be added!",
        },
        "guided_observer": {
            "prompt": "Now YOU try a quick guided problem so AI can observe your steps: A cargo van can hold 1,250 lb. If 1/2 ton is already loaded, how many more pounds fit?",
            "step1_label": "Step 1 — Convert 1/2 ton into pounds (1 ton = 2,000 lb):",
            "step1_placeholder": "e.g., 1/2 × 2000 = 1000 lb",
            "step1_regex": r"(2[,\s]?000|1[,\s]?000)",
            "step2_label": "Step 2 — Subtract Step 1 from 1,250 lb:",
            "step2_placeholder": "e.g., 1250 − 1000 = 250 lb",
            "step2_regex": r"\b250\b",
            "expected_summary": "1/2 × 2,000 = 1,000 lb → 1,250 − 1,000 = 250 lb!",
        },
        "target_gap_name": "Customary Weight Conversion: 1 Ton = 2,000 lb (1/2 Ton = 1,000 lb)",
        "wb1": "1 ton = 2,000 lb ⟹ 1/2 ton = 1,000 lb",
        "wb2": "1,300 lb − 1,000 lb = 300 lb more can be added",
        "correct_wb2_math": "1,300 − 1,000 = 300 lb",
        "leo_bug_prompt": "Wait, I got 800 lb too! I thought 1 ton was 1,000 pounds (just like 1,000 kg in a metric tonne!), so 1/2 ton would be 500 lb, and 1,300 − 500 = 800 lb. How many pounds are actually in 1 US ton?",
        "leo_healed_reaction": "AHA!! 💡 1 US Ton = 2,000 lb, NOT 1,000! So 1/2 ton is 1,000 lb, leaving 1,300 − 1,000 = 300 lb of cargo room. You fixed my flight plan!",
        "heal_regex": r"(2[,\s]?000|two\s*thousand|1[,\s]?000|300)",
        "sample_rule": "1 ton = 2,000 lb, so 1/2 ton = 1,000 lb, leaving 1,300 − 1,000 = 300 lb!",
        "default_psychometric": {
            "primary_pattern": "Schema Confusion (Metric Tonne vs US Ton)",
            "secondary_pattern": "Metric-Imperial Crosswire",
            "confidence": 94,
            "cognitive_domain_impact": "Schema Encoding",
            "affective_signal": "Strong Procedural Fluency — Only One Missing Memory Fact!",
            "child_coach_message": "Good news: your subtraction and fraction skills are totally on track! The ONLY tiny snag was remembering how heavy 1 US ton is in pounds—once you lock in 2,000 lb, you'll breeze right through this!",
            "memory_anchor_trick": "Picture TWO giant elephants = 1 US Ton = 2,000 lb (so 1/2 ton is 1 giant 1,000 lb elephant)!",
            "parent_teacher_tip": "Praise the child's accurate procedural execution (halving and subtracting) so they realize this isn't a math weakness—it is purely a single customary-unit vocabulary fact.",
            "root_cause": "The child imported the metric base-1,000 schema (1 tonne = 1,000 kg) into US customary pounds, computing 1/2 ton = 500 lb instead of 1,000 lb, which then corrupted the final subtraction (1,300 − 500 = 800 lb).",
            "cognitive_load": "MEDIUM — Right subtraction procedure, corrupted by wrong starting conversion anchor.",
            "intervention_type": "Cross-System Contrast + Fractional Ton Practice",
            "error_tags": ["schema-confusion", "metric-imperial-crosswire", "procedural-propagation"],
            "gemini_insight": "This is a textbook 'right procedure, wrong schema' psychometric profile: the child knows how to take half and subtract cleanly, showing strong arithmetic fluency—the ONLY barrier is a missing anchor fact (1 US ton = 2,000 lb).",
        },
        "practice_questions": [
            {
                "q": "A small delivery van carries 1/4 of a US ton of boxes. How many pounds is that? (Rule: 1 ton = 2,000 lb)",
                "correct_regex": r"\b500\b",
                "correct_answer": "500 lb",
                "explanation": "1 ton = 2,000 lb, so 1/4 of 2,000 = 2,000 ÷ 4 = 500 lb.",
                "difficulty": "🟢 Easy · Memorize 1 ton = 2,000 lb",
            },
            {
                "q": "A cargo trolley holds 850 lb. You need to load 1/2 ton onto it. How many MORE pounds of capacity does the trolley need?",
                "correct_regex": r"\b150\b",
                "correct_answer": "150 lb",
                "explanation": "1/2 ton = 1,000 lb. Extra needed = 1,000 − 850 = 150 lb.",
                "difficulty": "🟡 Medium · Cargo Trolley Twin",
            },
            {
                "q": "A bridge limit is 2 tons. A truck weighing 3,450 lb drives onto it. How many pounds BELOW the limit is the truck?",
                "correct_regex": r"\b550\b",
                "correct_answer": "550 lb",
                "explanation": "2 tons = 2 × 2,000 = 4,000 lb. Margin = 4,000 − 3,450 = 550 lb.",
                "difficulty": "🔴 Challenge · Multi-Ton Capacity",
            },
        ],
        "possible_mistakes": [
            {
                "id": "q4_800",
                "title": "Answering 800 (Assumed 1 US Ton = 1,000 lb)",
                "student_trap": "Computing 1/2 ton = 500 lb (from metric 1,000 kg) and subtracting 1,300 − 500 = 800 lb.",
                "pattern": "Metric-Imperial Crosswire (1 ton = 1,000 lb)",
                "domain": "Schema Encoding",
                "cognitive_reason": "Classic 'right procedure, wrong schema': strong halving and subtraction fluency, disrupted solely by importing metric 1,000 instead of 1 US ton = 2,000 lb.",
                "match_type": "num",
                "match_value": 800.0,
            },
            {
                "id": "q4_1000",
                "title": "Answering 1,000 (Stopped After Step 1 Ton → lb Conversion)",
                "student_trap": "Correctly converting 1/2 ton = 1,000 lb, but forgetting to subtract it from 1,300 lb capacity.",
                "pattern": "Working Memory Overload (Goal-Completion Illusion)",
                "domain": "Working Memory",
                "cognitive_reason": "Executive working memory dropped the second step ('how much MORE can be added?') right after successfully computing 1/2 of 2,000 lb.",
                "match_type": "num",
                "match_value": 1000.0,
            },
            {
                "id": "q4_2300",
                "title": "Answering 2,300 (Added Instead of Subtracting)",
                "student_trap": "Converting 1/2 ton = 1,000 lb, then adding 1,300 + 1,000 = 2,300 lb.",
                "pattern": "Operation Reversal Error (+ instead of −)",
                "domain": "Number Sense",
                "cognitive_reason": "The keyword 'more' ('how much more can be added?') triggered an automatic addition reflex instead of finding the remaining capacity difference.",
                "match_type": "num",
                "match_value": 2300.0,
            },
            {
                "id": "q4_650",
                "title": "Answering 650 (Halved 1,300 lb Instead of 1 Ton)",
                "student_trap": "Seeing '1/2' and taking half of 1,300 lb (650 lb) instead of half of 1 ton.",
                "pattern": "Target Misattribution (Wrong Base for Fraction)",
                "domain": "Unit Attention",
                "cognitive_reason": "The fraction '1/2' was applied to the most salient number in the prompt (1,300 lb) rather than to the unit '1 ton'.",
                "match_type": "num",
                "match_value": 650.0,
            },
        ],
    },
}


# ==========================================
# SMART PSYCHOMETRIC & AI ENGINE FUNCTIONS
# ==========================================
def parse_numeric_answer(text: str):
    """Extract first numeric value from student text answer."""
    if not text:
        return None
    cleaned = text.replace(",", "").strip()
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    if match:
        try:
            return float(match.group(0))
        except ValueError:
            return None
    return None


@st.cache_data
def encode_image_b64(filepath: str) -> tuple:
    ext = os.path.splitext(filepath)[1].lower()
    mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
    with open(filepath, "rb") as f:
        return mime, base64.b64encode(f.read()).decode("utf-8")


def render_question_image_with_blink(image_path: str, blink_boxes: list, show_blink: bool):
    """Render the question image; when show_blink=True, blink/highlight the exact hint spots on the image!"""
    if not image_path or not os.path.exists(image_path):
        return
    mime, b64 = encode_image_b64(image_path)
    overlays = ""
    if show_blink and blink_boxes:
        for box in blink_boxes:
            lbl = box.get("label", "👀 LOOK HERE!")
            overlays += (
                f'<div class="hint-blink-box" style="top:{box["top"]}%; left:{box["left"]}%; '
                f'width:{box["width"]}%; height:{box["height"]}%;">'
                f'<div class="hint-blink-tag">{lbl}</div></div>'
            )
    st.markdown(
        f'<div class="q-img-wrap"><img src="data:{mime};base64,{b64}" alt="Math Question"/>{overlays}</div>',
        unsafe_allow_html=True,
    )


def get_funny_two_liner_cue(question: dict, wrong_answer: str, api_key: str) -> str:
    """Return ONLY a funny, kid-friendly 2-liner cue pointing to the blinking hint in the image so the student slows down!"""
    qid = question["id"]
    ans_num = parse_numeric_answer(wrong_answer)

    # Smart answer-specific funny 2-liners (offline + fallback)
    fallback = question["funny_two_liner_cue"]
    if qid == "Q2" and ans_num is not None:
        if abs(ans_num - 2.5) < 0.05:
            fallback = (
                "Whoa, Speedy! 🏃‍♂️💨 You divided in pounds and totally ghosted that blinking <b><code>oz</code></b> at the bottom! 👻<br/>"
                "Turn those blinking <b>20 lbs</b> into ounces first (<b>1 lb = 16 oz</b>, Sweet 16!), then split into the <b>8 buckets</b>!"
            )
        elif abs(ans_num - 320) < 0.5:
            fallback = (
                "Nice 320 oz, superstar — wait, did you dump ALL 320 oz into ONE mega-bucket?! 😂🪣<br/>"
                "Slow down and peek at those <b>8 blinking red buckets</b> — share your 320 oz fairly among all 8!"
            )
    elif qid == "Q3" and ans_num is not None:
        if abs(ans_num - 500) < 0.5:
            fallback = (
                "Awesome 500 m, Captain — wait, you just parked the jet ON TOP of the blinking yellow <b>Maintenance Area</b>! ✈️💥<br/>"
                "Pump the brakes and subtract those blinking <b>100 m</b> of equipment space first!"
            )
        elif abs(ans_num - 600) < 0.5:
            fallback = (
                "Haha, hold up Captain! ✈️😄 You ADDED the blinking yellow <b>Maintenance Area</b> instead of clearing it out of the way!<br/>"
                "Slow down, take your 500 m hangar depth, and <b>subtract</b> those blinking <b>100 m</b>!"
            )
    elif qid == "Q4" and ans_num is not None:
        if abs(ans_num - 1000) < 0.5:
            fallback = (
                "Boom, you nailed <code>1/2 ton = 1,000 lb</code> — don't take off yet, Turbo Pilot! 🛫😂<br/>"
                "Check the blinking <b>1,300 lb</b> cargo hold — how much <b>MORE</b> space is left after loading 1,000 lb?"
            )
        elif abs(ans_num - 2300) < 0.5:
            fallback = (
                "Whoa, overload alarm! 🚨📦 Adding 1,000 lb to 1,300 lb would burst the plane's belly!<br/>"
                "Take a chill pill and <b>subtract</b> the blinking <b>1/2 ton</b> (1,000 lb) from the blinking <b>1,300 lb</b> capacity!"
            )

    if not api_key:
        return fallback



    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""You are a super fun, warm, encouraging math buddy for an 11-year-old (Grade 6) student.
The student just rushed and entered a wrong answer on this question:
QUESTION: {question['question_text']}
CORE RULE: {question['concept_rule']}
STUDENT'S WRONG ANSWER: {wrong_answer}
BLINKING HINTS CURRENTLY HIGHLIGHTED ON THE IMAGE: {', '.join(b['label'] for b in question.get('blink_boxes', []))}

Write EXACTLY 2 short, funny, kid-friendly sentences (NO MORE THAN 2 LINES TOTAL):
- Line 1: A playful, funny nudge telling them to slow down (stop rushing in overconfidence!) and look at the blinking highlighted hint in the image, reminding them of the conversion rule ({question['concept_rule']}).
- Line 2: A brief playful prompt telling them what step to check next WITHOUT giving away the final numeric answer!

Format with <br/> between Line 1 and Line 2. No markdown headers, no clinical/psychometric words, just fun 2 lines!"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        txt = response.text.strip().replace("\n\n", "<br/>").replace("\n", "<br/>")
        if txt:
            return txt
    except Exception:
        pass
    return fallback


CONGRATS_LINES = {
    "Q1": (
        "Woohoo!! High five, Fuel Master! You cracked Question 1 like a math superhero! "
        "16 quarts equals 4 gallons! Let's zoom over to Question 2!"
    ),
    "Q2": (
        "Boom shakalaka!! Awesome job, Fire Chief! 40 ounces in every single red bucket! "
        "You crushed Question 2! Ready for Question 3?"
    ),
    "Q3": (
        "Yaaay!! Cleared for takeoff, Captain Jet! 400 meters for the planes! "
        "Only ONE last mission left — let's fly to Question 4!"
    ),
    "Q4": (
        "MEGA VICTORY!! Hip hip hooray!! You conquered ALL FOUR airport math challenges! "
        "You are officially a Quanttoria Math Superstar!"
    ),
}

SOLUTION_SPEECH = {
    "Q1": (
        "Woohoo! That is correct! High five, Fuel Master! "
        "Here is the magic formula to remember: 1 gallon equals 4 quarts. "
        "Step 1: Multiply 4 gallons times 4, which gives 16 quarts. "
        "Step 2: 16 quarts equals 16 quarts, so both options are equally viable! "
        "Tap Next when you are ready for Mission 2!"
    ),
    "Q2": (
        "Awesome job, Fire Chief! That is correct! "
        "Remember our Sweet 16 formula: 1 pound equals 16 ounces. "
        "Step 1: Convert 20 pounds to ounces by multiplying 20 times 16, which equals 320 ounces. "
        "Step 2: Divide 320 ounces equally into 8 small buckets, giving 40 ounces in each bucket! "
        "Tap Next to fly to Mission 3!"
    ),
    "Q3": (
        "Yaaay! Cleared for takeoff, Captain Jet! That is correct! "
        "Remember the Kilo formula: 1 kilometer equals 1,000 meters. "
        "Step 1: Five tenths of 1,000 meters is half a kilometer, which equals 500 meters. "
        "Step 2: Subtract the 100 meter maintenance area: 500 minus 100 equals 400 meters available for the planes! "
        "Tap Next for our final mission!"
    ),
    "Q4": (
        "Mega victory! You nailed the final mission! "
        "Remember the heavy weight formula: 1 US ton equals 2,000 pounds. "
        "Step 1: Half of 2,000 pounds equals 1,000 pounds already loaded. "
        "Step 2: Subtract from the 1,300 pound cargo capacity: 1,300 minus 1,000 equals 300 pounds left! "
        "Tap Finish to claim your Math Champion trophy!"
    ),
}


def strip_for_speech(text: str) -> str:
    """Strip HTML tags, markdown markers, and emojis so Web Speech Synthesis reads smoothly."""
    clean = re.sub(r"<[^>]+>", " ", text or "")
    clean = re.sub(r"[`*_#]", "", clean)
    clean = re.sub(r"[^\x00-\x7F]+", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


@st.cache_data(show_spinner=False)
def synthesize_nobita_style_mp3(clean_text: str) -> str:
    """Generate a crystal-clear, playful youthful Nobita-style anime kid voice MP3 (base64) via edge-tts."""
    try:
        import asyncio
        import edge_tts

        async def _gen():
            comm = edge_tts.Communicate(
                clean_text,
                voice="en-US-AnaNeural",  # Studio-quality youthful cartoon kid voice!
                rate="-4%",               # Crisp, clear kid-friendly pace
                pitch="+6Hz",             # Playful, expressive Nobita-inspired youthful tone
            )
            chunks = []
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    chunks.append(chunk["data"])
            return b"".join(chunks)

        try:
            mp3_bytes = asyncio.run(_gen())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                mp3_bytes = loop.run_until_complete(_gen())
            finally:
                loop.close()

        if mp3_bytes:
            return base64.b64encode(mp3_bytes).decode("utf-8")
    except Exception:
        pass
    return ""


def render_cartoon_voice_player(spoken_text: str, enabled: bool, nonce: int, mood: str = "cue"):
    """Speak cues, hints, or congratulations aloud in a crystal-clear Nobita-style anime kid voice + Replay pill."""
    if not spoken_text:
        return
    clean_speech = strip_for_speech(spoken_text)
    if not clean_speech:
        return
    mp3_b64 = synthesize_nobita_style_mp3(clean_speech) if enabled else ""
    js_text = json.dumps(clean_speech)
    bg = "#DCFCE7" if mood == "cheer" else "#FEF3C7"
    border = "#16A34A" if mood == "cheer" else "#EA580C"
    txt_col = "#14532D" if mood == "cheer" else "#9A3412"
    label = "🧒 Nobi-Buddy is cheering for you!" if mood == "cheer" else "🧒 Nobi-Buddy has a funny clue for you!"
    auto_js = "true" if enabled else "false"
    audio_tag = (
        f'<audio id="nobiAudio" preload="auto" src="data:audio/mpeg;base64,{mp3_b64}"></audio>'
        if mp3_b64
        else ""
    )

    voice_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {{ margin: 0; padding: 0; font-family: 'Fredoka', -apple-system, sans-serif; background: transparent; }}
      .voice-pill {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        background: {bg};
        border: 2px solid {border};
        border-radius: 30px;
        padding: 6px 14px;
        color: {txt_col};
        font-size: 13px;
        font-weight: 700;
      }}
      .replay-btn {{
        background: {border};
        color: white;
        border: none;
        border-radius: 20px;
        padding: 5px 12px;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
      }}
      .replay-btn:hover {{ opacity: 0.9; transform: scale(1.04); }}
    </style>
    </head>
    <body>
      {audio_tag}
      <div class="voice-pill">
        <span id="vStatus">{label}</span>
        <button class="replay-btn" onclick="playBuddyVoice()">🔊 Replay Clear Voice</button>
      </div>
      <script>
        const msgText = {js_text};
        const shouldAuto = {auto_js};
        const nonceKey = "nobi_spoken_{nonce}";
        const audioEl = document.getElementById('nobiAudio');
        const statusEl = document.getElementById('vStatus');

        function speakFallbackClear() {{
          if (!('speechSynthesis' in window)) return;
          window.speechSynthesis.cancel();
          const u = new SpeechSynthesisUtterance(msgText);
          u.pitch = 1.18;  // Natural clear youthful kid pitch (no chipmunk distortion!)
          u.rate = 0.94;   // Crystal clear pace
          u.volume = 1.0;
          const voices = window.speechSynthesis.getVoices();
          const pref = voices.find(v => /en/i.test(v.lang) && /(ana|aria|google us english|samantha|zira)/i.test(v.name));
          if (pref) u.voice = pref;
          u.onstart = () => {{ statusEl.innerText = '🧒🎵 Speaking clearly...'; }};
          u.onend = () => {{ statusEl.innerText = '{label}'; }};
          window.speechSynthesis.speak(u);
        }}

        function playBuddyVoice() {{
          if (audioEl) {{
            audioEl.currentTime = 0;
            audioEl.onplay = () => {{ statusEl.innerText = '🧒🎵 Speaking...'; }};
            audioEl.onended = () => {{ statusEl.innerText = '{label}'; }};
            audioEl.play().catch(() => {{
              statusEl.innerText = '🔊 Tap Replay to hear Nobi-Buddy!';
            }});
          }} else {{
            speakFallbackClear();
          }}
        }}

        if (shouldAuto && !window.sessionStorage.getItem(nonceKey)) {{
          window.sessionStorage.setItem(nonceKey, "1");
          setTimeout(playBuddyVoice, 100);
        }}
      </script>
    </body>
    </html>
    """
    components.html(voice_html, height=48)


def render_speech_to_text_mic(qid: str, unit_label: str = ""):
    """Interactive browser Speech-to-Text widget so kids can speak their answer or math idea to Pip!"""
    hint_eg = f'Say your answer like "40 {unit_label}"!' if unit_label else 'Say "Option A", "Option B", or "Option C"!'
    mic_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: transparent; }}
      .stt-box {{
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border: 2px solid #818CF8;
        border-radius: 12px;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
      }}
      .mic-btn {{
        background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
        color: white;
        border: none;
        border-radius: 22px;
        padding: 7px 14px;
        font-size: 13px;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 3px 10px rgba(139, 92, 246, 0.3);
        transition: transform 0.12s;
      }}
      .mic-btn:hover {{ transform: scale(1.03); }}
      .mic-btn.listening {{
        background: linear-gradient(135deg, #EF4444 0%, #F97316 100%);
        animation: pulseMic 0.9s infinite;
      }}
      @keyframes pulseMic {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.55); }}
        50% {{ box-shadow: 0 0 0 9px rgba(239, 68, 68, 0); }}
      }}
      .transcript-pill {{
        flex: 1;
        min-width: 160px;
        background: white;
        border: 1px solid #C7D2FE;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 12.5px;
        color: #1E1B4B;
        font-weight: 600;
      }}
      .copy-btn {{
        background: #4F46E5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 11.5px;
        font-weight: 700;
        cursor: pointer;
        display: none;
      }}
    </style>
    </head>
    <body>
      <div class="stt-box">
        <button id="micBtn" class="mic-btn" onclick="toggleMic()">🎙️ Speak Your Answer</button>
        <div id="transcriptBox" class="transcript-pill">🐥 {hint_eg}</div>
        <button id="copyBtn" class="copy-btn" onclick="copyText()">📋 Copy</button>
      </div>
      <script>
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        let listening = false;
        let lastHeard = "";

        function toggleMic() {{
          const btn = document.getElementById('micBtn');
          const box = document.getElementById('transcriptBox');
          const copyBtn = document.getElementById('copyBtn');
          if (!SpeechRecognition) {{
            box.innerText = '⚠️ Speech-to-Text works best in Chrome or Edge — type your answer below!';
            return;
          }}
          if (listening && recognition) {{
            recognition.stop();
            return;
          }}
          recognition = new SpeechRecognition();
          recognition.lang = 'en-US';
          recognition.interimResults = true;
          recognition.maxAlternatives = 1;

          recognition.onstart = () => {{
            listening = true;
            btn.classList.add('listening');
            btn.innerText = '🔴 Listening... Tap to Stop';
            box.innerText = '🐥 Pip is listening... speak now!';
          }};
          recognition.onresult = (event) => {{
            let text = '';
            for (let i = 0; i < event.results.length; i++) {{
              text += event.results[i][0].transcript;
            }}
            lastHeard = text.trim();
            box.innerText = '🗣️ Pip heard: "' + lastHeard + '"';
            copyBtn.style.display = 'inline-block';
          }};
          recognition.onerror = (e) => {{
            box.innerText = '🐥 Oops! Mic permission needed (' + e.error + ') — or type below!';
          }};
          recognition.onend = () => {{
            listening = false;
            btn.classList.remove('listening');
            btn.innerText = '🎙️ Speak Your Answer';
          }};
          recognition.start();
        }}

        function copyText() {{
          if (!lastHeard) return;
          navigator.clipboard.writeText(lastHeard).then(() => {{
            const b = document.getElementById('copyBtn');
            b.innerText = '✅ Copied!';
            setTimeout(() => b.innerText = '📋 Copy', 1200);
          }});
        }}
      </script>
    </body>
    </html>
    """
    components.html(mic_html, height=62)




def check_answer_correct(question: dict, raw_answer: str) -> bool:
    if question["input_type"] == "mcq":
        return raw_answer == question["correct_option"]
    val = parse_numeric_answer(raw_answer)
    if val is None:
        return False
    return abs(val - question["correct_numeric"]) < 1e-6


def offline_smart_psychometric_diagnosis(question: dict, raw_answer: str, student_steps: str, error_history: list) -> dict:
    """Inspect the child's actual wrong answer & steps to pinpoint specific psychometric patterns even offline."""
    base = dict(question["default_psychometric"])
    ans_num = parse_numeric_answer(raw_answer)
    qid = question["id"]

    if qid == "Q1":
        if "16 quarts" in (raw_answer or ""):
            base["primary_pattern"] = "Number-Size Bias (Unit Blindness)"
            base["secondary_pattern"] = "Metric-Imperial Crosswire"
            base["confidence"] = 94
            base["root_cause"] = (
                "The child chose '16 quarts'—either comparing raw numbers (16 > 4) while ignoring the unit size, "
                "or assuming 1 gallon = 2 quarts (yielding 8 quarts < 16 quarts)."
            )
            base["gemini_insight"] = (
                "Selecting the option with the bigger raw number (16 vs 4) is a classic 'unit blindness' heuristic. "
                "Children naturally equate bigger numbers with bigger quantities until they build an automatic visual "
                "habit of converting both options into the same unit first."
            )
        elif "4 gallons" in (raw_answer or ""):
            base["primary_pattern"] = "Unit-Size Overcompensation"
            base["secondary_pattern"] = "Partial Fact Recall"
            base["confidence"] = 91
            base["root_cause"] = (
                "The child knew gallons are much bigger than quarts and picked '4 gallons' intuitively without "
                "multiplying 4 × 4 = 16 quarts to verify whether the two quantities are actually equal."
            )
            base["gemini_insight"] = (
                "Here the child avoided raw-number bias but fell into 'qualitative guessing'—trusting that the bigger "
                "unit always wins without running the exact ×4 conversion check."
            )

    elif qid == "Q2" and ans_num is not None:
        if abs(ans_num - 2.5) < 0.05:
            base["primary_pattern"] = "Unit Blindness (Skipped Conversion)"
            base["secondary_pattern"] = "Working Memory Overload"
            base["confidence"] = 96
            base["root_cause"] = (
                "The child computed 20 ÷ 8 = 2.5 lbs per bucket—correctly dividing the sand into 8 buckets, "
                "but completely skipped converting pounds into ounces (×16)!"
            )
            base["gemini_insight"] = (
                "Answering 2.5 proves the child understands equal-sharing division perfectly, but suffered 'unit-switch "
                "blindness' at the end of the word problem ('How many OUNCES?'). Highlighting the target unit first solves this."
            )
        elif abs(ans_num - 320) < 0.5:
            base["primary_pattern"] = "Working Memory Overload (Stopped at Step 1)"
            base["secondary_pattern"] = "Multi-Step Goal Drift"
            base["confidence"] = 95
            base["root_cause"] = (
                "The child accurately remembered 1 lb = 16 oz and calculated 20 × 16 = 320 oz total, "
                "but stopped before Step 2 (dividing 320 oz among the 8 small buckets)!"
            )
            base["gemini_insight"] = (
                "Stopping at 320 oz is a classic 'goal-completion illusion'—after finishing a hard multiplication, "
                "the brain feels done and forgets the final division step. A 2-box checklist cures this immediately."
            )
        elif abs(ans_num - 25) < 0.5:
            base["primary_pattern"] = "Base-10 Metric Overgeneralization"
            base["secondary_pattern"] = "Schema Confusion"
            base["confidence"] = 95
            base["root_cause"] = (
                "The child got 25 oz by assuming 1 lb = 10 oz (20 × 10 ÷ 8 = 25). Their division strategy is solid, "
                "but they substituted a base-10 metric rule instead of the customary 1 lb = 16 oz."
            )
        elif abs(ans_num - 30) < 0.5:
            base["primary_pattern"] = "Cross-Unit Anchor Confusion (12 vs 16)"
            base["secondary_pattern"] = "Partial Fact Recall"
            base["confidence"] = 94
            base["root_cause"] = (
                "The child got 30 oz by using 12 instead of 16 (20 × 12 ÷ 8 = 30)—mixing up '1 foot = 12 inches' "
                "with '1 pound = 16 ounces'!"
            )

    elif qid == "Q3" and ans_num is not None:
        if abs(ans_num - 500) < 0.5:
            base["primary_pattern"] = "Working Memory Overload (Stopped at Step 1)"
            base["secondary_pattern"] = "Multi-Step Goal Drift"
            base["confidence"] = 96
            base["root_cause"] = (
                "The child nailed the conversion (5/10 km = 500 m) but forgot Step 2: subtracting the 100 m "
                "maintenance area from the total hangar depth!"
            )
        elif abs(ans_num - 600) < 0.5:
            base["primary_pattern"] = "Operation Reversal Error (+ instead of −)"
            base["secondary_pattern"] = "Word-Problem Comprehension Slip"
            base["confidence"] = 93
            base["root_cause"] = (
                "The child converted 5/10 km = 500 m accurately, but ADDED 100 m (500 + 100 = 600 m) instead of "
                "subtracting the equipment area taken away from the planes."
            )
        elif abs(ans_num - 50) < 0.5 or ans_num < 0:
            base["primary_pattern"] = "Place Value & Prefix Drift (1 km = 100 m)"
            base["secondary_pattern"] = "Metric Prefix Confusion"
            base["confidence"] = 95
            base["root_cause"] = (
                "The child mapped 1 km = 100 m instead of 1,000 m, yielding 5/10 km = 50 m (off by a factor of 10)."
            )

    elif qid == "Q4" and ans_num is not None:
        if abs(ans_num - 800) < 0.5:
            base["primary_pattern"] = "Metric-Imperial Crosswire (1 ton = 1,000 lb)"
            base["secondary_pattern"] = "Schema Confusion"
            base["confidence"] = 97
            base["root_cause"] = (
                "Answering 800 lb pinpoints the exact Ghost Gap: the child assumed 1 ton = 1,000 lb → 1/2 ton = 500 lb, "
                "then accurately subtracted 1,300 − 500 = 800 lb."
            )
        elif abs(ans_num - 1000) < 0.5:
            base["primary_pattern"] = "Working Memory Overload (Stopped at Step 1)"
            base["secondary_pattern"] = "Multi-Step Goal Drift"
            base["confidence"] = 95
            base["root_cause"] = (
                "The child correctly converted 1/2 ton = 1,000 lb, but entered the loaded weight instead of "
                "subtracting it from the 1,300 lb plane capacity (1,300 − 1,000 = 300 lb)."
            )

    # Check for cross-question recurring psychometric theme
    if error_history:
        prev_patterns = [e["pattern"] for e in error_history if e["question_id"] != qid]
        if prev_patterns:
            base["recurring_note"] = (
                f"📈 Cross-Quiz Pattern Detected: Across {len(prev_patterns) + 1} questions, the child shows a "
                f"recurring pattern in unit-conversion schema anchoring ({', '.join(set(prev_patterns))}). "
                f"Targeted similar-concept drills below will lock this rule into long-term memory."
            )
    return base


COGNITIVE_EXPERT_SYSTEM_PROMPT = f"""You are Dr. Quanttoria, an Expert Cognitive Scientist and Educational Psychometrician specializing in K-12 Mathematics Learning.
You combine developmental math cognition, working-memory load analysis, psychometric error taxonomy, and warm, low-anxiety metacognitive coaching for students.

Follow your loaded skill protocol:
{ghost_mapper_skill}
"""


def update_cognitive_scores(event_type: str, domain: str = None):
    """Dynamically calibrate the student's 4-domain cognitive & psychometric profile."""
    scores = st.session_state.cognitive_scores
    if event_type == "first_try_correct":
        for k in scores:
            scores[k] = min(100, scores[k] + 5)
    elif event_type == "healed_correct":
        for k in scores:
            scores[k] = min(100, scores[k] + 3)
        if domain and domain in scores:
            scores[domain] = min(100, scores[domain] + 5)
    elif event_type == "drill_correct":
        if domain and domain in scores:
            scores[domain] = min(100, scores[domain] + 4)
        else:
            scores["Schema Encoding"] = min(100, scores["Schema Encoding"] + 3)
    elif event_type == "error":
        target = domain if (domain and domain in scores) else "Schema Encoding"
        scores[target] = max(30, scores[target] - 12)


def get_ai_psychometric_analysis(question: dict, raw_answer: str, student_steps: str, error_history: list, api_key: str) -> dict:
    """Use Gemini 2.5 Flash acting as an Expert Cognitive & Psychometric Specialist for Math Students."""
    fallback = offline_smart_psychometric_diagnosis(question, raw_answer, student_steps, error_history)
    if not api_key:
        return fallback


    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        history_summary = json.dumps(error_history[-6:]) if error_history else "None yet (first mistake)"
        scores_summary = json.dumps(st.session_state.get("cognitive_scores", {}))
        prompt = f"""{COGNITIVE_EXPERT_SYSTEM_PROMPT}

---
CASE TO DIAGNOSE:
QUESTION: {question['question_text']}
CORRECT ANSWER: {question['correct_answer_display']}
CONCEPT RULE: {question['concept_rule']}
STUDENT'S SUBMITTED ANSWER: {raw_answer}
STUDENT'S WORKING STEPS: {student_steps or '(not written)'}
SESSION ERROR HISTORY: {history_summary}
CURRENT 4-DOMAIN COGNITIVE SCORES: {scores_summary}

Return ONLY valid JSON with these EXACT keys:
{{
  "primary_pattern": "<psychometric error classification>",
  "secondary_pattern": "<secondary cognitive contributor or None>",
  "confidence": <integer 75-99>,
  "cognitive_domain_impact": "<EXACTLY one of: Schema Encoding, Working Memory, Unit Attention, Number Sense>",
  "affective_signal": "<brief assessment of student confidence / math-anxiety / guessing vs systematic misconception>",
  "child_coach_message": "<warm, encouraging 2-3 sentence metacognitive message spoken directly to the student validating their thinking while gently pointing to the fix>",
  "memory_anchor_trick": "<a super sticky 1-sentence mnemonic or mental image so the student memorizes '{question['concept_rule']}' permanently>",
  "parent_teacher_tip": "<1-2 sentence clinical instructional recommendation for a parent or math teacher>",
  "root_cause": "<2-3 clear sentences diagnosing WHY the student produced '{raw_answer}' instead of '{question['correct_answer_display']}'>",
  "cognitive_load": "<LOW, MEDIUM, or HIGH — concise working-memory explanation>",
  "intervention_type": "<evidence-based cognitive remediation strategy>",
  "error_tags": ["<tag1>", "<tag2>", "<tag3>"],
  "gemini_insight": "<3 concise sentences of expert cognitive-psychometric analysis connecting this error signature to how the student encodes and retrieves math schemas>",
  "recurring_note": "<if session history reveals a cross-question cognitive/psychometric pattern, describe it in 1-2 sentences; otherwise empty string>"
}}"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw = response.text.strip()
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        parsed = json.loads(raw)
        if "primary_pattern" in parsed and "root_cause" in parsed:
            for k, v in fallback.items():
                parsed.setdefault(k, v)
            return parsed
        return fallback

    except Exception:
        return fallback



def get_ai_practice_questions(question: dict, psycho_analysis: dict, api_key: str, force_variation: int = 0) -> list:
    """Use Gemini 2.5 Flash (as Cognitive & Psychometric Specialist) to design 3 memory-encoding similar-concept drills."""
    if not api_key:
        return question["practice_questions"]

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        prompt = f"""{COGNITIVE_EXPERT_SYSTEM_PROMPT}

---
DESIGN TARGETED REMEDIATION DRILLS:
A math student struggled with: {question['topic']} (Core Rule: {question['concept_rule']}).
Psychometric Diagnosis: {psycho_analysis.get('primary_pattern', 'Schema Confusion')}
Taxed Cognitive Domain: {psycho_analysis.get('cognitive_domain_impact', 'Schema Encoding')}
Root Cause: {psycho_analysis.get('root_cause', '')}
Memory Anchor Trick: {psycho_analysis.get('memory_anchor_trick', '')}
Variation seed: {force_variation}

Engineer EXACTLY 3 cognitive-load-scaffolded similar-concept practice questions to overwrite the misconception and lock '{question['concept_rule']}' into long-term memory:
- Question 1 (🟢 Easy · Schema Encoding): isolated single-step conversion in a fun everyday context (cooking, sports, animals).
- Question 2 (🟡 Medium · Guided Transfer): 2-step word problem mirroring the quiz structure with low extraneous cognitive load.
- Question 3 (🔴 Challenge · Mastery Lock): real-world comparison or multi-step problem proving durable transfer.

Each question must have a clean numeric or short-word answer.
Return ONLY a valid JSON array of 3 objects with EXACTLY these keys:
[
  {{
    "q": "<question text>",
    "correct_regex": "<python regex matching the right answer, e.g. \\b24\\b>",
    "correct_answer": "<short clear answer>",
    "explanation": "<1-2 sentence step-by-step explanation reinforcing the rule and memory anchor>",
    "difficulty": "🟢 Easy · Schema Encoding"
  }},
  ...
]"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw = response.text.strip()
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        parsed = json.loads(raw)
        if isinstance(parsed, list) and len(parsed) >= 1 and "q" in parsed[0]:
            return parsed[:3]
        return question["practice_questions"]
    except Exception:
        return question["practice_questions"]


def ask_cognitive_expert(user_question: str, question: dict, psycho_analysis: dict, api_key: str) -> str:
    """Interactive Cognitive & Psychometric Math Specialist consultation."""
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"""{COGNITIVE_EXPERT_SYSTEM_PROMPT}

---
ACTIVE STUDENT CONTEXT:
Question: {question['question_text']}
Core Rule: {question['concept_rule']}
Student's Wrong Answer: {st.session_state.get('last_wrong_answer', '')}
Psychometric Diagnosis: {psycho_analysis.get('primary_pattern', '')} ({psycho_analysis.get('cognitive_domain_impact', '')})
Memory Anchor: {psycho_analysis.get('memory_anchor_trick', '')}
4-Domain Cognitive Scores: {json.dumps(st.session_state.get('cognitive_scores', {}))}

USER (STUDENT / PARENT / TEACHER) ASKS:
"{user_question}"

Respond warmly, clearly, and concisely (3–5 sentences) as Dr. Quanttoria, an expert cognitive scientist and math psychometrician. Give concrete cognitive/memory advice without giving away the answer carelessly unless pedagogically helpful."""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text.strip()
        except Exception:
            pass

    # Smart Offline Cognitive & Psychometric Expert Fallback
    q_low = user_question.lower()
    if any(w in q_low for w in ["memory", "trick", "remember", "mnemonic", "memorize"]):
        return (
            f"🧠 **Memory Encoding Technique (Dr. Quanttoria):** {psycho_analysis.get('memory_anchor_trick', question['concept_rule'])} "
            f"To lock **{question['concept_rule']}** into long-term memory, say it aloud twice while sketching it on the whiteboard — "
            f"dual-coding (visual + verbal) doubles retention!"
        )
    if any(w in q_low for w in ["parent", "teacher", "tip", "clinical", "help my child"]):
        return (
            f"📋 **Clinical Guidance for Parents & Teachers:** {psycho_analysis.get('parent_teacher_tip', '')} "
            f"Right now the taxed cognitive domain is **{psycho_analysis.get('cognitive_domain_impact', 'Schema Encoding')}** "
            f"({psycho_analysis.get('affective_signal', '')}). Keep practice low-pressure and celebrate step-by-step reasoning."
        )
    if any(w in q_low for w in ["why", "mistake", "brain", "wrong", "pattern"]):
        return (
            f"🔬 **Cognitive Mechanism:** {psycho_analysis.get('root_cause', '')} "
            f"In psychometrics we classify this as **{psycho_analysis.get('primary_pattern', '')}**. "
            f"{psycho_analysis.get('child_coach_message', '')}"
        )
    return (
        f"🧠 **Dr. Quanttoria (Cognitive & Psychometric Expert):** Great question! For **{question['short_label']}**, "
        f"focus on one anchor first: **{question['concept_rule']}**. {psycho_analysis.get('memory_anchor_trick', '')} "
        f"Break the work into Step 1 (convert units on the whiteboard) and Step 2 (compute the final value) to keep working-memory load light!"
    )


def match_possible_mistake_id(question: dict, raw_answer: str):
    """Return the ID of the matching possible mistake trap if the student's wrong answer fits one."""
    ans_num = parse_numeric_answer(raw_answer)
    raw_low = (raw_answer or "").lower()
    for pm in question.get("possible_mistakes", []):
        mtype = pm.get("match_type")
        mval = pm.get("match_value")
        if mtype == "contains" and str(mval).lower() in raw_low:
            return pm["id"]
        if mtype == "num" and ans_num is not None:
            if abs(ans_num - float(mval)) < 0.05 or (float(mval) == 50.0 and ans_num < 0):
                return pm["id"]
    return None


def generate_teacher_parent_review_brief(error_log: list, solved_qs: list, cognitive_scores: dict, api_key: str) -> dict:
    """Generate a formal message addressed to Teacher / Parent explaining mistakes, cognitive/psychometric reasons, and analyzed patterns."""
    cache_sig = (len(error_log), tuple(solved_qs), bool(api_key))
    cached = st.session_state.get("teacher_review_cache")
    if cached and cached.get("_sig") == cache_sig:
        return cached

    # Build rich offline/fallback synthesis first
    total_mistakes = len(error_log)
    solved_count = len(solved_qs)
    strongest = max(cognitive_scores.items(), key=lambda x: x[1])
    growth = min(cognitive_scores.items(), key=lambda x: x[1])

    if total_mistakes == 0:
        fallback = {
            "_sig": cache_sig,
            "letter": (
                f"Dear Teacher / Parent,\n\n"
                f"So far, your student has solved {solved_count} of 4 quiz questions with zero recorded mistakes! "
                f"From a cognitive and psychometric standpoint, this indicates solid schema encoding across measurement units, "
                f"dependable working-memory control during multi-step word problems, and attentive reading of target units. "
                f"Even without errors triggered yet, you can review the 'All Possible Mistakes Matrix' below to see the exact "
                f"cognitive traps your student successfully avoided."
            ),
            "pattern_summary": "High First-Try Conceptual Accuracy — No Recurring Cognitive Bottlenecks Observed Yet",
            "cognitive_reasons": [
                "Strong automatic recall of customary and metric conversion anchors (quarts/gallons, oz/lb, m/km, lb/ton).",
                "Low working-memory fatigue: the student successfully carried converted values into the final arithmetic step.",
            ],
            "action_plan": [
                "Introduce multi-unit comparison challenges (e.g., comparing 3 different units at once) to stretch proportional reasoning.",
                "Ask the student to explain 'why' each conversion works aloud to reinforce long-term metacognitive confidence.",
            ],
        }
    else:
        pattern_counts = {}
        domain_counts = {}
        for e in error_log:
            pattern_counts[e["pattern"]] = pattern_counts.get(e["pattern"], 0) + 1
            dom = e.get("domain", "Schema Encoding")
            domain_counts[dom] = domain_counts.get(dom, 0) + 1

        top_pattern, top_pat_cnt = max(pattern_counts.items(), key=lambda x: x[1])
        top_domain = max(domain_counts.items(), key=lambda x: x[1])[0]
        qs_with_errors = sorted(set(e["question_id"] for e in error_log))
        solved_after_str = (
            f"and successfully corrected & solved {', '.join(solved_qs)}"
            if solved_qs
            else "and is currently working through guided practice toward the correct answer"
        )

        reasons = []
        seen_r = set()
        for e in error_log:
            r_txt = f"[{e['question_id']} · Attempt #{e.get('attempt_num', 1)} · Entered '{e['wrong_answer']}'] {e['pattern']}: {e.get('root_cause', '')}"
            if r_txt not in seen_r:
                seen_r.add(r_txt)
                reasons.append(r_txt)

        obs_list = st.session_state.get("step_observations", [])
        obs_note = (
            f" In guided step-by-step practice observations, the student's observed thinking style was "
            f"'{obs_list[-1].get('thinking_style', '')}' ({obs_list[-1].get('cue_responsiveness', '')})."
            if obs_list
            else ""
        )
        fallback = {
            "_sig": cache_sig,
            "letter": (
                f"Dear Teacher / Parent,\n\n"
                f"During this Quanttoria AI Maths session, your student made {total_mistakes} mistake(s) across "
                f"{', '.join(qs_with_errors)} {solved_after_str}. As a cognitive and psychometric specialist, I want to "
                f"reassure you that these errors are NOT signs of low math ability—they follow a very clear, fixable "
                f"cognitive signature!\n\n"
                f"The primary psychometric pattern analyzed by AI is '{top_pattern}' (observed {top_pat_cnt} time(s)), "
                f"most heavily taxing the student's '{top_domain}' domain (current profile: strongest in {strongest[0]} at "
                f"{strongest[1]}%, primary growth focus in {growth[0]} at {growth[1]}%).{obs_note} Using memory cues, worked examples, "
                f"and guided step-by-step practice rapidly rewires this pattern into durable mastery."
            ),
            "pattern_summary": (
                f"Primary Pattern: {top_pattern} ({top_pat_cnt}x) • Most Taxed Cognitive Domain: {top_domain} • "
                f"Cross-Session Profile: Strongest in {strongest[0]} ({strongest[1]}%), Growth Focus in {growth[0]} ({growth[1]}%)"
            ),
            "cognitive_reasons": reasons,
            "action_plan": [
                f"Anchor the missing conversion facts visually using sticky mnemonics before starting word problems (target domain: {top_domain}).",
                "Adopt a 2-Box Whiteboard Habit: Box 1 = 'Convert to the Target Unit', Box 2 = 'Solve the Final Question' to eliminate working-memory drop-offs.",
                "Have the student circle the target unit word (quarts, ounces, meters, pounds) in the question BEFORE doing any arithmetic.",
                "Run a 3-minute spaced-retrieval check in 48 hours on the missed conversion rules to move them into permanent long-term memory.",
            ],
        }

    if not api_key or total_mistakes == 0:
        st.session_state.teacher_review_cache = fallback
        return fallback


    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""{COGNITIVE_EXPERT_SYSTEM_PROMPT}

---
WRITE A FORMAL TEACHER / PARENT COGNITIVE & PSYCHOMETRIC REVIEW:
Solved Questions So Far: {solved_qs} (out of 4)
4-Domain Cognitive Profile: {json.dumps(cognitive_scores)}
Chronological Student Mistake Log (every mistake made before reaching the correct answer):
{json.dumps(error_log, indent=2)}
AI Step-by-Step Thinking Observations (how the student solved steps after Cue + Worked Example):
{json.dumps(st.session_state.get("step_observations", []), indent=2)}

Return ONLY valid JSON with these EXACT keys:
{{
  "letter": "<Warm, authoritative 2-paragraph message starting with 'Dear Teacher / Parent,' summarizing the student's exact mistakes, why their brain made them from cognitive & psychometric science, the pattern analyzed, and reassuring growth framing>",
  "pattern_summary": "<1-2 sentence executive synthesis of the overarching cognitive & psychometric pattern analyzed across all attempts>",
  "cognitive_reasons": ["<concise bullet explaining cognitive/psychometric reason for each distinct mistake>", "..."],
  "action_plan": ["<concrete classroom/home action step 1>", "<action step 2>", "<action step 3>"]
}}"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw = response.text.strip()
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        parsed = json.loads(raw)
        if "letter" in parsed and "pattern_summary" in parsed:
            parsed["_sig"] = cache_sig
            for k, v in fallback.items():
                parsed.setdefault(k, v)
            st.session_state.teacher_review_cache = parsed
            return parsed
    except Exception:
        pass

    st.session_state.teacher_review_cache = fallback
    return fallback



def observe_student_steps(question: dict, step1_text: str, step2_text: str, error_log: list, api_key: str) -> dict:
    """Observe how the student solves Step 1 & Step 2 after seeing the Cue + Worked Example, and study their overall thinking pattern."""
    obs = question["guided_observer"]
    s1_ok = bool(re.search(obs["step1_regex"], step1_text or "", re.IGNORECASE))
    s2_ok = bool(re.search(obs["step2_regex"], step2_text or "", re.IGNORECASE))

    if s1_ok and s2_ok:
        thinking_style = "Cue-Responsive Self-Corrector (Rapid Schema Transfer)"
        cue_responsiveness = "HIGH — Immediately applied the cognitive cue & worked example across both steps!"
        step_feedback = (
            f"🌟 **Awesome Step-by-Step Thinking!** You nailed Step 1 (applying `{question['concept_rule']}`) "
            f"AND carried it cleanly through Step 2! Your brain just built the right pathway—now go back up and solve Question {question['num']}!"
        )
        overall_study = (
            f"After receiving the cue ('{question['concept_rule']}') and a worked example, the student demonstrated rapid "
            f"near-transfer: both unit conversion (Step 1) and final execution (Step 2) were accurate. This confirms the original "
            f"error was a temporary schema/cue gap rather than a deep conceptual deficit."
        )
        ready = True
    elif s1_ok and not s2_ok:
        thinking_style = "Schema-Capable with Step-2 Executive Load"
        cue_responsiveness = "PARTIAL — Applied the unit cue in Step 1, but slipped during the Step 2 operation."
        step_feedback = (
            f"👏 **Great Step 1!** You remembered the cue (`{question['concept_rule']}`)! "
            f"Now double-check **Step 2**: expected flow is `{obs['expected_summary']}`. Take a breath and verify what Step 2 asks you to do with your Step 1 result!"
        )
        overall_study = (
            f"The student responded well to the unit-conversion cue in Step 1, showing intact schema acquisition, "
            f"but showed executive/working-memory friction in Step 2. Breaking problems into two numbered boxes reduces this bottleneck."
        )
        ready = False
    elif not s1_ok and s2_ok:
        thinking_style = "Intuitive Result-First Thinker (Skips Explicit Unit Setup)"
        cue_responsiveness = "MODERATE — Reached the right final result, but skipped writing the explicit Step 1 conversion."
        step_feedback = (
            f"💡 **Sharp instinct on Step 2!** You reached the right conclusion, though your Step 1 didn't show `{question['concept_rule']}` explicitly. "
            f"Writing Step 1 out (`{obs['expected_summary']}`) protects you from sneaky errors on harder multi-step questions!"
        )
        overall_study = (
            f"The student tends to compute intuitively or jump straight to Step 2 without externalizing the Step 1 unit conversion. "
            f"Encouraging brief written unit setups will prevent careless slips under timed exam load."
        )
        ready = True
    else:
        thinking_style = "Persistent Anchor Interference (Needs Visual Scaffolding)"
        cue_responsiveness = "NEEDS REINFORCEMENT — Old schema interfered even after the cue; visual whiteboard + Leo teaching recommended."
        step_feedback = (
            f"🌱 **Good try — let's walk through it together!** Compare your steps with the model: `{obs['expected_summary']}`. "
            f"Click **🍌 Nano Banana Visual** on the right whiteboard to see the picture of `{question['concept_rule']}`, then try the steps once more!"
        )
        overall_study = (
            f"Even immediately after a cue and worked example, the student's steps showed persistent interference from an entrenched "
            f"prior schema. Dual-coding (Nano Banana diagram + speaking the rule aloud to Leo) is recommended before independent retry."
        )
        ready = False

    fallback = {
        "question_id": question["id"],
        "step1_text": step1_text.strip(),
        "step2_text": step2_text.strip(),
        "step1_ok": s1_ok,
        "step2_ok": s2_ok,
        "thinking_style": thinking_style,
        "cue_responsiveness": cue_responsiveness,
        "step_feedback": step_feedback,
        "overall_study": overall_study,
        "ready_for_main": ready,
    }

    if not api_key:
        return fallback


    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""{COGNITIVE_EXPERT_SYSTEM_PROMPT}

---
OBSERVE THE STUDENT'S STEP-BY-STEP SOLVING PROCESS:
Main Quiz Concept: {question['topic']} (Rule: {question['concept_rule']})
Guided Problem Given After Cue + Worked Example: {obs['prompt']}
Expected Model Solution: {obs['expected_summary']}
Student's Step 1 Input: "{step1_text}"
Student's Step 2 Input: "{step2_text}"
Prior Mistakes This Session: {json.dumps(error_log[-5:])}

Carefully observe HOW the student executed Step 1 and Step 2 and study their overall thinking pattern.
Return ONLY valid JSON with these EXACT keys:
{{
  "step1_ok": <true or false>,
  "step2_ok": <true or false>,
  "thinking_style": "<concise 3-6 word label of the student's observed thinking style>",
  "cue_responsiveness": "<HIGH, PARTIAL, or NEEDS REINFORCEMENT — short explanation of how they responded to the cue>",
  "step_feedback": "<warm, encouraging 2-3 sentence feedback directly to the student praising what worked and guiding any slip>",
  "overall_study": "<2-3 sentence clinical cognitive observation of the student's overall thinking pattern for the Teacher/Parent Review>",
  "ready_for_main": <true or false>
}}"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw = response.text.strip()
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        parsed = json.loads(raw)
        if "thinking_style" in parsed and "step_feedback" in parsed:
            parsed["question_id"] = question["id"]
            parsed["step1_text"] = step1_text.strip()
            parsed["step2_text"] = step2_text.strip()
            for k, v in fallback.items():
                parsed.setdefault(k, v)
            return parsed
    except Exception:
        pass
    return fallback



# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
defaults = {
    "current_q_idx": 0,            # 0..3 for Q1..Q4
    "quiz_completed": False,
    "solved_questions": [],        # list of question IDs solved
    "first_try_solved": [],        # question IDs solved with zero mistakes
    "last_success_banner": "",     # green confirmation shown when auto-advancing
    "diagnosis_triggered": False,
    "last_wrong_answer": "",
    "ai_analysis": None,
    "gap_healed": False,
    "teach_explanation": "",
    "show_wb1": False,
    "show_wb2": False,
    "show_nano_banana": False,
    "session_error_log": [],       # list of dicts tracking EVERY wrong attempt across quiz
    "step_observations": [],       # list of dicts tracking AI step-by-step observations & thinking pattern study
    "practice_questions": [],
    "practice_idx": 0,
    "practice_completed_for": [],  # list of question IDs whose 3-drill booster was finished
    "practice_variation": 0,
    "practice_feedback": "",
    "practice_feedback_ok": False,
    "cognitive_scores": {
        "Schema Encoding": 75,
        "Working Memory": 75,
        "Unit Attention": 75,
        "Number Sense": 75,
    },
    "expert_chat_history": [],
    "show_teacher_parent_review": False,
    "teacher_review_cache": None,
    "active_funny_cue": "",
    "voice_enabled": True,
    "speech_nonce": 0,
    "last_spoken_text": "",
    "last_spoken_mood": "cue",
    "just_celebrated": False,
    "question_solved_pending_next": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = dict(v) if isinstance(v, dict) else (list(v) if isinstance(v, list) else v)


def reset_question_ui_state():
    st.session_state.diagnosis_triggered = False
    st.session_state.last_wrong_answer = ""
    st.session_state.ai_analysis = None
    st.session_state.gap_healed = False
    st.session_state.teach_explanation = ""
    st.session_state.show_wb1 = False
    st.session_state.show_wb2 = False
    st.session_state.show_nano_banana = False
    st.session_state.practice_questions = []
    st.session_state.practice_idx = 0
    st.session_state.practice_feedback = ""
    st.session_state.practice_feedback_ok = False
    st.session_state.expert_chat_history = []
    st.session_state.active_funny_cue = ""
    st.session_state.question_solved_pending_next = False


def reset_entire_quiz():
    for k, v in defaults.items():
        st.session_state[k] = dict(v) if isinstance(v, dict) else (list(v) if isinstance(v, list) else v)


# ==========================================
# SIDEBAR: AI STACK & LIVE PSYCHOMETRIC TRACKER
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg", width=155)
    st.markdown("### 🛠️ Quanttoria AI Engine")

    api_key_input = st.text_input(
        "Gemini API Key (Google AI Studio)",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Paste your API key from aistudio.google.com for live Gemini 2.5 Flash psychometric profiling & dynamic practice generation. Without a key, Smart Offline Demo Mode runs automatically.",
    )

    is_live = bool(api_key_input.strip())
    if is_live:
        st.success("🟢 Live Gemini 2.5 Flash Connected")
    else:
        st.info("🟡 Smart Offline AI Mode Active")

    # Quiz Progress Card
    st.markdown("---")
    solved_count = len(st.session_state.solved_questions)
    st.markdown(f"#### 📝 4-Question Quiz Progress ({solved_count}/4)")
    st.progress(solved_count / 4.0)
    for idx, qid in enumerate(QUIZ_ORDER):
        qobj = QUIZ_QUESTIONS[qid]
        if qid in st.session_state.solved_questions:
            st.markdown(f"✅ **{qobj['short_label']}** — Solved")
        elif not st.session_state.quiz_completed and idx == st.session_state.current_q_idx:
            st.markdown(f"🔵 **{qobj['short_label']}** — Active Now")
        else:
            st.markdown(f"🔒 {qobj['short_label']} — Locked until previous solved")

    # Cognitive & Psychometric Profile ONLY revealed after finishing the 4-question quiz!
    if st.session_state.quiz_completed:
        st.markdown("---")
        st.markdown("#### 🧬 Cognitive & Psychometric Profile")
        for domain_name, score in st.session_state.cognitive_scores.items():
            bar_c = "#10B981" if score >= 80 else ("#F59E0B" if score >= 60 else "#EF4444")
            st.markdown(f"""
            <div style="margin-bottom: 7px;">
                <div style="display:flex; justify-content:space-between; font-size:0.76rem; font-weight:700; color:#1E293B;">
                    <span>{domain_name}</span><span>{score}%</span>
                </div>
                <div style="background:#E2E8F0; border-radius:10px; height:7px; overflow:hidden; margin-top:2px;">
                    <div style="width:{score}%; height:100%; background:{bar_c}; border-radius:10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🧠 Detected Psychometric Patterns")
        if st.session_state.session_error_log:
            pattern_counts = {}
            for entry in st.session_state.session_error_log:
                p = entry["pattern"]
                pattern_counts[p] = pattern_counts.get(p, 0) + 1

            for pattern, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
                bar_w = min(count * 35, 100)
                bar_col = "#EF4444" if count >= 2 else "#F59E0B"
                tag = "⚠️ Recurring Pattern!" if count >= 2 else "👀 Detected"
                st.markdown(f"""
                <div style="margin-bottom: 8px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #1E293B;">{pattern}</div>
                    <div style="background: #E2E8F0; border-radius: 10px; height: 7px; overflow: hidden; margin: 3px 0;">
                        <div style="width: {bar_w}%; height: 100%; background: {bar_col}; border-radius: 10px;"></div>
                    </div>
                    <div style="font-size: 0.72rem; color: #64748B;">{count} occurrence{'s' if count > 1 else ''} · {tag}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🌟 Zero bottlenecks detected!")

        st.markdown("---")
        total_err_sb = len(st.session_state.session_error_log)
        tp_btn_label = (
            "⬅️ Back to Quiz Summary"
            if st.session_state.show_teacher_parent_review
            else f"👩‍🏫 Teacher / Parent Review ({total_err_sb})"
        )
        if st.button(tp_btn_label, use_container_width=True, type="primary"):
            st.session_state.show_teacher_parent_review = not st.session_state.show_teacher_parent_review
            st.rerun()
    else:
        st.markdown("---")
        st.caption("🔒 Cognitive & Psychometric Analysis and Teacher / Parent Review unlock automatically after Question 4 is solved!")

    st.markdown("---")
    st.session_state.voice_enabled = st.toggle(
        "🔊 Nobi-Style Kid Voice",
        value=st.session_state.voice_enabled,
        help="Clear, expressive Nobita-style anime kid voice (Microsoft Neural Ana) for cues, hints & cheers!",
    )

    if st.button("🔄 Restart 4-Question Quiz", use_container_width=True):
        reset_entire_quiz()
        st.rerun()

# ==========================================
# TOP HEADER BANNER (STRICTLY CHILD-FRIENDLY!)
# ==========================================
st.markdown("""
<div class="app-header">
    <div class="app-title">
        <span class="pip-mascot">🐥</span>
        <span>🧮 Quanttoria AI Maths</span>
        <span style="font-size: 1rem; font-weight: 500; opacity: 0.9;">| Airport Math Adventure with Pip!</span>
    </div>
    <div class="app-subtitle">
        Solve 4 fun visual challenges! Use your voice or whiteboard, catch blinking hints from Pip, and earn your Math Champion trophy! 🏆✨
    </div>
    <div class="badge-row">
        <span class="tech-badge">🐥 Pip Cartoon Voice Buddy</span>
        <span class="tech-badge">🎙️ Speech-to-Text Ready</span>
        <span class="tech-badge">✨ Blinking Visual Hints</span>
        <span class="tech-badge">📋 Fun Drawing Whiteboard</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4-QUESTION VISUAL STEPPER BAR (TEACHER/PARENT REVIEW UNLOCKS AFTER Q4!)
# ==========================================
stepper_html = '<div class="quiz-stepper" style="margin-bottom: 0;">'
for idx, qid in enumerate(QUIZ_ORDER):
    qobj = QUIZ_QUESTIONS[qid]
    is_solved = qid in st.session_state.solved_questions
    is_active = (not st.session_state.quiz_completed) and (idx == st.session_state.current_q_idx)
    if is_solved:
        cls = "step-pill solved"
        icon = "✅"
    elif is_active:
        cls = "step-pill active"
        icon = "🔵"
    else:
        cls = "step-pill"
        icon = "🔒"
    stepper_html += f'<div class="{cls}">{icon} {qobj["short_label"]}</div>'
stepper_html += "</div>"

if st.session_state.quiz_completed:
    step_col, review_btn_col = st.columns([4, 1.5], vertical_alignment="center")
    with step_col:
        st.markdown(stepper_html, unsafe_allow_html=True)
    with review_btn_col:
        err_cnt_top = len(st.session_state.session_error_log)
        top_tp_label = (
            "⬅️ Back to Quiz Summary"
            if st.session_state.show_teacher_parent_review
            else f"👩‍🏫 Teacher / Parent Review ({err_cnt_top})"
        )
        if st.button(top_tp_label, use_container_width=True, type="primary", key="top_tp_review_btn"):
            st.session_state.show_teacher_parent_review = not st.session_state.show_teacher_parent_review
            st.rerun()
else:
    st.markdown(stepper_html, unsafe_allow_html=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ==========================================
# DEDICATED TEACHER / PARENT COGNITIVE & PSYCHOMETRIC REVIEW VIEW (END OF QUIZ ONLY)
# ==========================================
if st.session_state.quiz_completed and st.session_state.show_teacher_parent_review:
    with st.spinner("🧠 Dr. Quanttoria preparing Teacher / Parent Cognitive & Psychometric Review..."):
        tp_brief = generate_teacher_parent_review_brief(
            st.session_state.session_error_log,
            st.session_state.solved_questions,
            st.session_state.cognitive_scores,
            api_key_input.strip(),
        )

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 60%, #312E81 100%); border-radius: 16px; padding: 24px 28px; color: white; margin-bottom: 18px; border: 2px solid #6366F1; box-shadow: 0 10px 28px rgba(49, 46, 129, 0.28);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div style="font-family: 'Fredoka', cursive; font-size: 1.7rem; font-weight: 700;">
                👩‍🏫👨‍👩‍👧 Teacher / Parent Cognitive & Psychometric Review
            </div>
            <span style="background: rgba(129, 140, 248, 0.28); border: 1px solid #818CF8; padding: 4px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 700;">
                Dr. Quanttoria • {'Gemini 2.5 Flash Live' if is_live else 'Cognitive & Psychometric Engine'}
            </span>
        </div>
        <div style="color: #C7D2FE; font-size: 0.94rem; margin-top: 6px;">
            <b>Quiz Progress:</b> {len(st.session_state.solved_questions)}/4 Solved &nbsp;•&nbsp;
            <b>Total Mistakes Logged Before Correct Answers:</b> {len(st.session_state.session_error_log)} &nbsp;•&nbsp;
            <b>First-Try Solved:</b> {len(st.session_state.first_try_solved)}/4
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Message Addressed Directly to Teacher / Parent
    letter_html = tp_brief["letter"].replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
    st.markdown(f"""
    <div style="background: #FFFBEB; border: 2px solid #F59E0B; border-left: 8px solid #D97706; border-radius: 14px; padding: 20px 24px; margin-bottom: 18px; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.14);">
        <div style="font-size: 1.12rem; font-weight: 800; color: #92400E; margin-bottom: 10px;">
            💌 AI Message Addressed to Teacher / Parent
        </div>
        <div style="color: #451A03; font-size: 0.97rem; line-height: 1.65;">
            {letter_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    tp_left, tp_right = st.columns([1.15, 1], gap="large")

    with tp_left:
        # 2. Pattern Analyzed by AI
        st.markdown("### 🔬 Pattern Analyzed by AI (Cognitive & Psychometric Synthesis)")
        bars_html = ""
        for d_name, d_score in st.session_state.cognitive_scores.items():
            b_col = "#34D399" if d_score >= 80 else ("#FBBF24" if d_score >= 60 else "#F87171")
            bars_html += f"""
            <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:0.84rem; font-weight:700; color:#E0E7FF;">
                    <span>{d_name}</span><span>{d_score}%</span>
                </div>
                <div style="background:rgba(255,255,255,0.12); border-radius:10px; height:8px; overflow:hidden; margin-top:3px;">
                    <div style="width:{d_score}%; height:100%; background:{b_col}; border-radius:10px;"></div>
                </div>
            </div>"""

        st.markdown(f"""
        <div class="psycho-card">
            <div class="psycho-title">📊 Overarching Pattern & 4-Domain Cognitive Profile</div>
            <div class="insight-box" style="margin-top: 0; margin-bottom: 14px;">
                <b>🎯 Pattern Analyzed:</b> {tp_brief['pattern_summary']}
            </div>
            {bars_html}
        </div>
        """, unsafe_allow_html=True)

        # 3. Chronological Log of Every Mistake Made Until Correct Answer + AI Reasons
        st.markdown("### 📝 Every Mistake Made Before Entering Correct Answer & AI's Reasons")
        if st.session_state.session_error_log:
            for idx, entry in enumerate(st.session_state.session_error_log, 1):
                q_meta = QUIZ_QUESTIONS[entry["question_id"]]
                solved_badge = (
                    "<span style='background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:10px;font-size:0.74rem;font-weight:700;'>✅ Later Solved Correctly</span>"
                    if entry["question_id"] in st.session_state.solved_questions
                    else "<span style='background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:10px;font-size:0.74rem;font-weight:700;'>⏳ Still Solving</span>"
                )
                steps_line = (
                    f"<br/><b>Student Working Written:</b> <code>{entry['student_steps']}</code>"
                    if entry.get("student_steps")
                    else ""
                )
                st.markdown(f"""
                <div style="background:#FFFFFF; border:2px solid #FCA5A5; border-left:6px solid #EF4444; border-radius:12px; padding:14px 16px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:6px;">
                        <span style="font-weight:800; color:#991B1B;">Mistake #{idx} • {q_meta['short_label']} (Attempt #{entry.get('attempt_num', 1)})</span>
                        {solved_badge}
                    </div>
                    <div style="font-size:0.9rem; color:#1E293B; line-height:1.55;">
                        <b>Student Entered:</b> <code style="background:#FEE2E2;color:#991B1B;padding:2px 6px;border-radius:4px;">{entry['wrong_answer']}</code>
                        &nbsp;→&nbsp; <b>Correct Answer:</b> <code style="background:#D1FAE5;color:#065F46;padding:2px 6px;border-radius:4px;">{q_meta['correct_answer_display']}</code>{steps_line}<br/>
                        <b>Psychometric Pattern:</b> <span style="color:#B91C1C;font-weight:700;">{entry['pattern']}</span> &nbsp;|&nbsp;
                        <b>Taxed Cognitive Domain:</b> <span style="color:#4338CA;font-weight:700;">{entry.get('domain', 'Schema Encoding')}</span><br/>
                        <b>Cognitive & Psychometric Reason:</b> {entry.get('root_cause', '')}<br/>
                        <b>Working-Memory Load & Signal:</b> {entry.get('cognitive_load', 'MEDIUM')} · <i>{entry.get('affective_signal', '')}</i>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🌟 No mistakes have been recorded yet! Once the student makes any wrong attempt (or finishes the quiz), every attempt and cognitive reason appears here.")

        # 3b. AI Step-by-Step Observations & Overall Thinking Pattern Study
        if st.session_state.step_observations:
            st.markdown("### 👁️ AI Step-by-Step Observation & Overall Thinking Pattern Study")
            for o_idx, ob in enumerate(st.session_state.step_observations, 1):
                q_m = QUIZ_QUESTIONS[ob["question_id"]]
                s1_icon = "✅" if ob.get("step1_ok") else "⚠️"
                s2_icon = "✅" if ob.get("step2_ok") else "⚠️"
                st.markdown(f"""
                <div class="observer-card">
                    <div style="font-weight: 800; color: #0E7490; font-size: 0.96rem; margin-bottom: 6px;">
                        👁️ Observation #{o_idx} • {q_m['short_label']} &nbsp;—&nbsp;
                        <span style="background:#0891B2;color:white;padding:2px 9px;border-radius:10px;font-size:0.76rem;">{ob.get('thinking_style', '')}</span>
                    </div>
                    <div style="font-size: 0.87rem; color: #164E63; line-height: 1.55;">
                        <b>{s1_icon} Step 1 Observed:</b> <code>{ob.get('step1_text') or '(blank)'}</code><br/>
                        <b>{s2_icon} Step 2 Observed:</b> <code>{ob.get('step2_text') or '(blank)'}</code><br/>
                        <b>Cue Responsiveness:</b> {ob.get('cue_responsiveness', '')}<br/>
                        <b>Overall Thinking Pattern Study:</b> {ob.get('overall_study', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # 4. Recommended Action Plan for Teacher / Parent
        st.markdown("### 🎯 Recommended Action Plan for Teacher / Parent")
        for step_i, act in enumerate(tp_brief.get("action_plan", []), 1):
            st.markdown(f"""
            <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-left:5px solid #10B981; border-radius:10px; padding:10px 14px; margin-bottom:8px; color:#065F46; font-size:0.9rem;">
                <b>Step {step_i}:</b> {act}
            </div>
            """, unsafe_allow_html=True)

    with tp_right:
        # 5. All Possible Mistakes Matrix Across All 4 Questions
        st.markdown("### 🗺️ All Possible Mistakes Matrix (Student Traps vs Avoided)")
        st.caption("Shows every classic psychometric mistake a student can make on each question and flags the exact ones your student hit before entering the correct answer:")

        triggered_ids = {e.get("matched_trap_id") for e in st.session_state.session_error_log if e.get("matched_trap_id")}

        for qid in QUIZ_ORDER:
            qobj = QUIZ_QUESTIONS[qid]
            q_errs = [e for e in st.session_state.session_error_log if e["question_id"] == qid]
            q_status = "✅ Solved" if qid in st.session_state.solved_questions else "⏳ Not Solved Yet"
            with st.expander(
                f"{qobj['short_label']} — {q_status} ({len(q_errs)} mistake{'s' if len(q_errs) != 1 else ''} logged)",
                expanded=(len(q_errs) > 0 or qid == QUIZ_ORDER[st.session_state.current_q_idx]),
            ):
                st.markdown(f"**Core Concept Rule:** `{qobj['concept_rule']}` · **Correct Answer:** `{qobj['correct_answer_display']}`")
                for pm in qobj.get("possible_mistakes", []):
                    hit = pm["id"] in triggered_ids
                    if hit:
                        border_c = "#EF4444"
                        bg_c = "#FEF2F2"
                        badge_html = "<span style='background:#DC2626;color:white;padding:2px 8px;border-radius:10px;font-size:0.72rem;font-weight:700;'>🔴 STUDENT HIT THIS MISTAKE</span>"
                    elif qid in st.session_state.solved_questions:
                        border_c = "#10B981"
                        bg_c = "#F0FDF4"
                        badge_html = "<span style='background:#059669;color:white;padding:2px 8px;border-radius:10px;font-size:0.72rem;font-weight:700;'>✅ AVOIDED</span>"
                    else:
                        border_c = "#CBD5E1"
                        bg_c = "#F8FAFC"
                        badge_html = "<span style='background:#64748B;color:white;padding:2px 8px;border-radius:10px;font-size:0.72rem;font-weight:700;'>⚪ POSSIBLE TRAP</span>"

                    st.markdown(f"""
                    <div style="background:{bg_c}; border:1.5px solid {border_c}; border-radius:10px; padding:10px 13px; margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:4px;">
                            <span style="font-weight:700; color:#0F172A; font-size:0.86rem;">{pm['title']}</span>
                            {badge_html}
                        </div>
                        <div style="font-size:0.82rem; color:#334155; line-height:1.45;">
                            <b>Pattern:</b> <code>{pm['pattern']}</code> ({pm['domain']})<br/>
                            <b>Why Students Make It:</b> {pm['cognitive_reason']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("⬅️ Back to Quiz Complete Summary", type="primary", use_container_width=True, key="bottom_back_quiz"):
        st.session_state.show_teacher_parent_review = False
        st.rerun()
    st.stop()

# ==========================================
# QUIZ COMPLETED: BIG CHILD-FRIENDLY CELEBRATION + COMPACT USP ANALYSIS SECTION
# ==========================================
if st.session_state.quiz_completed:
    st.balloons()
    first_try_cnt = len(st.session_state.first_try_solved)
    total_errors = len(st.session_state.session_error_log)

    # 1. Dominant Child-Friendly Victory Celebration + Pip's Cartoon Voice Cheer!
    st.markdown(f"""
    <div class="healed-alert-box" style="text-align: center; padding: 28px; border-width: 3px;">
        <div style="display:flex; justify-content:center; align-items:center; gap:14px; margin-bottom:8px;">
            <span class="pip-mascot">🐥</span>
            <span style="font-size: 3rem;">🏆</span>
            <span style="font-size: 2.4rem;">🎉</span>
        </div>
        <div style="font-family: 'Fredoka', cursive; font-size: 2.05rem; font-weight: 700; color: #065F46;">
            WOOHOO!! You Beat All 4 Airport Math Challenges!
        </div>
        <div style="color: #047857; font-size: 1.05rem; margin-top: 8px; font-weight: 600;">
            ⭐ <b>4 / 4 Missions Completed!</b> &nbsp;•&nbsp;
            🚀 <b>Super-Speed First-Try Wins:</b> {first_try_cnt} / 4 &nbsp;•&nbsp;
            🏅 <b>Official Quanttoria Math Champion!</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    render_cartoon_voice_player(
        CONGRATS_LINES["Q4"],
        enabled=st.session_state.voice_enabled,
        nonce=st.session_state.speech_nonce,
        mood="cheer",
    )

    # Child-friendly unlocked badges row
    st.markdown("### 🎖️ Your Unlocked Superpower Rules!")
    b_cols = st.columns(4)
    for b_idx, qid in enumerate(QUIZ_ORDER):
        qobj = QUIZ_QUESTIONS[qid]
        with b_cols[b_idx]:
            st.markdown(f"""
            <div style="background: #F0FDF4; border: 2px solid #34D399; border-radius: 14px; padding: 12px; text-align: center; height: 100%;">
                <div style="font-size: 1.4rem;">⭐</div>
                <div style="font-weight: 800; color: #065F46; font-size: 0.9rem;">{qobj['short_label']}</div>
                <div style="font-size: 0.8rem; color: #047857; font-family: 'Fira Code', monospace; margin-top: 4px; font-weight: 700;">
                    {qobj['concept_rule']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 2. Compact, Sophisticated USP Section (NOT dominating the child's view — Quanttoria's World-First Differentiator!)
    strongest = max(st.session_state.cognitive_scores.items(), key=lambda x: x[1])
    growth = min(st.session_state.cognitive_scores.items(), key=lambda x: x[1])
    if st.session_state.session_error_log:
        pattern_summary = {}
        for e in st.session_state.session_error_log:
            pattern_summary[e["pattern"]] = pattern_summary.get(e["pattern"], 0) + 1
        top_pattern = max(pattern_summary.items(), key=lambda x: x[1])[0]
        usp_line = (
            f"<b>Pattern Studied:</b> {top_pattern} ({total_errors} attempt{'s' if total_errors != 1 else ''} analyzed) &nbsp;•&nbsp; "
            f"<b>Top Strength:</b> {strongest[0]} ({strongest[1]}%) &nbsp;•&nbsp; "
            f"<b>Growth Focus:</b> {growth[0]} ({growth[1]}%)"
        )
    else:
        usp_line = (
            f"🌟 <b>Flawless Mastery!</b> Zero misconceptions across all 4 challenges — "
            f"<b>Top Strength:</b> {strongest[0]} ({strongest[1]}%)"
        )

    pills_html = "".join(
        f'<span class="domain-pill">{d}: {s}%</span>'
        for d, s in st.session_state.cognitive_scores.items()
    )

    st.markdown(f"""
    <div class="usp-compact-card">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:6px;">
            <div style="font-size:0.96rem; font-weight:800; color:#A5B4FC;">
                ✨ Quanttoria's Unique USP — AI Cognitive & Psychometric Snapshot
            </div>
            <span style="font-size:0.74rem; background:rgba(99,102,241,0.3); border:1px solid #818CF8; padding:2px 10px; border-radius:12px; color:#E0E7FF;">
                Powered by Dr. Quanttoria AI
            </span>
        </div>
        <div style="font-size:0.86rem; color:#E0E7FF; margin-bottom:8px;">{usp_line}</div>
        <div>{pills_html}</div>
    </div>
    """, unsafe_allow_html=True)

    act_c1, act_c2 = st.columns([1.4, 1])
    with act_c1:
        if st.button("👩‍🏫 Open Teacher / Parent Cognitive & Psychometric Review", type="primary", use_container_width=True, key="final_tp_review"):
            st.session_state.show_teacher_parent_review = True
            st.rerun()
    with act_c2:
        if st.button("🔁 Play the 4-Question Adventure Again!", use_container_width=True):
            reset_entire_quiz()
            st.rerun()

    # Optional Post-Quiz Fun Practice Booster (collapsed cleanly so it never overwhelms!)
    missed_qids = list(dict.fromkeys(e["question_id"] for e in st.session_state.session_error_log))
    if missed_qids:
        with st.expander("🎯 Bonus Fun Practice (Strengthen Your Superpowers!)", expanded=False):
            chosen_drill_qid = st.radio(
                "Pick a superpower to practice:",
                options=missed_qids,
                format_func=lambda q: f"{QUIZ_QUESTIONS[q]['short_label']} ({QUIZ_QUESTIONS[q]['concept_rule']})",
                horizontal=True,
                key="post_drill_sel",
            )
            drill_q = QUIZ_QUESTIONS[chosen_drill_qid]
            for d_i, pq in enumerate(drill_q["practice_questions"], 1):
                st.markdown(f"**{pq['difficulty']} — Practice {d_i}:** {pq['q']}")
                u_ans = st.text_input("Your Answer:", key=f"post_pq_{chosen_drill_qid}_{d_i}", placeholder="Type answer...")
                c_a, c_b = st.columns(2)
                with c_a:
                    if st.button(f"✅ Check Practice {d_i}", key=f"chk_post_{chosen_drill_qid}_{d_i}", use_container_width=True):
                        if re.search(pq["correct_regex"], u_ans or "", re.IGNORECASE):
                            st.success(f"🎉 Woohoo! Spot on! {pq['explanation']}")
                        else:
                            st.warning(f"Almost! Answer: **{pq['correct_answer']}** — {pq['explanation']}")
                with c_b:
                    if st.button("💡 Show Trick", key=f"exp_post_{chosen_drill_qid}_{d_i}", use_container_width=True):
                        st.info(f"**Answer:** {pq['correct_answer']}  \n{pq['explanation']}")
                st.markdown("---")

    st.stop()


# ==========================================
# ACTIVE QUESTION CONTEXT
# ==========================================
current_qid = QUIZ_ORDER[st.session_state.current_q_idx]
problem = QUIZ_QUESTIONS[current_qid]

# ==========================================
# 50/50 TWO-PANEL SPLIT SCREEN LAYOUT
# ==========================================
left_col, right_col = st.columns([1, 1], gap="large")

# ==========================================
# LEFT PANEL: Question Image + Solution Steps & Next Button (on Correct) OR Cue + Answer Box
# ==========================================
with left_col:
    st.markdown(f"""
    <div class="question-frame-header">
        <span>🖼️ Mission {problem['num']} of 4 &nbsp;•&nbsp; {problem['short_label']}</span>
        <span style="background: #FFFFFF; color: #4338CA; padding: 2px 10px; border-radius: 12px; font-size: 0.78rem; border: 1px solid #C7D2FE;">
            {problem['topic']}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Display Question Image — BLINKS & HIGHLIGHTS THE EXACT HINT AREA WHEN A MISTAKE IS MADE!
    if problem.get("image_file") and os.path.exists(problem["image_file"]):
        render_question_image_with_blink(
            problem["image_file"],
            problem.get("blink_boxes", []),
            show_blink=(st.session_state.diagnosis_triggered and not st.session_state.question_solved_pending_next),
        )
    else:
        st.info(problem["question_text"])

    # ==========================================================
    # STATE A: QUESTION SOLVED → SHOW CONGRATS + SOLUTION STEPS & FORMULA + PIP VOICE + NEXT BUTTON!
    # ==========================================================
    if st.session_state.question_solved_pending_next:
        if st.session_state.just_celebrated:
            st.balloons()
            st.session_state.just_celebrated = False

        st.markdown(f"""
        <div class="healed-alert-box" style="border-width: 3px;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                <span class="pip-mascot" style="width:46px;height:46px;font-size:1.7rem;">🐥</span>
                <div>
                    <div class="healed-alert-title" style="margin-bottom:2px;">🎉 THAT'S CORRECT!! AWESOME JOB!</div>
                    <div style="color:#047857; font-size:0.9rem; font-weight:600;">
                        Look at the magic formula & solution steps Pip is explaining before you click Next:
                    </div>
                </div>
            </div>
            <div style="background:#FFFFFF; border:2px solid #34D399; border-radius:12px; padding:14px 16px; color:#0F172A; font-size:0.93rem; line-height:1.65;">
                <div style="background:#EEF2FF; color:#3730A3; display:inline-block; padding:3px 12px; border-radius:8px; font-weight:800; font-family:'Fira Code',monospace; margin-bottom:8px;">
                    📐 Formula: {problem['concept_rule']}
                </div><br/>
                <b>① Step 1 (Apply Formula):</b> <span style="font-family:'Fira Code',monospace; color:#1D4ED8; font-weight:700;">{problem['wb1']}</span><br/>
                <b>② Step 2 (Solve & Check):</b> <span style="font-family:'Fira Code',monospace; color:#047857; font-weight:700;">{problem['wb2']}</span><br/>
                <b>✅ Final Answer:</b> <span style="background:#D1FAE5; color:#065F46; padding:2px 8px; border-radius:6px; font-weight:800;">{problem['correct_answer_display']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Speak congratulations + exact formula & solution steps aloud in crystal-clear Nobita-style kid voice!
        render_cartoon_voice_player(
            SOLUTION_SPEECH.get(current_qid, CONGRATS_LINES.get(current_qid, "Awesome job!")),
            enabled=st.session_state.voice_enabled,
            nonce=st.session_state.speech_nonce,
            mood="cheer",
        )

        is_last_q = st.session_state.current_q_idx >= len(QUIZ_ORDER) - 1
        next_btn_label = (
            "🏆 FINISH QUIZ & CLAIM MY TROPHY!"
            if is_last_q
            else f"➡️ NEXT QUESTION (Mission {problem['num'] + 1} of 4)"
        )
        if st.button(next_btn_label, type="primary", use_container_width=True, key=f"next_q_btn_{current_qid}"):
            if not is_last_q:
                st.session_state.current_q_idx += 1
                reset_question_ui_state()
                st.rerun()
            else:
                st.session_state.speech_nonce += 1
                st.session_state.quiz_completed = True
                reset_question_ui_state()
                st.rerun()

    # ==========================================================
    # STATE B: STUDENT STILL SOLVING → SHOW BLINKING CUE (ON MISTAKE) + SPEECH-TO-TEXT + ANSWER BOX
    # ==========================================================
    else:
        # ONLY show Pip's funny 2-liner age-friendly cue + Clear Kid Voice when a mistake is made!
        if st.session_state.diagnosis_triggered and st.session_state.active_funny_cue:
            st.markdown(f"""
            <div class="funny-cue-box" style="display:flex; gap:12px; align-items:flex-start;">
                <div class="pip-mascot">🐥</div>
                <div>
                    <div class="funny-cue-title">😜 Slow Down & Peek at the Blinking Hint Above!</div>
                    <div class="funny-cue-text">{st.session_state.active_funny_cue}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            render_cartoon_voice_player(
                st.session_state.active_funny_cue,
                enabled=st.session_state.voice_enabled,
                nonce=st.session_state.speech_nonce,
                mood="cue",
            )

        # Speech-to-Text Voice Input Widget (Talk to Buddy!)
        st.markdown("#### 🎙️ Speak or Type Your Answer")
        render_speech_to_text_mic(current_qid, problem.get("unit_label", ""))

        # Answer Submission Box
        if problem["input_type"] == "mcq":
            student_answer = st.radio(
                "Pick the right option from the picture above:",
                options=problem["options"],
                index=None,
                key=f"mcq_{current_qid}",
            )
        else:
            ans_c1, ans_c2 = st.columns([3, 1])
            with ans_c1:
                student_answer = st.text_input(
                    f"Enter your answer (in {problem['unit_label']}):",
                    value="",
                    placeholder=f"Type number in {problem['unit_label']}...",
                    key=f"num_{current_qid}",
                )
            with ans_c2:
                st.markdown(
                    f"<div style='padding-top: 34px; font-weight: 800; font-size: 1.15rem; color: #1E293B;'>{problem['unit_label']}</div>",
                    unsafe_allow_html=True,
                )

        student_steps = st.text_area(
            "Optional — Jot down your quick math thought (or draw on the whiteboard!):",
            value="",
            placeholder="e.g., How did you work it out?",
            height=60,
            key=f"steps_{current_qid}",
        )

        submit_btn = st.button(
            f"🚀 Check My Answer for Mission {problem['num']}!",
            use_container_width=True,
            type="primary",
        )

        if submit_btn:
            if not student_answer or not str(student_answer).strip():
                st.warning("🐥 Oops! Pick or type an answer first!")
            else:
                is_correct = check_answer_correct(problem, str(student_answer))
                if is_correct:
                    # Mark solved & silently update cognitive profile for end-of-quiz USP report
                    st.session_state.teacher_review_cache = None
                    if current_qid not in st.session_state.solved_questions:
                        st.session_state.solved_questions.append(current_qid)
                    had_error = any(e["question_id"] == current_qid for e in st.session_state.session_error_log)
                    if not had_error:
                        if current_qid not in st.session_state.first_try_solved:
                            st.session_state.first_try_solved.append(current_qid)
                        update_cognitive_scores("first_try_correct")
                    else:
                        taxed = (st.session_state.ai_analysis or {}).get("cognitive_domain_impact")
                        update_cognitive_scores("healed_correct", domain=taxed)

                    # Pause on THIS question to display & speak Congratulations + Formula + Solution Steps + NEXT button!
                    st.session_state.diagnosis_triggered = False
                    st.session_state.question_solved_pending_next = True
                    st.session_state.speech_nonce += 1
                    st.session_state.last_spoken_text = SOLUTION_SPEECH.get(current_qid, CONGRATS_LINES.get(current_qid, ""))
                    st.session_state.last_spoken_mood = "cheer"
                    st.session_state.just_celebrated = True
                    st.rerun()
                else:
                    # Wrong answer → SILENTLY log & analyze cognitive/psychometric pattern for end of quiz,
                    # and show ONLY the funny 2-liner cue + clear kid voice + blink the hint in the image!
                    st.session_state.diagnosis_triggered = True
                    st.session_state.last_wrong_answer = str(student_answer)

                    with st.spinner("🐥 Lighting up a blinking clue for you..."):
                        analysis = get_ai_psychometric_analysis(
                            problem,
                            str(student_answer),
                            student_steps,
                            st.session_state.session_error_log,
                            api_key_input.strip(),
                        )
                        st.session_state.ai_analysis = analysis
                        cue_txt = get_funny_two_liner_cue(
                            problem, str(student_answer), api_key_input.strip()
                        )
                        st.session_state.active_funny_cue = cue_txt
                        st.session_state.speech_nonce += 1
                        st.session_state.last_spoken_text = cue_txt
                        st.session_state.last_spoken_mood = "cue"

                    attempt_num = sum(1 for e in st.session_state.session_error_log if e["question_id"] == current_qid) + 1
                    matched_trap_id = match_possible_mistake_id(problem, str(student_answer))
                    st.session_state.session_error_log.append({
                        "question_id": current_qid,
                        "attempt_num": attempt_num,
                        "wrong_answer": str(student_answer),
                        "student_steps": (student_steps or "").strip(),
                        "matched_trap_id": matched_trap_id,
                        "pattern": analysis.get("primary_pattern", "Schema Confusion"),
                        "secondary_pattern": analysis.get("secondary_pattern", ""),
                        "domain": analysis.get("cognitive_domain_impact", "Schema Encoding"),
                        "root_cause": analysis.get("root_cause", ""),
                        "cognitive_load": analysis.get("cognitive_load", "MEDIUM"),
                        "affective_signal": analysis.get("affective_signal", ""),
                        "parent_teacher_tip": analysis.get("parent_teacher_tip", ""),
                        "rule": problem["concept_rule"],
                    })
                    st.session_state.teacher_review_cache = None
                    update_cognitive_scores("error", domain=analysis.get("cognitive_domain_impact"))
                    st.rerun()


# ==========================================
# RIGHT PANEL: Classroom Whiteboard + Nano Banana + Stylus Canvas
# ==========================================
with right_col:
    st.markdown("""
    <div style="background: #FFFFFF; border: 2px solid #CBD5E1; border-radius: 14px; padding: 14px 18px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-family: 'Fredoka', cursive; font-size: 1.35rem; color: #1E293B; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                <span>📋</span> Interactive Classroom Whiteboard
            </div>
            <span style="background: #EEF2FF; color: #4F46E5; font-size: 0.78rem; font-weight: 700; padding: 3px 10px; border-radius: 12px; border: 1px solid #C7D2FE;">
                Live Stylus & Math Canvas
            </span>
        </div>
        <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">
            Work out your calculations on the board below, or reveal step-by-step hints & visual diagrams:
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_wb1, col_wb2, col_nb = st.columns(3)
    with col_wb1:
        if st.button("🔍 Hint 1 (Magic Rule)", use_container_width=True):
            st.session_state.show_wb1 = not st.session_state.show_wb1
            if st.session_state.show_wb1:
                st.session_state.speech_nonce += 1
    with col_wb2:
        if st.button("🎯 Hint 2 (Step 2)", use_container_width=True):
            st.session_state.show_wb2 = not st.session_state.show_wb2
            if st.session_state.show_wb2:
                st.session_state.speech_nonce += 1
    with col_nb:
        if st.button("🍌 Picture Clue!", use_container_width=True, type="primary"):
            st.session_state.show_nano_banana = not st.session_state.show_nano_banana

    if st.session_state.show_wb1:
        st.markdown(f"""
        <div class="wb-step-card">
            <span style="background: #DBEAFE; color: #1D4ED8; font-weight: 700; font-size: 0.74rem; padding: 2px 8px; border-radius: 4px;">
                🐥 PIP'S MAGIC RULE HINT (STEP 1)
            </span>
            <div style="font-size: 1.15rem; font-weight: 700; color: #1E40AF; margin-top: 8px;">
                {problem['wb1']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        render_cartoon_voice_player(
            f"Psst! Magic rule alert! {problem['wb1'].replace('⟹', ', which means ')}",
            enabled=st.session_state.voice_enabled,
            nonce=st.session_state.speech_nonce + 1000,
            mood="cue",
        )

    if st.session_state.show_wb2:
        st.markdown(f"""
        <div class="wb-step-card wb2">
            <span style="background: #D1FAE5; color: #047857; font-weight: 700; font-size: 0.74rem; padding: 2px 8px; border-radius: 4px;">
                🐥 PIP'S FINAL STEP HINT (STEP 2)
            </span>
            <div style="font-size: 1.15rem; font-weight: 700; color: #065F46; margin-top: 8px;">
                {problem['wb2']}
            </div>
            <div style="font-size: 0.84rem; color: #475569; margin-top: 4px;">
                ✅ <b>Check:</b> {problem['correct_wb2_math']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        render_cartoon_voice_player(
            f"Here comes step two! {problem['wb2'].replace('⟹', ', so ')}",
            enabled=st.session_state.voice_enabled,
            nonce=st.session_state.speech_nonce + 2000,
            mood="cue",
        )

    if problem.get("solution_image_file") and os.path.exists(problem["solution_image_file"]):
        if st.checkbox("📖 View Teacher Solution Board", value=False, key=f"sol_img_{current_qid}"):
            st.image(problem["solution_image_file"], caption="Whiteboard Solution Guide", use_container_width=True)

    # NANO BANANA VISUAL AID (TAILORED TO EACH OF THE 4 QUESTIONS)
    if st.session_state.show_nano_banana:
        st.markdown("""
        <div style="background: #FFFBEB; border: 2px solid #F59E0B; border-radius: 12px; padding: 12px; margin-bottom: 12px;">
            <div style="font-weight: 700; color: #B45309; display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span>🍌</span> Nano Banana Visual Concept Diagram
            </div>
        """, unsafe_allow_html=True)

        if current_qid == "Q1":
            svg_diagram = """
            <svg viewBox="0 0 760 275" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#0F172A; border-radius: 10px; font-family: 'Inter', sans-serif;">
                <rect x="35" y="28" width="215" height="190" rx="14" fill="#EAB308" stroke="#CA8A04" stroke-width="4"/>
                <text x="62" y="68" fill="#713F12" font-size="15" font-weight="800">BARREL OPTION</text>
                <text x="62" y="114" fill="#1E293B" font-size="28" font-weight="800">16 QUARTS</text>
                <text x="62" y="150" fill="#854D0E" font-size="14">Single Fuel Drum</text>
                <text x="62" y="192" fill="#422006" font-size="13" font-weight="700">Total: 16 Quarts</text>

                <text x="295" y="138" fill="#38BDF8" font-size="44" font-weight="900">=</text>
                <text x="282" y="166" fill="#94A3B8" font-size="12" font-weight="700">EXACTLY EQUAL</text>

                <g transform="translate(385, 28)">
                    <rect x="0" y="0" width="72" height="92" rx="8" fill="#38BDF8" stroke="#0284C7" stroke-width="2"/>
                    <text x="14" y="42" fill="#0C4A6E" font-size="14" font-weight="800">1 GAL</text>
                    <text x="12" y="68" fill="#FFFFFF" font-size="12" font-weight="700">4 qt</text>

                    <rect x="86" y="0" width="72" height="92" rx="8" fill="#38BDF8" stroke="#0284C7" stroke-width="2"/>
                    <text x="100" y="42" fill="#0C4A6E" font-size="14" font-weight="800">1 GAL</text>
                    <text x="98" y="68" fill="#FFFFFF" font-size="12" font-weight="700">4 qt</text>

                    <rect x="172" y="0" width="72" height="92" rx="8" fill="#38BDF8" stroke="#0284C7" stroke-width="2"/>
                    <text x="186" y="42" fill="#0C4A6E" font-size="14" font-weight="800">1 GAL</text>
                    <text x="184" y="68" fill="#FFFFFF" font-size="12" font-weight="700">4 qt</text>

                    <rect x="258" y="0" width="72" height="92" rx="8" fill="#38BDF8" stroke="#0284C7" stroke-width="2"/>
                    <text x="272" y="42" fill="#0C4A6E" font-size="14" font-weight="800">1 GAL</text>
                    <text x="270" y="68" fill="#FFFFFF" font-size="12" font-weight="700">4 qt</text>

                    <rect x="0" y="112" width="330" height="44" rx="8" fill="#1E293B" stroke="#6366F1" stroke-width="2"/>
                    <text x="18" y="139" fill="#A5F3FC" font-size="15" font-weight="700">4 Gallons × 4 = 16 Quarts Total</text>
                </g>

                <rect x="35" y="236" width="680" height="26" rx="6" fill="#14532D"/>
                <text x="52" y="254" fill="#86EFAC" font-size="12" font-weight="700">✅ RULE: 1 gallon = 4 quarts → Both options give the exact same 16 quarts!</text>
            </svg>
            """
        elif current_qid == "Q2":
            svg_diagram = """
            <svg viewBox="0 0 760 280" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#0F172A; border-radius: 10px; font-family: 'Inter', sans-serif;">
                <rect x="30" y="24" width="240" height="190" rx="14" fill="#B45309" stroke="#F59E0B" stroke-width="3"/>
                <text x="55" y="62" fill="#FEF3C7" font-size="14" font-weight="800">STEP 1: CONVERT TO OZ</text>
                <text x="55" y="102" fill="#FFFFFF" font-size="26" font-weight="800">20 lbs Sand</text>
                <text x="55" y="138" fill="#FDE68A" font-size="15" font-weight="700">1 lb = 16 oz</text>
                <rect x="50" y="156" width="200" height="38" rx="8" fill="#78350F"/>
                <text x="64" y="180" fill="#4ADE80" font-size="16" font-weight="800">20 × 16 = 320 oz</text>

                <path d="M 285 118 L 340 118 M 328 106 L 342 118 L 328 130" stroke="#38BDF8" stroke-width="4" stroke-linecap="round" fill="none"/>
                <text x="284" y="150" fill="#93C5FD" font-size="12" font-weight="700">÷ 8 Buckets</text>

                <g transform="translate(360, 24)">
                    <text x="0" y="20" fill="#A5F3FC" font-size="14" font-weight="800">STEP 2: SHARE EQUALLY INTO 8 BUCKETS</text>
                    <rect x="0" y="36" width="80" height="72" rx="10" fill="#DC2626" stroke="#FCA5A5" stroke-width="2"/><text x="18" y="78" fill="#FFF" font-size="16" font-weight="800">40 oz</text>
                    <rect x="92" y="36" width="80" height="72" rx="10" fill="#DC2626" stroke="#FCA5A5" stroke-width="2"/><text x="110" y="78" fill="#FFF" font-size="16" font-weight="800">40 oz</text>
                    <rect x="184" y="36" width="80" height="72" rx="10" fill="#DC2626" stroke="#FCA5A5" stroke-width="2"/><text x="202" y="78" fill="#FFF" font-size="16" font-weight="800">40 oz</text>
                    <rect x="276" y="36" width="80" height="72" rx="10" fill="#DC2626" stroke="#FCA5A5" stroke-width="2"/><text x="294" y="78" fill="#FFF" font-size="16" font-weight="800">40 oz</text>

                    <rect x="0" y="122" width="80" height="72" rx="10" fill="#DC2626" stroke="#FCA5A5" stroke-width="2"/><text x="18" y="164" fill="#FFF" font-size="16" font-weight="800">40 oz</text>
                    <rect x="92" y="122" width="80" height="72" rx="10" fill="#DC2626" stroke="#FCA5A5" stroke-width="2"/><text x="110" y="164" fill="#FFF" font-size="16" font-weight="800">40 oz</text>
                    <rect x="184" y="122" width="80" height="72" rx="10" fill="#DC2626" stroke="#FCA5A5" stroke-width="2"/><text x="202" y="164" fill="#FFF" font-size="16" font-weight="800">40 oz</text>
                    <rect x="276" y="122" width="80" height="72" rx="10" fill="#DC2626" stroke="#FCA5A5" stroke-width="2"/><text x="294" y="164" fill="#FFF" font-size="16" font-weight="800">40 oz</text>
                </g>

                <rect x="30" y="236" width="690" height="28" rx="6" fill="#14532D"/>
                <text x="48" y="255" fill="#86EFAC" font-size="13" font-weight="700">✅ CHECK: 8 buckets × 40 oz = 320 oz = 20 lbs! Each bucket holds 40 oz.</text>
            </svg>
            """
        elif current_qid == "Q3":
            svg_diagram = """
            <svg viewBox="0 0 760 275" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#0F172A; border-radius: 10px; font-family: 'Inter', sans-serif;">
                <text x="35" y="42" fill="#A5F3FC" font-size="15" font-weight="800">STEP 1: CONVERT 5/10 KM TO METERS (1 km = 1,000 m)</text>
                <rect x="35" y="58" width="690" height="58" rx="10" fill="#1E293B" stroke="#38BDF8" stroke-width="3"/>
                <text x="55" y="94" fill="#FFFFFF" font-size="22" font-weight="800">Total Hangar Depth = (5/10) × 1,000 m = 500 m</text>

                <text x="35" y="148" fill="#FDE68A" font-size="15" font-weight="800">STEP 2: SUBTRACT THE 100 m EQUIPMENT AREA</text>
                <rect x="35" y="162" width="140" height="58" rx="10" fill="#EAB308" stroke="#CA8A04" stroke-width="3"/>
                <text x="50" y="188" fill="#422006" font-size="12" font-weight="800">EQUIPMENT</text>
                <text x="64" y="209" fill="#1E293B" font-size="18" font-weight="900">100 m</text>

                <rect x="185" y="162" width="540" height="58" rx="10" fill="#0284C7" stroke="#38BDF8" stroke-width="3"/>
                <text x="210" y="198" fill="#FFFFFF" font-size="22" font-weight="800">✈️ AVAILABLE FOR PLANES: 500 m − 100 m = 400 m</text>

                <rect x="35" y="236" width="690" height="26" rx="6" fill="#14532D"/>
                <text x="52" y="254" fill="#86EFAC" font-size="13" font-weight="700">✅ RULE: 'Kilo' = 1,000 → 5/10 km = 500 m → 500 − 100 = 400 m available!</text>
            </svg>
            """
        else:
            svg_diagram = """
            <svg viewBox="0 0 760 285" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#0F172A; border-radius: 10px; font-family: 'Inter', sans-serif;">
                <rect x="30" y="22" width="700" height="76" rx="10" fill="#1E293B" stroke="#6366F1" stroke-width="3" stroke-dasharray="6,4"/>
                <text x="50" y="50" fill="#C7D2FE" font-size="14" font-weight="700">ANCHOR BENCHMARK (US CUSTOMARY WEIGHT)</text>
                <text x="50" y="80" fill="#38BDF8" font-size="22" font-weight="800">1 US TON = 2,000 LBS</text>

                <rect x="30" y="118" width="440" height="96" rx="10" fill="#B45309" stroke="#F59E0B" stroke-width="3"/>
                <text x="50" y="148" fill="#FEF3C7" font-size="14" font-weight="700">📦 ALREADY LOADED (1/2 TON)</text>
                <text x="50" y="184" fill="#FFFFFF" font-size="24" font-weight="800">1,000 LBS</text>
                <text x="50" y="205" fill="#FDE68A" font-size="12" font-weight="600">2,000 ÷ 2 = 1,000 lb</text>

                <rect x="485" y="118" width="245" height="96" rx="10" fill="#065F46" stroke="#10B981" stroke-width="3"/>
                <text x="505" y="148" fill="#A7F3D0" font-size="14" font-weight="700">✈️ SPACE LEFT</text>
                <text x="505" y="184" fill="#FFFFFF" font-size="24" font-weight="800">300 LBS</text>
                <text x="505" y="205" fill="#6EE7B7" font-size="12" font-weight="600">1,300 − 1,000 = 300 lb</text>

                <rect x="30" y="236" width="700" height="28" rx="6" fill="#14532D"/>
                <text x="48" y="255" fill="#86EFAC" font-size="13" font-weight="700">✅ RULE: 1 US Ton = 2,000 lb (not 1,000!) → 1,300 − 1,000 = 300 lb left.</text>
            </svg>
            """

        st.markdown(svg_diagram, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ULTRA-RESPONSIVE INTERACTIVE FREEHAND DRAWING CANVAS (POINTER EVENTS API)
    st.markdown("#### ✍️ Freehand Stylus & Scratchpad Whiteboard")
    stamp_rule = problem["concept_rule"]
    canvas_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0; padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        user-select: none; -webkit-user-select: none;
        background: transparent;
      }}
      #board-wrapper {{
        border: 2px solid #3B82F6;
        border-radius: 12px;
        background: #FFFFFF;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        overflow: hidden;
      }}
      .toolbar {{
        background: #F8FAFC;
        border-bottom: 2px solid #E2E8F0;
        padding: 8px 12px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 8px;
      }}
      .tool-btn {{
        border: 1px solid #CBD5E1;
        background: white;
        border-radius: 6px;
        padding: 5px 9px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 4px;
      }}
      .tool-btn:hover {{ background: #EFF6FF; border-color: #3B82F6; }}
      .tool-btn.active {{ background: #DBEAFE; border-color: #2563EB; color: #1D4ED8; }}
      .color-dot {{
        width: 22px; height: 22px;
        border-radius: 50%;
        cursor: pointer;
        border: 2px solid #E2E8F0;
      }}
      .color-dot.active {{ border-color: #0F172A; box-shadow: 0 0 0 2px #3B82F6; transform: scale(1.15); }}
      #paintCanvas {{
        display: block;
        width: 100%;
        height: 390px;
        background-color: #FFFFFF;
        touch-action: none;
        cursor: crosshair;
      }}
      .status-bar {{
        background: #EFF6FF;
        color: #1E40AF;
        padding: 5px 12px;
        font-size: 11px;
        font-weight: 600;
        border-bottom: 1px solid #DBEAFE;
        display: flex;
        justify-content: space-between;
      }}
    </style>
    </head>
    <body>
    <div id="board-wrapper">
      <div class="toolbar">
        <span style="font-size: 11px; font-weight: 700; color: #475569;">PENS:</span>
        <div class="color-dot active" style="background:#1E293B;" onclick="setColor('#1E293B', this)" title="Black"></div>
        <div class="color-dot" style="background:#2563EB;" onclick="setColor('#2563EB', this)" title="Blue"></div>
        <div class="color-dot" style="background:#DC2626;" onclick="setColor('#DC2626', this)" title="Red"></div>
        <div class="color-dot" style="background:#16A34A;" onclick="setColor('#16A34A', this)" title="Green"></div>
        <button class="tool-btn" id="eraserBtn" onclick="toggleEraser(this)">🧽 Eraser</button>
        <div style="width: 1px; height: 18px; background: #CBD5E1;"></div>
        <button class="tool-btn" onclick="setSize(2, this)">2px</button>
        <button class="tool-btn active" onclick="setSize(5, this)">5px</button>
        <button class="tool-btn" onclick="setSize(12, this)">12px</button>
        <div style="width: 1px; height: 18px; background: #CBD5E1;"></div>
        <button class="tool-btn" onclick="stampText('{stamp_rule}', '#2563EB')">📝 Stamp Rule</button>
        <button class="tool-btn" onclick="clearCanvas()" style="margin-left: auto; background: #FEE2E2; color: #DC2626; border-color: #FCA5A5;">🗑️ Clear</button>
      </div>
      <div class="status-bar">
        <span>✍️ Click & drag with mouse, stylus, or touch to solve Question {problem['num']}:</span>
        <span id="posIndicator">Whiteboard Ready</span>
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

      function drawBackgroundGrid() {{
        const w = canvas.width;
        const h = canvas.height;
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, w, h);
        ctx.strokeStyle = '#F1F5F9';
        ctx.lineWidth = 1;
        for (let x = 0; x < w; x += 25) {{
          ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
        }}
        for (let y = 0; y < h; y += 25) {{
          ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
        }}
      }}

      function setupCanvasResolution() {{
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width || 700;
        canvas.height = rect.height || 390;
        drawBackgroundGrid();
      }}

      function getCoords(e) {{
        const rect = canvas.getBoundingClientRect();
        return {{
          x: (e.clientX - rect.left) * (canvas.width / rect.width),
          y: (e.clientY - rect.top) * (canvas.height / rect.height)
        }};
      }}

      function startPosition(e) {{
        e.preventDefault();
        try {{ canvas.setPointerCapture(e.pointerId); }} catch(err){{}}
        painting = true;
        const pos = getCoords(e);
        lastX = pos.x; lastY = pos.y;
        ctx.beginPath();
        const r = (isEraser ? currentWidth * 3 : currentWidth) / 2;
        ctx.arc(lastX, lastY, Math.max(r, 1.5), 0, Math.PI * 2);
        ctx.fillStyle = isEraser ? '#FFFFFF' : currentColor;
        ctx.fill();
        posIndicator.innerText = 'Writing...';
      }}

      function endPosition(e) {{
        if (painting) {{
          painting = false;
          try {{ canvas.releasePointerCapture(e.pointerId); }} catch(err){{}}
          posIndicator.innerText = 'Whiteboard Ready';
        }}
      }}

      function draw(e) {{
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
        lastX = pos.x; lastY = pos.y;
      }}

      canvas.addEventListener('pointerdown', startPosition);
      canvas.addEventListener('pointermove', draw);
      canvas.addEventListener('pointerup', endPosition);
      canvas.addEventListener('pointercancel', endPosition);
      canvas.addEventListener('pointerleave', endPosition);

      function setColor(color, el) {{
        isEraser = false; currentColor = color; previousColor = color;
        document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('active'));
        if (el) el.classList.add('active');
        document.getElementById('eraserBtn').classList.remove('active');
        canvas.style.cursor = 'crosshair';
      }}

      function toggleEraser(btn) {{
        isEraser = !isEraser;
        if (isEraser) {{
          btn.classList.add('active');
          document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('active'));
          canvas.style.cursor = 'cell';
        }} else {{
          btn.classList.remove('active');
          setColor(previousColor, document.querySelector('.color-dot'));
        }}
      }}

      function setSize(s, btn) {{
        currentWidth = s;
        btn.parentElement.querySelectorAll('.tool-btn').forEach(b => {{
          if (b.innerText.includes('px')) b.classList.remove('active');
        }});
        btn.classList.add('active');
      }}

      function clearCanvas() {{
        drawBackgroundGrid();
        posIndicator.innerText = 'Board Cleared';
      }}

      function stampText(text, color) {{
        const x = 25 + Math.random() * Math.max(canvas.width - 260, 40);
        const y = 55 + Math.random() * Math.max(canvas.height - 100, 40);
        ctx.save();
        ctx.font = 'bold 21px "Courier New", monospace';
        ctx.fillStyle = color;
        ctx.fillText(text, x, y);
        ctx.restore();
        posIndicator.innerText = 'Stamped: ' + text;
      }}

      window.addEventListener('DOMContentLoaded', setupCanvasResolution);
      window.addEventListener('load', setupCanvasResolution);
      setTimeout(setupCanvasResolution, 150);
    </script>
    </body>
    </html>
    """
    components.html(canvas_html, height=480)
