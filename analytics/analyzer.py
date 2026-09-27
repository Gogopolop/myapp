# ринемает данные и считает
from analytics.score import calc_score
from analytics.recommendations import generate_recommendations


def analyze_repo(data: dict) -> dict:
    score_result = calc_score(data)
    recommendations = generate_recommendations(score_result["categories"], data)

    return {
        "repo": data.get("repo", "unknown"),
        "score": score_result["score"],
        "categories": score_result["categories"],
        "recommendations": recommendations,
    }