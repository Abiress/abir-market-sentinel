# 🛡️ Abir Market Sentinel &nbsp;`v1.0.1`

**Abir Market Sentinel** is an AI-first insider trading detection engine that combines behavioral anomaly detection, intent analysis, and cross-source correlation, then secures flagged evidence with quantum-ready controls.

> **v1.0.1** — Phase 1-3 hardened · 29 tests passing · 0.102s full pipeline · 7/7 pentest PASS

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.1-0A7EA4?style=flat-square" />
  <img src="https://img.shields.io/badge/Tests-29%20passed-brightgreen?style=flat-square" />
  <img src="https://github.com/Abiress/abir-market-sentinel/actions/workflows/ci.yml/badge.svg" />
  <img src="https://github.com/Abiress/abir-market-sentinel/actions/workflows/publish.yml/badge.svg" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Security-PQC%20Ready-1B5E20?style=flat-square" />
  <img src="https://img.shields.io/badge/FIPS-203%2F204%20Aligned-0D47A1?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square&logo=opensourceinitiative" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/Abiress/abir-market-sentinel?style=flat-square&logo=github" />
  <img src="https://img.shields.io/github/forks/Abiress/abir-market-sentinel?style=flat-square&logo=github" />
  <img src="https://img.shields.io/github/issues/Abiress/abir-market-sentinel?style=flat-square" />
  <img src="https://img.shields.io/github/last-commit/Abiress/abir-market-sentinel?style=flat-square" />
</p>

## Table of Contents

