import hashlib
import json
from datetime import datetime, timezone
from typing import List, Dict

class TamperEvidentAuditLog:
    def __init__(self):
        self.logs = []
        self.hash_chain = []
        self._initialize_chain()
    
    def _initialize_chain(self):
        genesis = hashlib.sha256(b"ABIR_MARKET_SENTINEL_GENESIS").hexdigest()
        self.hash_chain.append(genesis)
    
    def _compute_entry_hash(self, entry: Dict, prev_hash: str) -> str:
        content = json.dumps(entry, sort_keys=True) + prev_hash
        return hashlib.sha256(content.encode()).hexdigest()

    def _hash_payload(self, entry: Dict) -> Dict:
        payload = dict(entry)
        payload.pop('entry_hash', None)
        return payload
    
    def log_event(self, event_type: str, details: Dict, user: str = "system") -> Dict:
        entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': event_type,
            'details': details,
            'user': user,
            'prev_hash': self.hash_chain[-1]
        }
        entry_hash = self._compute_entry_hash(self._hash_payload(entry), self.hash_chain[-1])
        entry['entry_hash'] = entry_hash
        self.hash_chain.append(entry_hash)
        self.logs.append(entry)
        return entry
    
    def verify_chain_integrity(self) -> bool:
        for i in range(len(self.logs)):
            entry = self.logs[i]
            prev_hash = self.hash_chain[i]
            computed = self._compute_entry_hash(self._hash_payload(entry), prev_hash)
            if computed != entry['entry_hash']:
                return False
        return True
    
    def get_logs(self, limit: int = 100, event_type: str = None) -> List[Dict]:
        logs = self.logs[-limit:]
        if event_type:
            logs = [l for l in logs if l['event_type'] == event_type]
        return logs
    
    def export_for_compliance(self) -> Dict:
        return {
            'total_entries': len(self.logs),
            'chain_valid': self.verify_chain_integrity(),
            'first_entry': self.logs[0] if self.logs else None,
            'last_entry': self.logs[-1] if self.logs else None,
            'hash_chain_length': len(self.hash_chain)
        }
