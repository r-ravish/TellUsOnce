# Tell Us Once — Backend API

**Student Welfare / Joined-Up Case Management MVP**

## 🎯 Project Purpose

Students facing hardship currently have to visit multiple departments and repeatedly explain the same situation. **Tell Us Once** solves this by letting the student tell their story **once**. The backend automatically:

1. Receives the student's story
2. Masks sensitive information (PII)
3. Uses AI to understand the situation
4. Converts the story into structured requests
5. Determines urgency, risk, and confidence
6. Checks documents and policies
7. Auto-approves **only** safe routine cases
8. Routes other requests to the correct department
9. Escalates risky/uncertain cases to a human
10. Maintains a shared case timeline and audit trail

### Core Safety Rule

> **AI SUGGESTS. PLAIN RULES DECIDE.**
>
> The system **NEVER** declines or rejects a student's request.
> It may only: **approve**, **route**, or **escalate**.

---

## 🛠️ Tech Stack

| Technology      | Purpose                    |
| --------------- | -------------------------- |
| Python 3.11+    | Runtime                    |
| FastAPI         | Web framework              |
| SQLite          | Database                   |
| SQLAlchemy      | ORM                        |
| Pydantic        | Data validation            |
| OpenAI API      | AI story analysis          |
| python-dotenv   | Environment configuration  |
| pytest          | Testing                    |

---

## 📦 Installation

### 1. Clone and checkout

```bash
git clone https://github.com/r-ravish/TellUsOnce.git
cd TellUsOnce/Backend
git checkout Madhav
```

### 2. Create virtual environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key (optional — the backend works without it):

```env
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=sqlite:///./tell_us_once.db
```

---

## 🚀 Running the Backend

```bash
uvicorn app.main:app --reload
```

Or:

```bash
python run.py
```

The API will be available at: **http://localhost:8000**

- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📡 API Endpoints

| Method | Endpoint                          | Description                          |
| ------ | --------------------------------- | ------------------------------------ |
| GET    | `/api/health`                     | Health check                         |
| GET    | `/api/departments`                | List all 12 departments              |
| GET    | `/api/cases`                      | List all cases                       |
| GET    | `/api/cases/{id}`                 | Get case details with timeline/audit |
| GET    | `/api/cases/{id}?department=Name` | Department-filtered case view        |
| POST   | `/api/intake`                     | Submit a student story               |
| POST   | `/api/requests/{id}/action`       | Department staff action              |
| GET    | `/api/gaps`                       | System gaps and issues               |
| POST   | `/api/demo/reset`                 | Reset database to demo data          |

---

## 🗄️ Database

SQLite database with 5 tables:

- **departments** — 12 university departments
- **cases** — Student cases with original/masked story
- **requests** — Individual needs extracted from each case
- **timeline** — Ordered events for each case
- **audit_logs** — Detailed audit trail of every decision

---

## 🤖 AI Behavior

The AI analyzes the student's masked story and returns structured JSON:

```json
{
  "summary": "...",
  "urgency": "low | medium | high",
  "risk_flag": true/false,
  "confidence": 0.0-1.0,
  "needs": [
    {
      "request_type": "fee_extension",
      "documents_mentioned": ["supporting letter"],
      "days_requested": 5,
      "suggested_action": "approve",
      "reason": "..."
    }
  ]
}
```

### AI Fallback

If OpenAI is unavailable (no API key, timeout, error), the system uses a **safe fallback**:

- Generates a basic summary via keyword matching
- Sets low confidence (0.3)
- **Never** auto-approves
- Routes or escalates all requests for human review

---

## 🔒 Policy Gate

A request is **auto-approved** only when **ALL** conditions are true:

1. ✅ Policy explicitly allows auto-approval
2. ✅ Requested days ≤ policy limit
3. ✅ Required documents are present
4. ✅ `risk_flag == false`
5. ✅ AI confidence ≥ 0.85

If **any** condition fails → **route** or **escalate** (never decline).

### Policies

| Request Type             | Department           | Auto-Approve | Limit   | Required Document    |
| ------------------------ | -------------------- | ------------ | ------- | -------------------- |
| Fee Extension            | Accounts             | ✅ Yes       | 7 days  | Supporting letter    |
| Medical Leave            | Head of Department   | ✅ Yes       | 3 days  | Medical certificate  |
| Attendance Condonation   | Head of Department   | ❌ No        | —       | —                    |
| Exam Deferral            | Exam Cell            | ❌ No        | —       | —                    |
| Hostel Notice            | Hostel               | ❌ No        | —       | —                    |
| Counselling Support      | Counselling          | ❌ Always escalate | — | —                    |

---

## 🧪 Testing

Run the full test suite:

```bash
pytest
```

With verbose output:

```bash
pytest -v
```

Tests cover:
- Health, department, case endpoints
- Intake processing pipeline
- Routine fee extension auto-approval
- Fee extension exceeding limit
- Attendance condonation routing
- Exam deferral routing
- Counselling escalation
- Risk/distress escalation
- Prompt injection protection
- Missing documents handling
- Low AI confidence handling
- Department staff actions
- Timeline creation
- Audit log creation
- Demo reset
- Core safety invariant (no decline/reject)
- PII masking
- Multi-department complex cases

---

## 🔄 Demo Reset

Reset the database with 3 demo scenarios:

```bash
curl -X POST http://localhost:8000/api/demo/reset
```

### Demo Scenarios

| Case | Scenario                      | Expected Result    |
| ---- | ----------------------------- | ------------------ |
| A    | 5-day fee extension + letter   | **AUTO APPROVED**  |
| B    | Hospital + multi-department    | **ROUTED**         |
| C    | Distress + prompt injection    | **ESCALATED**      |

---

## 📋 Example API Requests

### Submit a Student Story

```bash
curl -X POST http://localhost:8000/api/intake \
  -H "Content-Type: application/json" \
  -d '{
    "student_reference": "STUDENT-001",
    "story": "My father was hospitalized and I need a 5 day fee extension. I have the supporting letter."
  }'
```

### Department Action

```bash
curl -X POST http://localhost:8000/api/requests/1/action \
  -H "Content-Type: application/json" \
  -d '{
    "action": "accept",
    "note": "Processing request."
  }'
```

### Check System Gaps

```bash
curl http://localhost:8000/api/gaps
```

### View Case Details

```bash
curl http://localhost:8000/api/cases/1
```

### Department-Filtered View

```bash
curl "http://localhost:8000/api/cases/1?department=Accounts"
```
