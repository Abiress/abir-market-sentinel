from abir_guard import Vault
from abir_guard.ml_kem import MLKEMHybrid
import json
from datetime import datetime

class QuantumVault:
    def __init__(self, agent_id="market-sentinel"):
        self.vault = Vault()
        self.agent_id = agent_id
        self.kem = MLKEMHybrid()
        self._ensure_keys()

    def _ensure_keys(self):
        keys = self.vault.list_keypairs()
        if self.agent_id not in keys:
            self.vault.generate_keypair(self.agent_id)

    def store_trade_data(self, trade_record: dict) -> str:
        data = json.dumps(trade_record).encode()
        return self.vault.store(self.agent_id, data)

    def retrieve_trade_data(self, ciphertext: str) -> dict:
        plaintext = self.vault.retrieve(self.agent_id, ciphertext)
        return json.loads(plaintext)

    def store_anomaly_score(self, score_data: dict) -> str:
        data = json.dumps(score_data).encode()
        return self.vault.store(f"{self.agent_id}-anomaly", data)

    def quantum_encrypt(self, data: bytes) -> tuple:
        return self.kem.encapsulate(data)
