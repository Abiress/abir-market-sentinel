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
import warnings

class QuantumVault:
    def __init__(self, agent_id="market-sentinel"):
        if not ABIR_GUARD_AVAILABLE:
            raise ImportError(
                "abir-guard not installed. Install from: "
                "https://github.com/Abiress/abir-guard"
            )
        self.vault = AbirVault()
        self.agent_id = agent_id
        self.kem = HybridKem()
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
        return self.kem.encapsulate(data)
