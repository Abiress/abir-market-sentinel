import pandas as pd
from datetime import timedelta
from typing import List, Dict

class TradeNewsCorrelator:
    def __init__(self, time_window_hours=24):
        self.time_window = timedelta(hours=time_window_hours)
    
    def correlate_trades_with_news(self, trades: pd.DataFrame, news: pd.DataFrame) -> pd.DataFrame:
        if news.empty:
            trades['related_news_count'] = 0
            trades['related_news'] = [[] for _ in range(len(trades))]
            return trades

        correlated = trades.copy()
        news_with_ts = news.copy()
        news_with_ts['_published_at_ts'] = pd.to_datetime(news_with_ts['published_at'])
        correlated['related_news'] = [[] for _ in range(len(trades))]
        correlated['related_news_count'] = 0

        for idx, trade in trades.iterrows():
            trade_time = pd.to_datetime(trade['timestamp'])
            window_start = trade_time - self.time_window
            window_end = trade_time + self.time_window

            relevant_news = news_with_ts[
                (news_with_ts['_published_at_ts'] >= window_start) &
                (news_with_ts['_published_at_ts'] <= window_end)
            ]

            trade_symbol = trade.get('symbol')
            if trade_symbol is not None and 'symbol' in relevant_news.columns:
                relevant_news = relevant_news[relevant_news['symbol'] == trade_symbol]

            correlated.at[idx, 'related_news'] = relevant_news.drop(columns=['_published_at_ts']).to_dict('records')
            correlated.at[idx, 'related_news_count'] = len(relevant_news)

        return correlated
    
    def correlate_with_agent_actions(self, trades: pd.DataFrame, agent_logs: pd.DataFrame) -> pd.DataFrame:
        if agent_logs.empty:
            trades['agent_actions_prior_1h'] = 0
            trades['info_requests'] = [[] for _ in range(len(trades))]
            return trades

        correlated = trades.copy()
        logs_with_ts = agent_logs.copy()
        logs_with_ts['_timestamp_ts'] = pd.to_datetime(logs_with_ts['timestamp'])
        correlated['agent_actions_prior_1h'] = 0
        correlated['info_requests'] = [[] for _ in range(len(trades))]

        for idx, trade in trades.iterrows():
            trade_time = pd.to_datetime(trade['timestamp'])
            one_hour_before = trade_time - timedelta(hours=1)

            recent_actions = logs_with_ts[
                (logs_with_ts['_timestamp_ts'] <= trade_time) &
                (logs_with_ts['_timestamp_ts'] >= one_hour_before)
            ]

            info_reqs = recent_actions[recent_actions.get('action_type') == 'info_request']

            correlated.at[idx, 'agent_actions_prior_1h'] = len(recent_actions)
            correlated.at[idx, 'info_requests'] = info_reqs.drop(columns=['_timestamp_ts']).to_dict('records')

        return correlated
