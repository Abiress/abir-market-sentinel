import pytest
from datetime import datetime
from src.security.audit import TamperEvidentAuditLog
from src.security.canary import CanaryTradeManager
from src.security.key_rotation import QuantumKeyRotationManager
from src.security.fips_mode import FIPSEncryptor
from src.security.differential_privacy import DifferentialEntropyCollector, SpectreDefender

def test_audit_log_creation():
    log = TamperEvidentAuditLog()
    assert len(log.hash_chain) == 1  # Genesis block
    assert len(log.logs) == 0

def test_audit_log_event():
    log = TamperEvidentAuditLog()
    entry = log.log_event("test_event", {"key": "value"}, user="tester")
    assert len(log.logs) == 1
    assert entry['event_type'] == 'test_event'
    assert entry['user'] == 'tester'
    assert 'entry_hash' in entry

def test_audit_chain_integrity():
    log = TamperEvidentAuditLog()
    log.log_event("event1", {"data": 1})
    log.log_event("event2", {"data": 2})
    log.log_event("event3", {"data": 3})
    assert log.verify_chain_integrity() == True

def test_canary_deployment():
    manager = CanaryTradeManager()
    canaries = manager.deploy_canaries(count=5)
    assert len(canaries) == 5
    assert all(c['is_canary'] for c in canaries)

def test_canary_breach_detection():
    manager = CanaryTradeManager()
    canary = manager.generate_canary_trade()
    assert manager.check_canary_access(canary['trade_id']) == True
    status = manager.get_breach_status()
    assert status['breach_detected'] == True
    assert status['canary_access_count'] == 1

def test_key_rotation_manager():
    mgr = QuantumKeyRotationManager(default_max_operations=100)
    mgr.register_key("test-key")
    assert "test-key" in mgr.keys
    mgr.record_usage("test-key", "encrypt")
    assert mgr.keys["test-key"]['operation_count'] == 1
    assert mgr.needs_rotation("test-key") == False

def test_key_rotation_needed():
    mgr = QuantumKeyRotationManager(default_max_operations=2)
    mgr.register_key("rotate-me")
    mgr.record_usage("rotate-me", "encrypt")
    mgr.record_usage("rotate-me", "encrypt")
    assert mgr.needs_rotation("rotate-me") == True

def test_key_rotation_execute():
    mgr = QuantumKeyRotationManager(default_max_operations=2)
    mgr.register_key("old-key")
    result = mgr.rotate_key("old-key")
    assert 'new_key' in result
    assert mgr.keys["old-key"]['status'] == 'rotated'
    assert result['new_key'] in mgr.keys

def test_fips_mode():
    fips = FIPSEncryptor()
    assert fips.is_approved('AES-256-GCM') == True
    assert fips.is_approved('X25519') == False

def test_fips_strict_mode():
    fips = FIPSEncryptor()
    fips.set_strict_mode(True)
    assert fips.strict_mode == True
    status = fips.get_compliance_status()
    assert status['fips_203_compliant'] == True

def test_differential_privacy():
    collector = DifferentialEntropyCollector(epsilon=0.5, sample_count=10)
    noise = collector.collect()
    assert len(noise) == 32 * 4  # 32 floats * 4 bytes each
    assert collector.estimate_privacy_budget() > 0

def test_spectre_defender():
    defender = SpectreDefender()
    import numpy as np
    data = np.array([1.0, 2.0, 3.0])
    noisy = defender.inject_noise(data)
    assert len(noisy) == len(data)
    assert not np.array_equal(data, noisy)  # Should be different due to noise
