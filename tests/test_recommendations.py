from src.calculations.recommendations import (
    recommend_prepayment_target,
)


def test_recommendation_selects_best_interest_saving():
    loans = [
        {
            "id": 1,
            "loan_name": "Home Loan",
            "interest_rate": 8.5,
            "outstanding_principal": 3000000,
            "remaining_tenure_months": 120,
        },
        {
            "id": 2,
            "loan_name": "Personal Loan",
            "interest_rate": 14,
            "outstanding_principal": 200000,
            "remaining_tenure_months": 48,
        },
    ]

    result = recommend_prepayment_target(
        loans=loans,
        prepayment_amount=100000,
    )

    assert result["strategy"] == "maximum_interest_saving"

    assert result["recommended_loan"]["interest_saved"] == max(
        candidate["interest_saved"]
        for candidate in result["candidates"]
    )

def test_recommendation_returns_candidates():
    loans = [
        {
            "id": 1,
            "loan_name": "Loan A",
            "interest_rate": 10,
            "outstanding_principal": 500000,
            "remaining_tenure_months": 60,
        },
        {
            "id": 2,
            "loan_name": "Loan B",
            "interest_rate": 12,
            "outstanding_principal": 300000,
            "remaining_tenure_months": 48,
        },
    ]

    result = recommend_prepayment_target(
        loans=loans,
        prepayment_amount=100000,
    )

    assert len(result["candidates"]) == 2
    assert result["recommended_loan"] == (
        result["candidates"][0]
    )