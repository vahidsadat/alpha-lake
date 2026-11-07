# AlphaLake Architecture

## 1. Overview

AlphaLake is an AI-assisted financial research platform combining SEC financial data, Databricks analytics, FastAPI, PostgreSQL, a local Ollama LLM, Next.js, Docker Compose, and Terraform.

The project is being developed incrementally: technologies are added when they solve a concrete product or engineering need.

## 2. Current High-Level Architecture

```text
User
 │
 ▼
Next.js Frontend
 │
 ├── Chat UI
 ├── Conversation sidebar
 ├── New chat
 ├── Rename / delete chat
 └── Watchlist UI (next)
 │
 ├── REST
 └── WebSocket
 │
 ▼
FastAPI Backend
 ├── Chat orchestration
 ├── Conversation APIs
 ├── Company APIs
 ├── AI tool integration
 └── Watchlist APIs (next)
 │
 ├──────────────► PostgreSQL
 │                conversations
 │                messages
 │                watchlists (next)
 │                users (future)
 │
 ├──────────────► Ollama
 │                qwen3:4b-instruct
 │                local inference
 │                tool calling
 │
 └──────────────► Databricks
                  Bronze / Silver / Gold
                  Delta Lake
                  financial metrics
                  reporting views
                  │
                  ▼
                  SEC
                  Company Facts
                  ticker / CIK reference
                  filings (future)
```

## 3. Repository Responsibilities

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
    ├── app/
    ├── component/
    └── utils/

infrastructure/
└── terraform/
```

Exact file names may evolve, but the architectural boundaries should remain stable.

## 4. Data Engineering Architecture

```text
SEC source
   │
   ▼
Bronze
   │ raw / minimally processed SEC data
   ▼
Silver
   │ normalized and validated financial facts
   ▼
Gold Core
   │ annual company financials
   ▼
Gold Derived
   ├── growth metrics
   ├── rolling metrics
   └── cash-flow-quality metrics
```

Current Gold outputs:

- `alphalake.gold.company_financials`
- `alphalake.gold.growth_metrics`
- `alphalake.gold.rolling_metrics`
- `alphalake.gold.cash_flow_quality`

AI/reporting queries use:

- `alphalake.gold.v_company_financials_report`

`company_financials` uses change-aware merge logic in Databricks. Derived Gold datasets currently use full overwrite, so the full relevant Silver dataset must be available when rebuilding them.

## 5. Operational vs Analytical Data

### PostgreSQL

PostgreSQL stores operational application state:

- conversations
- messages
- conversation titles
- watchlists (next)
- users (future)
- preferences (future)

### Databricks

Databricks stores analytical financial data:

- SEC facts
- normalized financial data
- historical metrics
- derived ratios
- aggregations
- reporting views

```text
PostgreSQL
→ what the application/user currently owns or remembers

Databricks
→ what financial data AlphaLake can analyze
```

## 6. Conversation Architecture

Conversation history is now persisted in PostgreSQL.

```text
User sends message
      │
      ▼
FastAPI
      ├── ensure conversation exists
      ├── load history from PostgreSQL
      ├── process with AI
      ├── save current user message
      └── save assistant response
      ▼
PostgreSQL
```

PostgreSQL is the source of truth for conversation history.

Current sidebar behavior:

- list conversations
- select an existing conversation
- load its message history
- create a new UUID for a new chat
- show an overflow menu on hover
- close the menu on click-away
- rename conversations
- delete conversations

The active session ID is owned by the dashboard/page component:

```text
Dashboard
├── SideBar
│   └── selects / creates session
└── AIConversation
    └── reacts to active sessionId
```

## 7. AI Architecture

AlphaLake uses Ollama through an OpenAI-compatible client.

Current model:

```text
qwen3:4b-instruct
```

Financial tool flow:

```text
User question
   │
   ▼
LLM
   │
   ├── normal response
   └── tool call
         │
         ▼
get_financial_report(...)
         │
         ▼
Databricks Gold reporting view
         │
         ▼
structured financial data
         │
         ▼
LLM answer
```

Tool-returned financial data should be treated as authoritative, and the model should avoid unsupported causal explanations or invented claims.

## 8. API Communication

REST is used for resource operations such as:

- list conversations
- get conversation messages
- rename conversation
- delete conversation
- company-related endpoints
- future watchlist operations

WebSocket is used for interactive AI chat.

```text
Frontend
├── REST → resource management
└── WebSocket → live chat
```

## 9. Docker Architecture

Current local integration stack:

```text
Docker Compose
├── frontend
├── backend
├── ollama
└── ollama-pull
```

Databricks remains external.

Terraform is infrastructure tooling and is not a runtime Compose service.

Backend-to-Ollama inside Compose uses:

```text
http://ollama:11434
```

Local development outside Compose can use:

```text
http://localhost:11434
```

## 10. Infrastructure as Code

Terraform remains under:

```text
infrastructure/terraform/
```

It is used for Databricks infrastructure and job configuration.

## 11. SEC Company Reference Data

AlphaLake already retrieves:

```text
https://www.sec.gov/files/company_tickers.json
```

and can resolve:

```text
ticker → CIK
```

This can evolve into a searchable company reference layer for the watchlist feature.

Suggested normalized company reference:

```text
company
├── cik
├── ticker
├── company_name
└── exchange   # optional if using the exchange dataset
```

The frontend should not hardcode the complete company universe.

Preferred flow:

```text
SEC ticker dataset
      │
      ▼
backend / ingestion layer
      │
      ▼
searchable company reference
      │
      ▼
frontend company search
      │
      ▼
user selects company
```

## 12. Next Feature: Watchlist

Initial product flow:

```text
User opens Watchlist
      │
      ▼
search / choose company
      │
      ▼
frontend sends ticker / CIK
      │
      ▼
FastAPI
      │
      ▼
PostgreSQL watchlist state
```

PostgreSQL stores which companies are watched. Databricks remains responsible for the financial analytics for those companies.

A minimal future watchlist model could contain:

```text
watchlists
├── user_id       # once authentication exists
├── ticker or cik
└── created_at
```

Before authentication exists, AlphaLake can use a simpler single-user implementation and evolve it later.

## 13. Planned Evolution

```text
Watchlist
→ company search
→ company detail page
→ authentication / users
→ SEC filing ingestion
→ RAG with citations
→ background jobs
```

Technologies should be introduced only when justified:

- Redis: when caching or distributed transient state becomes useful
- Kafka: when genuine event-driven fan-out appears
- Kubernetes: when deployment/orchestration complexity requires it
- Snowflake: only for a concrete business/customer requirement

## 14. Architectural Principles

1. Keep transformation logic reusable.
2. Separate operational and analytical data.
3. Keep frontend state ownership clear.
4. Persist important application state in PostgreSQL.
5. Use Databricks for financial analytics.
6. Let AI call tools for authoritative data.
7. Prefer meaningful product features over technology collection.
8. Add infrastructure only when there is a real need.
9. Keep local development possible.
10. Evolve the architecture incrementally instead of designing prematurely for massive scale.
