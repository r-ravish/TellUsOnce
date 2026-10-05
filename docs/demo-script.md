# TellUsOnce — Demo Script & Judge Workflow
**3-minute demo | Role 1 speaking parts highlighted**

---

## ⚡ Before You Start (30 seconds before judges arrive)

Run these in two separate terminal windows:

```bash
# Terminal 1 — Backend
cd tellusonce/backend
python3 run.py

# Terminal 2 — Frontend
cd tellusonce
npm run dev
```

Open **two browser windows** side by side:
- **Window A**: http://localhost:5173  → "View as: Accounts"
- **Window B**: http://localhost:5173  → "View as: Counselling"

Reset to clean state:
```bash
curl -X POST http://localhost:8000/api/demo/reset
```

---

## 🎬 Demo Flow (3 minutes total)

---

### PART 1 — The Problem (40 seconds) | *Role 6 speaks*

> **Say:**
> "Meet Riya. Her father was hospitalised. She was away for 9 days.
> She needs a fee extension, attendance condonation, an exam deferral,
> and hostel clearance — four different offices.
> Today she has to physically visit each one, repeat her story four times,
> and hope someone coordinates.
> Tell Us Once solves this in a single submission."

**Show:** The case list page with the 3 pre-seeded cases visible.

---

### PART 2 — The Shared Live View (40 seconds) | *Role 4 speaks*

> **Say:**
> "Every support office sees one shared, live case — created once.
> Here's Case 2: Riya's hospitalisation case.
> It has 4 requests, each already routed to the right department.
> Watch Window A (Accounts) and Window B (Counselling)."

**Click:** Open Case 2 in both windows.
- Window A → switch "View as" → Accounts → sees fee_extension
- Window B → switch "View as" → Counselling → sees different filtered view

**Action in Window A:** Click Accept on the fee_extension request.

> **Say:** "Accounts just accepted the fee request. Watch Window B refresh automatically."

