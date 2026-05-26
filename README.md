# Content Strategy Agent

A LangGraph-based autonomous agent that generates 30-day social media content calendars monthly. Runs on the 1st of each month or can be triggered manually via API.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required keys:
- `ANTHROPIC_API_KEY` — Claude API key
- `TAVILY_API_KEY` — Web search for trends
- `MONGODB_URI` — MongoDB Atlas connection
- `SENDGRID_API_KEY` — Email notifications
- `GOOGLE_SERVICE_ACCOUNT_JSON` — Google Sheets access

Optional config:
- `NICHE` — Your industry/niche (default: SaaS)
- `PLATFORMS` — Comma-separated list (default: LinkedIn,Instagram)
- `BRAND_TONE` — Your brand voice
- `COMPETITOR_URLS` — Comma-separated competitor websites

### 3. Start the API Server

```bash
uvicorn api.main:app --reload
```

The server runs on `http://localhost:8000`

Health check: `GET http://localhost:8000/health`

## API Endpoints

### Generate Content Plan

```bash
POST /api/generate-plan
{
  "month": "June 2025"
}
```

Returns:
```json
{
  "plan_id": "uuid",
  "status": "completed",
  "calendar_days": 30,
  "quality_score": 8
}
```

### Approve Plan

```bash
POST /api/approve/{plan_id}
```

### Check Status

```bash
GET /api/status/{plan_id}
```

### Get Calendar

```bash
GET /api/calendar/{plan_id}
```

Returns the full 30-day calendar in JSON format.

## Architecture

### LangGraph Workflow

```
START → supervisor → planner → research → decision
                                           ↓
                                    calendar_builder → notifier → END
                                      ↑ (retry)
                                    decision
```

**Nodes:**
1. **Supervisor** — Understands mission, reads config
2. **Planner** — Breaks mission into research tasks
3. **Research** — Runs 4 tools in parallel:
   - Trend Scraper (Tavily)
   - Competitor Scraper (Playwright)
   - Analytics Reader (CSV/MongoDB)
   - Campaign Checker (YAML/MongoDB)
4. **Decision** — Evaluates research quality (1-10), decides to retry or proceed
5. **Calendar Builder** — Generates 30-day plan via Claude, parses into structured format
6. **Notifier** — Sends email + saves to Google Sheets

### Key Components

- **graph/** — LangGraph workflow definition
- **agents/** — Thin LLM agent wrappers
- **tools/** — LangChain tools for research
- **llm/** — Claude client + prompts + chains
- **db/mongo/** — MongoDB models + repositories
- **output/** — Google Sheets + email delivery
- **memory/** — ChromaDB vector memory
- **api/** — FastAPI endpoints
- **scheduler/** — APScheduler for monthly cron

## Database Schema

### MongoDB Collections

**plans** — Each monthly plan
```json
{
  "plan_id": "uuid",
  "month": "June 2025",
  "niche": "SaaS",
  "platforms": ["LinkedIn", "Instagram"],
  "status": "pending|approved|rejected",
  "created_at": "timestamp",
  "approved_at": "timestamp"
}
```

**calendars** — 30-day structured calendars
```json
{
  "calendar_id": "uuid",
  "plan_id": "uuid",
  "days": [
    {
      "day": 1,
      "date": "2025-06-01",
      "platform": "LinkedIn",
      "content_type": "Post",
      "topic": "AI Trends in SaaS",
      "notes": "Tie to recent news"
    }
  ],
  "quality_score": 8,
  "status": "draft|approved|published",
  "created_at": "timestamp"
}
```

**results** — Delivery records
```json
{
  "result_id": "uuid",
  "plan_id": "uuid",
  "sheet_url": "https://...",
  "email_sent": true,
  "notification_email": "...",
  "sent_at": "timestamp"
}
```

## Scheduler

Automatically runs on:
- **Day:** 1st of every month
- **Time:** 6:00 AM (UTC)

To run the scheduler:

```bash
python -c "import asyncio; from scheduler.cron import run_scheduler; asyncio.run(run_scheduler())"
```

## Development Notes

### Adding Custom Tools

Add a new tool in `tools/` as a `@tool` decorated function:

```python
from langchain_core.tools import tool

@tool
def my_tool(param: str) -> list[dict]:
    """Tool description."""
    return [{"result": "data"}]
```

Then add it to the research_node for parallel execution.

### Customizing Prompts

All prompts are in `llm/prompts.py`. Modify the PromptTemplate instances to change agent behavior.

### Running Locally

```bash
# Install
pip install -r requirements.txt

# Setup MongoDB locally or use Atlas
# Fill in .env

# Run API
uvicorn api.main:app --reload

# In another terminal, trigger a plan
curl -X POST http://localhost:8000/api/generate-plan \
  -H "Content-Type: application/json" \
  -d '{"month": "June 2025"}'
```

## Next Steps

- [ ] Implement Google Sheets creation (gspread)
- [ ] Implement SendGrid email delivery
- [ ] Add approval workflow (approval_node)
- [ ] Add content generation node (create actual post copy)
- [ ] Test with real MongoDB + API keys
- [ ] Deploy to Railway/Render
- [ ] Add monitoring + error alerts
