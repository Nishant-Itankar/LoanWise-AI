import pytest

from src.calculations.loan_analysis import (
    analyze_remaining_loan,
)


def test_remaining_loan_analysis():
    result = analyze_remaining_loan(
        outstanding_principal=400000,
        annual_interest_rate=10,
        remaining_tenure_months=48,
    )

    assert result["remaining_principal"] == 400000.00
    assert result["emi"] > 0
    assert result["remaining_interest"] > 0
    assert result["remaining_repayment"] > 400000


def test_zero_outstanding_loan():
    result = analyze_remaining_loan(
        outstanding_principal=0,
        annual_interest_rate=10,
        remaining_tenure_months=48,
    )

    assert result["emi"] == 0
    assert result["remaining_interest"] == 0
    assert result["remaining_repayment"] == 0


def test_invalid_remaining_loan():
    with pytest.raises(ValueError):
        analyze_remaining_loan(
            outstanding_principal=400000,
            annual_interest_rate=10,
            remaining_tenure_months=0,
        )