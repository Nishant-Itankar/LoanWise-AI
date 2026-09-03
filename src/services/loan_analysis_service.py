from src.calculations.loan_analysis import (
    analyze_remaining_loan,
)
from src.repositories.loan_repository import (
    get_loan_by_id,
)


def get_loan_analysis(loan_id: int) -> dict:
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    loan = get_loan_by_id(loan_id)

    if not loan:
        raise ValueError(
            "Loan not found."
        )

    analysis = analyze_remaining_loan(
        outstanding_principal=float(
            loan["outstanding_principal"]
        ),
        annual_interest_rate=float(
            loan["interest_rate"]
        ),
        remaining_tenure_months=int(
            loan["remaining_tenure_months"]
        ),
    )

    return {
        "loan_id": loan_id,
        "loan_name": loan["loan_name"],
        "interest_rate": float(
            loan["interest_rate"]
        ),
        "interest_type": loan["interest_type"],
        "emi": float(loan["emi"]),
        "remaining_tenure_months": int(
            loan["remaining_tenure_months"]
        ),
        "outstanding_principal": float(
            loan["outstanding_principal"]
        ),
        "analysis": analysis,
    }
    