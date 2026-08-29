from src.calculations.strategies import (
    rank_loans_by_emi,
    rank_loans_by_interest_rate,
    rank_loans_by_outstanding,
)


LOANS = [
    {
        "loan_name": "Home Loan",
        "interest_rate": 8.5,
        "outstanding_principal": 3000000,
        "emi": 28000,
    },
    {
        "loan_name": "Car Loan",
        "interest_rate": 10.5,
        "outstanding_principal": 500000,
        "emi": 15000,
    },
    {
        "loan_name": "Personal Loan",
        "interest_rate": 14,
        "outstanding_principal": 200000,
        "emi": 10000,
    },
]


def test_rank_by_interest_rate():
    result = rank_loans_by_interest_rate(LOANS)

    assert result[0]["loan_name"] == "Personal Loan"
    assert result[-1]["loan_name"] == "Home Loan"


def test_rank_by_outstanding():
    result = rank_loans_by_outstanding(LOANS)

    assert result[0]["loan_name"] == "Home Loan"
    assert result[-1]["loan_name"] == "Personal Loan"


def test_rank_by_emi():
    result = rank_loans_by_emi(LOANS)

    assert result[0]["loan_name"] == "Home Loan"
    assert result[-1]["loan_name"] == "Personal Loan"