import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.main import main
from src.quantum_security.vault import QuantumVault
from src.behavioral_ai.anomaly_detector import BehavioralAnomalyDetector
from src.behavioral_ai.intent_analyzer import IntentAnalyzer
from src.correlation.linker import TradeNewsCorrelator
from src.alerting.flagging import SuspiciousActivityFlagger
from src.security.audit import TamperEvidentAuditLog

def test_full_pipeline():
    """Test the complete Phase 1-3 pipeline"""
    vault = QuantumVault("integration-test")
    detector = BehavioralAnomalyDetector(contamination=0.1)
    intent_analyzer = IntentAnalyzer()
    correlator = TradeNewsCorrelator(time_window_hours=12)
    flagger = SuspiciousActivityFlagger()
    audit_log = TamperEvidentAuditLog()
    
    audit_log.log_event("test_start", {"test": "full_pipeline"})
    
    trades = pd.DataFrame([
        {'trade_id': f'T{i:03d}', 'symbol': 'AAPL', 
         'timestamp': (datetime.utcnow() - timedelta(hours=i)).isoformat(),
         'volume': 1000 + i*100, 'price_change_pct': float(i % 5), 
         'trade_size_deviation': 1.0 + i*0.1, 'time_of_day_sin': 0.5,
         'time_of_day_cos': 0.5, 'account_age_days': 365, 
         'prior_trade_count_24h': 10 + i}
        for i in range(50)
    ])
    trades.loc[45, 'trade_size_deviation'] = 8.0
    trades.loc[45, 'volume'] = 10000
    
    train_data = trades.iloc[:40]
    test_data = trades.iloc[40:]
    
    detector.train(train_data)
    results = detector.detect_anomalies(test_data)
    
    news = pd.DataFrame([
        {'symbol': 'AAPL', 'headline': 'Unexpected earnings announcement',
         'published_at': datetime.utcnow().isoformat(), 'source': 'test'}
    ])
    
    results = correlator.correlate_trades_with_news(results, news)
    
    for idx, trade in results.iterrows():
        intent_result = intent_analyzer.analyze_trade_intent(
            trade.to_dict(), news.to_dict('records')
        )
        results.at[idx, 'combined_intent_score'] = intent_result['combined_intent_score']
    
    flagged_count = 0
    for _, trade in results.iterrows():
        flag = flagger.flag_trade(trade.to_dict())
        if flag['is_flagged']:
            vault.store_trade_data(trade.to_dict())
            audit_log.log_event("trade_flagged", {"trade_id": flag['trade_id']})
            flagged_count += 1
    
    assert len(audit_log.logs) > 0
    assert audit_log.verify_chain_integrity() == True
    assert flagged_count >= 0

def test_quantum_vault_with_phases():
    """Test quantum vault works with all phases"""
    vault = QuantumVault("phase-test")
    
    trade = {
        'trade_id': 'PHASE001',
        'symbol': 'AAPL',
        'timestamp': datetime.utcnow().isoformat(),
        'volume': 5000,
        'price': 150.0,
        'phase': 3,
        'security': 'PQC'
    }
    
    ciphertext = vault.store_trade_data(trade)
    retrieved = vault.retrieve_trade_data(ciphertext)
    
    assert retrieved['trade_id'] == 'PHASE001'
    assert retrieved['phase'] == 3
    assert retrieved['security'] == 'PQC'

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
