# GhostBug AI — Session Context & Resume Guide
> Last updated: 2026-11-20 at 18:18 IST

---

## 🧠 Project Summary

**GhostBug AI** is a two-panel (50/50 split-screen) educational web app built with Python + Streamlit.
It diagnoses hidden prerequisite misconceptions ("Ghost Gaps") in Grade 6 student math working steps.

**Hackathon:** Quanttoria AI Hackathon  
**GitHub Repo URL:** `https://github.com/princysuganddh/quanttoriaAiHackathon.git`  
**GitHub Account:** `princysuganddh`

---

## 📂 File Locations

| File/Folder | Path |
|---|---|
| **Main project (GitHub submission)** | `C:\Users\HP\Desktop\quanttoria AI hackathon` |
| **Scratch/dev copy** | `C:\Users\HP\.gemini\antigravity\scratch\ghostbug_ai` |
| **App entry point** | `app.py` (in both locations) |
| **Q.05 question image** | `assets\hangar_fuel_question.png` |
| **Q.05 solution image** | `assets\hangar_fuel_solution.png` |
| **Original screenshots** | `C:\Users\HP\Pictures\Screenshots\Screenshot 2026-11-20 115238.png` (question) |
|  | `C:\Users\HP\Pictures\Screenshots\Screenshot 2026-11-20 115320.png` (solution) |
| **Skills folder** | `skills\ghost_mapper.md`, `skills\deliberate_bug_leo.md` |
| **Push helper** | `push_to_github.py` (dulwich-based) |
| **Deployment** | `Dockerfile`, `requirements.txt`, `.dockerignore` |

---

## 🛠 Tech Stack

- **Python:** `C:\Users\HP\AppData\Local\Programs\Python\Python311\python.exe` (3.11)
- **Streamlit:** 1.67.0
- **Google GenAI SDK:** google-genai 3.6.1
- **Pillow:** 13.0.0
- **Dulwich (pure Python git):** 1.2.21
- **Deployment target:** Google Cloud Run (port 8080)

### Install dependencies (if needed):
```powershell
& "C:\Users\HP\AppData\Local\Programs\Python\Python311\python.exe" -m pip install streamlit==1.67.0 google-genai==3.6.1 pillow==13.0.0 requests==2.34.2 dulwich==1.2.21
```

---

## 🚀 How to Run the App

```powershell
& "C:\Users\HP\AppData\Local\Programs\Python\Python311\python.exe" -m streamlit run "C:\Users\HP\.gemini\antigravity\scratch\ghostbug_ai\app.py" --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

Then open: **http://localhost:8501**

> ⚠️ Always use the **full Python path** — the `python` command points to the Windows Store stub and won't work.

---

## 📌 App Features (What's Built)

### Left Panel
- Problem image display (Q.05 Hangar Fuel shown by default)
- Student answer input
- Gemini 2.5 Flash diagnostic engine (or Offline Demo Mode)
- Red Ghost Alert for misconceptions
- Leo AI classmate (deliberate bug peer-learning)
- "Teach Leo" healing box with heal_regex validation
- Gemini Live Voice simulation

### Right Panel
- Interactive classroom whiteboard
- WB1 / WB2 step reveals
- Nano Banana SVG visual aid (gallons vs quarts for Q.05)
- **HTML5 freehand drawing canvas** (fully working — uses Pointer Events API)

### Problems Loaded
| ID | Name | Type |
|---|---|---|
| Q.05 | Hangar Fuel: 16 quarts vs 4 gallons | Image-based (default) |
| Q.01 | Fraction word problem | Text-based |
| Q.02 | Ratio problem | Text-based |

---

## ⚠️ Known Issues & Constraints

### Hard Rules (Never Break)
- ❌ **Never use the word "GeoGebra"** anywhere — not in app, README, skills, or comments
- ✅ Q.05 must display the actual screenshot image (not just text)
- ✅ Q.05 must be the default selected problem on app load
- ✅ Offline Demo Mode must work without an API key

### GitHub Blockers
1. **Repo doesn't exist on GitHub yet**
   - Must be created manually at https://github.com/new
   - Name: `quanttoriaAiHackathon`
   - Leave "Initialize with README" **unchecked**

2. **Previous PAT was a Fine-Grained PAT** — scoped only to other repos, cannot create or access `quanttoriaAiHackathon`
   - Need a **Classic PAT** with `repo` scope
   - Generate at: https://github.com/settings/tokens → "Generate new token (classic)"

3. **Git for Windows not installed** (requires admin/UAC)
   - Workaround: `push_to_github.py` uses dulwich (pure Python git)
   - Once repo is created + Classic PAT obtained, run:
   ```powershell
   cd "C:\Users\HP\Desktop\quanttoria AI hackathon"
   & "C:\Users\HP\AppData\Local\Programs\Python\Python311\python.exe" push_to_github.py YOUR_CLASSIC_TOKEN
   ```

---

## 📋 Remaining To-Do (Priority Order)

### 🔴 Blockers
- [ ] Create `quanttoriaAiHackathon` repo on GitHub manually
- [ ] Generate a Classic PAT with `repo` scope
- [ ] Run `push_to_github.py` to push all 3 commits

### 🟡 Nice-to-Have
- [ ] Live Gemini API integration (needs Gemini API key in sidebar)
- [ ] Cloud Run deployment: `gcloud run deploy ghostbug-ai --source . --platform managed --region us-central1 --allow-unauthenticated`
- [ ] Add more problems (Q.03, Q.04, etc.)

---

## 🗂 Local Git State

```
Branch:   main
Remote:   origin → https://github.com/princysuganddh/quanttoriaAiHackathon.git
Commits:  3
  1. Initial commit: GhostBug AI for Quanttoria Hackathon
  2. Add GitHub push utility script
  3. Update: Purge geogebra, integrate question screenshots Q.05
Status:   Ahead of remote (remote repo doesn't exist yet)
```

---

## 💬 How to Resume in a New Session

1. Paste this file (or its path) into the chat
2. Tell the AI: *"Resume the GhostBug AI project. Context is in CONTEXT.md at C:\Users\HP\Desktop\quanttoria AI hackathon\CONTEXT.md"*
3. The AI will read this file and pick up exactly where you left off

---

## 🔑 Credentials & Keys Needed

| Credential | Status | Where to Get |
|---|---|---|
| GitHub Classic PAT (repo scope) | ❌ Not yet obtained | https://github.com/settings/tokens |
| Gemini API Key | ⚪ Optional (Demo Mode works without it) | https://aistudio.google.com/app/apikey |
| Google Cloud credentials | ⚪ Optional (for Cloud Run deploy) | https://console.cloud.google.com |

> ⚠️ Never share tokens in plain text in a public repo. Use environment variables or Streamlit secrets.

---

*This file was auto-generated by Antigravity AI to preserve session context.*
