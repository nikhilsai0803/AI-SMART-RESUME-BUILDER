"""
ai_engine.py – Free AI-powered features for Smart Resume Analyzer AI
Uses:
  • Hugging Face Inference API (free tier) for real AI generation
  • Rule-based fallback (sklearn / regex) when HF is unavailable
No paid APIs required.
"""

import re
import os
import json
import random
import logging
import urllib.request
import urllib.error
from collections import Counter

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# HUGGING FACE FREE API CONFIG
# ─────────────────────────────────────────────────────────────────────────────

# Set HF_TOKEN in your environment (free at https://huggingface.co/settings/tokens)
# Leave blank to use rule-based fallback only — the app still works without it.
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Free model: google/flan-t5-large  (fast, lightweight, no GPU needed on free tier)
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

# Timeout for HF API calls (seconds)
HF_TIMEOUT = 20


def _hf_generate(prompt: str, max_new_tokens: int = 300) -> str:
    """
    Call the Hugging Face free Inference API.
    Returns generated text, or "" on any error so the caller uses fallback.
    """
    if not HF_TOKEN:
        return ""

    payload = json.dumps({
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": 0.7,
            "do_sample": True,
            "return_full_text": False,
        }
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        req = urllib.request.Request(HF_API_URL, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=HF_TIMEOUT) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            if isinstance(body, list) and body:
                return body[0].get("generated_text", "").strip()
            if isinstance(body, dict):
                if "error" in body:
                    logger.warning(f"HF API error: {body['error']}")
                    return ""
                return body.get("generated_text", "").strip()
    except urllib.error.HTTPError as e:
        logger.warning(f"HF API HTTP error {e.code}: {e.reason}")
    except Exception as e:
        logger.warning(f"HF API call failed: {e}")

    return ""


# ─────────────────────────────────────────────────────────────────────────────
# SKILL TAXONOMY
# ─────────────────────────────────────────────────────────────────────────────

SKILL_TAXONOMY = {
    "python": ["data science", "ml", "backend", "automation", "scripting"],
    "java": ["backend", "enterprise", "android"],
    "javascript": ["frontend", "fullstack", "web"],
    "typescript": ["frontend", "fullstack", "angular"],
    "c++": ["systems", "game dev", "embedded"],
    "c#": ["game dev", ".net", "unity"],
    "go": ["backend", "devops", "systems"],
    "rust": ["systems", "webassembly"],
    "swift": ["ios", "macos"],
    "kotlin": ["android", "backend"],
    "php": ["backend", "web"],
    "ruby": ["backend", "web"],
    "r": ["data science", "statistics"],
    "scala": ["big data", "spark"],
    "dart": ["flutter", "mobile"],
    "react": ["frontend", "fullstack"],
    "angular": ["frontend", "enterprise"],
    "vue": ["frontend"],
    "html": ["frontend", "web"],
    "css": ["frontend", "web"],
    "node.js": ["backend", "fullstack"],
    "express": ["backend", "api"],
    "django": ["backend", "python"],
    "flask": ["backend", "python"],
    "fastapi": ["backend", "python"],
    "spring": ["backend", "java"],
    "laravel": ["backend", "php"],
    "sql": ["data", "backend"],
    "mysql": ["database"],
    "postgresql": ["database"],
    "mongodb": ["database", "nosql"],
    "redis": ["database", "cache"],
    "elasticsearch": ["search", "data"],
    "pandas": ["data science", "python"],
    "numpy": ["data science", "python"],
    "tensorflow": ["ml", "deep learning"],
    "pytorch": ["ml", "deep learning"],
    "scikit-learn": ["ml", "python"],
    "keras": ["deep learning"],
    "spark": ["big data"],
    "hadoop": ["big data"],
    "tableau": ["data visualization"],
    "power bi": ["data visualization"],
    "aws": ["cloud", "devops"],
    "azure": ["cloud", "microsoft"],
    "gcp": ["cloud", "google"],
    "docker": ["devops", "containers"],
    "kubernetes": ["devops", "orchestration"],
    "terraform": ["devops", "iac"],
    "ansible": ["devops", "automation"],
    "jenkins": ["devops", "ci/cd"],
    "github actions": ["devops", "ci/cd"],
    "linux": ["systems", "devops"],
    "git": ["version control"],
    "machine learning": ["ml"],
    "deep learning": ["ml"],
    "nlp": ["ml", "ai"],
    "computer vision": ["ml", "ai"],
    "llm": ["ai", "nlp"],
    "langchain": ["ai", "llm"],
    "openai": ["ai", "api"],
    "communication": ["soft"],
    "leadership": ["soft"],
    "problem solving": ["soft"],
    "teamwork": ["soft"],
    "agile": ["methodology"],
    "scrum": ["methodology"],
    "project management": ["management"],
}

WEAK_WORDS = {
    "helped", "assisted", "worked on", "was responsible for",
    "involved in", "participated in", "tried", "attempted",
    "contributed to", "did", "made", "handled",
}

POWER_VERBS = {
    "developed", "engineered", "architected", "designed", "implemented",
    "led", "managed", "spearheaded", "launched", "deployed", "automated",
    "optimized", "reduced", "increased", "improved", "delivered",
    "built", "created", "established", "scaled", "transformed",
    "streamlined", "accelerated", "mentored", "collaborated",
    "analyzed", "researched", "solved", "debugged", "refactored",
    "integrated", "migrated", "modernized", "pioneered",
}

QUANTIFIER_PATTERN = re.compile(
    r"\b(\d+%|\d+x|\$[\d,]+|\d+\s*(million|billion|k|users|clients|customers|"
    r"hours|days|weeks|months|years|times|percent|requests|transactions))\b",
    re.IGNORECASE,
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. SMART RESUME FEEDBACK ENGINE
# ─────────────────────────────────────────────────────────────────────────────

class SmartFeedbackEngine:

    def generate_feedback(self, resume_text: str, job_role: str = "", required_skills=None) -> dict:
        required_skills = required_skills or []
        lines = [l.strip() for l in resume_text.split("\n") if l.strip()]

        feedback = {
            "overall_grade": "", "impact_score": 0,
            "strengths": [], "critical_issues": [], "improvements": [],
            "section_feedback": {}, "writing_quality": {}, "ats_tips": [],
            "ai_summary": "",
        }
        scores = []

        contact  = self._check_contact(resume_text);           feedback["section_feedback"]["contact"]    = contact;    scores.append(contact["score"])
        summary  = self._check_summary(resume_text, job_role); feedback["section_feedback"]["summary"]   = summary;   scores.append(summary["score"])
        exp      = self._check_experience(resume_text);         feedback["section_feedback"]["experience"] = exp;       scores.append(exp["score"])
        skill_fb = self._check_skills(resume_text, required_skills); feedback["section_feedback"]["skills"] = skill_fb; scores.append(skill_fb["score"])
        wq       = self._check_writing_quality(resume_text, lines);   feedback["writing_quality"] = wq;                 scores.append(wq["score"])
        ats      = self._check_ats_compatibility(resume_text);  feedback["ats_tips"] = ats["tips"];                    scores.append(ats["score"])

        impact_score = round(sum(scores) / len(scores))
        feedback["impact_score"] = impact_score
        feedback["overall_grade"] = self._grade(impact_score)

        for section, data in feedback["section_feedback"].items():
            if data["score"] >= 80:
                feedback["strengths"].append(data.get("positive", f"Good {section} section"))
            elif data["score"] < 50:
                feedback["critical_issues"].extend(data.get("issues", []))

        all_improvements = []
        for section, data in feedback["section_feedback"].items():
            for tip in data.get("tips", []):
                all_improvements.append({"section": section, "tip": tip, "priority": 100 - data["score"]})
        feedback["improvements"] = sorted(all_improvements, key=lambda x: -x["priority"])[:8]

        # Optional AI executive summary
        feedback["ai_summary"] = self._ai_executive_summary(resume_text[:800], job_role, impact_score)
        return feedback

    def _ai_executive_summary(self, resume_snippet, job_role, score):
        if not HF_TOKEN:
            return ""
        prompt = (
            f"Write a 2-sentence professional executive summary for a resume "
            f"{'targeting ' + job_role + ' ' if job_role else ''}"
            f"with quality score {score}/100. Resume excerpt: {resume_snippet[:400]}"
        )
        result = _hf_generate(prompt, max_new_tokens=120)
        return result if len(result) > 20 else ""

    def _check_contact(self, text):
        has_email    = bool(re.search(r"[\w.-]+@[\w.-]+\.\w+", text))
        has_phone    = bool(re.search(r"(\+?\d[\d\s\-().]{7,}\d)", text))
        has_linkedin = "linkedin" in text.lower()
        has_github   = "github" in text.lower()
        has_portfolio = bool(re.search(r"https?://", text))
        items = [has_email, has_phone, has_linkedin, has_github, has_portfolio]
        score = int(sum(items) / len(items) * 100)
        tips, issues = [], []
        if not has_email:    issues.append("Missing email address")
        if not has_phone:    issues.append("Missing phone number")
        if not has_linkedin: tips.append("Add your LinkedIn profile URL")
        if not has_github:   tips.append("Add your GitHub profile")
        if not has_portfolio: tips.append("Consider adding a portfolio/personal website URL")
        return {"score": score, "tips": tips, "issues": issues,
                "positive": "Contact section is complete with all key details"}

    def _check_summary(self, text, job_role):
        match = re.search(r"(summary|objective|profile|about me)[:\s]+([\s\S]{50,400}?)(?=\n[A-Z]|\Z)", text, re.IGNORECASE)
        if not match:
            return {"score": 30, "tips": ["Add a professional summary (3-5 sentences)"],
                    "issues": ["No professional summary found"], "positive": ""}
        summary_text = match.group(2).strip()
        wc = len(summary_text.split())
        score = 100; tips, issues = [], []
        if wc < 30:   score -= 30; tips.append(f"Summary too short ({wc} words). Aim for 50-80 words")
        elif wc > 120: score -= 20; tips.append(f"Summary too long ({wc} words). Keep under 100 words")
        if job_role and job_role.lower() not in summary_text.lower():
            score -= 15; tips.append(f"Mention your target role '{job_role}' in the summary")
        if not any(v in summary_text.lower() for v in POWER_VERBS):
            score -= 10; tips.append("Use strong action verbs in your summary")
        return {"score": max(0, score), "tips": tips, "issues": issues,
                "positive": "Strong professional summary with good detail"}

    def _check_experience(self, text):
        score = 100; tips, issues = [], []
        bullet_count      = len(re.findall(r"[•\-\*›➤▶]", text))
        quantified        = len(QUANTIFIER_PATTERN.findall(text))
        action_verb_lines = sum(1 for l in text.split("\n") if any(l.strip().lower().startswith(v) for v in POWER_VERBS))
        weak_found        = [w for w in WEAK_WORDS if w in text.lower()]
        date_count        = len(re.findall(r"\b(20\d{2}|19\d{2})\b", text))
        if bullet_count < 5:      score -= 20; tips.append("Use more bullet points (3-5 per role)")
        if quantified < 2:        score -= 25; tips.append("Add quantified achievements e.g. 'Reduced load time by 40%'")
        if action_verb_lines < 3: score -= 15; tips.append(f"Start bullets with power verbs: {', '.join(list(POWER_VERBS)[:6])}")
        if weak_found:            score -= 10; tips.append(f"Replace weak phrases: {', '.join(weak_found[:3])}")
        if date_count < 2:        score -= 10; issues.append("Include employment dates for each role")
        return {"score": max(0, score), "tips": tips, "issues": issues,
                "positive": f"Experience section uses {quantified} quantified achievements",
                "stats": {"bullet_count": bullet_count, "quantified": quantified, "action_verbs": action_verb_lines}}

    def _check_skills(self, text, required_skills):
        text_lower = text.lower()
        found   = [s for s in required_skills if s.lower() in text_lower]
        missing = [s for s in required_skills if s.lower() not in text_lower]
        score   = int((len(found) / len(required_skills)) * 100) if required_skills else 70
        taxonomy_found = [s for s in SKILL_TAXONOMY if s in text_lower]
        tips, issues = [], []
        if missing:               tips.append(f"Add missing skills if you have them: {', '.join(missing[:5])}")
        if len(taxonomy_found) < 5: tips.append("Expand your skills section with specific tools and technologies")
        return {"score": score, "tips": tips, "issues": issues,
                "positive": f"Matched {len(found)}/{len(required_skills)} required skills",
                "found": found, "missing": missing}

    def _check_writing_quality(self, text, lines):
        score = 100; tips = []
        pronouns = len(re.findall(r"\b(I|me|my|myself)\b", text, re.IGNORECASE))
        if pronouns > 3: score -= 15; tips.append(f"Remove first-person pronouns (found {pronouns})")
        cliches = ["team player","detail-oriented","self-starter","hard worker","passionate",
                   "results-driven","go-getter","think outside the box","synergy","leverage"]
        found_cliches = [c for c in cliches if c in text.lower()]
        if found_cliches: score -= len(found_cliches)*5; tips.append(f"Replace overused buzzwords: {', '.join(found_cliches[:3])}")
        wc = len(text.split())
        if wc < 300:    score -= 20; tips.append(f"Resume too short ({wc} words). Aim for 400-700 words")
        elif wc > 1200: score -= 10; tips.append(f"Resume may be too long ({wc} words). Keep to 1-2 pages")
        return {"score": max(0, score), "tips": tips, "word_count": wc,
                "has_pronouns": pronouns > 3, "cliches_found": found_cliches}

    def _check_ats_compatibility(self, text):
        score = 100; tips = []
        if len(re.findall(r"[^\x00-\x7F]", text)) > 10: score -= 10; tips.append("Avoid special characters — they confuse ATS parsers")
        if not re.search(r"[\w.-]+@[\w.-]+\.\w+", text): score -= 20; tips.append("Missing email — critical for ATS contact parsing")
        if sum(1 for h in ["experience","education","skills","summary","projects"] if h in text.lower()) < 3:
            score -= 20; tips.append("Use standard section headings for better ATS parsing")
        most_common = [w for w, c in Counter(text.lower().split()).most_common(20) if len(w) > 4]
        if most_common: tips.append(f"Top keywords: {', '.join(most_common[:5])}")
        if score == 100: tips.append("Good ATS compatibility — no major formatting issues detected")
        return {"score": max(0, score), "tips": tips}

    def _grade(self, score):
        if score >= 90: return "A+"
        if score >= 80: return "A"
        if score >= 70: return "B+"
        if score >= 60: return "B"
        if score >= 50: return "C"
        return "D"


# ─────────────────────────────────────────────────────────────────────────────
# 2. SKILL GAP ANALYZER
# ─────────────────────────────────────────────────────────────────────────────

class SkillGapAnalyzer:
    LEARNING_RESOURCES = {
        "python":          {"url": "https://docs.python.org/3/tutorial/",   "label": "Python Official Tutorial"},
        "javascript":      {"url": "https://javascript.info/",              "label": "javascript.info (free)"},
        "react":           {"url": "https://react.dev/learn",               "label": "React Official Docs"},
        "sql":             {"url": "https://www.w3schools.com/sql/",        "label": "W3Schools SQL"},
        "machine learning":{"url": "https://www.coursera.org/learn/machine-learning", "label": "Coursera ML (audit free)"},
        "docker":          {"url": "https://docs.docker.com/get-started/",  "label": "Docker Get Started"},
        "kubernetes":      {"url": "https://kubernetes.io/docs/tutorials/", "label": "Kubernetes Tutorials"},
        "aws":             {"url": "https://aws.amazon.com/free/",          "label": "AWS Free Tier + Docs"},
        "git":             {"url": "https://git-scm.com/book/en/v2",        "label": "Pro Git (free book)"},
        "typescript":      {"url": "https://www.typescriptlang.org/docs/",  "label": "TypeScript Handbook"},
        "tensorflow":      {"url": "https://www.tensorflow.org/tutorials",  "label": "TensorFlow Tutorials"},
        "pandas":          {"url": "https://pandas.pydata.org/docs/getting_started/", "label": "Pandas Getting Started"},
        "linux":           {"url": "https://linuxcommand.org/",             "label": "LinuxCommand.org (free)"},
        "java":            {"url": "https://dev.java/learn/",               "label": "Java Official Tutorials"},
        "go":              {"url": "https://go.dev/tour/",                  "label": "A Tour of Go"},
        "rust":            {"url": "https://doc.rust-lang.org/book/",       "label": "The Rust Book (free)"},
        "agile":           {"url": "https://agilemanifesto.org/",           "label": "Agile Manifesto + Guide"},
    }

    def analyze_gaps(self, resume_text, job_role, required_skills, category=""):
        text_lower = resume_text.lower()
        user_skills = {s for s in SKILL_TAXONOMY if re.search(rf"\b{re.escape(s)}\b", text_lower)}
        needed_skills   = {s.lower() for s in required_skills}
        gap_skills      = needed_skills - user_skills
        matching_skills = needed_skills & user_skills

        gap_analysis = sorted([
            {"skill": s, "priority": self._priority(s, job_role), "time_to_learn": self._time_estimate(s),
             "resource": self.LEARNING_RESOURCES.get(s, {"url":"https://www.freecodecamp.org/learn","label":"freeCodeCamp (free)"}),
             "category": self._skill_category(s)}
            for s in gap_skills], key=lambda x: -x["priority"])

        exp_years    = self._estimate_experience(resume_text)
        target_level = self._suggest_level(exp_years, matching_skills, needed_skills)

        return {
            "job_role": job_role, "user_skills": sorted(user_skills),
            "required_skills": sorted(needed_skills), "matching_skills": sorted(matching_skills),
            "gap_skills": [g["skill"] for g in gap_analysis], "gap_analysis": gap_analysis,
            "match_percentage": round(len(matching_skills) / max(len(needed_skills), 1) * 100),
            "transferable_skills": self._find_transferable(user_skills, needed_skills),
            "experience_years_est": exp_years, "target_level": target_level,
            "learning_roadmap": self._build_roadmap(gap_analysis),
        }

    def _priority(self, skill, job_role):
        p = 50
        if skill in SKILL_TAXONOMY and any(t in job_role.lower() for t in SKILL_TAXONOMY[skill]): p += 30
        if skill in ["python","javascript","sql","git","linux","java"]: p += 20
        return min(p, 100)

    def _time_estimate(self, skill):
        if skill in {"machine learning","kubernetes","aws","system design","rust","tensorflow"}: return "3-6 months"
        if skill in {"react","docker","typescript","pandas","java","go"}: return "1-3 months"
        return "2-4 weeks"

    def _skill_category(self, skill):
        if skill not in SKILL_TAXONOMY: return "Technical"
        tags = SKILL_TAXONOMY[skill]
        if "soft" in tags: return "Soft Skill"
        if "ml" in tags or "ai" in tags: return "AI/ML"
        if "cloud" in tags or "devops" in tags: return "Cloud/DevOps"
        if "database" in tags: return "Database"
        if "frontend" in tags: return "Frontend"
        if "backend" in tags: return "Backend"
        return "Technical"

    def _find_transferable(self, user_skills, needed_skills):
        result = []
        for us in user_skills:
            if us not in SKILL_TAXONOMY: continue
            for ns in needed_skills:
                if ns not in SKILL_TAXONOMY: continue
                overlap = set(SKILL_TAXONOMY[us]) & set(SKILL_TAXONOMY[ns])
                if overlap and us != ns and ns not in user_skills:
                    result.append({"have": us, "needed": ns, "reason": f"Both relate to {', '.join(list(overlap)[:2])}"})
        return result[:5]

    def _estimate_experience(self, text):
        years = [int(y) for y in re.findall(r"\b(20\d{2})\b", text)]
        return max(0, max(years) - min(years)) if len(years) >= 2 else 0

    def _suggest_level(self, years, matching, needed):
        pct = len(matching) / max(len(needed), 1) * 100
        if years >= 5 and pct >= 70: return "Senior"
        if years >= 2 and pct >= 50: return "Mid-level"
        return "Junior / Entry-level"

    def _build_roadmap(self, gap_analysis):
        return [
            {"phase": "Phase 1 – Critical Gaps (Start Now)",        "skills": [g for g in gap_analysis if g["priority"] >= 70][:3]},
            {"phase": "Phase 2 – Important Additions (1-3 months)", "skills": [g for g in gap_analysis if 40 <= g["priority"] < 70][:3]},
            {"phase": "Phase 3 – Nice to Have (3-6 months)",        "skills": [g for g in gap_analysis if g["priority"] < 40][:3]},
        ]


# ─────────────────────────────────────────────────────────────────────────────
# 3. AI INTERVIEW QUESTION GENERATOR  (FIXED)
# ─────────────────────────────────────────────────────────────────────────────

class InterviewQuestionGenerator:
    """
    Generates role-specific interview questions.
    - Always works using built-in question bank (no external deps).
    - If HF_TOKEN is set, adds real AI-generated questions as a bonus section.
    """

    QUESTION_BANK = {
        "behavioral": [
            "Tell me about a time you faced a major technical challenge. How did you overcome it?",
            "Describe a project where you had to learn a new technology quickly.",
            "Give an example of when you had to prioritize multiple deadlines.",
            "Tell me about a time you disagreed with your team's technical decision.",
            "Describe a situation where you improved a process or system significantly.",
            "Tell me about your biggest professional failure and what you learned.",
            "Give an example of when you mentored or helped a junior colleague.",
            "Describe a time you had to deliver bad news to a stakeholder.",
            "Tell me about a project you're most proud of and your specific contribution.",
            "How do you handle working in a fast-paced, ambiguous environment?",
        ],
        "system_design": [
            "How would you design a URL shortening service like bit.ly?",
            "Design a rate limiter for an API.",
            "How would you build a notification system that handles 1M+ users?",
            "Design a distributed cache system.",
            "How would you architect a real-time chat application?",
            "Explain the trade-offs between SQL and NoSQL databases.",
            "How do you handle database migrations without downtime?",
            "What is CAP theorem? Give a real-world example.",
            "How would you design a system for processing large files?",
            "Explain microservices vs monolith — when would you choose each?",
        ],
        "coding_concepts": [
            "Explain time complexity vs space complexity with an example.",
            "What's the difference between a stack and a queue?",
            "Explain recursion and give a simple example.",
            "What is memoization? When would you use it?",
            "Explain the difference between BFS and DFS.",
            "What is a hash collision? How is it resolved?",
            "Explain SOLID principles with examples.",
            "What's the difference between synchronous and asynchronous programming?",
            "Explain REST vs GraphQL — when would you choose each?",
            "What is database indexing and how does it improve performance?",
        ],
        "culture_fit": [
            "How do you stay updated with the latest technology trends?",
            "Describe your ideal working environment.",
            "How do you approach code reviews — as a reviewer and reviewee?",
            "What does 'done' mean to you in a software project?",
            "How do you balance technical debt with delivering new features?",
            "Describe your debugging process when you encounter a hard bug.",
            "How do you estimate the time required for a task?",
            "What's your approach to writing documentation?",
            "How do you handle feedback that you disagree with?",
            "What side projects or open-source contributions have you made?",
        ],
    }

    ROLE_QUESTIONS = {
        "frontend": [
            "Explain the difference between CSS Grid and Flexbox.",
            "What is the virtual DOM and how does React use it?",
            "How do you optimise a slow-rendering React component?",
            "Explain the concept of code splitting and lazy loading.",
            "What are Web Vitals and how do you improve them?",
            "How would you handle state management in a large React app?",
            "Explain CORS and how you'd resolve a CORS error.",
            "What is accessibility (a11y) and how do you implement it?",
        ],
        "backend": [
            "What is the N+1 query problem and how do you solve it?",
            "Explain connection pooling and why it matters.",
            "How do you implement authentication vs authorisation?",
            "What is idempotency? Give an API example.",
            "Explain database transactions and ACID properties.",
            "How would you implement a job queue system?",
            "What strategies do you use for API versioning?",
            "Explain the difference between JWT and session-based auth.",
        ],
        "data science": [
            "Explain bias-variance trade-off in machine learning.",
            "How do you handle class imbalance in a dataset?",
            "What is feature engineering? Give an example.",
            "Explain cross-validation and when you'd use k-fold.",
            "How do you detect and handle overfitting?",
            "What's the difference between supervised and unsupervised learning?",
            "Explain precision vs recall — when would you optimise for each?",
            "How do you approach a new machine learning problem end-to-end?",
        ],
        "devops": [
            "Explain the CI/CD pipeline you've worked with.",
            "What's the difference between Docker and a VM?",
            "How would you handle a production outage?",
            "Explain blue-green deployment vs canary deployment.",
            "What is Infrastructure as Code? Why is it important?",
            "How do you monitor application health in production?",
            "Explain Kubernetes pods, deployments, and services.",
            "What security practices do you follow in a CI/CD pipeline?",
        ],
        "machine learning": [
            "Explain gradient descent and its variants (SGD, Adam).",
            "What is transfer learning? When would you use it?",
            "Explain attention mechanisms in transformer models.",
            "How do you evaluate a classification model beyond accuracy?",
            "What is regularisation? Explain L1 vs L2.",
            "How would you deploy an ML model to production?",
            "Explain the difference between batch and online learning.",
            "What is data augmentation and when is it useful?",
        ],
    }

    def generate(self, job_role: str, skills: list, experience_level: str = "mid",
                 num_questions: int = 15) -> dict:
        # ── Input sanitisation ────────────────────────────────────────────────
        if not job_role or str(job_role).strip() in ("", "None"):
            job_role = "Software Engineer"
        skills           = skills or []
        experience_level = experience_level or "mid"
        num_questions    = max(5, min(int(num_questions), 30))
        role_lower       = job_role.lower()

        questions = {
            "behavioral":   [],
            "technical":    [],
            "system_design":[],
            "role_specific":[],
            "culture_fit":  [],
            "ai_generated": [],
        }

        # ── Behavioral ────────────────────────────────────────────────────────
        bq = random.sample(self.QUESTION_BANK["behavioral"],
                           min(max(2, num_questions // 5), len(self.QUESTION_BANK["behavioral"])))
        questions["behavioral"] = [{"q": q, "tip": "Use the STAR method: Situation → Task → Action → Result"} for q in bq]

        # ── Culture fit ───────────────────────────────────────────────────────
        cq = random.sample(self.QUESTION_BANK["culture_fit"],
                           min(max(1, num_questions // 6), len(self.QUESTION_BANK["culture_fit"])))
        questions["culture_fit"] = [{"q": q, "tip": ""} for q in cq]

        # ── System design (mid/senior) ────────────────────────────────────────
        if experience_level in ("mid", "senior"):
            sq = random.sample(self.QUESTION_BANK["system_design"],
                               min(max(2, num_questions // 5), len(self.QUESTION_BANK["system_design"])))
            questions["system_design"] = [{"q": q, "tip": "Draw architecture diagrams when possible"} for q in sq]

        # ── Coding concepts ───────────────────────────────────────────────────
        tq = random.sample(self.QUESTION_BANK["coding_concepts"],
                           min(max(2, num_questions // 5), len(self.QUESTION_BANK["coding_concepts"])))
        questions["technical"] = [{"q": q, "tip": "Provide a concrete code example"} for q in tq]

        # ── Role-specific ─────────────────────────────────────────────────────
        role_bucket = self._detect_role_bucket(role_lower)
        if role_bucket and role_bucket in self.ROLE_QUESTIONS:
            pool = self.ROLE_QUESTIONS[role_bucket]
            rq   = random.sample(pool, min(max(3, num_questions // 3), len(pool)))
            questions["role_specific"] = [{"q": q, "tip": self._role_tip(role_bucket)} for q in rq]

        # ── Skill-specific ────────────────────────────────────────────────────
        for q in self._generate_skill_questions(skills[:5])[:3]:
            questions["role_specific"].append({"q": q, "tip": "Explain with a real project example"})

        # ── AI-generated via HF (bonus, graceful fallback) ────────────────────
        ai_qs = self._generate_ai_questions(job_role, skills, experience_level)
        if ai_qs:
            questions["ai_generated"] = [
                {"q": q, "tip": "AI-generated — tailor your answer to your own experience"}
                for q in ai_qs
            ]

        total = sum(len(v) for v in questions.values())
        return {
            "job_role": job_role,
            "experience_level": experience_level,
            "total_questions": total,
            "questions": questions,
            "prep_tips": self._prep_tips(role_lower),
            "ai_powered": bool(HF_TOKEN),
        }

    def _generate_ai_questions(self, job_role, skills, level):
        """HF-powered: 3 unique contextual questions. Returns [] if token not set or API fails."""
        if not HF_TOKEN:
            return []
        skills_str = ", ".join(skills[:5]) if skills else "general programming"
        prompt = (
            f"Generate 3 unique technical interview questions for a {level}-level {job_role} "
            f"who knows {skills_str}. One question per line. No numbering. No extra text."
        )
        raw = _hf_generate(prompt, max_new_tokens=200)
        if not raw:
            return []
        lines = [l.strip(" -•1234567890.)").strip() for l in raw.split("\n") if l.strip()]
        return [l for l in lines if len(l) > 20 and "?" in l][:3]

    def _detect_role_bucket(self, role_lower):
        if any(w in role_lower for w in ["front","ui","react","angular","vue"]): return "frontend"
        if any(w in role_lower for w in ["back","api","server","django","node"]): return "backend"
        if any(w in role_lower for w in ["data scien","machine learn","ai engineer"]): return "data science"
        if any(w in role_lower for w in ["devops","sre","platform","infra"]): return "devops"
        if any(w in role_lower for w in ["deep learn","nlp","computer vision"]): return "machine learning"
        return None

    def _role_tip(self, bucket):
        return {
            "frontend":        "Mention performance metrics and browser compatibility",
            "backend":         "Discuss trade-offs and scalability considerations",
            "data science":    "Walk through your end-to-end data pipeline",
            "devops":          "Mention specific tools and metrics from your experience",
            "machine learning":"Discuss dataset, model choice, evaluation, and deployment",
        }.get(bucket, "Use specific examples from your experience")

    def _generate_skill_questions(self, skills):
        templates = [
            "Describe a project where you used {skill} in production.",
            "What are the limitations of {skill} and how did you work around them?",
            "How do you ensure code quality when working with {skill}?",
            "What's the most complex thing you've built with {skill}?",
            "Compare {skill} with alternatives — when would you choose it?",
        ]
        return [random.choice(templates).format(skill=s) for s in skills]

    def _prep_tips(self, role_lower):
        tips = [
            "Research the company's tech stack on their engineering blog",
            "Prepare 3-5 specific project stories using the STAR method",
            "Practice coding problems on LeetCode (free) or HackerRank",
            "Review your most recent project in detail — interviewers love specifics",
            "Prepare questions to ask the interviewer about their engineering culture",
        ]
        if any(w in role_lower for w in ["senior","lead","architect"]): tips.append("Prepare leadership, mentoring, and technical vision scenarios")
        if any(w in role_lower for w in ["data","ml"]): tips.append("Be ready to discuss a full ML project lifecycle from data to deployment")
        return tips


# ─────────────────────────────────────────────────────────────────────────────
# 4. FIXED /ai-questions ROUTE HELPER  (replaces broken CSV dependency)
# ─────────────────────────────────────────────────────────────────────────────

def generate_questions_from_prompt(prompt: str) -> dict:
    """
    Drop-in replacement for the old CSV-based ai_questions route logic.
    Parses the user's natural-language prompt and returns questions.
    No CSV required. Works 100% offline; adds AI questions if HF_TOKEN is set.
    """
    result = {"questions": [], "skills_str": "", "warning": None, "error": None}

    if not prompt or not prompt.strip():
        result["warning"] = "Please enter a prompt to generate questions."
        return result

    # Parse number
    num_match = re.search(r"(\d+)", prompt)
    num_q = min(int(num_match.group(1)), 50) if num_match else 15

    # Parse skills
    sk_match = re.search(r"\b(on|about|for|in)\s+(.+?)(\.|$)", prompt, re.IGNORECASE)
    raw_skills_str = sk_match.group(2) if sk_match else prompt
    user_skills = [
        s.strip().lower()
        for s in re.split(r",\s*|\s+and\s+|\s+&\s+", raw_skills_str)
        if s.strip() and len(s.strip()) > 1 and s.strip().lower() not in ("me","the","a","an","some","questions")
    ]

    if not user_skills:
        result["warning"] = "No skills detected. Try: 'Give me 10 questions on Python and SQL'."
        return result

    result["skills_str"] = ", ".join(s.title() for s in user_skills)

    # Generate using built-in engine
    gen      = InterviewQuestionGenerator()
    job_role = user_skills[0].title() + " Developer"
    data     = gen.generate(job_role=job_role, skills=user_skills, experience_level="mid", num_questions=num_q)

    # Flatten all questions
    flat = []
    for cat, items in data["questions"].items():
        for item in items:
            flat.append(item["q"] if isinstance(item, dict) else str(item))

    # Prioritise questions that mention the user's skills
    skill_matched = [q for q in flat if any(sk in q.lower() for sk in user_skills)]
    other_qs      = [q for q in flat if q not in skill_matched]

    # Optional: HF bonus questions go first
    if HF_TOKEN:
        ai_prompt = (
            f"Generate {min(5, num_q)} interview questions specifically about "
            f"{', '.join(user_skills[:4])}. One per line. No numbering."
        )
        raw_ai = _hf_generate(ai_prompt, max_new_tokens=250)
        if raw_ai:
            ai_lines = [l.strip(" -•1234567890.)").strip() for l in raw_ai.split("\n") if l.strip()]
            ai_qs    = [l for l in ai_lines if len(l) > 20 and "?" in l]
            flat     = ai_qs + skill_matched + other_qs

    result["questions"] = (flat if HF_TOKEN else skill_matched + other_qs)[:num_q]

    if not result["questions"]:
        result["warning"] = f"Could not generate questions for: {result['skills_str']}. Try more common skills like Python, React, SQL."

    return result


# ─────────────────────────────────────────────────────────────────────────────
# 5. RESUME REWRITE SUGGESTER
# ─────────────────────────────────────────────────────────────────────────────

class ResumeSuggester:
    VERB_UPGRADES = {
        "helped": "supported", "worked on": "developed", "was responsible for": "owned",
        "assisted": "collaborated with", "tried to": "implemented", "did": "executed",
        "made": "engineered", "handled": "managed", "participated in": "contributed to", "involved in": "led",
    }

    def suggest_rewrites(self, resume_text, job_role=""):
        suggestions = []
        for line in resume_text.split("\n"):
            line = line.strip()
            if not line or len(line) < 15: continue
            is_bullet = bool(re.match(r"^[•\-\*›]", line)) or (
                len(line) < 200 and any(line.strip().lower().startswith(v) for v in POWER_VERBS | WEAK_WORDS))
            if not is_bullet: continue
            issues = []; improved = line
            for weak, strong in self.VERB_UPGRADES.items():
                if weak in line.lower():
                    improved = re.compile(re.escape(weak), re.IGNORECASE).sub(
                        strong.capitalize() if line.startswith(line[0].upper()) else strong, line, count=1)
                    issues.append(f"Replaced weak verb '{weak}' → '{strong}'"); break
            if not QUANTIFIER_PATTERN.search(line) and len(line.split()) > 5:
                issues.append("Add a measurable result (%, time saved, team size, users impacted)")
                improved += " [Add metric: e.g., 'reducing X by Y%' or 'serving Z+ users']"
            if re.search(r"\bI\b|\bmy\b", line, re.IGNORECASE):
                improved = re.sub(r"\bI\b", "", improved, flags=re.IGNORECASE).strip()
                improved = re.sub(r"\bmy\b", "the", improved, flags=re.IGNORECASE)
                issues.append("Removed first-person pronouns")
            if issues:
                suggestions.append({"original": line, "improved": improved.strip(), "issues": issues,
                                    "score_before": self._line_score(line), "score_after": self._line_score(improved)})
        return {"bullet_rewrites": suggestions[:10], "summary_suggestion": self._suggest_summary(resume_text, job_role),
                "total_improvements": len(suggestions),
                "quick_wins": [s for s in suggestions if s["score_after"] - s["score_before"] >= 20][:3]}

    def _line_score(self, line):
        s = 50
        if any(line.lower().startswith(v) for v in POWER_VERBS): s += 20
        if QUANTIFIER_PATTERN.search(line): s += 20
        if any(w in line.lower() for w in WEAK_WORDS): s -= 20
        if re.search(r"\bI\b|\bmy\b", line, re.IGNORECASE): s -= 10
        return max(0, min(100, s))

    def _suggest_summary(self, text, job_role):
        years  = len(re.findall(r"\b(20\d{2})\b", text))
        skills = [s for s in list(SKILL_TAXONOMY.keys())[:10] if s in text.lower()]
        skills_str = ", ".join(skills[:3]) if skills else "relevant technologies"
        if job_role:
            return (f"Results-driven {job_role} with {max(1, years // 2)}+ years of experience "
                    f"building scalable solutions using {skills_str}. Proven track record of delivering "
                    f"high-impact projects on time. Passionate about clean code and continuous learning.")
        return (f"Detail-oriented software professional with hands-on experience in {skills_str}. "
                f"Strong problem-solver focused on robust, maintainable solutions. "
                f"Collaborative team player committed to engineering excellence.")


# ─────────────────────────────────────────────────────────────────────────────
# 6. JOB-ROLE OPTIMIZER
# ─────────────────────────────────────────────────────────────────────────────

class RoleOptimizer:
    def optimize_for_role(self, resume_text, job_role, required_skills, category=""):
        text_lower       = resume_text.lower()
        keywords_to_add  = [s for s in required_skills if s.lower() not in text_lower]
        keywords_present = [s for s in required_skills if s.lower() in text_lower]
        r = job_role.lower()
        return {
            "job_role": job_role,
            "keyword_coverage": round(len(keywords_present) / max(len(required_skills), 1) * 100),
            "keywords_present": keywords_present, "keywords_to_add": keywords_to_add,
            "emphasize": self._what_to_emphasize(r), "tone_tips": self._tone_tips(r),
            "section_order": self._section_order(r),
            "keyword_density": {s: {"count": c, "density": round(c / max(len(text_lower.split()), 1) * 100, 2)}
                                 for s in required_skills if (c := text_lower.count(s.lower())) > 0},
            "tailoring_checklist": self._tailoring_checklist(job_role, keywords_to_add),
        }

    def _what_to_emphasize(self, r):
        if "senior" in r or "lead" in r: return ["Leadership & mentoring","Architecture decisions","Cross-team impact","Business metrics"]
        if "data" in r or "ml" in r:     return ["Dataset sizes","Model accuracy improvements","Business impact of ML","Publications"]
        if "front" in r:                  return ["Performance metrics","Accessibility work","Design system contributions","User engagement"]
        if "back" in r or "api" in r:    return ["Throughput/latency","Scale handled","Database optimisations","API design"]
        if "devops" in r or "sre" in r:  return ["Uptime/reliability","Deployment frequency","Cost savings","Incident response"]
        return ["Quantified achievements","Technologies used","Team collaboration","Project outcomes"]

    def _tone_tips(self, r):
        if "manager" in r or "lead" in r:         return ["Lead with leadership achievements","Quantify team size","Show cross-functional collaboration"]
        if "research" in r or "scientist" in r:   return ["Mention publications/patents","Highlight dataset scale","Include academic achievements"]
        return ["Use active voice and strong action verbs","Lead each bullet with the most impactful part","Tailor keywords from the job description"]

    def _section_order(self, r):
        if "data" in r or "research" in r: return ["Contact","Summary","Education","Skills","Research/Projects","Experience","Publications"]
        if "fresh" in r or "intern" in r:  return ["Contact","Summary","Education","Projects","Skills","Experience (if any)"]
        return ["Contact","Summary","Experience","Skills","Projects","Education"]

    def _tailoring_checklist(self, job_role, missing_skills):
        return [
            {"item": f"Add missing keywords: {', '.join(missing_skills[:4]) if missing_skills else 'None missing — great!'}", "done": len(missing_skills) == 0},
            {"item": "Customise your summary to mention this specific role",    "done": False},
            {"item": "Mirror language from the job description",                "done": False},
            {"item": "Quantify at least 3 achievements in experience section",  "done": False},
            {"item": "Ensure your most relevant experience is listed first",    "done": False},
        ]


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC FACTORY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

_feedback_engine = SmartFeedbackEngine()
_gap_analyzer    = SkillGapAnalyzer()
_question_gen    = InterviewQuestionGenerator()
_rewrite_engine  = ResumeSuggester()
_role_optimizer  = RoleOptimizer()


def get_smart_feedback(resume_text, job_role="", required_skills=None):
    return _feedback_engine.generate_feedback(resume_text, job_role, required_skills)

def get_skill_gaps(resume_text, job_role, required_skills, category=""):
    return _gap_analyzer.analyze_gaps(resume_text, job_role, required_skills, category)

def get_interview_questions(job_role, skills, experience_level="mid", num=15):
    return _question_gen.generate(job_role, skills, experience_level, num)

def get_rewrite_suggestions(resume_text, job_role=""):
    return _rewrite_engine.suggest_rewrites(resume_text, job_role)

def get_role_optimization(resume_text, job_role, required_skills, category=""):
    return _role_optimizer.optimize_for_role(resume_text, job_role, required_skills, category)

# NEW: used by the fixed /ai-questions route
def get_questions_from_prompt(prompt: str) -> dict:
    return generate_questions_from_prompt(prompt)
