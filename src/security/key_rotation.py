from datetime import datetime, timedelta
from typing import Dict, List
import hashlib
import json

class QuantumKeyRotationManager:
    def __init__(self, default_max_operations: int = 1000, default_max_age_hours: int = 24):
        self.keys = {}
        self.default_max_operations = default_max_operations
        self.default_max_age_hours = default_max_age_hours

    def register_key(self, key_id: str, max_operations: int = None, max_age_hours: int = None):
        self.keys[key_id] = {
            'created_at': datetime.utcnow().isoformat(),
            'operation_count': 0,
            'max_operations': max_operations or self.default_max_operations,
            'max_age_hours': max_age_hours or self.default_max_age_hours,
            'status': 'active'
        }

    def record_usage(self, key_id: str, operation: str = "encrypt"):
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not registered")
        self.keys[key_id]['operation_count'] += 1

    def needs_rotation(self, key_id: str) -> bool:
        if key_id not in self.keys:
            return False
        key = self.keys[key_id]
        age = datetime.utcnow() - datetime.fromisoformat(key['created_at'])
        age_hours = age.total_seconds() / 3600
        return (key['operation_count'] >= key['max_operations'] or
                age_hours >= key['max_age_hours'])

    def rotate_key(self, key_id: str) -> Dict:
        if key_id not in self.keys:
            raise ValueError(f"Key {key_id} not registered")
        old_key = self.keys[key_id].copy()
        new_key_id = f"{key_id}_rotated_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self.keys[new_key_id] = {
            'created_at': datetime.utcnow().isoformat(),
            'operation_count': 0,
            'max_operations': old_key['max_operations'],
            'max_age_hours': old_key['max_age_hours'],
            'status': 'active',
            'replaces': key_id
        }
        self.keys[key_id]['status'] = 'rotated'
        return {
            'old_key': key_id,
            'new_key': new_key_id,
            'rotated_at': datetime.utcnow().isoformat()
        }

    def get_key_metadata(self, key_id: str) -> Dict:
        return self.keys.get(key_id, {})

    def list_keys_needing_rotation(self) -> List[str]:
        return [k for k in self.keys if self.needs_rotation(k)]
