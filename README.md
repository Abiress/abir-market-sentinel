# Abir Market Sentinel

AI Insider Trading Detection Engine with Quantum-Ready Security, extending [Abir-Guard](https://github.com/Abiress/abir-guard).

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green?style=flat-square&logo=python)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square&logo=opensourceinitiative)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)](https://github.com/Abiress/abir-market-sentinel)

## Features

- **Behavioral AI Anomaly Detection**: Uses Isolation Forest to detect abnormal trade patterns
- **Intent-Based Flagging**: Goes beyond rule-based detection to identify suspicious intent
- **Trade-News Correlation**: Links trades with news events and agent actions
- **Quantum-Safe Storage**: Uses Abir-Guard's post-quantum cryptography (ML-KEM-1024, ML-DSA-65)
- **Multi-Layer Detection**: Combines behavioral, intent, and correlation analysis

## Quick Start

```bash
# Install abir-guard from GitHub
bash install_abir_guard.sh

# Install dependencies
pip install -r requirements.txt

# Run detection
python src/main.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Data Sources                           │
│  Market Data API │ News Feeds │ Agent Logs              │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│          Behavioral AI Detection Engine                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Anomaly      │  │ Intent       │  │ Correlation │ │
│  │ Detector     │  │ Analyzer     │  │ Engine      │ │
│  └──────────────┘  └──────────────┘  └────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│         Quantum-Safe Storage (Abir-Guard)                │
│  - ML-KEM-1024 encryption                              │
│  - AES-256-GCM envelope                                │
│  - Audit logs with hash chain                          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Alerting & Flagging                        │
│  - Risk scoring                                        │
│  - Threat notification                                 │
│  - Flagged trade storage                               │
└─────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.10+
- abir-guard >= 3.1.0

### From Source

```bash
git clone https://github.com/Abiress/abir-market-sentinel.git
cd abir-market-sentinel

# Install abir-guard
bash install_abir_guard.sh

# Install package
pip install -e ".[dev]"
```

## Usage

```python
from src.quantum_security.vault import QuantumVault
from src.behavioral_ai.anomaly_detector import BehavioralAnomalyDetector
from src.alerting.flagging import SuspiciousActivityFlagger

# Initialize components
vault = QuantumVault("market-sentinel")
detector = BehavioralAnomalyDetector()
flagger = SuspiciousActivityFlagger()

# Train and detect
detector.train(historical_trades)
results = detector.detect_anomalies(recent_trades)

# Flag suspicious activity
for _, trade in results.iterrows():
    flag = flagger.flag_trade(trade.to_dict())
    if flag['is_flagged']:
        vault.store_trade_data(trade.to_dict())
```

## Project Structure

```
abir_market_sentinel/
├── src/
│   ├── quantum_security/    # PQC integration with Abir-Guard
│   ├── behavioral_ai/      # Anomaly & intent detection
│   ├── correlation/         # Trade-news-agent linking
│   ├── alerting/           # Risk scoring & flagging
│   └── data_ingestion/     # Market data feeds
├── tests/                  # Unit tests
├── config/                 # Configuration files
└── examples/               # Usage examples
```

## Built With

**Languages**: Python, Rust, Go, JavaScript (via abir-guard)

**Security**: NIST PQC (ML-KEM-1024, ML-DSA-65), AES-256-GCM, Argon2id

**AI/ML**: Scikit-learn, PyTorch, Transformers (FinBERT)

**Licensed under MIT 2026**

## Mission Support 🇮🇳🌍

This project aligns with and supports:

| Mission | Badge | Description |
|---------|--------|-------------|
| 🇮🇳 **Indian Quantum Mission** | IQM | Quantum-resilient cryptography for India's National Quantum Mission |
| 🌍 **Global Quantum Mission** | GQM | NIST FIPS 203/204 compliant worldwide |
| 🇮🇳🌍 **Indian AI Mission** | IAI | Quantum-secure memory vaults for sovereign AI agents |

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
