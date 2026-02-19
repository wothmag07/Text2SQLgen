# Text2SQLgen

An AI-powered natural language to SQL query engine built on a medical database. Ask questions in plain English and get back structured SQL results — powered by Groq's LLaMA 3.3 70B model, FastAPI, React, and PostgreSQL, all orchestrated with Docker Compose.

## Architecture

```
User  →  React UI (Nginx :3000)
            → FastAPI Backend (Uvicorn :8000)
                → Groq LLM API (llama-3.3-70b-versatile)
                → PostgreSQL :5432 (llm schema)
            ← SQL + formatted results
```

## Features

- **Natural Language Queries** — type a question like *"What is the average BMI of diabetic patients?"* and get SQL + results
- **Intelligent Agent** — maintains conversation history (last 5 exchanges) for context-aware follow-ups
- **Schema-Aware** — automatically extracts and caches the database schema so the LLM generates accurate queries
- **Safety First** — only `SELECT` / `WITH` queries are allowed; `INSERT`, `UPDATE`, `DELETE` are rejected
- **Deterministic Output** — temperature set to 0.0 for consistent SQL generation
- **Dark-Themed UI** — responsive chat interface with collapsible SQL blocks and scrollable result tables
- **Suggestion Chips** — pre-built example questions to get started quickly
- **One-Command Deployment** — `docker-compose up --build` spins up the entire stack

## Tech Stack

| Layer | Technology |
|-------|------------|
| LLM | Groq API — `llama-3.3-70b-versatile` |
| Backend | FastAPI 0.115 · Uvicorn · psycopg2 |
| Frontend | React 19 · Vite 6 · Axios |
| Database | PostgreSQL 16 (Alpine) |
| Proxy | Nginx (Alpine) |
| Orchestration | Docker Compose |

## Database

Five medical datasets are auto-loaded from CSV on first startup into the `llm` schema:

| Table | Records | Description |
|-------|---------|-------------|
| `llm.heartattack_data` | ~8,700 | Heart attack risk factors across countries |
| `llm.breastcancer_data` | ~286 | Breast cancer diagnosis & treatment |
| `llm.livercirrhosis_data` | ~418 | Liver cirrhosis progression & lab results |
| `llm.diabetes_data` | ~768 | Diabetes risk factors & outcomes |
| `llm."glaucoma_Data"` | ~100,000 | Glaucoma diagnosis & eye measurements |

## Project Structure

```
Text2SQLgen/
├── docker-compose.yml          # Full-stack orchestration
├── .env.example                # Environment variable template
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py             # FastAPI app, CORS, health check
│       ├── config.py           # Env var loading
│       ├── database.py         # PostgreSQL connection & schema extraction
│       ├── agents/
│       │   ├── base.py         # Abstract Agent class
│       │   └── text2sql.py     # Text2SQL agent (Groq + query pipeline)
│       └── routes/
│           └── chat.py         # /api/chat, /api/schema, /api/suggestions
│
├── frontend/
│   ├── Dockerfile              # Multi-stage: Node build → Nginx serve
│   ├── nginx.conf              # SPA routing + API proxy
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx             # Main component & state
│       ├── App.css             # Dark theme styles
│       ├── api/
│       │   └── chat.js         # Axios API client
│       └── components/
│           ├── ChatWindow.jsx  # Scrollable message container
│           ├── MessageBubble.jsx # Message display + SQL toggle + result table
│           ├── InputBar.jsx    # User input form
│           └── Suggestions.jsx # Example question chips
│
├── db/
│   ├── init.sql                # Schema & table creation
│   └── load-data.sh            # CSV import via psql \COPY
│
└── datatables/                 # Medical CSV datasets
    ├── heart_attack_prediction_dataset.csv
    ├── breast-cancer.csv
    ├── cirrhosis.csv
    ├── diabetes.csv
    └── glaucoma_dataset.csv
```

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- A free [Groq API key](https://console.groq.com/keys)

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/gowthamarulmozhi/Text2SQLgen.git
   cd Text2SQLgen
   ```

2. **Create your environment file**

   ```bash
   cp .env.example .env
   ```

   Open `.env` and add your Groq API key:

   ```env
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
   POSTGRES_DB=wothmag
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=qwerty
   DATABASE_URL=postgresql://postgres:qwerty@db:5432/wothmag
   ```

3. **Start the application**

   ```bash
   docker-compose up --build
   ```

4. **Open in browser**

   | Service | URL |
   |---------|-----|
   | Frontend | [http://localhost:3000](http://localhost:3000) |
   | Backend API | [http://localhost:8000](http://localhost:8000) |
   | API Docs (Swagger) | [http://localhost:8000/docs](http://localhost:8000/docs) |

### Startup Sequence

1. PostgreSQL starts and passes its health check
2. `init.sql` creates the `llm` schema and tables
3. `load-data.sh` imports all CSV datasets
4. Backend waits for DB readiness, then starts Uvicorn
5. Frontend builds the React app, Nginx begins serving

## API Reference

### `POST /api/chat`

Send a natural language question and receive SQL + results.

**Request**

```json
{
  "message": "How many patients have diabetes?",
  "history": [
    ["Previous question", "Previous answer"]
  ]
}
```

**Response**

```json
{
  "response": "There are 268 patients with diabetes.",
  "sql": "SELECT COUNT(*) FROM llm.diabetes_data WHERE \"Outcome\" = 1;",
  "columns": ["count"],
  "results": [[268]],
  "error": null
}
```

### `GET /api/schema`

Returns the full database schema (tables, columns, data types).

### `GET /api/suggestions`

Returns a list of 8 example questions to get started.

### `GET /health`

Health check endpoint.

```json
{ "status": "ok" }
```

## Example Questions

- How many patients are there in total across all tables?
- What is the average BMI of diabetic patients?
- Show the top 5 countries with the highest heart attack rates
- What percentage of breast cancer patients received irradiation?
- List all liver cirrhosis patients in Stage 4
- What is the average intraocular pressure for glaucoma patients by type?

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | *(required)* |
| `POSTGRES_DB` | Database name | `wothmag` |
| `POSTGRES_USER` | PostgreSQL user | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `qwerty` |
| `DATABASE_URL` | Full connection string | `postgresql://postgres:qwerty@db:5432/wothmag` |

## Local Development (without Docker)

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

> Requires a running PostgreSQL instance. Update `DATABASE_URL` in `.env` to point to `localhost` instead of `db`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

> Vite dev server runs on port 5173 and proxies `/api` requests to `localhost:8000`.

## License

[MIT](LICENSE) — Gowtham Arulmozhi
