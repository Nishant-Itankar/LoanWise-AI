from src.calculations.ai_decisions import (
    analyze_financial_decisions,
)


def make_loan(
    loan_id=1,
    loan_name="Test Loan",
    interest_rate=10,
    outstanding_principal=100000,
    emi=5000,
    remaining_interest=20000,
    remaining_repayment=120000,
):
    return {
        "loan_id": loan_id,
        "loan_name": loan_name,
        "interest_rate": interest_rate,
        "outstanding_principal": outstanding_principal,
        "emi": emi,
        "analysis": {
            "remaining_interest": remaining_interest,
            "remaining_repayment": remaining_repayment,
        },
    }


def make_context(loans):
    return {
        "user_id": 1,
        "portfolio": {
            "loan_count": len(loans),
            "total_outstanding_principal": sum(
                loan["outstanding_principal"]
                for loan in loans
            ),
            "total_emi": sum(
                loan["emi"]
                for loan in loans
            ),
        },
        "loans": loans,
    }


def test_empty_context():
    result = analyze_financial_decisions(
        {
            "portfolio": {},
            "loans": [],
        }
    )

    assert result["has_loans"] is False
    assert result["loan_count"] == 0
    assert result["priority_loan"] is None


def test_single_loan():
    loan = make_loan()

    result = analyze_financial_decisions(
        make_context([loan])
    )

    assert result["has_loans"] is True
    assert result["loan_count"] == 1

    assert (
        result["priority_loan"]["loan_id"]
        == 1
    )

    assert (
        result["highest_interest_loan"]["loan_id"]
        == 1
    )


def test_highest_interest_loan_is_priority():
    loans = [
        make_loan(
            loan_id=1,
            loan_name="Low Rate",
            interest_rate=8,
            outstanding_principal=300000,
        ),
        make_loan(
            loan_id=2,
            loan_name="High Rate",
            interest_rate=14,
            outstanding_principal=100000,
        ),
    ]

    result = analyze_financial_decisions(
        make_context(loans)
    )

    assert (
        result["highest_interest_loan"]["loan_id"]
        == 2
    )

    assert (
        result["priority_loan"]["loan_id"]
        == 2
    )

    assert (
        result["priority_loan"]["reason"]
        == "Highest interest rate"
    )


def test_larger_balance_breaks_interest_rate_tie():
    loans = [
        make_loan(
            loan_id=1,
            loan_name="Smaller Loan",
            interest_rate=10,
            outstanding_principal=100000,
        ),
        make_loan(
            loan_id=2,
            loan_name="Larger Loan",
            interest_rate=10,
            outstanding_principal=500000,
        ),
    ]

    result = analyze_financial_decisions(
        make_context(loans)
    )

    assert (
        result["priority_loan"]["loan_id"]
        == 2
    )


def test_highest_emi_loan():
    loans = [
        make_loan(
            loan_id=1,
            emi=5000,
        ),
        make_loan(
            loan_id=2,
            emi=15000,
        ),
    ]

    result = analyze_financial_decisions(
        make_context(loans)
    )

    assert (
        result["highest_emi_loan"]["loan_id"]
        == 2
    )

    assert (
        result["highest_emi_loan"]["emi"]
        == 15000
    )


def test_largest_outstanding_loan():
    loans = [
        make_loan(
            loan_id=1,
            outstanding_principal=100000,
        ),
        make_loan(
            loan_id=2,
            outstanding_principal=450000,
        ),
    ]

    result = analyze_financial_decisions(
        make_context(loans)
    )

    assert (
        result["largest_outstanding_loan"][
            "loan_id"
        ]
        == 2
    )


def test_total_remaining_interest():
    loans = [
        make_loan(
            loan_id=1,
            remaining_interest=25000,
        ),
        make_loan(
            loan_id=2,
            remaining_interest=35000,
        ),
    ]

    result = analyze_financial_decisions(
        make_context(loans)
    )

    assert (
        result["total_remaining_interest"]
        == 60000
    )


def test_total_remaining_repayment():
    loans = [
        make_loan(
            loan_id=1,
            remaining_repayment=125000,
        ),
        make_loan(
            loan_id=2,
            remaining_repayment=225000,
        ),
    ]

    result = analyze_financial_decisions(
        make_context(loans)
    )

    assert (
        result["total_remaining_repayment"]
        == 350000
    )


def test_invalid_context():
    try:
        analyze_financial_decisions(None)
        assert False
    except ValueError as error:
        assert (
            str(error)
            == "Financial context must be a dictionary."
        )