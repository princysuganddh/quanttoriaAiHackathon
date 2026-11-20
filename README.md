# 🧮 Quanttoria AI Maths: Child-Friendly Adaptive Quiz & Cognitive-Psychometric Engine

> **Built for the Quanttoria AI Hackathon**  
> *Stack: Gemini 2.5 Flash, Microsoft Neural Kid Voice (`edge-tts`), Web Speech-to-Text, Google Agent Skills, Interactive Whiteboard, and Google Cloud Run*

---

## ✨ What Makes Quanttoria AI Maths Unique

Most math tutor apps either grade kids harshly with red Xs or overwhelm them with clinical jargon mid-quiz. **Quanttoria AI Maths** separates the **child's joyful learning flow** from the **deep AI cognitive & psychometric intelligence**:

1. **🖼️ 4-Question Visual Airport Math Adventure (`Q1 → Q2 → Q3 → Q4`)**:
   - **Q1 · Hangar Fuel**: `16 quarts` vs `4 gallons` (`1 gal = 4 qt`)
   - **Q2 · Fire Sand**: `20 lbs` sand shared into `8 small buckets` → `40 oz` (`1 lb = 16 oz`)
   - **Q3 · Hangar Depth**: `5/10 km` minus `100 m` maintenance area → `400 m` (`1 km = 1,000 m`)
   - **Q4 · Plane Cargo**: `1,300 lb` capacity minus `1/2 ton` loaded → `300 lb` (`1 US ton = 2,000 lb`)
2. **✨ Blinking Visual Hints + Funny 2-Liner Age-Friendly Cues**:
   - When a student makes a mistake, the exact hint spot **blinks & glows directly on the question image** paired with a funny, playful 2-liner cue so kids slow down and stop rushing in overconfidence.
3. **🔊 Crystal-Clear Nobita-Style Neural Kid Voice & 🎙️ Speech-to-Text**:
   - Powered by `edge-tts` (`en-US-AnaNeural`) with natural offline fallback — speaks cues, hints, congratulations, magic formulas, and step-by-step solutions aloud.
   - Built-in Web Speech Recognition mic lets kids speak answers aloud.
4. **🎉 Solution Steps + Formula + `NEXT` Button Flow**:
   - On every correct answer, balloons celebrate the win, the magic formula & 2-step solution are displayed and spoken aloud, and the next question loads only when the student taps **`➡️ NEXT QUESTION`**.
5. **🔬 Compact End-of-Quiz USP — Dr. Quanttoria AI Cognitive & Psychometric Review**:
   - Silently tracks every mistake attempt and cognitive domain (*Schema Encoding*, *Working Memory*, *Unit Attention*, *Number Sense*) throughout the quiz without distracting the child.
   - After Q4 is solved, unlocks the **`👩‍🏫 Teacher / Parent Review`** dashboard with:
     - Formal AI letter addressed directly to the Teacher / Parent
     - Overarching cognitive & psychometric pattern analyzed by AI
     - Chronological log of every mistake made before entering the correct answer + AI's cognitive reasons
     - **All Possible Mistakes Matrix** highlighting traps the student triggered vs. avoided
     - Post-quiz similar-concept practice booster

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

---

## ☁️ Google Cloud Run Deployment

```bash
gcloud run deploy quanttoria-ai-maths \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```
