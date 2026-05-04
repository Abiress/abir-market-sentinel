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
        correlated['related_news'] = [[] for _ in range(len(trades))]
        correlated['related_news_count'] = 0
        
        for idx, trade in trades.iterrows():
            trade_time = pd.to_datetime(trade['timestamp'])
            window_start = trade_time - self.time_window
            window_end = trade_time + self.time_window
            
            relevant_news = news[
                (pd.to_datetime(news['published_at']) >= window_start) &
                (pd.to_datetime(news['published_at']) <= window_end)
            ]
            
            correlated.at[idx, 'related_news'] = relevant_news.to_dict('records')
            correlated.at[idx, 'related_news_count'] = len(relevant_news)
        
        return correlated
    
    def correlate_with_agent_actions(self, trades: pd.DataFrame, agent_logs: pd.DataFrame) -> pd.DataFrame:
        if agent_logs.empty:
            trades['agent_actions_prior_1h'] = 0
            trades['info_requests'] = [[] for _ in range(len(trades))]
            return trades
        
        correlated = trades.copy()
        correlated['agent_actions_prior_1h'] = 0
        correlated['info_requests'] = [[] for _ in range(len(trades))]
        
        for idx, trade in trades.iterrows():
            trade_time = pd.to_datetime(trade['timestamp'])
            one_hour_before = trade_time - timedelta(hours=1)
            
            recent_actions = agent_logs[
                (pd.to_datetime(agent_logs['timestamp']) <= trade_time) &
                (pd.to_datetime(agent_logs['timestamp']) >= one_hour_before)
            ]
            
            info_reqs = recent_actions[recent_actions.get('action_type') == 'info_request']
            
            correlated.at[idx, 'agent_actions_prior_1h'] = len(recent_actions)
            correlated.at[idx, 'info_requests'] = info_reqs.to_dict('records')
        
        return correlated
