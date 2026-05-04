# Abir Market Sentinel

**AI Insider Trading Detection Engine with Quantum-Ready Security**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green?style=flat-square&logo=python)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square&logo=opensourceinitiative)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)](https://github.com/Abiress/abir-market-sentinel)

---

## Overview

Abir Market Sentinel is an AI-powered insider trading detection engine that goes beyond rule-based systems by detecting **intent-based market manipulation**. It extends [Abir-Guard](https://github.com/Abiress/abir-guard) for quantum-ready security.

### Key Innovations
- **Behavioral AI**: Detects abnormal trade patterns using Isolation Forest
- **Intent Analysis**: Flags suspicious intent (not just activity) using NLP
- **Multi-Source Correlation**: Links trades with news events and agent actions
- **Quantum-Safe Storage**: ML-KEM-1024 + AES-256-GCM via Abir-Guard

---

## System Flowchart

```
┌─────────────────────────────────────────────────────────────────┐
│                   DATA INGESTION                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ Market Data  │  │ News Feeds  │  │ Agent Logs  │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│          BEHAVIORAL AI DETECTION ENGINE                    │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │ Anomaly           │  │ Intent           │            │
│  │ Detector         │  │ Analyzer         │            │
│  │ (Isolation       │  │ (FinBERT +      │            │
│  │  Forest)        │  │  Keyword Scan)  │            │
│  └────────┬─────────┘  └────────┬─────────┘            │
│           │                    │                               │
│  ┌────────▼────────────────▼─────────┐                  │
│  │      Correlation Engine                       │                  │
│  │  • Trade-News Linking                    │                  │
│  │  • Agent Action Correlation               │                  │
│  └────────┬──────────────────────────────┘                  │
└─────────┼──────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│              RISK SCORING & FLAGGING                         │
│  Formula: risk = |anomaly|×0.4 + intent×0.4 + news×0.2  │
│  Threshold: >0.6 → Flag for investigation                  │
└─────────┼──────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│         QUANTUM-SAFE STORAGE (Abir-Guard)                    │
│  ┌──────────────────────────────────────────────┐            │
│  │ ML-KEM-1024 + X25519 Hybrid KEM           │            │
│  │ AES-256-GCM Envelope Encryption            │            │
│  │ Tamper-Evident Audit Log (SHA-256)       │            │
│  └──────────────────────────────────────────────┘            │
└─────────┼──────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│              ALERTING & COMPLIANCE                          │
│  • Real-time notifications                            │
│  • SEC Rule 10b-5 compliance reports                  │
│  • MiFID II transaction reporting (Phase 5)             │
└─────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
abir-market-sentinel/
├── README.md                    # This file
├── LICENSE                     # MIT License (2026)
├── CITATION.cff               # Academic citation
├── THREAT_MODEL.md            # Zero-trust threat model
├── SECURITY.md                # Vulnerability reporting
├── CONTRIBUTING.md            # Contribution guidelines
├── CODE_OF_CONDUCT.md         # Community standards
├── PUBLISHING.md              # PyPI publishing guide
├── config/
│   └── config.yaml          # Configuration file
├── src/
│   ├── quantum_security/     # Phase 1: PQC via Abir-Guard
│   │   └── vault.py         # ML-KEM-1024 + AES-256-GCM
│   ├── behavioral_ai/        # Phase 2: AI Detection
│   │   ├── anomaly_detector.py  # Isolation Forest
│   │   └── intent_analyzer.py # Intent analysis
│   ├── correlation/          # Phase 2: Linking
│   │   └── linker.py       # Trade-news-agent correlation
│   ├── alerting/            # Phase 2: Flagging
│   │   └── flagging.py     # Risk scoring
│   ├── data_ingestion/      # Phase 1: Data feeds
│   │   └── market_data.py
│   ├── security/            # Phase 3: Hardening
│   │   ├── audit.py        # Tamper-evident logs
│   │   ├── canary.py       # Honeypot trades
│   │   ├── key_rotation.py # Quantum key manager
│   │   ├── fips_mode.py   # FIPS 140-3 compliance
│   │   └── differential_privacy.py # Laplace noise
│   └── api/                # Phase 2: Real-time API
│       └── realtime_api.py  # Flask endpoints
├── tests/                    # Test suites
│   ├── test_anomaly_detector.py
│   ├── test_intent_analyzer.py
│   ├── test_quantum_vault.py
│   ├── test_phase3_security.py
│   └── test_integration.py
├── examples/                 # Usage examples
│   └── run_detection.py
└── .github/                 # CI/CD + Templates
    ├── workflows/
    │   ├── ci.yml          # Test pipeline
    │   └── publish.yml    # PyPI publish
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

## Phase Implementation Status

### Phase 1: Foundation ✅ Complete
- Quantum security layer via Abir-Guard integration
- Behavioral anomaly detection (Isolation Forest)
- Basic trade data ingestion
- Basic flagging system
- GitHub repository setup

### Phase 2: Intelligence ✅ Complete
- FinBERT intent analyzer
- Trade-news correlation engine
- Agent action correlation
- Advanced risk scoring algorithm
- Real-time detection API (Flask)

### Phase 3: Security Hardening ✅ Complete
- Tamper-evident audit logs (SHA-256 hash chain)
- Canary trade detection (honeypots)
- Quantum key rotation manager
- FIPS 140-3 compliance mode
- Differential privacy (Laplace noise)

### Phase 4: Scale & Performance 📋 Planned
- Distributed detection across nodes
- Real-time streaming (Kafka/Event Hub)
- GPU acceleration for model inference

### Phase 5: Enterprise & Compliance 📋 Planned
- SEC Rule 10b-5 compliance reporting
- MiFID II transaction reporting
- Web dashboard with visualization

---

## Quick Start

### Prerequisites
- Python 3.10+
- [abir-guard](https://github.com/Abiress/abir-guard) >= 3.1.0

### Installation

```bash
# Clone the repository
git clone https://github.com/Abiress/abir-market-sentinel.git
cd abir-market-sentinel

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
```

---

## API Usage

### Real-time Detection

```bash
curl -X POST <http://localhost:5000/api/detect> \\
  -H "Content-Type: application/json" \\
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

## Quantum Security Features

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

## Mission Support 🇮🇳🌍

This project aligns with:

| Mission | Badge | Description |
|---------|--------|-------------|
| 🇮🇳 **Indian Quantum Mission** | IQM | Quantum-resilient cryptography for India's NQM |
| 🌍 **Global Quantum Mission** | GQM | NIST FIPS 203/204 compliant worldwide |
| 🇮🇳🌍 **Indian AI Mission** | IAI | Quantum-secure memory vaults for sovereign AI |

---

## Developer

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

Built with Rust, Python, Go, JavaScript · Secured by NIST PQC, AES-256-GCM, Argon2id, ML-DSA-65, ML-KEM-1024 · Licensed under MIT 2026