*(2-second polling updates Window B's timeline)*

---

### PART 3 — Tell Us Once Intake with LLM (80 seconds) | *Roles 1, 3, 5 speak*

#### Step 3a — Paste the story | *Role 5 clicks*

Go to **Intake** page. Click the **"Riya's Story"** sample button (or paste):

```
Father had surgery. I was home 9 days. My attendance is short,
I missed the mid-term, and my fee is due Friday.
I have my hospital letter.
```

Click **Submit**.

#### Step 3b — Explain the AI | *Role 1 (YOU) speaks — 25 seconds*

> **Say:**
> "Before that story reaches the AI, Role 3's function strips out
> any names, phone numbers, and IDs — the model only sees
> clean, anonymised text.
>
> Then our AI helper — running on Azure Foundry with gpt-4.1-mini
> in Korea Central — reads it once and returns a structured case:
> urgency HIGH, no risk flag, four separate needs, each with a
> suggested action and a reason.
>
> The AI only *suggests*. A separate rules engine makes every decision."

**Show:** The new case appearing with 4 requests, each with a decision card.

#### Step 3c — Show the policy gate | *Role 3 speaks*

> **Say:**
> "The policy gate checks 5 conditions before approving anything:
> the policy allows auto-approve, days within the limit,
> required documents present, no risk flag, confidence above 85%.
> If all 5 pass → auto-approved with a reason.
> If any fail → routed to the department.
> There is **no decline function** — the AI cannot reject anyone."

**Point to:** Case 1 (DEMO-001) — fee_extension → **Auto Approved** ✅

---

### PART 4 — The Three Cases (shown together) | *Roles 1 + 3 speak*

Point to all 3 cases in the list:

| Case | Student | What happened | Status |
|---|---|---|---|
| Case 1 | DEMO-001 | 5-day fee extension, sanction letter present | ✅ **Auto Approved** |
| Case 2 | DEMO-002 | 9-day hospitalisation, 4 departments | 🔀 **Routed** to Accounts, HoD, Exam Cell, Hostel |
| Case 3 | DEMO-003 | Distress wording detected | 🚨 **Escalated** — human contact shown |

> *Role 1 (YOU) on Case 3:*
> "Azure's content filter caught the distress wording before it even
> reached our model — that's a guardrail we didn't have to build.
> Our code treats any 400 response as a risk signal and escalates immediately.
> Two separate safety layers — the AI and the platform."

---

### PART 5 — Escalation & Human Contact (20 seconds) | *Role 5 speaks*

**Click:** Case 3 (DEMO-003)

**Show:**
- 🚨 Red risk badge
- Counselling request → status: **Escalated**
- Human contact panel visible (name, phone, location of welfare advisor)
- Decision card: *"An AI flagged this for human review"*

---

### PART 6 — The Gaps Panel (15 seconds) | *Role 5 speaks*

**Click:** Gaps tab in the list view.

> **Say:**
> "This panel shows every request that's falling through the cracks —
> unowned, stuck in 'Routed', or students spread across 3+ departments.
> A coordinator can see the entire picture in one place."

---

### PART 7 — Impact (30 seconds) | *Role 2 speaks*

> **Say:**
> "Before: Riya visits 4 offices, retells her story 4 times, waits days for each.
> After: story submitted once, 4 requests created and routed in under 5 seconds,
> routine ones auto-approved instantly.
>
> This is not a pilot on real students — all data here is synthetic.
> But the design targets are based on real university welfare workflows,
> and the platform maps directly onto ServiceNow's Virtual Agent,
> case records, and Flow Designer — presented as a concept."

---

## 🚨 Safety Net: If Live LLM Fails

If the API call fails during the demo:
1. The system **automatically falls back to cached outputs** — no crash, no error to students
2. Say plainly: *"This output is from our verified cache — our fallback ladder ensures the demo always runs, even if Azure is slow."*
3. To force cache-only mode: set `LLM_PROVIDER=__stub__` in `.env`, restart backend

---

## ❓ Likely Judge Questions — YOUR answers (Role 1)

| Question | Your answer |
|---|---|
| **Why Azure Foundry?** | "Deploy and manage the model in one place with built-in safety tooling. One env var switches to any other provider if it fails." |
| **Why gpt-4.1-mini?** | "The task is structured extraction from short text — a small, fast model is accurate enough, cheaper, and more consistent." |
| **What if the AI is wrong?** | "It only suggests. The policy gate checks 5 hard rules independently. The AI cannot approve or decline by itself." |
| **What stops prompt injection?** | "Three layers: PII masking before the model sees anything; the system prompt tells the AI to treat student text as untrusted; and the gate enforces rules regardless of what the AI suggests. Show Story 6." |
| **What about privacy?** | "Names, phones, emails, IDs are stripped by regex before anything leaves the server. Only masked text reaches the model. All demo data is synthetic." |
| **What if the service goes down?** | "Cached outputs for all 8 demo stories. Safe default escalates to human. The demo keeps running." |
| **Story 5 — distress?** | "Azure's content filter triggered a 400 before the model saw it. Our code escalates any refusal as a risk signal. Human contact shown immediately. We never try to counsel or diagnose." |

---

## 🎯 Definition of Done — Check at 11:15

- [ ] `GET /api/health` → `{"status":"healthy"}`
- [ ] Case list shows 3 demo cases after `POST /api/demo/reset`
- [ ] Case 1 shows **Auto Approved** with a visible reason
- [ ] Case 2 shows **4 requests Routed** to different departments
- [ ] Case 3 shows **Escalated** with risk badge and human contact panel
- [ ] Accepting in Window A updates Window B within 2 seconds
- [ ] Pasting a new story creates a valid multi-request case
- [ ] Gaps panel shows stuck/unowned requests
- [ ] `POST /api/demo/reset` returns to clean state cleanly
- [ ] Backup video recorded

---

## 🖥️ Local URLs

| Service | URL |
|---|---|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **Health check** | http://localhost:8000/api/health |
| **Reset demo** | `POST http://localhost:8000/api/demo/reset` |
| **Gaps** | `GET http://localhost:8000/api/gaps` |

---

## 📋 Speaking Order

| Part | Who | Time |
|---|---|---|
| Problem | Role 6 | 40s |
| Shared view + live update | Role 4 | 40s |
| Intake + LLM explanation | **Role 1 (YOU)** | 25s |
| Policy gate + decision cards | Role 3 | 25s |
| Cases A/B/C overview | **Role 1 (YOU)** | 10s on Case C |
| Escalation / human contact | Role 5 | 20s |
| Gaps panel | Role 5 | 15s |
| Impact | Role 2 | 30s |

---

*All data is synthetic. All policy values are fictional. Not Chitkara's real policies.*
