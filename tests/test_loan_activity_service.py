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

def test_activity_summary_for_loan_with_payment():
    result = get_loan_activity_summary(130)

    assert result["loan_id"] == 130
    assert result["payment_count"] >= 1
    assert result["total_emi_paid"] >= 11500.00
    assert result["total_principal_paid"] >= 8833.33
    assert result["total_interest_paid"] >= 2666.67
    assert result["total_extra_payments"] >= 0.00
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