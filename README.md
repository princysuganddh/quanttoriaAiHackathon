# 👻 GhostBug AI: Prerequisite Gap Diagnostic & Healing Engine

> **Built for the Google AI Hackathon**  
> *Stack: Gemini 2.5 Flash, Nano Banana Visual Aid, Google Agent Skills, and Google Cloud Run*

---

## 🎯 The Core Problem: Invisible "Ghost Gaps" in Middle School Math
When middle school students fail multi-step Grade 6 GeoGebra word problems, traditional EdTech tools and LMS auto-graders report that the student failed Grade 6 concepts (e.g. algebraic subtraction, ratios, or problem-solving).

In reality, over **80% of student failures** are caused by unstated, un-tested **Ghost Gaps**—foundational prerequisite standards from Grade 4 or 5 that quietly poison the student's working steps.

### Target Curriculum Problems
1. **Q.01 (Plane Cargo Capacity)**:
   - *Problem*: The available capacity of the cargo area in a commercial plane is 1,300 lb. If 1/2 ton of the cargo is loaded, how much more can be added?
   - *Target Solution*: 300 lb
   - *Whiteboard Step 1 (WB1)*: $1\text{ ton} = 2,000\text{ lb} \implies 1/2\text{ ton} = 1,000\text{ lb}$
   - *Whiteboard Step 2 (WB2)*: $1,300\text{ lb} - 1,000\text{ lb} = 300\text{ lb}$
   - *Classic Mistake*: Student calculates $1/2\text{ ton} = 500\text{ lb}$, leading to $1,300 - 500 = 800\text{ lb}$ (Confusing 1 ton = 1,000 kg with US Customary units).

2. **Q.02 (Cargo Trolleys)**:
   - *Problem*: To load 1/2 ton cargo on the plane, trolleys were brought. If the capacity of the trolleys is 850 lb, by what amount should its capacity be increased?
   - *Target Solution*: 150 lb
   - *Whiteboard Step 1 (WB1)*: $1\text{ ton} = 2,000\text{ lb} \implies 1/2\text{ ton} = 1,000\text{ lb}$
   - *Whiteboard Step 2 (WB2)*: $1,000\text{ lb} - 850\text{ lb} = 150\text{ lb}$
   - *Classic Mistake*: Student calculates $1/2\text{ ton} = 500\text{ lb}$, leading to $850 - 500 = 350\text{ lb}$ (or asserting the trolley has extra space).

---

## 🧠 Google Agent Skills Architecture (`skills/`)
GhostBug AI implements modular Google Agent Skills:
- **`skills/ghost_mapper.md`**:
  Diagnostic agent skill that inspects student multi-line working steps, isolates the prerequisite standard (`CCSS.MATH.4.MD.A.1`), and maps the exact cognitive misconception.
- **`skills/deliberate_bug_leo.md`**:
  Peer-learning agent skill that spawns **Leo**, an AI classmate who is infected with the exact same bug on a deliberate variation (`1/4 ton`). Harnesses the **Protégé Effect** (learning by teaching) to heal the prerequisite gap.

---

## 🖥️ Two-Panel 50/50 Architecture
- **Left Panel (GeoGebra + GhostBug AI & Leo)**:
  - Curriculum problem switcher (Q.01 & Q.02).
  - Student working steps input (pre-filled with the classic 500 lb mistake).
  - Gemini 2.5 Flash Diagnostic Engine triggering the glowing **Red Ghost Alert**.
  - **Deliberate Bug Leo** companion chat.
  - Interactive **'Teach Leo'** healing box turning green (**'Ghost Gap Healed!'**) upon student explanation.
  - Simulated **Gemini Live Voice Input** toggle with live audio wave pulse.
- **Right Panel (Interactive Digital Whiteboard + Nano Banana)**:
  - Grid-lined Classroom Whiteboard styling.
  - Step reveals: `Reveal WB1 (Tons → lbs)` and `Reveal WB2 (Final Answer)`.
  - **Nano Banana Visual Aid**: Generates educational visual partition diagram showing 1 ton = 2,000 lb split into two 1,000 lb crates (with clean SVG fallback).
  - **HTML5 Freehand Canvas**: Zero-dependency browser whiteboard canvas with multi-color pens (Black, Blue, Red, Green), stroke width, and eraser/clear controls.

---

## ☁️ Google Cloud Run Deployment
GhostBug AI is containerized and production-ready for Google Cloud Run:

```bash
# 1-Command Deploy to Google Cloud Run
gcloud run deploy ghostbug-ai \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```