- [What's New in v1.0.1](#whats-new-in-v101)
- [At a Glance](#at-a-glance)
- [Verified Status](#verified-status)
- [Benchmark and Security Validation (May 2026)](#benchmark-and-security-validation-may-2026)
- [Latest Improvements (May 2026)](#latest-improvements-may-2026)
- [System Flow](#system-flow)
- [Installation and Setup](#installation-and-setup)
- [Run and Test](#run-and-test)
- [Project Structure](#project-structure)
- [Roadmap Snapshot](#roadmap-snapshot)
- [Governance and Security Docs](#governance-and-security-docs)
- [Detailed Product Narrative (Original)](#-why-this-matters)

## What's New in v1.0.1

| # | Change | Category |
|---|--------|---------|
| 1 | Symbol-aware trade-to-news correlation — MSFT news no longer matches AAPL trades | Bug Fix |
| 2 | Unique trade IDs using timestamp + sequence counter (no more ID collisions) | Bug Fix |
| 3 | Optional FinBERT intent engine with safe heuristic fallback | Enhancement |
| 4 | Untrained-model guardrail in API `/detect` endpoint (returns HTTP 400, not crash) | Enhancement |
| 5 | Optimized correlation loop: precomputed timestamps reduce latency from 0.121s → 0.091s | Performance |
| 6 | Tamper-evident audit chain indexing corrected — deterministic verify across all chain sizes | Bug Fix |
| 7 | `hmac` import added to `differential_privacy.py` — `constant_time_compare` now functional | Bug Fix |
| 8 | Full timezone-aware UTC migration — zero Python 3.14 deprecation warnings | Maintenance |
| 9 | Isolation Forest fallback (`_FallbackIsolationModel`) when `scikit-learn` absent | Resilience |
| 10 | In-memory vault fallback (`_FallbackVault`) when `abir-guard` absent for dev/CI use | Resilience |

> Full benchmark (0.102s total, 241 trades) and penetration validation (7/7 PASS) documented below.

## At a Glance

| Area | Current Status |
|------|----------------|
| Version | **v1.0.1** — Phase 1-3 hardened, benchmarked, pentest-validated |
| Detection Core | Behavioral anomaly detection (Isolation Forest) + intent analysis + symbol-aware correlation |
| Security | Tamper-evident audit chain, canary trades, key rotation, differential privacy, FIPS mode |
| Quantum Posture | Abir-Guard integration path with ML-KEM-1024 and hybrid KEM; fallback vault for dev/CI |
| API | Flask real-time endpoints — `/api/detect`, `/api/train`, `/api/health` with guardrails |
| Runtime Resilience | Optional dependency fallbacks (sklearn, abir-guard) — zero hard crashes in CI |
| Performance | 241-trade pipeline in **0.102s**; correlation optimized to **0.091s** |
| Test Health | **29 passed**, zero warnings, Python 3.14.4 |
| Phases | Phase 1-3 + stabilization complete, Phase 4-5 planned |

## Verified Status

This repository was validated locally on **May 12, 2026 (v1.0.1)**:

- Test command: `/usr/bin/python3 -m pytest -q`
- Result: **`29 passed`**, zero warnings
- Python: 3.14.4 (system)
- Notes: All timezone-aware UTC, optional-dependency fallbacks active, Phase 1-3 fully functional.

## Benchmark and Security Validation (May 2026)

### Full Pipeline Benchmark

Measured on the local development environment using the end-to-end Phase 1-3 path:

- Input size: `241 trades`, `48 test trades`, `2 news items`, `10 agent logs`
- Ingestion: `0.002220s`
- Model train: `0.005207s`
- Anomaly detect: `0.001858s`
- Correlation: `0.090947s`
- Intent + flag scoring: `0.001784s`
- Total pipeline time: `0.102017s`

### Penetration-Style Security Validation

Validated controls and abuse-path checks:

- Audit log tamper detection: `PASS` (modified entries invalidate chain)
- Canary breach trigger path: `PASS`
- Key rotation misuse guard: `PASS` (missing key usage raises)
- Cross-symbol correlation isolation: `PASS`
- FIPS strict non-approved algorithm guard: `PASS`
- Side-channel noise injector behavior: `PASS`
- Vault encryption/decryption roundtrip: `PASS`

## Latest Improvements (v1.0.1 — May 2026)

- Added robust fallback model path in anomaly detection when `scikit-learn` is unavailable.
- Added in-memory vault fallback when `abir-guard` is unavailable for local/dev reliability.
- Fixed audit chain verification edge case to ensure deterministic tamper checks.
- Improved API detection endpoint with untrained-model guardrails and safe auto-training behavior.
- Added symbol-aware trade-to-news correlation for tighter intent context.
- Added optional FinBERT sentiment path with safe heuristic fallback.
- Migrated codebase and tests to timezone-aware UTC to remove Python deprecation warnings.
- Added real workflow badges for CI and publish pipelines.

## System Flow

```text
Market Trades + News + Agent Logs
             |
             v
Behavioral AI Detection (anomaly + intent)
             |
             v
Correlation Engine (trade/news/agent link)
             |
             v
Risk Scoring + Flagging
             |
             v
Quantum/Security Layer (vault + audit + canary + key rotation)
             |
             v
Compliance and Alert Outputs
```

## Installation and Setup

### Prerequisites

- Python 3.10+
- `pip`
- Optional: `abir-guard` for production-grade PQC backend

### Local Setup

```bash
git clone https://github.com/Abiress/abir-market-sentinel.git
cd abir-market-sentinel

pip install -r requirements.txt
pip install -e "."
```

## Run and Test

### Run Main Pipeline

```bash
/usr/bin/python3 src/main.py
```

### Run API

```bash
/usr/bin/python3 src/api/realtime_api.py
```

### Run Tests

```bash
/usr/bin/python3 -m pytest -q
```

## Project Structure

```text
abir-market-sentinel/
├── src/
│   ├── alerting/           # Risk scoring and trade flagging
│   ├── api/                # Flask real-time API
│   ├── behavioral_ai/      # Anomaly detector + intent analyzer
│   ├── correlation/        # Trade-news-agent correlation
│   ├── data_ingestion/     # Market/news/agent mock ingestion
│   ├── quantum_security/   # Abir-Guard-backed (or fallback) vault
│   ├── security/           # Audit, canary, FIPS mode, key rotation, privacy
│   └── main.py             # End-to-end pipeline entry
├── tests/                  # Unit + integration tests
├── config/                 # Runtime configuration
├── examples/               # Example runner
├── PHASES.md               # Phase-by-phase plan and progress
├── THREAT_MODEL.md         # Zero-trust threat model
└── README.md               # This document
```

## Roadmap Snapshot

| Phase | Status | Version |
|-------|--------|---------|
| Phase 1 — Foundation | ✅ Complete | v1.0.1 |
| Phase 2 — Intelligence | ✅ Complete | v1.0.1 |
| Phase 3 — Security Hardening | ✅ Complete | v1.0.1 |
| Phase 3.1 — Stabilization | ✅ Complete | v1.0.1 |
| Phase 4 — Scale and Performance | 🟡 Planned | v1.1.0 |
| Phase 5 — Enterprise and Compliance | 🟡 Planned | v2.0.0 |

See `PHASES.md` for full milestone detail.

## Governance and Security Docs

- `THREAT_MODEL.md`: architecture-level threats and mitigations
- `SECURITY.md`: reporting and response process
- `CONTRIBUTING.md`: development and PR conventions
- `CODE_OF_CONDUCT.md`: community expectations
- `CITATION.cff`: citation metadata
- `LICENSE`: MIT terms

---

## Detailed Product Narrative (Original)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-green?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square&logo=opensourceinitiative" />
  <img src="https://img.shields.io/github/last-commit/Abiress/abir-market-sentinel?style=flat-square" />
  <img src="https://img.shields.io/github/stars/Abiress/abir-market-sentinel?style=flat-square&logo=github" />
</p>

**The World's First AI-Powered Insider Trading Detection Engine with Quantum-Ready Security.**

Built on top of [Abir-Guard](https://github.com/Abiress/abir-guard) (NIST FIPS 203/204), this engine goes beyond rule-based detection by analyzing **intent, not just activity**.

---

## 🎯 Why This Matters

### The Problem
Current insider trading detection is **rule-based, not AI-behavioral**. Banks use static thresholds (“trade > $1M = flag”), which misses:
- Sophisticated traders using **slow-drip accumulation**
- **Rumor-based positioning** before news breaks
- **Cross-market manipulation** across related symbols
- **AI agents** with prior knowledge injecting trades

### The Solution
Abir Market Sentinel detects **intent-based market manipulation**:
- ✅ **Behavioral AI**: Isolation Forest detects abnormal patterns
- ✅ **Intent Analysis**: NLP flags suspicious motivation (not just activity)
- ✅ **Multi-Source Correlation**: Links trades ↔ news ↔ agent actions
- ✅ **Quantum-Safe**: ML-KEM-1024 + AES-256-GCM via Abir-Guard

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   DATA INGESTION                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ Market Data  │  │ News Feeds  │  │ Agent Logs  │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────┐
│          BEHAVIORAL AI DETECTION ENGINE                    │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │ Anomaly           │  │ Intent           │            │
│  │ Detector         │  │ Analyzer         │            │
│  │ (Isolation       │  │ (FinBERT +      │            │
│  │  Forest)        │  │  Keyword Scan)  │            │
│  └────────┬─────────┘  └────────┬─────────┘            │
│           │                    │                               │
│  ┌────────▼────────▼─────────┐                  │
│  │      Correlation Engine                       │                  │
│  │  • Trade-News Linking                    │                  │
│  │  • Agent Action Correlation               │                  │
│  └────────┬──────────────────────────────┘                  │
└─────────┼──────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              RISK SCORING & FLAGGING                         │
│  Formula: risk = |anomaly|×0.4 + intent×0.4 + news×0.2  │
│  Threshold: >0.6 → Flag for investigation                  │
└─────────┼──────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│         QUANTUM-SAFE STORAGE (Abir-Guard)                    │
│  ┌──────────────────────────────────────────────┐            │
│  │ ML-KEM-1024 + X25519 Hybrid KEM           │            │
│  │ AES-256-GCM Envelope Encryption            │            │
│  │ Tamper-Evident Audit Log (SHA-256)       │            │
│  └──────────────────────────────────────────────┘            │
└─────────┼──────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              ALERTING & COMPLIANCE                          │
│  • Real-time notifications                            │
│  • SEC Rule 10b-5 compliance reports                  │
│  • MiFID II transaction reporting (Phase 5)             │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Why Abir-Guard?

| Feature | Traditional Solutions | **Abir Market Sentinel** |
|---------|----------------------|--------------------------|
| Detection Type | Rule-based (static thresholds) | **AI-Behavioral (Isolation Forest)** |
| Intent Analysis | ❌ None | ✅ **NLP + Keyword Scanning** |
| News Correlation | ❌ None | ✅ **Time-window Linking** |
| Agent Tracking | ❌ None | ✅ **Cross-Agent Correlation** |
| Encryption | AES-256 only | ✅ **ML-KEM-1024 + AES-256-GCM** |
| Quantum-Safe | ❌ Vulnerable to HNDL | ✅ **NIST FIPS 203/204 Compliant** |
| Audit Trail | Basic logs | ✅ **Tamper-Evident SHA-256 Chain** |
| Breach Detection | ❌ None | ✅ **Canary Trades (Honeypots)** |

---

## 🚀 Use Cases

### 1. Detecting Insider Trading Before Earnings
**Scenario**: A trader consistently trades just hours before major earnings announcements with suspicious precision.

**How Sentinel Helps**:
- Behavioral AI flags unusual trade timing patterns
- Intent analyzer detects references to "confidential info" or "insider knowledge"
- Correlation engine links trades to upcoming earnings news
- Risk score exceeds 0.6 → Trade flagged for investigation

```python
# Example flagged output
{
  "trade_id": "T0045",
  "risk_score": 0.78,
  "reason": "Behavioral anomaly; Suspicious intent identified; 3 related news events",
  "flagged_at": "2026-05-04T10:30:00"
}
```

### 2. Market Manipulation via Rumor Spread
**Scenario**: An agent spreads rumors about a company while simultaneously taking large positions.

**How Sentinel Helps**:
- Agent action correlation detects info requests before trades
- News sentiment analysis identifies rumor-based headlines
- Intent analysis flags "not public" keyword mentions
- Combined intent score triggers alert

### 3. Honeypot Protection (Canary Trades)
**Scenario**: An attacker gains access to the trade database and starts querying flagged trades.

**How Sentinel Helps**:
- Canary trades (honeypots) planted in the database
- Any access to canary trades triggers breach alert
- Tamper-evident audit logs record the breach attempt
- Quantum encryption (ML-KEM-1024) protects data even if exfiltrated

### 4. Regulatory Compliance (SEC Rule 10b-5)
**Scenario**: Financial institution needs to prove they monitor for insider trading.

**How Sentinel Helps**:
- Tamper-evident audit logs with SHA-256 hash chains
- Export reports in regulatory formats (Phase 5)
- Quantum-safe storage meets "Harvest Now, Decrypt Later" threats
- FIPS 140-3 compliance mode (NIST standards)

### 5. Cross-Market Manipulation Detection
**Scenario**: Same actor manipulates multiple related stocks across different markets.

**How Sentinel Helps**:
- Trade-news correlation across multiple symbols
- Agent action tracking across markets
- Behavioral patterns detected even with small trade sizes
- Distributed detection (Phase 4) for multi-market coverage

---

## 📥 Quick Start

### Prerequisites
- Python 3.10+
- [abir-guard](https://github.com/Abiress/abir-guard) >= 3.1.0

### Installation

```bash
# Clone the repository
git clone https://github.com/Abiress/abir-market-sentinel.git
cd abir-market-sentinel/

# Install abir-guard from source
bash install_abir_guard.sh

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e ".[dev]"
```

### Run Detection

```bash
python src/main.py
```

Expected output:
```
======================================================================
Abir Market Sentinel - AI Insider Trading Detection Engine
Phase 1: Foundation | Phase 2: Intelligence | Phase 3: Security
======================================================================

[Phase 1] Ingesting market data...
    Loaded 200 trades, 2 news items

[Phase 2] Detecting anomalies with intent analysis...
    Found 5 anomalous trades

[Phase 3] Flagging suspicious activity...
    FLAGGED: Trade T045 | Risk: 0.72
             Reason: Suspicious intent identified; Multiple correlated news events
======================================================================
SUMMARY: 3 trades flagged out of 200
Quantum-secured storage active via Abir-Guard
Audit log entries: 8
Audit chain valid: True
Canary status: {'breach_detected': False, ...}
======================================================================
```

---

## 🌐 API Usage

### Real-time Detection

```bash
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{
    "trades": [{"trade_id": "T001", "symbol": "AAPL", "volume": 10000}],
    "news": [{"headline": "Apple earnings surprise"}]
  }'
```

Response:
```json
{
  "total_trades": 1,
  "anomalies_detected": 1,
  "flagged_trades": [
    {"trade_id": "T001", "risk_score": 0.75, "reason": "..."}
  ]
}
```

---

## 🔒 Quantum Security Features

### Post-Quantum Cryptography
- **ML-KEM-1024** (NIST FIPS 203) for key encapsulation
- **ML-DSA-65** (NIST FIPS 204) for digital signatures
- **AES-256-GCM** for data encryption (128-bit quantum resistance)
- **Hybrid KEM**: ML-KEM + X25519 (both must break)

### Security Controls
- Tamper-evident audit logs with SHA-256 hash chains
- Canary trades to detect data breaches
- Automated quantum key rotation
- FIPS 140-3 compliance mode
- Differential privacy with Laplace noise injection

---

## 🇮🇳🌍 Mission Support

This project aligns with:

| Mission | Badge | Description |
|---------|--------|-------------|
| 🇮🇳 **Indian Quantum Mission** | IQM | Quantum-resilient cryptography for India's NQM |
| 🌍 **Global Quantum Mission** | GQM | NIST FIPS 203/204 compliant worldwide |
| 🇮🇳🌍 **Indian AI Mission** | IAI | Quantum-secure memory vaults for sovereign AI |

---

## 👨‍💻 Developer

**Abir Maheshwari**
- Founder at Artificial Quantum Dyson Intelligence, Biro Labs, Aquilldriver
- AI Engineer | Quantum Computing Researcher

**Connect**
- Email: abhirsxn@gmail.com
- LinkedIn: [abirmaheshwari](https://in.linkedin.com/in/abirmaheshwari)
- Instagram: [@anantraga31](https://instagram.com/anantraga31)
- Medium: [@abirmaheshwari](https://office.qz.com/@abirmaheshwari)

---

🇮🇳 **Made in India, for the World.**

**Secured by NIST PQC, AES-256-GCM, Argon2id, ML-DSA-65, ML-KEM-1024**
· v1.0.1 · Licensed under MIT 2026
