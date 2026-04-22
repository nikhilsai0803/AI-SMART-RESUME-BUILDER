---
title: Smart AI Resume Builder
emoji: 🧠
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: true
license: mit
short_description: AI-powered resume analyzer, builder & interview prep tool
---

# 🧠 Smart AI Resume Builder

An AI-powered platform to analyze, build, and optimize resumes for job seekers and recruiters.

## Features

- **ATS Score Analyzer** — ML-powered resume scoring
- **Resume Builder** — Generate professional DOCX resumes
- **AI Feedback** — Smart suggestions powered by Hugging Face
- **Skill Gap Analysis** — Compare skills vs. job requirements
- **Interview Prep** — Auto-generate interview questions by role
- **Recruiter Screening** — Bulk resume screening with CSV export

## Demo Accounts

| Role | Email | Password |
|---|---|---|
| Job Seeker | `user@demo.com` | `password` |
| Recruiter | `recruiter@demo.com` | `password` |

## Environment Variables (optional)

Set these in Space Settings → Repository secrets to unlock full AI features:

- `HF_TOKEN` — Hugging Face token for AI generation
- `ADZUNA_APP_ID` + `ADZUNA_APP_KEY` — For live job search
- `FLASK_SECRET_KEY` — Secure session secret