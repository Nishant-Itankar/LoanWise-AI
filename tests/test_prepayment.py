import pytest

from src.calculations.prepayment import (
    analyze_prepayment,
)


def test_prepayment_reduces_principal():
    result = analyze_prepayment(
        outstanding_principal=400000,
        annual_interest_rate=10,
        remaining_tenure_months=48,
        prepayment_amount=100000,
    )

    assert result["principal_before"] == 400000.00
    assert result["principal_after"] == 300000.00


def test_prepayment_saves_interest():
    result = analyze_prepayment(
        outstanding_principal=400000,
        annual_interest_rate=10,
        remaining_tenure_months=48,
        prepayment_amount=100000,
    )

    assert result["interest_saved"] > 0


def test_prepayment_rejects_excess_amount():
    with pytest.raises(ValueError):
        analyze_prepayment(
            outstanding_principal=400000,
            annual_interest_rate=10,
            remaining_tenure_months=48,
            prepayment_amount=500000,
        )