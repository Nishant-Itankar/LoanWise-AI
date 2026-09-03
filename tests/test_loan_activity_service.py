from src.services.loan_activity_service import (
    get_loan_activity,
    get_loan_activity_summary,
)


def test_activity_rejects_invalid_loan_id():
    try:
        get_loan_activity(0)
        assert False
    except ValueError as error:
        assert str(error) == "Loan ID must be positive."


def test_activity_rejects_missing_loan():
    try:
        get_loan_activity(999999)
        assert False
    except ValueError as error:
        assert str(error) == "Loan not found."


def test_activity_summary_for_loan_with_payment(monkeypatch):
    loan = {
        "id": 1,
        "outstanding_principal": 391166.67,
    }

    payment = {
        "id": 1,
        "loan_id": 1,
        "emi_amount": 11500.00,
        "principal_component": 8833.33,
        "interest_component": 2666.67,
        "outstanding_balance": 391166.67,
        "extra_payment": 0.00,
    }

    monkeypatch.setattr(
        "src.services.loan_activity_service.get_loan_by_id",
        lambda loan_id: loan,
    )

    monkeypatch.setattr(
        "src.services.loan_activity_service.get_payments_by_loan",
        lambda loan_id: [payment],
    )

    result = get_loan_activity_summary(1)

    assert result["loan_id"] == 1
    assert result["payment_count"] == 1
    assert result["total_emi_paid"] == 11500.00
    assert result["total_principal_paid"] == 8833.33
    assert result["total_interest_paid"] == 2666.67
    assert result["total_extra_payments"] == 0.00
    assert result["latest_outstanding_balance"] == 391166.67


def test_activity_summary_rejects_invalid_loan_id():
    try:
        get_loan_activity_summary(0)
        assert False
    except ValueError as error:
        assert str(error) == "Loan ID must be positive."


def test_activity_summary_rejects_missing_loan():
    try:
        get_loan_activity_summary(999999)
        assert False
    except ValueError as error:
        assert str(error) == "Loan not found."