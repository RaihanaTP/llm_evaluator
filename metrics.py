# metrics.py
# This file contains the functions that SCORE each AI response.
# Think of this as your grading rubric.

# Pricing per 1000 tokens (as of early 2025, approximate)
MODEL_COSTS = {
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
}

def calculate_relevance_score(response: str, ideal_answer: str, question: str) -> float:
    """
    Scores how relevant the response is to the question.
    We do this by checking keyword overlap between the response and ideal answer.
    Returns a score between 0 and 1.
    
    Note: In a production system, you'd use embeddings for this.
    For this project, keyword overlap is simple and explainable.
    """
    if not response or len(response.strip()) == 0:
        return 0.0
    
    # Extract meaningful keywords from ideal answer (ignore short/common words)
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "it", "its",
                  "in", "on", "at", "to", "for", "of", "and", "or", "but",
                  "that", "this", "with", "by", "from", "as", "be", "can",
                  "all", "not", "have", "has", "had", "do", "does", "did"}
    
    ideal_words = set(
        word.lower().strip(".,!?()") 
        for word in ideal_answer.split() 
        if word.lower() not in stop_words and len(word) > 3
    )
    
    response_words = set(
        word.lower().strip(".,!?()") 
        for word in response.split() 
        if word.lower() not in stop_words and len(word) > 3
    )
    
    if not ideal_words:
        return 0.5
    
    # What fraction of ideal keywords appear in the response?
    overlap = len(ideal_words.intersection(response_words))
    score = min(overlap / len(ideal_words), 1.0)
    
    return round(score, 3)


def calculate_hallucination_score(response: str, ideal_answer: str) -> float:
    """
    Estimates hallucination risk — how much is the response saying things
    not grounded in the ideal answer?
    
    Lower score = more hallucination risk.
    Returns a score between 0 and 1 (1 = low hallucination risk).
    """
    if not response or len(response.strip()) == 0:
        return 0.0
    
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "it", "its",
                  "in", "on", "at", "to", "for", "of", "and", "or", "but",
                  "that", "this", "with", "by", "from", "as", "be", "can",
                  "all", "not", "have", "has", "had", "do", "does", "did"}
    
    ideal_words = set(
        word.lower().strip(".,!?()") 
        for word in ideal_answer.split() 
        if word.lower() not in stop_words and len(word) > 3
    )
    
    response_words = [
        word.lower().strip(".,!?()") 
        for word in response.split() 
        if word.lower() not in stop_words and len(word) > 3
    ]
    
    if not response_words:
        return 0.5
    
    # What fraction of response words are grounded in the ideal answer?
    grounded = sum(1 for word in response_words if word in ideal_words)
    score = grounded / len(response_words)
    
    # Scale it so it's not too harsh (response can use synonyms etc)
    score = min(score * 2.5, 1.0)
    
    return round(score, 3)


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculates the cost of an API call in USD.
    """
    if model not in MODEL_COSTS:
        return 0.0
    
    costs = MODEL_COSTS[model]
    input_cost = (input_tokens / 1000) * costs["input"]
    output_cost = (output_tokens / 1000) * costs["output"]
    
    return round(input_cost + output_cost, 6)


def calculate_response_length_score(response: str) -> dict:
    """
    Returns word count and a length category.
    """
    words = len(response.split())
    if words < 20:
        category = "Too Short"
    elif words < 80:
        category = "Concise"
    elif words < 150:
        category = "Detailed"
    else:
        category = "Very Long"
    
    return {"word_count": words, "length_category": category}


def compute_all_metrics(response: str, ideal_answer: str, question: str,
                         model: str, input_tokens: int, output_tokens: int,
                         latency_seconds: float) -> dict:
    """
    Master function — runs all metrics and returns a complete score card.
    """
    relevance = calculate_relevance_score(response, ideal_answer, question)
    hallucination = calculate_hallucination_score(response, ideal_answer)
    cost = calculate_cost(model, input_tokens, output_tokens)
    length_info = calculate_response_length_score(response)
    
    # Overall quality score: weighted average of relevance and hallucination
    overall_quality = round((relevance * 0.6) + (hallucination * 0.4), 3)
    
    return {
        "relevance_score": relevance,
        "hallucination_score": hallucination,
        "overall_quality": overall_quality,
        "cost_usd": cost,
        "latency_seconds": round(latency_seconds, 2),
        "word_count": length_info["word_count"],
        "length_category": length_info["length_category"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }
