# 🧠 Smart Resume Analyzer AI — v2.0

> **100% free · No paid APIs · Runs entirely locally**

A full-stack Flask web app that uses AI-powered analysis to help job seekers optimize their resumes, identify skill gaps, prepare for interviews, and tailor applications to specific roles — all without spending a single rupee on external APIs.

---

## ✨ What's New in v2.0

| Feature | Description |
|---|---|
| 🧠 **AI Smart Feedback** | Deep resume grading (A+ to D) with impact score, writing quality check, ATS compatibility analysis, and prioritised improvements |
| 📊 **Skill Gap Analyzer** | Compares your skills against role requirements, detects transferable skills, estimates experience level, and builds a 3-phase learning roadmap with free learning resources |
| 💬 **Smart Interview Questions** | Role-specific, experience-level-aware questions across 5 categories (behavioral, technical, system design, role-specific, culture fit) with STAR method tips |
| ✍️ **Resume Rewrite Suggestions** | Bullet-by-bullet rewrites — replaces weak verbs, adds metric prompts, removes first-person pronouns, and scores each improvement |
| 🎯 **Role Optimizer** | Keyword coverage analysis, tailoring checklist, recommended section order, tone tips, and keyword density heatmap for any target role |

---

## 🚀 Feature Overview

### Existing Features (v1)
- **ATS Analyzer** – Upload PDF/DOCX resume, get ATS score (ML model + rule-based), keyword match, section scores
- **Resume Builder** – Build a polished DOCX resume from a form
- **AI Questions (CSV)** – Filter questions from a CSV by skill keywords
- **Job Search** – Powered by Adzuna API (free tier, optional)
- **Recruiter Panel** – Bulk upload resumes, filter by criteria, export CSV
- **User Auth** – Signup/Login with roles (Job Seeker / Recruiter)

### New AI Features (v2)
All new features use **zero paid APIs**. Everything runs locally using:
- Python standard library (regex, collections, math)
- scikit-learn (for existing ATS ML model)
- Rule-based NLP with a hand-curated skill taxonomy of 80+ skills

---

## 🗂️ Project Structure

```
smart-resume-ai/
├── app.py                        # Main Flask app + all routes (v1 + v2 AI routes)
├── requirements.txt              # Dependencies
├── ats_model.pkl                 # Pre-trained ATS scoring model (sklearn)
├── tfidf_vectorizer.pkl          # TF-IDF vectorizer for ATS model
│
├── config/
│   ├── __init__.py
│   └── job_roles.py              # 50+ job roles with required skills
│
├── utils/
│   ├── __init__.py
│   ├── resume_parser.py          # PDF/DOCX text extraction
│   ├── resume_analyzer.py        # Rule-based resume analysis engine (v1)
│   └── ai_engine.py              # ⭐ NEW: All AI enhancement modules (v2)
│
├── templates/
│   ├── base.html                 # Layout + sidebar (updated with new nav links)
│   ├── index.html                # Landing page
│   ├── dashboard.html            # User dashboard
│   ├── analyze.html / result.html # ATS analyzer
│   ├── builder.html              # Resume builder
│   ├── ai_questions.html         # Legacy CSV-based questions
│   ├── job_search.html           # Job search
│   ├── feedback.html             # User feedback
│   ├── recruiter.html            # Recruiter panel
│   ├── ai_feedback.html          # ⭐ NEW: Smart feedback results
│   ├── skill_gap.html            # ⭐ NEW: Skill gap + roadmap
│   ├── smart_questions.html      # ⭐ NEW: Role-aware interview questions
│   ├── rewrite.html              # ⭐ NEW: Bullet rewrite suggestions
│   └── role_optimizer.html       # ⭐ NEW: Role tailoring optimizer
│
├── static/
│   ├── css/style.css             # All styles (v1 + v2 additions at bottom)
│   └── js/main.js
│
└── uploads/                      # Temp upload folder (auto-cleaned)
```

---

## ⚙️ Installation — Step by Step

### Prerequisites
- Python 3.10 or higher
- pip

### Step 1 — Clone / Extract the project
```bash
# If using git:
git clone <your-repo-url> smart-resume-ai
cd smart-resume-ai

# Or just extract the zip and cd into the folder
```

### Step 2 — Create a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

That's it! All core AI features work with just Flask + scikit-learn + PyPDF2 + python-docx.

