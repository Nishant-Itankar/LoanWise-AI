from src.services.loan_analysis_service import (
    get_loan_analysis,
)


def test_loan_analysis_rejects_invalid_loan_id():
    try:
        get_loan_analysis(0)
        assert False
    except ValueError as error:
        assert str(error) == "Loan ID must be positive."


def test_loan_analysis_rejects_missing_loan():
    try:
        get_loan_analysis(999999)
        assert False
    except ValueError as error:
        assert str(error) == "Loan not found."


def test_loan_analysis_returns_current_loan_data(monkeypatch):
    loan = {
        "id": 1,
        "loan_name": "Test Loan",
        "interest_rate": 8.0,
        "interest_type": "fixed",
        "emi": 11500.0,
        "remaining_tenure_months": 47,
        "outstanding_principal": 391166.67,
    }

    monkeypatch.setattr(
        "src.services.loan_analysis_service.get_loan_by_id",
        lambda loan_id: loan,
    )

    result = get_loan_analysis(1)

    assert result["loan_id"] == 1
    assert result["interest_rate"] == 8.0
    assert result["interest_type"] == "fixed"
    assert result["emi"] == 11500.0
    assert result["remaining_tenure_months"] == 47
    assert result["outstanding_principal"] == 391166.67


def test_loan_analysis_returns_remaining_analysis(monkeypatch):
    loan = {
        "id": 1,
        "loan_name": "Test Loan",
        "interest_rate": 8.0,
        "interest_type": "fixed",
        "emi": 11500.0,
        "remaining_tenure_months": 47,
        "outstanding_principal": 391166.67,
    }

    monkeypatch.setattr(
        "src.services.loan_analysis_service.get_loan_by_id",
        lambda loan_id: loan,
    )

    result = get_loan_analysis(1)

    analysis = result["analysis"]

    assert analysis["remaining_principal"] == 391166.67
    assert analysis["emi"] == 9722.05
    assert analysis["remaining_interest"] == 65769.75
    assert analysis["remaining_repayment"] == 456936.42