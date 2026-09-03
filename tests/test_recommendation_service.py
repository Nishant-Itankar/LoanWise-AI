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


def test_recommendation_service_returns_result(monkeypatch):
    test_loans = [
        {
            "id": 1,
            "loan_name": "Test Personal Loan",
            "interest_rate": 12.0,
            "outstanding_principal": 100000.0,
            "remaining_tenure_months": 24,
            "status": "active",
        },
        {
            "id": 2,
            "loan_name": "Test Car Loan",
            "interest_rate": 8.0,
            "outstanding_principal": 200000.0,
            "remaining_tenure_months": 36,
            "status": "active",
        },
    ]

    monkeypatch.setattr(
        "src.services.recommendation_service.get_loans_by_user",
        lambda user_id: test_loans,
    )

    result = recommend_prepayment(
        user_id=67,
        prepayment_amount=20000,
    )

    assert result["strategy"] == (
        "maximum_interest_saving"
    )

    assert "recommended_loan" in result
    assert "candidates" in result
    assert result["recommended_loan"]["loan_id"] == 1


def test_recommendation_service_uses_active_loans(
    monkeypatch,
):
    test_loans = [
        {
            "id": 1,
            "loan_name": "Active Test Loan",
            "interest_rate": 10.0,
            "outstanding_principal": 100000.0,
            "remaining_tenure_months": 24,
            "status": "active",
        },
        {
            "id": 2,
            "loan_name": "Archived Test Loan",
            "interest_rate": 20.0,
            "outstanding_principal": 200000.0,
            "remaining_tenure_months": 36,
            "status": "archived",
        },
    ]

    monkeypatch.setattr(
        "src.services.recommendation_service.get_loans_by_user",
        lambda user_id: test_loans,
    )

    result = recommend_prepayment(
        user_id=67,
        prepayment_amount=20000,
    )

    assert len(result["candidates"]) == 1
    assert result["candidates"][0]["loan_id"] == 1