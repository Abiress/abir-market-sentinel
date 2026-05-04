import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from datetime import datetime, timedelta
from src.quantum_security.vault import QuantumVault
from src.behavioral_ai.anomaly_detector import BehavioralAnomalyDetector
from src.behavioral_ai.intent_analyzer import IntentAnalyzer
from src.correlation.linker import TradeNewsCorrelator
from src.alerting.flagging import SuspiciousActivityFlagger
from src.data_ingestion.market_data import MarketDataIngestor
from src.security.audit import TamperEvidentAuditLog
from src.security.canary import CanaryTradeManager
from src.security.key_rotation import QuantumKeyRotationManager

def main():
    print("=" * 70)
    print("Abir Market Sentinel - AI Insider Trading Detection Engine")
    print("Phase 1: Foundation | Phase 2: Intelligence | Phase 3: Security")
    print("=" * 70)
    
    # Initialize all components
    vault = QuantumVault("market-sentinel")
    ingestor = MarketDataIngestor()
    detector = BehavioralAnomalyDetector(contamination=0.1)
    intent_analyzer = IntentAnalyzer()
    correlator = TradeNewsCorrelator(time_window_hours=24)
    flagger = SuspiciousActivityFlagger()
    
    # Phase 3: Security components
    audit_log = TamperEvidentAuditLog()
    canary_manager = CanaryTradeManager()
    key_rotation = QuantumKeyRotationManager(default_max_operations=1000)
    
    audit_log.log_event("system_start", {"version": "0.1.0", "phases": [1, 2, 3]})
    
    print("\n[Phase 1] Ingesting market data...")
    end = datetime.utcnow()
    start = end - timedelta(days=7)
    trades = ingestor.fetch_trades("AAPL", start, end)
    news = ingestor.fetch_news(["AAPL", "MSFT"], hours=24)
    agent_logs = ingestor.fetch_agent_logs("trading-agent-001", hours=24)
    print(f"    Loaded {len(trades)} trades, {len(news)} news items")
    audit_log.log_event("data_ingestion", {"trades": len(trades), "news": len(news)})
    
    print("\n[Phase 1] Training behavioral anomaly detector...")
    train_data = trades.sample(frac=0.8, random_state=42)
    detector.train(train_data)
    audit_log.log_event("model_training", {"samples": len(train_data)})
    
    print("\n[Phase 2] Detecting anomalies with intent analysis...")
    test_data = trades.drop(train_data.index)
    results = detector.detect_anomalies(test_data)
    anomalies = results[results['is_anomaly']]
    print(f"    Found {len(anomalies)} anomalous trades")
    
    print("\n[Phase 2] Correlating with news and agent actions...")
    results = correlator.correlate_trades_with_news(results, news)
    results = correlator.correlate_with_agent_actions(results, agent_logs)
    
    print("\n[Phase 2] Analyzing intent for each trade...")
    for idx, trade in results.iterrows():
        intent_result = intent_analyzer.analyze_trade_intent(
            trade.to_dict(), trade.get('related_news', [])
        )
        results.at[idx, 'combined_intent_score'] = intent_result['combined_intent_score']
        results.at[idx, 'flagged_for_intent'] = intent_result['flagged_for_intent']
    
    print("\n[Phase 3] Deploying canary trades...")
    canaries = canary_manager.deploy_canaries(count=3)
    print(f"    Deployed {len(canaries)} canary trades")
    audit_log.log_event("canary_deployment", {"count": len(canaries)})
    
    print("\n[Phase 3] Flagging suspicious activity with audit logging...")
    flagged_results = []
    for _, trade in results.iterrows():
        flag = flagger.flag_trade(trade.to_dict())
        flagged_results.append(flag)
        
        if flag['is_flagged']:
            vault.store_trade_data(trade.to_dict())
            audit_log.log_event("trade_flagged", {
                "trade_id": flag['trade_id'],
                "risk_score": flag['risk_score'],
                "reason": flag['reason']
            })
            print(f"    FLAGGED: Trade {flag['trade_id']} | Risk: {flag['risk_score']:.2f}")
            print(f"             Reason: {flag['reason']}")
    
    print("\n[Phase 3] Registering keys for rotation...")
    key_rotation.register_key("market-sentinel", max_operations=5000)
    audit_log.log_event("key_registration", {"key_id": "market-sentinel"})
    
    summary = flagger.get_flagged_summary()
    
    print(f"\n{'='*70}")
    print(f"SUMMARY: {summary['total_flagged']} trades flagged out of {len(trades)}")
    print(f"Quantum-secured storage active via Abir-Guard")
    print(f"Audit log entries: {len(audit_log.logs)}")
    print(f"Audit chain valid: {audit_log.verify_chain_integrity()}")
    print(f"Canary status: {canary_manager.get_breach_status()}")
    print(f"{'='*70}")
    
    audit_log.log_event("system_shutdown", {"flagged_count": summary['total_flagged']})
    print("\nFinal Audit Log Export:")
    print(audit_log.export_for_compliance())

if __name__ == "__main__":
    main()
