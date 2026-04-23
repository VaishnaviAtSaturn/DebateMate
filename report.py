def generate_report(scores_list: list, arguments_list: list, topic: str) -> dict:
    """
    Generate a comprehensive debate performance report.

    Args:
        scores_list: List of score dicts from scorer.score_argument()
        arguments_list: List of argument strings from the user
        topic: The debate topic string

    Returns:
        dict with overall_score, avg_clarity, avg_relevance, avg_logic,
        best_argument, worst_argument, ai_verdict, tip
    """
    if not scores_list or not arguments_list:
        return {
            "overall_score": 0.0,
            "avg_clarity": 0.0,
            "avg_relevance": 0.0,
            "avg_logic": 0.0,
            "best_argument": "No arguments submitted.",
            "worst_argument": "No arguments submitted.",
            "ai_verdict": "No debate data available.",
            "tip": "Start a debate to receive personalized feedback.",
        }

    # Compute averages across all rounds
    num_rounds = len(scores_list)

    avg_clarity = round(
        sum(s["clarity"] for s in scores_list) / num_rounds, 2
    )
    avg_relevance = round(
        sum(s["relevance"] for s in scores_list) / num_rounds, 2
    )
    avg_logic = round(
        sum(s["logic"] for s in scores_list) / num_rounds, 2
    )

    # Overall score: average of all round "overall" scores * 10 (to get /100)
    avg_overall = sum(s["overall"] for s in scores_list) / num_rounds
    overall_score = round(avg_overall * 10, 1)

    # Find best and worst arguments by their overall score
    paired = list(zip(scores_list, arguments_list))
    best_pair = max(paired, key=lambda x: x[0]["overall"])
    worst_pair = min(paired, key=lambda x: x[0]["overall"])
    best_argument = best_pair[1]
    worst_argument = worst_pair[1]

    # AI verdict based on overall score out of 100
    if overall_score > 75:
        ai_verdict = (
            "You dominated this debate. Your arguments were sharp, "
            "logical and well-structured."
        )
    elif overall_score >= 50:
        ai_verdict = (
            "A competitive debate. Some strong points but inconsistency "
            "cost you. Keep pushing."
        )
    else:
        ai_verdict = (
            "The AI won this round. Your arguments lacked evidence and "
            "structure. Practice more."
        )

    # Personalized tip based on weakest metric
    metrics = {
        "clarity": avg_clarity,
        "relevance": avg_relevance,
        "logic": avg_logic,
    }
    weakest_metric = min(metrics, key=metrics.get)

    if weakest_metric == "clarity":
        tip = (
            "Use shorter sentences. One point per argument. "
            "Cut everything unnecessary."
        )
    elif weakest_metric == "relevance":
        tip = (
            "Every sentence must connect directly to the topic. Stay focused."
        )
    else:
        tip = (
            "Use words like because, therefore, evidence shows. "
            "Back every claim with a reason."
        )

    return {
        "overall_score": overall_score,
        "avg_clarity": avg_clarity,
        "avg_relevance": avg_relevance,
        "avg_logic": avg_logic,
        "best_argument": best_argument,
        "worst_argument": worst_argument,
        "ai_verdict": ai_verdict,
        "tip": tip,
    }