### Step 4 — (Optional) Install spaCy for better text extraction
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Step 5 — Run the app
```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## 🔑 Demo Accounts

Two accounts are pre-seeded on every startup:

| Role | Email | Password |
|---|---|---|
| Job Seeker | user@demo.com | password |
| Recruiter | recruiter@demo.com | password |

Or sign up for a new account.

---

## 📖 Usage Guide

### 1. ATS Analyzer (original)
1. Sign in → go to **ATS Analyzer** in the sidebar
2. Upload your PDF or DOCX resume
3. Optionally select a Category + Role for targeted scoring
4. Get your ATS score, keyword match, section scores, and improvement suggestions

### 2. 🧠 AI Smart Feedback (new)
1. Go to **Smart Feedback** in the sidebar
2. Upload resume + optionally select target role
3. Get a letter grade (A+ to D), impact score out of 100, and:
   - Section-by-section scores with colour bars
   - Prioritised improvement list (high / medium / low)
   - Writing quality analysis (pronouns, buzzwords, word count)
   - ATS compatibility tips

### 3. 📊 Skill Gap Analyzer (new)
1. Go to **Skill Gap** in the sidebar
2. Upload resume + select target role (required)
3. See:
   - Circular match meter (0-100%)
   - Skills you have vs. skills you're missing
   - Transferable skills detected
   - 3-phase learning roadmap with free resource links

### 4. 💬 Smart Interview Questions (new)
1. Go to **Smart Questions** in the sidebar
2. Select role, experience level (Junior / Mid / Senior), and number of questions
3. Get questions grouped by type: Behavioral, Technical, System Design, Role-Specific, Culture Fit
4. Click any question to reveal expert tips
5. Print the full set for offline practice

### 5. ✍️ Resume Rewrite Suggestions (new)
1. Go to **Rewrite Help** in the sidebar
2. Upload resume + optionally select target role
3. Get:
   - Quick wins (highest-impact improvements)
   - AI-suggested professional summary
   - Bullet-by-bullet before/after comparisons with scores

### 6. 🎯 Role Optimizer (new)
1. Go to **Role Optimizer** in the sidebar
2. Upload resume + select target role (required)
3. Get:
   - Keyword coverage donut chart
   - Missing vs. present keywords
   - What to emphasize for this role
   - Recommended section order
   - Tailoring checklist
   - Keyword frequency density chart

---

## 🤖 How AI Is Used

All AI in v2 is **local, free, and explainable** — no black boxes.

### `utils/ai_engine.py` — 5 AI modules

#### 1. `SmartFeedbackEngine`
- **Technique:** Rule-based NLP + pattern matching
- **How it works:** Analyses 6 dimensions (contact, summary, experience, skills, writing quality, ATS compat), scores each 0-100, aggregates to a letter grade. Uses regex patterns for quantification detection, weak verb detection, first-person pronoun removal, cliché detection.

#### 2. `SkillGapAnalyzer`
- **Technique:** Set intersection on a 80+ skill taxonomy
- **How it works:** Extracts skills from resume text using whole-word regex, compares against required skills from `job_roles.py`, detects transferable skills via shared taxonomy tags (e.g. Python and TypeScript both have "backend" tag → transferable), builds a 3-phase learning roadmap sorted by priority score.

#### 3. `InterviewQuestionGenerator`
- **Technique:** Role bucket detection + randomised sampling from curated question banks
- **How it works:** Detects role type (frontend/backend/ML/devops etc.) from job title keywords, samples from a 50+ question bank per category, adjusts categories by experience level (e.g. system design only for mid/senior), generates skill-specific questions via templates.

#### 4. `ResumeSuggester`
- **Technique:** Pattern substitution + impact scoring
- **How it works:** Scans bullet-like lines, replaces weak verbs (e.g. "helped" → "supported"), flags lines lacking quantification, removes first-person pronouns, scores each line before/after (0-100) based on presence of power verbs, metrics, and absence of weak language.

#### 5. `RoleOptimizer`
- **Technique:** Keyword matching + role-specific heuristics
- **How it works:** Computes keyword coverage using exact/case-insensitive matching, uses role-based rule tables (e.g. for Senior roles → emphasize leadership metrics), generates a tailoring checklist, computes keyword density (count / total words).

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.x |
| AI/ML | scikit-learn (ATS model), custom rule-based NLP |
| Document parsing | PyPDF2, python-docx, pdfminer.six |
| Frontend | Jinja2 templates, vanilla CSS (custom design system), vanilla JS |
| Auth | Werkzeug password hashing, Flask sessions |
| Fonts | Google Fonts (Syne + DM Sans) |
| Icons | Font Awesome 6 |

---

## 🔧 Environment Variables (optional)

| Variable | Purpose | Default |
|---|---|---|
| `FLASK_SECRET_KEY` | Session signing key | `resumelens-ai-secret-2025` |
| `ADZUNA_APP_ID` | Job Search API ID | (empty — job search disabled) |
| `ADZUNA_APP_KEY` | Job Search API Key | (empty — job search disabled) |

Set in a `.env` file or your shell before running:
```bash
export FLASK_SECRET_KEY="your-secret-key-here"
export ADZUNA_APP_ID="your-id"
export ADZUNA_APP_KEY="your-key"
```

---

## 🐞 Bugs Fixed

| Bug | Fix |
|---|---|
| ATS score could exceed 100 due to weighted sum rounding | Added `max(0, min(100, score))` clamps in analyzer |
| `extract_skills()` returned a set — caused JSON serialisation errors | Converted to list before returning |
| Session `best_score` compared int to None without guard | Added `if best is None or score > best` check |
| `routes_additions.py` imported but never registered | Moved all routes directly into `app.py` in v2 |

---

## 📝 Notes

- All uploaded files are **deleted immediately** after processing — nothing is stored on disk.
- User data is **in-memory only** — it resets when the server restarts. For production, replace `USERS` dict with a proper database (SQLite/PostgreSQL + SQLAlchemy).
- The ATS ML model (`ats_model.pkl`) is a pre-trained scikit-learn model included in the project.

---

## 📜 License

MIT — free to use, modify, and distribute.

---

*Built with Flask · Powered by Python · 100% Free AI*
