# Publishing Guide - Abir Market Sentinel

This guide covers publishing Abir Market Sentinel to PyPI and setting up the distribution.

## Prerequisites

```bash
# Install build and publish tools
pip install build twine setuptools wheel

# Verify installations
python -m build --version
twine --version
```

## PyPI Publishing

### 1. Update Version

Before publishing, update the version in:
- `pyproject.toml`
- `src/__init__.py`

Version format: `MAJOR.MINOR.PATCH` (e.g., `0.1.0`)

### 2. Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build

# Verify build artifacts
ls -la dist/
```

Expected output:
```
dist/
├── abir_market_sentinel-0.1.0-py3-none-any.whl
└── abir_market_sentinel-0.1.0.tar.gz
```

### 3. Test Upload (TestPyPI)

```bash
# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# Install from TestPyPI to verify
pip install --index-url https://test.pypi.org/simple/ abir-market-sentinel
```

### 4. Production Upload (PyPI)

```bash
# Upload to PyPI
python -m twine upload dist/*

# Verify installation
pip install abir-market-sentinel
```

### 5. Verify Installation

```python
import abir_market_sentinel
print(abir_market_sentinel.__version__)
```

## Publishing Checklist

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Code linted (`flake8 src/`)
- [ ] Documentation updated
- [ ] Version numbers updated consistently
- [ ] CHANGELOG.md updated (if exists)
- [ ] Git tag created for version
- [ ] TestPyPI upload verified
- [ ] PyPI upload successful

## Version Tagging

```bash
# Create git tag for the version
git tag -a v0.1.0 -m "Release v0.1.0: Initial AI insider trading detection"
git push origin v0.1.0
```

## Dependencies Publishing Notes

Abir Market Sentinel depends on `abir-guard` which is published on both PyPI and crates.io:

- **PyPI**: https://pypi.org/project/abir-guard/
- **crates.io**: https://crates.io/crates/abir_guard

Ensure abir-guard is properly installed before publishing:
```bash
pip install abir-guard>=3.1.0
```

## Automated Publishing (Optional)

### GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: python -m twine upload dist/*
```

## Troubleshooting

### PyPI Rejects Upload

- Ensure version number is incremented
- Check package name availability on PyPI
- Verify all required files are present (README.md, LICENSE, etc.)

### Import Errors After Install

- Verify abir-guard is properly installed
- Check Python version compatibility (>=3.10)
- Ensure all dependencies are listed in `pyproject.toml`

## Quantum Security Note

When publishing, ensure that:
- No test credentials or keys are included
- Abir-Guard's PQC implementation is properly referenced
- Quantum-safe claims are accurately documented

---

For more information, see:
- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Abir-Guard Publishing](https://github.com/Abiress/abir-guard/blob/master/PUBLISHING.md)
