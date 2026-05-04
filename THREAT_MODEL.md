# Threat Model - Abir Market Sentinel

Zero-trust threat model for AI insider trading detection with quantum-ready security.

## System Overview

Abir Market Sentinel detects insider trading using behavioral AI, correlating trades with news/agent actions, and flagging suspicious intent. It extends abir-guard for quantum-safe data protection.

```
┌─────────────────────────────────────────────────────────┐
│                   Data Sources                           │
│  Market Data API │ News Feeds │ Agent Logs              │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Data Ingestion Layer                        │
│  - API authentication                                  │
│  - Rate limiting                                       │
│  - Input validation                                    │
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

## Threat Actors

### 1. Nation-State Adversaries (Quantum-Capable)
**Capabilities**: Quantum computers, Harvest Now Decrypt Later (HNDL) attacks
**Motivation**: Financial espionage, undermining market integrity

**Mitigations**:
- ML-KEM-1024 (NIST FIPS 203) post-quantum encryption
- AES-256-GCM (Grover-resistant at 128-bit effective security)
- Hybrid KEM: ML-KEM + X25519 (both must break)

### 2. Insider Threats
**Capabilities**: Legitimate access to systems, knowledge of detection logic
**Motivation**: Financial gain, sabotage

**Mitigations**:
- Least privilege access
- Audit logs with tamper-evident hash chains
- Canary trade patterns to detect system gaming
- Separation of detection and alerting duties

### 3. Financial Criminals
**Capabilities**: Sophisticated trading strategies, potential malware
**Motivation**: Evade detection, manipulate markets

**Mitigations**:
- Behavioral AI with continuous learning
- Intent-based detection (not just rule-based)
- Correlation engine detecting coincident anomalies
- Dynamic threshold adjustment

### 4. Hackers/APT Groups
**Capabilities**: Exploit vulnerabilities, data exfiltration
**Motivation**: Data theft, ransom, disruption

**Mitigations**:
- Input validation on all API endpoints
- Rate limiting and API authentication
- Encrypted storage of flagged trades
- Network segmentation (recommended deployment)

## Data Flow Threats

### Data at Rest

| Asset | Threat | Likelihood | Impact | Mitigation |
|-------|---------|------------|--------|------------|
| Flagged trades DB | Unauthorized access | Medium | High | Abir-Guard PQC encryption |
| Model weights | Theft/manipulation | Low | Medium | File integrity monitoring |
| Audit logs | Tampering | Medium | High | SHA-256 hash chain |
| API credentials | Theft | Medium | High | HSM/TPM storage (abir-guard) |

### Data in Transit

| Asset | Threat | Likelihood | Impact | Mitigation |
|-------|---------|------------|--------|------------|
| Market data API | Interception | Low | Medium | TLS 1.3 |
| News feed | Manipulation | Medium | Medium | Source verification |
| Alert notifications | Interception | Low | High | E2E encryption |

### Data in Use

| Asset | Threat | Likelihood | Impact | Mitigation |
|-------|---------|------------|--------|------------|
| Trade data in memory | Memory scraping | Low | High | Zero-copy where possible |
| ML model inference | Adversarial inputs | Medium | Medium | Input sanitization |
| Detection rules | Reverse engineering | Low | Medium | Obfuscation (optional) |

## AI-Specific Threats

### Adversarial Attacks

**Evasion Attacks**: Crafting trades to evade detection
- *Mitigation*: Ensemble detection, dynamic thresholds, intent analysis

**Poisoning Attacks**: Corrupting training data
- *Mitigation*: Data validation, outlier detection, periodic retraining

**Model Extraction**: Stealing detection logic
- *Mitigation*: Rate limiting on API, minimal model exposure

### Intent Detection Threats

**False Positive Manipulation**: Triggering excessive flags to hide real threats
- *Mitigation*: Alert correlation, analyst verification queue

**Context Manipulation**: Planting fake news to justify trades
- *Mitigation*: News source reputation scoring, cross-source verification

## Quantum Threats

### Harvest Now, Decrypt Later (HNDL)

**Threat**: Adversary collects encrypted flagged trades today, decrypts when quantum computers available

**Mitigation**:
- ML-KEM-1024 (NIST FIPS 203) for key encapsulation
- AES-256-GCM for data encryption (quantum-resistant at 128-bit)
- Hybrid approach: Classical + Post-quantum (both must fail)

### Quantum Key Extraction

**Threat**: Quantum algorithm extracts encryption keys

**Mitigation**:
- ML-DSA-65 signatures (NIST FIPS 204) for integrity
- Key rotation policies
- Abir-guard's quantum-safe key management

### Future Quantum Break

**Threat**: Cryptographically relevant quantum computer (CRQC) breaks current crypto

**Mitigation**:
- Already using NIST-standardized post-quantum algorithms
- Abir-guard provides seamless algorithm upgrade path
- No additional changes needed for quantum readiness

## Attack Scenarios

### Scenario 1: Insider Exfiltrates Flagged Trades

1. Insider accesses database with flagged trades
2. Attempts to decrypt historical flagged data
3. **Blocked by**: ML-KEM-1024 encryption, requires both quantum and classical key compromise

### Scenario 2: Attacker Poisons Training Data

1. Attacker injects fake "normal" trades during training window
2. Model learns to ignore similar suspicious patterns
3. **Detected by**: Outlier detection in training data, periodic model validation

### Scenario 3: HNDL Attack on Audit Logs

1. Attacker collects encrypted audit logs
2. Waits for quantum computer to decrypt
3. **Blocked by**: Hash chain integrity, PQC encryption, alert correlation

## Security Controls Summary

### Cryptographic Controls
- **ML-KEM-1024**: Post-quantum key encapsulation (NIST FIPS 203)
- **ML-DSA-65**: Post-quantum digital signatures (NIST FIPS 204)
- **AES-256-GCM**: Symmetric encryption with 128-bit quantum resistance
- **Hybrid KEM**: ML-KEM + X25519 (defense in depth)

### Operational Controls
- Input validation on all data sources
- Rate limiting on API endpoints
- Audit logging with tamper-evident hash chains
- Regular security audits and penetration testing

### AI-Specific Controls
- Adversarial training and input sanitization
- Ensemble detection methods
- Intent-based analysis (not just pattern matching)
- Human-in-the-loop for high-risk flags

## Compliance & Standards

- **NIST Post-Quantum Cryptography**: FIPS 203 (ML-KEM), FIPS 204 (ML-DSA)
- **Financial Regulations**: MiFID II, SEC Rule 10b-5 (insider trading detection)
- **AI Ethics**: Explainable AI for flagged trades, bias detection in models

## Incident Response

1. **Detection**: Automated alerts from flagging system
2. **Analysis**: Correlate with audit logs, verify intent signals
3. **Containment**: Revoke compromised credentials via abir-guard CRL
4. **Eradication**: Rotate all encryption keys using abir-guard
5. **Recovery**: Restore from PQC-encrypted backups
6. **Lessons Learned**: Update threat model, patch vulnerabilities

---

*This threat model is aligned with abir-guard's security architecture and extends it for financial market detection scenarios.*
