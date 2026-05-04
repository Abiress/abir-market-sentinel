# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of Abir Market Sentinel seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **security@abir-market-sentinel.dev**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

### What to Include

Please include the following information in your report:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Disclosure Policy

We follow a coordinated disclosure policy:

1. **Report Received** - We acknowledge receipt within 48 hours
2. **Triage** - We confirm the issue and determine its severity (1-5 business days)
3. **Fix Development** - We develop and test a fix
4. **Disclosure** - We coordinate with you on disclosure timeline (typically 90 days max)

### Safe Harbor

We consider security research and vulnerability disclosure activities conducted under this policy to be:
- Authorized in view of any applicable anti-hacking laws
- Compliant with any applicable rules of any applicable bug bounty program
- Exempt from restrictions in our Terms of Service (TOS) related to:
  - Testing of vulnerabilities
  - Reverse engineering of software

### Scope

This security policy applies to:

- The Abir Market Sentinel core detection engine
- The quantum security layer using abir-guard
- API endpoints and data ingestion modules
- Configuration and deployment scripts

### Out of Scope

- Third-party dependencies (report to respective maintainers)
- abir-guard itself (report to [Abiress/abir-guard](https://github.com/Abiress/abir-guard/security))
- Denial of Service (DoS) attacks
- Social engineering attacks
- Physical attacks on infrastructure

### Recognition

We appreciate your efforts to responsibly disclose your findings and will acknowledge your contributions in:
- Security advisories (with your permission)
- Our Hall of Fame (if applicable)
- Release notes for the fix

### Quantum Security Considerations

Given our use of post-quantum cryptography via abir-guard:

- We monitor NIST post-quantum standardization updates
- We test against known quantum cryptanalysis attacks
- We follow abir-guard's quantum-safe practices

If you discover a vulnerability in our quantum-safe implementation:
- Specify if it affects classical or quantum threat models
- Include analysis of quantum advantage required to exploit
- Reference relevant NIST PQC standards

## Contact

- Security Email: security@abir-market-sentinel.dev
- GPG Key: [Download](https://abir-market-sentinel.dev/security.gpg)

---

Thank you for helping keep Abir Market Sentinel and our users safe!
