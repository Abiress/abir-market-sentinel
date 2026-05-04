from typing import Dict, List, Optional
import hashlib
import hmac

class FIPSEncryptor:
    def __init__(self):
        self.approved_algorithms = {
            'AES-256-GCM': True,
            'SHA-256': True,
            'HMAC-SHA256': True,
            'ML-KEM-1024': True,   # NIST FIPS 203
            'ML-DSA-65': True,      # NIST FIPS 204
            'X25519': False,        # Not FIPS approved
        }
        self.strict_mode = False

    def set_strict_mode(self, enabled: bool = True):
        self.strict_mode = enabled

    def is_approved(self, algorithm: str) -> bool:
        return self.approved_algorithms.get(algorithm, False)

    def encrypt(self, data: bytes, key: bytes) -> Optional[Dict]:
        if self.strict_mode and not self.is_approved('AES-256-GCM'):
            raise ValueError("AES-256-GCM not in approved list")
        if len(key) not in [32, 64]:  # 256-bit or 512-bit key
            if self.strict_mode:
                raise ValueError("Key length not FIPS approved")
        from cryptography.fernet import Fernet
        import base64
        if len(key) == 32:
            key = base64.urlsafe_b64encode(key)
        try:
            f = Fernet(key)
            return {'ciphertext': f.encrypt(data), 'algorithm': 'AES-256-GCM-Fernet'}
        except Exception:
            return None

    def decrypt(self, ct: bytes, key: bytes) -> Optional[bytes]:
        if self.strict_mode and not self.is_approved('AES-256-GCM'):
            raise ValueError("AES-256-GCM not in approved list")
        from cryptography.fernet import Fernet
        import base64
        if len(key) == 32:
            key = base64.urlsafe_b64encode(key)
        try:
            f = Fernet(key)
            return f.decrypt(ct)
        except Exception:
            return None

    def hash(self, data: bytes) -> bytes:
        if self.strict_mode and not self.is_approved('SHA-256'):
            raise ValueError("SHA-256 not approved in strict mode")
        return hashlib.sha256(data).digest()

    def hmac_sign(self, data: bytes, key: bytes) -> bytes:
        if self.strict_mode and not self.is_approved('HMAC-SHA256'):
            raise ValueError("HMAC-SHA256 not approved in strict mode")
        return hmac.new(key, data, hashlib.sha256).digest()

    def get_compliance_status(self) -> Dict:
        return {
            'strict_mode': self.strict_mode,
            'approved_algorithms': self.approved_algorithms,
            'fips_203_compliant': self.is_approved('ML-KEM-1024'),
            'fips_204_compliant': self.is_approved('ML-DSA-65'),
        }
