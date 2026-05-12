# src/__init__.py - Lazy imports to avoid premature numpy loading
import sys
import os

# Only import types that don't require numpy/pandas
__version__ = "1.0.1"

# Lazy import function
def _get_vault():
    from src.quantum_security.vault import QuantumVault
    return QuantumVault

def _get_detector():
    from src.behavioral_ai.anomaly_detector import BehavioralAnomalyDetector
    return BehavioralAnomalyDetector

__all__ = ["__version__"]
