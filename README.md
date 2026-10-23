# Sovereign AI Agent Engine (Python / FastAPI + Ollama)

[![CI](https://github.com/NoorSiddiquiDubai/sovereign-ai-agent-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/NoorSiddiquiDubai/sovereign-ai-agent-engine/actions/workflows/ci.yml)

> **Author & Architect:** Noor Siddiqui (Founder, IZN AI · Director, Agro National)  
> **Production Standard:** Sovereign Enterprise AI Infrastructure for GCC & Global Enterprises  
> **Operating Doctrine:** *"No Evidence, No Done."*

---

## 🌟 Overview
The **Sovereign AI Agent Engine** is an auditable, self-hosted multi-agent workflow framework designed for enterprises that require **100% data residency and jurisdictional sovereignty** (GCC on-soil / private VPS). 

Unlike brittle OpenAI API wrappers, this engine operates on private open-weights models (Ollama / vLLM / DeepSeek / Llama 3) running behind Linux systemd daemons and Nginx reverse proxies, with mandatory **Human-in-the-Loop (HITL)** approval gates and immutable audit logging.

---

## 🏗️ Architecture

```
[Inbound Intake: WhatsApp / Webhook / REST API]
                      │
                      ▼
[FastAPI Ingestion Gateway (Token Validation & Payload Sanitization)]
                      │
                      ▼
[Sovereign Agent Orchestrator (Ollama / Local LLM)]
  ├─ Lead Qualification & Intent Classification Agent
  ├─ Regulatory Compliance & Disclaimer Agent
  └─ Commercial Proposal / Quotation Drafting Agent
                      │
                      ▼
[Human-in-the-Loop (HITL) Gate: State Locked -> Awaiting Signature]
  ├─ Approved   ──► Outbound Delivery (Webhook / WhatsApp) + Audit Log
  └─ Rejected   ──► Revision Queue + Operator Telemetry
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Local Ollama instance (or remote sovereign Ollama host)

### Local Run
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the engine
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Dockerized Production Deployment
```bash
docker compose up -d --build
```

---

## 🧪 Deterministic Verification
Every build is certified using automated end-to-end tests:
```bash
pytest tests/ -v
```
Rule: *If a test fails, the build is not certified. No evidence, no done.*

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run tests
```bash
pytest --tb=short
```

### Run the engine locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Run with Docker
```bash
docker build -t sovereign-ai-agent-engine .
docker run -p 8000:8000 sovereign-ai-agent-engine
```

---

## License & Provenance
Authored by Noor Siddiqui. Part of the IZN AI Sovereign Engineering Suite.  
Licensed under the MIT License.
