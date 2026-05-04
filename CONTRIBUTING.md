# Contributing to Abir Market Sentinel

Thank you for your interest in contributing to Abir Market Sentinel! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/abir-market-sentinel.git
   cd abir-market-sentinel
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```
4. Install abir-guard from source:
   ```bash
   git clone https://github.com/Abiress/abir-guard.git
   pip install ./abir-guard
   ```

## How to Contribute

### Reporting Bugs

- Use the GitHub issue tracker
- Describe the bug with steps to reproduce
- Include expected vs actual behavior
- Mention your OS, Python version, and relevant package versions

### Suggesting Enhancements

- Open an issue with the "enhancement" label
- Describe the feature and its use case
- Discuss implementation approach if possible

### Adding Detection Models

When adding new behavioral AI models:

1. Place model code in `src/behavioral_ai/`
2. Include model card documentation
3. Add unit tests in `tests/`
4. Update the model registry in `src/behavioral_ai/__init__.py`

## Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git commit -m "feat: add your feature description"
   ```

3. Push to your fork and submit a Pull Request

4. PR Checklist:
   - [ ] Code follows project style guidelines
   - [ ] Tests added/updated for new functionality
   - [ ] Documentation updated
   - [ ] All tests pass (`pytest tests/`)
   - [ ] No new linting errors (`flake8 src/`)

## Coding Standards

### Python Style

- Follow PEP 8
- Use type hints where appropriate
- Run `black` for formatting: `black src/ tests/`
- Maximum line length: 100 characters

### Documentation

- Use Google-style docstrings
- Document all public functions and classes
- Include usage examples for complex functions

Example:
```python
def analyze_intent(trade_data: dict, news_context: list) -> dict:
    """Analyze trading intent based on behavioral patterns.
    
    Args:
        trade_data: Dictionary containing trade details
        news_context: List of related news articles
        
    Returns:
        Dictionary with intent analysis results including
        suspicion score and flagged signals.
    """
    pass
```

## Testing

- Write tests using pytest
- Aim for >80% code coverage
- Place tests in the `tests/` directory
- Name test files as `test_*.py`

Run tests:
```bash
pytest tests/ -v --cov=src
```

## Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Update THREAT_MODEL.md if security model changes

## Quantum Security Notes

When contributing to the quantum security layer:

- All sensitive data MUST use Abir-Guard's PQC encryption
- Test with ML-KEM-1024 and hybrid modes
- Document quantum resistance properties
- Follow abir-guard's security best practices

## Review Process

- All PRs require at least one review
- Maintainers may request changes
- Address feedback promptly and professionally
- Once approved, maintainers will merge

## Questions?

Feel free to open an issue for any questions about contributing!

---

Thank you for contributing to Abir Market Sentinel! 🚀
