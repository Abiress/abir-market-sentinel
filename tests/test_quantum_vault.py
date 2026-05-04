import pytest
from src.quantum_security.vault import QuantumVault
import json

def test_vault_initialization():
    vault = QuantumVault("test-sentinel")
    keys = vault.vault.list_keypairs()
    assert "test-sentinel" in keys

def test_store_and_retrieve():
    vault = QuantumVault("test-sentinel-2")
    trade_record = {
        'trade_id': 'T001',
        'symbol': 'AAPL',
        'timestamp': '2026-05-04T10:00:00',
        'volume': 1000,
        'price': 150.0
    }
    ciphertext = vault.store_trade_data(trade_record)
    assert ciphertext is not None
    retrieved = vault.retrieve_trade_data(ciphertext)
    assert retrieved['trade_id'] == 'T001'
    assert retrieved['symbol'] == 'AAPL'

def test_anomaly_storage():
    vault = QuantumVault("test-sentinel-3")
    score_data = {
        'trade_id': 'T002',
        'anomaly_score': -0.85,
        'is_anomaly': True,
        'timestamp': '2026-05-04T10:05:00'
    }
    ciphertext = vault.store_anomaly_score(score_data)
    assert ciphertext is not None
