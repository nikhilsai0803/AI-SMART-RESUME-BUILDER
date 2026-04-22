# 🧠 Smart AI Resume Builder

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-black?logo=flask)
![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Free%20API-orange)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Powered-f7931e?logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Hugging%20Face%20Spaces-yellow)](https://huggingface.co/spaces/sharmasai12/Smart-resume)

**An AI-powered resume analysis, building, and optimization platform for job seekers and recruiters.**

[🚀 Live Demo](#live-demo) • [✨ Features](#features) • [⚙️ Installation](#installation) • [🔑 API Keys](#api-keys) • [🤝 Contributing](#contributing)

</div>

---

## 📸 Screenshots

> *Upload your resume → get instant ATS score, skill gap analysis, AI feedback, and interview prep — all in one platform.*

---

## ✨ Features

### 👤 For Job Seekers
| Feature | Description |
|---|---|
| **ATS Score Analyzer** | ML-powered ATS score using a trained TF-IDF + classification model |
| **Resume Builder** | Form-based DOCX resume generator with professional formatting |
| **AI Feedback** | Smart feedback on resume content, tone, and structure via Hugging Face API |
| **Skill Gap Analysis** | Compare your skills against job role requirements |
| **Resume Rewriter** | AI-powered suggestions to improve bullet points and summaries |
| **Role Optimizer** | Tailor your resume for specific job categories and roles |
| **Interview Prep** | Generate custom interview questions by role, level, and skill set |
| **Job Search** | Live job listings via Adzuna API (free tier) |

### 🏢 For Recruiters
| Feature | Description |
|---|---|
| **Bulk Resume Screening** | Upload multiple resumes at once for batch analysis |
| **Criteria-Based Filtering** | Filter by education level, skills, and ATS score threshold |
| **Candidate Ranking** | Automatically ranks candidates by match percentage |
| **CSV Export** | Export shortlisted candidates as a CSV report |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, Flask 3.x
- **ML Models:** scikit-learn (TF-IDF + trained ATS classifier), joblib
- **AI Engine:** Hugging Face Inference API (`google/flan-t5-large`) with rule-based fallback
- **Document Parsing:** pdfminer.six, PyPDF2, python-docx
- **Resume Generation:** python-docx
- **Job Search:** Adzuna API (free tier)
- **Database:** SQLite (persistent via `/data` volume on Hugging Face Spaces)
- **Frontend:** Jinja2 templates, Bootstrap, vanilla JS

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/sharmasai12/Smart-AI-Resume-Builder.git
cd Smart-AI-Resume-Builder
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Install spaCy for enhanced NLP
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### 5. Set environment variables

Create a `.env` file in the project root or export directly:

```bash
# Required for session security (change this in production!)
export FLASK_SECRET_KEY="your-strong-secret-key"

# Optional: Hugging Face free token for AI features
# Get yours at https://huggingface.co/settings/tokens
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxx"

# Optional: Adzuna API keys for live job search
# Get free keys at https://developer.adzuna.com
export ADZUNA_APP_ID="your_app_id"
export ADZUNA_APP_KEY="your_app_key"
```

### 6. Run the app
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 🔑 API Keys

The app works **without any API keys** using rule-based fallbacks. Keys unlock enhanced features:

| Key | Purpose | Where to Get | Required? |
|---|---|---|---|
| `HF_TOKEN` | AI feedback, rewriting, interview questions | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | ❌ Optional |
| `ADZUNA_APP_ID` + `ADZUNA_APP_KEY` | Live job search listings | [developer.adzuna.com](https://developer.adzuna.com) | ❌ Optional |
| `FLASK_SECRET_KEY` | Secure sessions | Generate any random string | ✅ Recommended |

---

## 🧪 Demo Accounts

The app seeds two demo accounts on startup:

| Role | Email | Password |
|---|---|---|
| Job Seeker | `user@demo.com` | `password` |
| Recruiter | `recruiter@demo.com` | `password` |

---

## 📁 Project Structure

```
Smart-AI-Resume-Builder/
├── app.py                          # Main Flask application & all routes
├── requirements.txt                # Python dependencies
├── ats_model.pkl                   # Trained ATS scoring ML model
├── tfidf_vectorizer.pkl            # TF-IDF vectorizer for ML scoring
├── Candidate_Sample_Set_Randomized.csv  # Sample data used for training
├── config/
│   ├── __init__.py
│   └── job_roles.py                # Job categories, roles & required skills
├── utils/
│   ├── __init__.py
│   ├── ai_engine.py                # HF API + rule-based AI features
│   ├── resume_analyzer.py          # ATS scoring & keyword analysis
│   └── resume_parser.py            # PDF/DOCX text extraction
├── templates/                      # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── analyze.html
│   ├── result.html
│   ├── builder.html
│   ├── ai_feedback.html
│   ├── skill_gap.html
│   ├── smart_questions.html
│   ├── rewrite.html
│   ├── role_optimizer.html
│   ├── recruiter.html
│   └── ...
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## 🚀 Live Demo

The app is deployed on **Hugging Face Spaces**.

👉 **[Try the Live Demo](https://huggingface.co/spaces/sharmasai12/Smart-resume)**

---

## 🔒 Notes on Production Use

- User data is stored in **SQLite** (`/data/app.db`) — persists across restarts on Hugging Face Spaces via the persistent volume
- Set a strong `FLASK_SECRET_KEY` in production — never use the default
- The `uploads/` folder is ephemeral — uploaded resumes are processed and immediately deleted, nothing is stored
- Sessions use `SameSite=None; Secure` cookies with `ProxyFix` for compatibility with the Hugging Face HTTPS proxy

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push and open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
Built with ❤️ using Flask + Hugging Face + scikit-learn
</div>
