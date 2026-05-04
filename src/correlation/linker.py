import pandas as pd
from datetime import timedelta
from typing import List, Dict

class TradeNewsCorrelator:
    def __init__(self, time_window_hours=24):
        self.time_window = timedelta(hours=time_window_hours)

    def correlate_trades_with_news(self, trades: pd.DataFrame, news: pd.DataFrame) -> pd.DataFrame:
        correlated = []
        for _, trade in trades.iterrows():
            trade_time = pd.to_datetime(trade['timestamp'])
            window_start = trade_time - self.time_window
            window_end = trade_time + self.time_window
            relevant_news = news[
                (pd.to_datetime(news['published_at']) >= window_start) &
                (pd.to_datetime(news['published_at']) <= window_end)
            ]
            correlated.append({
                **trade.to_dict(),
                'related_news_count': len(relevant_news),
                'related_news': relevant_news.to_dict('records') if not relevant_news.empty else []
            })
        return pd.DataFrame(correlated)

    def correlate_with_agent_actions(self, trades: pd.DataFrame, agent_logs: pd.DataFrame) -> pd.DataFrame:
        correlated = []
        for _, trade in trades.iterrows():
            trade_time = pd.to_datetime(trade['timestamp'])
            recent_actions = agent_logs[
                (pd.to_datetime(agent_logs['timestamp']) <= trade_time) &
                (pd.to_datetime(agent_logs['timestamp']) >= trade_time - timedelta(hours=1))
            ]
            pre_trade_queries = recent_actions[
                recent_actions.get('action_type') == 'info_request'
            ].sort_values('timestamp', ascending=False)
            correlated.append({
                **trade.to_dict(),
                'agent_actions_prior_1h': len(recent_actions),
                'info_requests': pre_trade_queries.to_dict('records') if not pre_trade_queries.empty else []
            })
        return pd.DataFrame(correlated)
