from src.calculations.portfolio import (
    analyze_loan_portfolio,
)


def test_empty_portfolio():
    result = analyze_loan_portfolio([])

    assert result["loan_count"] == 0
    assert result["total_outstanding_principal"] == 0
    assert result["total_emi"] == 0


def test_portfolio_totals():
    loans = [
        {
            "original_principal": 1000000,
            "outstanding_principal": 800000,
            "interest_rate": 10,
            "emi": 25000,
        },
        {
            "original_principal": 500000,
            "outstanding_principal": 300000,
            "interest_rate": 8,
            "emi": 10000,
        },
    ]

    result = analyze_loan_portfolio(loans)

    assert result["loan_count"] == 2
    assert result["total_original_principal"] == 1500000
    assert result["total_outstanding_principal"] == 1100000
    assert result["total_emi"] == 35000


def test_weighted_interest_rate():
    loans = [
        {
            "original_principal": 1000000,
            "outstanding_principal": 800000,
            "interest_rate": 10,
            "emi": 25000,
        },
        {
            "original_principal": 500000,
            "outstanding_principal": 300000,
            "interest_rate": 8,
            "emi": 10000,
        },
    ]

    result = analyze_loan_portfolio(loans)

    expected_rate = (
        (800000 * 10) + (300000 * 8)
    ) / 1100000

    assert round(
        result["weighted_interest_rate"],
        2,
    ) == round(expected_rate, 2)