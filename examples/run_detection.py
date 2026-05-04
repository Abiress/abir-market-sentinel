import pandas as pd
from datetime import datetime, timedelta
from src.quantum_security.vault import QuantumVault
from src.behavioral_ai.anomaly_detector import BehavioralAnomalyDetector
from src.behavioral_ai.intent_analyzer import IntentAnalyzer
from src.correlation.linker import TradeNewsCorrelator
from src.alerting.flagging import SuspiciousActivityFlagger

def run_example():
    print("=" * 60)
    print("Abir Market Sentinel - Example Detection Run")
    print("=" * 60)
    vault = QuantumVault("example-sentinel")
    detector = BehavioralAnomalyDetector(contamination=0.15)
    intent_analyzer = IntentAnalyzer()
    correlator = TradeNewsCorrelator(time_window_hours=12)
    flagger = SuspiciousActivityFlagger()
    trades = pd.DataFrame([
        {'trade_id': f'T{i:03d}', 'symbol': 'AAPL', 'timestamp': (datetime.utcnow() - timedelta(hours=i)).isoformat(),
         'volume': 1000 + i*100, 'price_change_pct': float(i % 10), 'trade_size_deviation': 1.0 + i*0.1,
         'time_of_day_sin': 0.5, 'time_of_day_cos': 0.5, 'account_age_days': 365, 'prior_trade_count_24h': 10 + i}
        for i in range(50)
    ])
    trades.loc[45, 'trade_size_deviation'] = 8.0
    trades.loc[45, 'volume'] = 10000
    detector.train(trades.iloc[:40])
    results = detector.detect_anomalies(trades.iloc[40:])
    news = pd.DataFrame([
        {'symbol': 'AAPL', 'headline': 'Unexpected CEO resignation announced', 'published_at': datetime.utcnow().isoformat(), 'source': 'reuters'}
    ])
    correlated = correlator.correlate_trades_with_news(results, news)
    print(f"\nDetected {correlated['is_anomaly'].sum()} anomalies in recent trades")
    for idx, trade in correlated.iterrows():
        if trade['is_anomaly'] or trade['trade_size_deviation'] > 5:
            intent = intent_analyzer.analyze_trade_intent(trade.to_dict(), news.to_dict('records'))
            flag = flagger.flag_trade({**trade.to_dict(), **intent})
            if flag['is_flagged']:
                vault.store_trade_data(trade.to_dict())
                print(f"\nFLAGGED: {flag['trade_id']}")
                print(f"  Risk Score: {flag['risk_score']:.2f}")
                print(f"  Reason: {flag['reason']}")
    print(f"\n{'-'*60}")
    print("All flagged trades securely stored using Abir-Guard PQC encryption")

if __name__ == "__main__":
    run_example()
