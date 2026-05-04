import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

class IntentAnalyzer:
    def __init__(self, model_name="ProsusAI/finbert"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=self.model,
            tokenizer=self.tokenizer,
            truncation=True
        )
        self.suspicious_keywords = [
            "提前知道", "内幕", "insider", "confidential", "not public",
            "friend told", "hearsay", "rumor", "提前交易", "private info"
        ]

    def analyze_text_intent(self, text: str) -> dict:
        sentiment = self.sentiment_pipeline(text[:512])[0]
        text_lower = text.lower()
        keyword_hits = sum(1 for kw in self.suspicious_keywords if kw in text_lower)
        suspicion_score = min(keyword_hits * 0.2 + (
            0.3 if sentiment['label'] == 'negative' else 0
        ), 1.0)
        return {
            'sentiment': sentiment['label'],
            'sentiment_score': sentiment['score'],
            'keyword_hits': keyword_hits,
            'suspicion_score': suspicion_score,
            'is_suspicious': suspicion_score > 0.4
        }

    def analyze_trade_intent(self, trade: dict, news_context: list) -> dict:
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
        combined_score = min(
            len(intent_signals) * 0.25 + news_score * 0.5,
            1.0
        )
        return {
            'intent_signals': intent_signals,
            'news_suspicion': news_score,
            'combined_intent_score': combined_score,
            'flagged_for_intent': combined_score > 0.5
        }
