# AlphaLake

AlphaLake is an AI-assisted financial research platform built as a hands-on engineering project across data engineering, backend development, cloud infrastructure, AI, and frontend product development.

The project currently combines SEC financial data, Databricks analytics, FastAPI, PostgreSQL, a local Ollama LLM, Next.js, Docker Compose, and Terraform.

The goal is not to collect technologies. AlphaLake is being developed feature by feature, with each new component added when it solves a concrete engineering or product problem.

## Current Status

AlphaLake currently supports:

- SEC Company Facts ingestion
- Bronze / Silver / Gold transformations
- PySpark + Delta Lake processing in Databricks
- financial data quality checks
- Gold financial and derived metrics
- Databricks Jobs managed with Terraform
- FastAPI backend
- REST APIs
- WebSocket chat
- local LLM inference with Ollama
- `qwen3:4b-instruct`
- AI tool calling against Databricks financial data
- Next.js chat interface
- PostgreSQL-backed conversation persistence
- conversation history loading
- conversation sidebar
- new chats with generated UUID session IDs
- persisted conversation titles
- rename conversation
- delete conversation
- hover action menu with click-away behavior
- Docker Compose integration for frontend, backend and Ollama
- SEC ticker → CIK resolution

The next main product feature is a company watchlist.

## Architecture

```text
User
 │
 ▼
Next.js
 │
 ├── REST
 └── WebSocket
 │
 ▼
FastAPI
 ├──────────────► PostgreSQL
 │                conversations
 │                messages
 │                watchlists (next)
 │
 ├──────────────► Ollama
 │                qwen3:4b-instruct
 │
 └──────────────► Databricks
                  Bronze / Silver / Gold
                  SEC financial analytics
```

For a more detailed breakdown, see `architecture.md`.

## Data Pipeline

AlphaLake uses a medallion-style analytical pipeline.

```text
SEC
 │
 ▼
Bronze
 │
 ▼
Silver
 │
 ▼
Gold Core
 │
 ├── company financials
 │
 ▼
Gold Derived
 ├── growth metrics
 ├── rolling metrics
 └── cash-flow-quality metrics
```

Current Gold outputs:

```text
alphalake.gold.company_financials
alphalake.gold.growth_metrics
alphalake.gold.rolling_metrics
alphalake.gold.cash_flow_quality
```

The AI layer can query:

```text
alphalake.gold.v_company_financials_report
```

## Current AI Flow

AlphaLake uses a local Ollama model through an OpenAI-compatible client.

```text
User question
     │
     ▼
qwen3:4b-instruct
     │
     ├── normal response
     └── tool call
           │
           ▼
      backend AI tool
           │
           ▼
       Databricks
           │
           ▼
   financial result
           │
           ▼
     assistant answer
```

The model is expected to treat tool-returned financial data as authoritative.

## Conversation System

Conversation history is persisted in PostgreSQL.

```text
message arrives
     │
     ▼
ensure conversation exists
     │
     ▼
load prior history
     │
     ▼
process with AI
     │
     ▼
store user + assistant messages
```

The frontend sidebar can:

- list conversations
- select a conversation
- load its messages
- create a new chat
- rename a conversation
- delete a conversation

The active session ID is owned by the page/dashboard component and shared with the sidebar and chat component through React props and state.

## Operational vs Analytical Storage

### PostgreSQL

PostgreSQL stores application state:

```text
conversations
messages
conversation titles
watchlists (next)
users (future)
```

### Databricks

Databricks stores analytical financial data:

```text
SEC facts
historical financial data
normalized metrics
derived metrics
aggregations
reporting views
```

## SEC Company Data

AlphaLake already contains code using:

```text
https://www.sec.gov/files/company_tickers.json
```

The current helper can resolve:

```text
ticker → CIK
```

This dataset will also support the upcoming company-search/watchlist feature.

The frontend should not contain a hardcoded master list of companies. The backend/data layer should expose searchable company metadata derived from SEC reference data.

## Next Feature: Watchlist

Initial idea:

```text
User opens Watchlist
     │
     ▼
searches or chooses company
     │
     ▼
frontend sends ticker / CIK
     │
     ▼
FastAPI
     │
     ▼
PostgreSQL
```

PostgreSQL will store which companies are watched. Databricks remains responsible for financial analytics for those companies.

Later this can support:

- company detail pages
- filing alerts
- financial summaries
- personalized dashboards
- earnings/filing workflows

## Tech Stack

### Data Engineering
- Python
- PySpark
- Delta Lake
- Databricks
- SEC EDGAR / Company Facts data

### Backend
- FastAPI
- Pydantic
- SQLAlchemy
- REST
- WebSockets

### Operational Database
- PostgreSQL

### AI
- Ollama
- `qwen3:4b-instruct`
- OpenAI-compatible Python client
- tool calling

### Frontend
- Next.js
- React
- TypeScript
- Material UI
- Tailwind CSS
- React Markdown

### Infrastructure
- Docker
- Docker Compose
- Terraform
- GitHub Actions

## Docker

Local integration stack:

```text
frontend
backend
ollama
ollama-pull
```

Databricks stays external.

Typical local ports:

```text
Next.js      3000
FastAPI      8000
PostgreSQL   5432
Ollama       11434
```

Inside Docker Compose, services communicate using service names rather than localhost, for example:

```text
http://ollama:11434
```

## Terraform

Terraform configuration lives under:

```text
infrastructure/terraform/
```

It is used for Databricks infrastructure and job configuration.

## Project Structure

```text
src/
├── ai/
├── api/
├── db/
├── ingestion/
├── storage/
├── transformations/
├── pipelines/
├── runtime/
└── quality/

frontend/
└── alphalake/

infrastructure/
└── terraform/
```

## Development Principles

- implement real product flows rather than résumé-only features
- keep backend and data engineering tightly connected
- separate OLTP and OLAP concerns
- prefer reusable pipeline functions
- use AI tools for grounded financial answers
- persist important application state
- keep local development possible
- add infrastructure only when there is a real engineering need
- learn through implementation, debugging, and iteration

## Roadmap

### Near term

- [x] SEC financial ingestion
- [x] Bronze / Silver / Gold pipeline
- [x] Databricks analytical layer
- [x] Terraform-managed Databricks jobs
- [x] AI financial tool calling
- [x] FastAPI backend
- [x] WebSocket chat
- [x] Next.js chat UI
- [x] Docker Compose integration
- [x] PostgreSQL conversation persistence
- [x] conversation sidebar
- [x] rename / delete conversations
- [ ] company reference/search layer
- [ ] watchlist
- [ ] company detail page

### Later

- [ ] authentication and users
- [ ] SEC filing ingestion
- [ ] RAG over 10-K / 10-Q filings
- [ ] citations in AI answers
- [ ] background jobs
- [ ] filing / earnings alerts

### Only when justified

- Redis
- Kafka
- Kubernetes
- additional analytical warehouses such as Snowflake

## Project Direction

AlphaLake is evolving toward a small but realistic financial research product where:

```text
data engineering
+ backend engineering
+ operational data
+ analytical data
+ AI
+ frontend product design
```

work together as one system.

The project is intentionally being developed incrementally so that each architectural decision is connected to an actual requirement.
