# 🛡️ Kavach — Legal AI Trust Platform

**Making AI safe, reliable, and defensible for legal practice**

[![WashU Law Challenge](https://img.shields.io/badge/WashU%20Law-2026-blue)](https://law.washu.edu/about/ai-initiative/ai-collaborative/washu-law-international-vibe-coding-challenge/)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal)](https://fastapi.tiangolo.com)

---

## 🎯 The Problem

Every day, lawyers use AI to draft briefs, research cases, and advise clients. But:

- **87% of lawyers fear AI hallucinations**
- **A single fabricated citation** can destroy a lawyer's career
- **Privileged information** can be leaked to AI tools
- **No way to verify** if AI output is trustworthy

## 💡 Our Solution

Kavach (कवच — Sanskrit for "Shield/Armor") provides:

### 1. 📜 Citation Verification
- Verifies case citations against Indian Kanoon
- Curated database of 20+ landmark cases
- Supreme Court & High Court coverage
- **No more hallucinated citations in briefs**

### 2. 🔒 Privilege Shield
- Detects 7 types of sensitive content:
  - Attorney-client privilege
  - Work product
  - Confidential information
  - Personal data (Aadhaar, PAN, phone)
  - Financial data
  - Medical records
  - Trade secrets
- **Generates safe, redacted versions for AI tools**

### 3. 📊 Confidence Scoring
- Trust scores for every AI output
- Citation accuracy score
- Source reliability score
- Privilege safety score
- **Know exactly how much to trust AI**

### 4. ⚖️ Case Prediction
- Win probability for 8 case types
- Timeline estimation
- Remedy recommendations
- Risk factor identification
- **Data-driven litigation strategy**

### 5. 📋 Audit Trail
- Immutable logs of every operation
- Court-defensible evidence
- Compliance with disclosure requirements
- **Prove you used AI responsibly**

---

## 🚀 Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
# Open frontend/index.html in browser
# Or serve with any static file server
```

### API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze` | POST | Complete trust analysis |
| `/verify-citation` | POST | Verify single citation |
| `/scan-privilege` | POST | Scan for privilege issues |
| `/predict-case` | POST | Predict case outcome |
| `/batch-verify` | POST | Verify multiple citations |
| `/audit/history` | GET | Get audit trail |
| `/audit/report` | GET | Generate audit report |

---

## 🎬 Demo

See Kavach in action:

1. **Text Analysis** — Paste legal text, get trust score + redacted version
2. **Citation Verification** — Verify any case citation instantly
3. **Case Prediction** — Get win probability and strategy recommendations

---

## 🏗️ Architecture

```
kavach/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── ai/
│   │   ├── kavach_engine.py       # Main orchestration
│   │   ├── citation_verifier.py   # Citation verification
│   │   ├── privilege_shield.py    # Privilege detection
│   │   ├── confidence_scorer.py   # Trust scoring
│   │   ├── case_predictor.py      # Case outcome prediction
│   │   └── audit_trail.py         # Audit logging
│   └── requirements.txt
├── frontend/
│   └── index.html                 # Demo interface
├── docs/
│   ├── demo-script.md             # Video demo script
│   └── submission.md              # 500-word submission
└── README.md
```

---

## 🔒 Security & Privacy

- **No data storage** — All analysis is ephemeral
- **No external calls** — Citation verification uses local database
- **Audit trail** — Complete logs for accountability
- **Privilege protection** — Automatic detection and redaction

---

## 🎓 For Judges

Kavach addresses the #1 concern of every legal AI user: **trust**.

- **Citation verification** prevents hallucinated cases from reaching court
- **Privilege shield** protects attorney-client confidentiality
- **Confidence scores** show exactly how reliable AI output is
- **Audit trail** provides evidence of responsible AI use

---

## 🛠️ Built With

- **AI:** Codex + Nous Portal (100% vibe coded)
- **Backend:** Python FastAPI
- **Frontend:** HTML + Tailwind CSS
- **Legal Data:** Indian Kanoon API + Curated database

---

## 📄 License

MIT

---

## 👤 Author

**Lokesh** — Final year BA LLB student at DSNLU Visakhapatnam

Built for [WashU Law International Vibe Coding Challenge 2026](https://law.washu.edu/about/ai-initiative/ai-collaborative/washu-law-international-vibe-coding-challenge/)

---

*🛡️ Kavach — Because AI should make law better, not riskier.*
