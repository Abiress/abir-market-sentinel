from flask import Flask, request, jsonify
from src.quantum_security.vault import QuantumVault
from src.behavioral_ai.anomaly_detector import BehavioralAnomalyDetector
from src.behavioral_ai.intent_analyzer import IntentAnalyzer
from src.correlation.linker import TradeNewsCorrelator
from src.alerting.flagging import SuspiciousActivityFlagger
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Initialize components
vault = QuantumVault("api-sentinel")
detector = BehavioralAnomalyDetector()
intent_analyzer = IntentAnalyzer()
correlator = TradeNewsCorrelator()
flagger = SuspiciousActivityFlagger()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'abir-market-sentinel',
        'version': '0.1.0',
        'quantum_safe': True
    })

@app.route('/api/detect', methods=['POST'])
def detect_insider_trading():
    try:
        data = request.json
        trades = pd.DataFrame(data.get('trades', []))
        news = pd.DataFrame(data.get('news', []))
        agent_logs = pd.DataFrame(data.get('agent_logs', []))
        
        if trades.empty:
            return jsonify({'error': 'No trades provided'}), 400
        
        results = detector.detect_anomalies(trades)
        if not news.empty:
            results = correlator.correlate_trades_with_news(results, news)
        if not agent_logs.empty:
            results = correlator.correlate_with_agent_actions(results, agent_logs)
        
        flagged = []
        for _, trade in results.iterrows():
            intent = intent_analyzer.analyze_trade_intent(
                trade.to_dict(),
                trade.get('related_news', [])
            )
            trade_dict = {**trade.to_dict(), **intent}
            flag = flagger.flag_trade(trade_dict)
            
            if flag['is_flagged']:
                vault.store_trade_data(trade.to_dict())
                flagged.append({
                    'trade_id': flag['trade_id'],
                    'risk_score': flag['risk_score'],
                    'reason': flag['reason']
                })
        
        return jsonify({
            'total_trades': len(trades),
            'anomalies_detected': int(results['is_anomaly'].sum()),
            'flagged_trades': flagged,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    try:
        data = request.json
        historical_trades = pd.DataFrame(data.get('historical_trades', []))
        
        if historical_trades.empty:
            return jsonify({'error': 'No historical data provided'}), 400
        
        detector.train(historical_trades)
        return jsonify({
            'status': 'Model trained successfully',
            'training_samples': len(historical_trades)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
