from datetime import datetime
from typing import List, Dict

class SuspiciousActivityFlagger:
    def __init__(self, anomaly_weight=0.4, intent_weight=0.4, correlation_weight=0.2):
        self.anomaly_weight = anomaly_weight
        self.intent_weight = intent_weight
        self.correlation_weight = correlation_weight
        self.flagged_activities = []

    def calculate_risk_score(self, trade_record: Dict) -> float:
        anomaly_score = trade_record.get('anomaly_score', 0)
        intent_score = trade_record.get('combined_intent_score', 0)
        news_count = trade_record.get('related_news_count', 0)
        correlation_score = min(news_count * 0.1, 1.0)
        risk_score = (
            abs(anomaly_score) * self.anomaly_weight +
            intent_score * self.intent_weight +
            correlation_score * self.correlation_weight
        )
        return min(risk_score, 1.0)

    def flag_trade(self, trade_record: Dict) -> Dict:
        risk_score = self.calculate_risk_score(trade_record)
        is_flagged = risk_score > 0.6
        flag_record = {
            'trade_id': trade_record.get('trade_id'),
            'timestamp': trade_record.get('timestamp'),
            'risk_score': risk_score,
            'is_flagged': is_flagged,
            'reason': self._generate_reason(trade_record, risk_score),
            'flagged_at': datetime.utcnow().isoformat()
        }
        if is_flagged:
            self.flagged_activities.append(flag_record)
        return flag_record

    def _generate_reason(self, trade: Dict, score: float) -> str:
        reasons = []
        if trade.get('is_anomaly'):
            reasons.append("Behavioral anomaly detected")
        if trade.get('flagged_for_intent'):
            reasons.append("Suspicious intent identified")
        if trade.get('related_news_count', 0) > 2:
            reasons.append("Multiple correlated news events")
        if not reasons:
            reasons.append("Elevated risk score")
        return "; ".join(reasons)

    def get_flagged_summary(self) -> Dict:
        return {
            'total_flagged': len(self.flagged_activities),
            'flagged_trades': self.flagged_activities,
            'high_risk_threshold': 0.6
        }
