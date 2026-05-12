"""
Quantum Security Module - Interface with Abir-Guard for PQC
Uses ML-KEM-1024 via abir-guard's HybridKem class
"""
try:
    from abir_guard.ml_kem import HybridKem
    from abir_guard import Vault as AbirVault
    ABIR_GUARD_AVAILABLE = True
except ImportError:
    ABIR_GUARD_AVAILABLE = False
    HybridKem = None
    AbirVault = None

import json
import uuid
import warnings


class _FallbackVault:
    def __init__(self):
        self._store = {}
        self._keys = set()

    def list_keypairs(self):
        return sorted(self._keys)

    def generate_keypair(self, key_id: str):
        self._keys.add(key_id)

    def store(self, key_id: str, data: bytes) -> str:
        self._keys.add(key_id)
        token = f"fallback:{key_id}:{uuid.uuid4().hex}"
        self._store[token] = data
        return token

    def retrieve(self, key_id: str, ciphertext: str) -> bytes:
        _ = key_id
        if ciphertext not in self._store:
            raise KeyError("Ciphertext not found in fallback vault")
        return self._store[ciphertext]

class QuantumVault:
    def __init__(self, agent_id="market-sentinel"):
        self.agent_id = agent_id
        if ABIR_GUARD_AVAILABLE:
            self.vault = AbirVault()
            self.kem = HybridKem()
        else:
            warnings.warn(
                "abir-guard not installed; using in-memory fallback vault. "
                "Install abir-guard for production-grade PQC.",
                RuntimeWarning,
            )
            self.vault = _FallbackVault()
            self.kem = None
        self._ensure_keys()
    
    def _ensure_keys(self):
        try:
            keys = self.vault.list_keypairs()
            if self.agent_id not in keys:
                self.vault.generate_keypair(self.agent_id)
        except Exception as e:
            warnings.warn(f"Could not ensure keys: {e}")
    
    def store_trade_data(self, trade_record: dict) -> str:
        data = json.dumps(trade_record).encode()
        return self.vault.store(self.agent_id, data)
    
    def retrieve_trade_data(self, ciphertext: str) -> dict:
        plaintext = self.vault.retrieve(self.agent_id, ciphertext)
        return json.loads(plaintext)
    
    def store_anomaly_score(self, score_data: dict) -> str:
        data = json.dumps(score_data).encode()
        return self.vault.store(f"{self.agent_id}-anomaly", data)
    
    def quantum_encrypt(self, data: bytes):
        if self.kem is None:
            return {"ciphertext": data, "mode": "fallback"}
        return self.kem.encapsulate(data)
