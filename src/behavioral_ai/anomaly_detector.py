import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd

class BehavioralAnomalyDetector:
    def __init__(self, contamination=0.1):
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_columns = [
            'volume', 'price_change_pct', 'trade_size_deviation',
            'time_of_day_sin', 'time_of_day_cos',
            'account_age_days', 'prior_trade_count_24h'
        ]
    
    def extract_features(self, trades_df: pd.DataFrame) -> np.ndarray:
        features = []
        for _, trade in trades_df.iterrows():
            feature_vec = [
                float(trade.get('volume', 0)),
                float(trade.get('price_change_pct', 0)),
                float(trade.get('trade_size_deviation', 0)),
                float(trade.get('time_of_day_sin', 0)),
                float(trade.get('time_of_day_cos', 0)),
                float(trade.get('account_age_days', 0)),
                float(trade.get('prior_trade_count_24h', 0)),
            ]
            features.append(feature_vec)
        return np.array(features)
    
    def train(self, historical_trades: pd.DataFrame):
        if len(historical_trades) < 10:
            raise ValueError("Need at least 10 samples to train")
        features = self.extract_features(historical_trades)
        scaled = self.scaler.fit_transform(features)
        self.model.fit(scaled)
        self.is_trained = True
    
    def detect_anomalies(self, recent_trades: pd.DataFrame) -> pd.DataFrame:
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        features = self.extract_features(recent_trades)
        scaled = self.scaler.transform(features)
        scores = self.model.decision_function(scaled)
        predictions = self.model.predict(scaled)
        results = recent_trades.copy()
        results['anomaly_score'] = scores
        results['is_anomaly'] = predictions == -1
        return results
