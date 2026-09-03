from src.services.recommendation_service import (
    recommend_prepayment,
)


def test_recommendation_service_rejects_invalid_user_id():
    try:
        recommend_prepayment(
            user_id=0,
            prepayment_amount=100000,
        )
        assert False
    except ValueError as error:
        assert str(error) == "User ID must be positive."


def test_recommendation_service_rejects_invalid_amount():
    try:
        recommend_prepayment(
            user_id=67,
            prepayment_amount=0,
        )
        assert False
    except ValueError as error:
        assert (
            str(error)
            == "Prepayment amount must be greater than zero."
        )


def test_recommendation_service_returns_result():
    result = recommend_prepayment(
        user_id=67,
        prepayment_amount=20000,
    )

    assert result["strategy"] == (
        "maximum_interest_saving"
    )

    assert "recommended_loan" in result
    assert "candidates" in result


def test_recommendation_service_uses_active_loans():
    result = recommend_prepayment(
        user_id=67,
        prepayment_amount=20000,
    )

    for candidate in result["candidates"]:
        assert candidate["loan_id"] > 0
        assert candidate["interest_saved"] >= 0