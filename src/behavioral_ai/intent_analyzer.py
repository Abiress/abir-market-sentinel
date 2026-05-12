import numpy as np
from typing import List, Dict

class IntentAnalyzer:
    def __init__(self, model_name="ProsusAI/finbert"):
        self.model_name = model_name
        self.suspicious_keywords = [
            "insider", "confidential", "not public",
            "friend told", "hearsay", "rumor",
            "提前知道", "内幕", "private info", "提前交易"
        ]
        self.positive_words = ["good", "great", "excellent", "up", "gain", "profit"]
        self.negative_words = ["bad", "crash", "down", "loss", "sell", "panic"]
        self._finbert = None
        self._finbert_checked = False

    def _load_finbert(self):
        if self._finbert_checked:
            return self._finbert
        self._finbert_checked = True
        try:
            from transformers import pipeline
            self._finbert = pipeline("sentiment-analysis", model=self.model_name)
        except Exception:
            self._finbert = None
        return self._finbert

    def _analyze_sentiment(self, text: str):
        finbert = self._load_finbert()
        if finbert is not None:
            try:
                result = finbert(text[:512])[0]
                label = str(result.get('label', 'neutral')).lower()
                score = float(result.get('score', 0.5))
                if 'neg' in label:
                    return 'negative', score, 'finbert'
                if 'pos' in label:
                    return 'positive', score, 'finbert'
                return 'neutral', score, 'finbert'
            except Exception:
                pass

        text_lower = text.lower()
        pos_count = sum(1 for w in self.positive_words if w in text_lower)
        neg_count = sum(1 for w in self.negative_words if w in text_lower)

        if neg_count > pos_count:
            return 'negative', 0.8, 'heuristic'
        if pos_count > neg_count:
            return 'positive', 0.8, 'heuristic'
        return 'neutral', 0.5, 'heuristic'
    
    def analyze_text_intent(self, text: str) -> Dict:
        text_lower = text.lower()
        keyword_hits = sum(1 for kw in self.suspicious_keywords if kw in text_lower)
        sentiment, sentiment_score, sentiment_engine = self._analyze_sentiment(text)
        
        suspicion_score = min(keyword_hits * 0.5 + (0.2 if sentiment == 'negative' else 0), 1.0)
        
        return {
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'sentiment_engine': sentiment_engine,
            'keyword_hits': keyword_hits,
            'suspicion_score': suspicion_score,
            'is_suspicious': suspicion_score > 0.4
        }
    
    def analyze_trade_intent(self, trade: Dict, news_context: List[Dict]) -> Dict:
        intent_signals = []
        
        if trade.get('trade_size_deviation', 0) > 3.0:
            intent_signals.append('unusual_size')
        if trade.get('timing_precision_hours', 99) < 2:
            intent_signals.append('precise_timing')
        if trade.get('prior_knowledge_indicator', False):
            intent_signals.append('prior_knowledge')
        
        news_score = 0.0
        for news in news_context:
            result = self.analyze_text_intent(news.get('headline', ''))
            if result['is_suspicious']:
                news_score = max(news_score, result['suspicion_score'])
        
        combined_score = min(len(intent_signals) * 0.25 + news_score * 0.5, 1.0)
        
        return {
            'intent_signals': intent_signals,
            'news_suspicion': news_score,
            'combined_intent_score': combined_score,
            'flagged_for_intent': combined_score > 0.5
        }
