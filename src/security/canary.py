import random
import string
from datetime import datetime
from typing import Dict, List

class CanaryTradeManager:
    def __init__(self):
        self.canary_trades = {}
        self.access_log = []

    def generate_canary_trade(self, symbol: str = "CANARY") -> Dict:
        canary_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        canary = {
            'trade_id': f"CANARY_{canary_id}",
            'symbol': symbol,
            'timestamp': datetime.utcnow().isoformat(),
            'price': 999.99,
            'volume': 1,
            'is_canary': True,
            'created_at': datetime.utcnow().isoformat()
        }
        self.canary_trades[canary['trade_id']] = canary
        return canary

    def check_canary_access(self, trade_id: str) -> bool:
        is_canary = trade_id in self.canary_trades
        self.access_log.append({
            'trade_id': trade_id,
            'is_canary': is_canary,
            'accessed_at': datetime.utcnow().isoformat()
        })
        return is_canary

    def get_breach_status(self) -> Dict:
        canary_accessed = [log for log in self.access_log if log['is_canary']]
        return {
            'breach_detected': len(canary_accessed) > 0,
            'canary_access_count': len(canary_accessed),
            'total_canaries': len(self.canary_trades),
            'accessed_canaries': canary_accessed
        }

    def deploy_canaries(self, count: int = 5) -> List[Dict]:
        deployed = []
        for _ in range(count):
            canary = self.generate_canary_trade()
            deployed.append(canary)
        return deployed
