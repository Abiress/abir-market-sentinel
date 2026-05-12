import numpy as np
import pandas as pd

try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    IsolationForest = None
    StandardScaler = None
    SKLEARN_AVAILABLE = False


class _NumpyScaler:
    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit_transform(self, features: np.ndarray) -> np.ndarray:
        self.mean_ = np.mean(features, axis=0)
        self.scale_ = np.std(features, axis=0)
        self.scale_[self.scale_ == 0] = 1.0
        return (features - self.mean_) / self.scale_

    def transform(self, features: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.scale_ is None:
            raise ValueError("Scaler must be fit before transform")
        return (features - self.mean_) / self.scale_


class _FallbackIsolationModel:
    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination
        self.center_ = None
        self.threshold_ = None

    def fit(self, scaled_features: np.ndarray):
        self.center_ = np.median(scaled_features, axis=0)
        distances = np.linalg.norm(scaled_features - self.center_, axis=1)
        percentile = max(0.0, min(100.0, 100 * (1.0 - self.contamination)))
        self.threshold_ = float(np.percentile(distances, percentile))

    def decision_function(self, scaled_features: np.ndarray) -> np.ndarray:
        distances = np.linalg.norm(scaled_features - self.center_, axis=1)
        return self.threshold_ - distances

    def predict(self, scaled_features: np.ndarray) -> np.ndarray:
        scores = self.decision_function(scaled_features)
        return np.where(scores < 0, -1, 1)

class BehavioralAnomalyDetector:
    def __init__(self, contamination=0.1):
        self.contamination = contamination
        if SKLEARN_AVAILABLE:
            self.model = IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=100
            )
            self.scaler = StandardScaler()
        else:
            self.model = _FallbackIsolationModel(contamination=contamination)
            self.scaler = _NumpyScaler()
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
