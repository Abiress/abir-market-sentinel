import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict

class MarketDataIngestor:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.example.com"
    
    def fetch_trades(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        trades = []
        current = start
        while current < end:
            trades.append({
                'trade_id': f"T{datetime.now().timestamp():.0f}",
                'symbol': symbol,
                'timestamp': current.isoformat(),
                'price': 100.0 + (hash(str(current)) % 50),
                'volume': 1000 + (hash(str(current)) % 5000),
                'trade_size_deviation': (hash(str(current)) % 100) / 10.0,
                'account_age_days': 365,
                'prior_trade_count_24h': hash(str(current)) % 50,
            })
            current += timedelta(hours=1)
        return pd.DataFrame(trades)
    
    def fetch_news(self, symbols: List[str], hours=24) -> pd.DataFrame:
        news = []
        for symbol in symbols:
            news.append({
                'symbol': symbol,
                'headline': f"Market update for {symbol}",
                'published_at': datetime.utcnow().isoformat(),
                'source': 'mock_source'
            })
        return pd.DataFrame(news)
    
    def fetch_agent_logs(self, agent_id: str, hours=24) -> pd.DataFrame:
        logs = []
        for i in range(10):
            logs.append({
                'agent_id': agent_id,
                'timestamp': (datetime.utcnow() - timedelta(hours=i)).isoformat(),
                'action_type': 'info_request' if i % 2 == 0 else 'trade_execution',
                'details': f"Action {i}"
            })
        return pd.DataFrame(logs)
