import re
from transformers import pipeline

# Logical connector words that indicate strong reasoning
LOGIC_CONNECTORS = [
    "because", "therefore", "however", "evidence",
    "research", "study", "data", "proves", "shows",
    "according", "furthermore", "hence", "thus",
    "consequently", "as a result", "for example",
]

# Load HuggingFace sentiment model once at module level
_sentiment_pipeline = None

def _load_sentiment_pipeline():
    """Load the sentiment analysis pipeline, with fallback on failure."""
    global _sentiment_pipeline
    if _sentiment_pipeline is not None:
        return _sentiment_pipeline
    try:
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        )
        return _sentiment_pipeline
    except Exception:
        return None


def _compute_clarity_score(text: str) -> float:
    """
    Score clarity based on average words per sentence.
    Under 15 words avg  =>  9-10
    15-20 words avg     =>  7-8
    20-25 words avg     =>  5-6
    25-30 words avg     =>  4-5
    Over 30 words avg   =>  2-4
    """
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    if not sentences:
        return 5.0

    word_counts = [len(s.split()) for s in sentences]
    avg_words = sum(word_counts) / len(word_counts)

    if avg_words <= 10:
        score = 10.0
    elif avg_words <= 15:
        score = 9.0 - ((avg_words - 10) / 5) * 1.0  # 9-10 range
    elif avg_words <= 20:
        score = 7.0 + ((20 - avg_words) / 5) * 1.0  # 7-8 range
    elif avg_words <= 25:
        score = 5.0 + ((25 - avg_words) / 5) * 2.0  # 5-7 range
    elif avg_words <= 30:
        score = 4.0 + ((30 - avg_words) / 5) * 1.0  # 4-5 range
    else:
        score = max(2.0, 4.0 - ((avg_words - 30) / 10) * 2.0)

    return round(min(10.0, max(0.0, score)), 2)


def _compute_relevance_score(text: str) -> float:
    """
    Use HuggingFace sentiment confidence score mapped to 0-10.
    Higher confidence in any sentiment = more decisive = more relevant.
    Falls back to 5.0 if model unavailable.
    """
    pipe = _load_sentiment_pipeline()
    if pipe is None:
        return 5.0

    try:
        results = pipe(text[:512])  # Truncate to model max length
        confidence = results[0]["score"]  # 0.0 to 1.0
        # Map confidence to 0-10: higher confidence = higher relevance score
        score = confidence * 10.0
        return round(min(10.0, max(0.0, score)), 2)
    except Exception:
        return 5.0


def _compute_logic_score(text: str) -> float:
    """
    Score logic by counting logical connector words.
    0 connectors = 2/10
    1 connector  = 5/10
    2 connectors = 7/10
    3+ connectors = 9/10
    """
    text_lower = text.lower()
    connector_count = 0

    for connector in LOGIC_CONNECTORS:
        if connector in text_lower:
            connector_count += 1

    if connector_count == 0:
        return 2.0
    elif connector_count == 1:
        return 5.0
    elif connector_count == 2:
        return 7.0
    else:
        return 9.0


def score_argument(text: str) -> dict:
    """
    Score a debate argument across three dimensions.

    Returns:
        dict with keys: clarity, relevance, logic, overall (all 0-10 floats)
    """
    if not text or not text.strip():
        return {
            "clarity": 5.0,
            "relevance": 5.0,
            "logic": 5.0,
            "overall": 5.0,
        }

    try:
        clarity = _compute_clarity_score(text)
        relevance = _compute_relevance_score(text)
        logic = _compute_logic_score(text)
        overall = round((clarity + relevance + logic) / 3, 2)

        return {
            "clarity": clarity,
            "relevance": relevance,
            "logic": logic,
            "overall": overall,
        }

    except Exception:
        # Fallback: return neutral scores if anything goes wrong
        return {
            "clarity": 5.0,
            "relevance": 5.0,
            "logic": 5.0,
            "overall": 5.0,
        }
