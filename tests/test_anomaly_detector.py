import pytest
import pandas as pd
import numpy as np
from src.behavioral_ai.anomaly_detector import BehavioralAnomalyDetector

def test_detector_initialization():
    detector = BehavioralAnomalyDetector(contamination=0.1)
    assert detector.contamination == 0.1
    assert detector.is_trained == False

def test_feature_extraction():
    detector = BehavioralAnomalyDetector()
    df = pd.DataFrame([
        {'volume': 1000, 'price_change_pct': 5.0, 'trade_size_deviation': 1.5,
         'time_of_day_sin': 0.5, 'time_of_day_cos': 0.5, 'account_age_days': 365,
         'prior_trade_count_24h': 10}
    ])
    features = detector.extract_features(df)
    assert features.shape == (1, 7)

def test_training_and_detection():
    detector = BehavioralAnomalyDetector(contamination=0.1)
    historical = pd.DataFrame([
        {'volume': 1000 + i*10, 'price_change_pct': float(i % 10), 'trade_size_deviation': 1.0,
         'time_of_day_sin': 0.5, 'time_of_day_cos': 0.5, 'account_age_days': 365,
         'prior_trade_count_24h': 10 + i} for i in range(100)
    ])
    detector.train(historical)
    assert detector.is_trained == True
    recent = pd.DataFrame([
        {'volume': 5000, 'price_change_pct': 15.0, 'trade_size_deviation': 5.0,
         'time_of_day_sin': 0.5, 'time_of_day_cos': 0.5, 'account_age_days': 30,
         'prior_trade_count_24h': 100}
    ])
    results = detector.detect_anomalies(recent)
    assert 'is_anomaly' in results.columns
    assert 'anomaly_score' in results.columns

def test_anomaly_flagging():
    detector = BehavioralAnomalyDetector(contamination=0.05)
    normal = pd.DataFrame([
        {'volume': 1000, 'price_change_pct': 1.0, 'trade_size_deviation': 0.5,
         'time_of_day_sin': 0.5, 'time_of_day_cos': 0.5, 'account_age_days': 365,
         'prior_trade_count_24h': 5} for _ in range(90)
    ])
    anomalous = pd.DataFrame([
        {'volume': 10000, 'price_change_pct': 20.0, 'trade_size_deviation': 10.0,
         'time_of_day_sin': 0.5, 'time_of_day_cos': 0.5, 'account_age_days': 10,
         'prior_trade_count_24h': 200}
    ])
    all_data = pd.concat([normal, anomalous], ignore_index=True)
    detector.train(normal)
    results = detector.detect_anomalies(all_data)
    assert results.iloc[-1]['is_anomaly'] == True
