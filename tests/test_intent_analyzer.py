import pytest
from src.behavioral_ai.intent_analyzer import IntentAnalyzer

def test_intent_analyzer_init():
    analyzer = IntentAnalyzer()
    assert analyzer.suspicious_keywords is not None
    assert len(analyzer.suspicious_keywords) > 0

def test_text_intent_analysis():
    analyzer = IntentAnalyzer()
    result = analyzer.analyze_text_intent("Market is doing great today")
    assert 'suspicion_score' in result
    assert 'is_suspicious' in result

def test_suspicious_text_intent():
    analyzer = IntentAnalyzer()
    result = analyzer.analyze_text_intent("I have insider information about the merger")
    assert result['is_suspicious'] == True
    assert result['keyword_hits'] > 0

def test_trade_intent_analysis():
    analyzer = IntentAnalyzer()
    trade = {
        'trade_size_deviation': 4.0,
        'timing_precision_hours': 1,
        'prior_knowledge_indicator': True
    }
    news_context = [{'headline': 'Company announces surprise earnings'}]
    result = analyzer.analyze_trade_intent(trade, news_context)
    assert 'combined_intent_score' in result
    assert 'flagged_for_intent' in result

def test_trade_flagging():
    analyzer = IntentAnalyzer()
    trade = {
        'trade_size_deviation': 5.0,
        'timing_precision_hours': 0,
        'prior_knowledge_indicator': True
    }
    news_context = [{'headline': '内幕交易被查处'}]
    result = analyzer.analyze_trade_intent(trade, news_context)
    assert result['flagged_for_intent'] == True
    assert result['combined_intent_score'] > 0.5
