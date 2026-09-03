from src.calculations.portfolio import analyze_loan_portfolio
from src.repositories.loan_repository import get_loans_by_user


def get_dashboard_data(user_id: int) -> dict:
    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    loans = get_loans_by_user(user_id)

    active_loans = [
        loan
        for loan in loans
        if loan["status"] == "active"
    ]

    portfolio = analyze_loan_portfolio(
        active_loans
    )

    loan_summary = [
        {
            "id": loan["id"],
            "loan_name": loan["loan_name"],
            "loan_type": loan["loan_type"],
            "lender": loan["lender"],
            "original_principal": float(
                loan["original_principal"]
            ),
            "outstanding_principal": float(
                loan["outstanding_principal"]
            ),
            "interest_rate": float(
                loan["interest_rate"]
            ),
            "interest_type": loan["interest_type"],
            "emi": float(loan["emi"]),
            "original_tenure_months": loan[
                "original_tenure_months"
            ],
            "remaining_tenure_months": loan[
                "remaining_tenure_months"
            ],
            "loan_start_date": loan[
                "loan_start_date"
            ],
            "emi_due_day": loan["emi_due_day"],
            "processing_charges": float(
                loan["processing_charges"]
            ),
            "prepayment_rules": loan[
                "prepayment_rules"
            ],
            "prepayment_charges": float(
                loan["prepayment_charges"]
            ),
            "status": loan["status"],
        }
        for loan in active_loans
    ]

    return {
        "portfolio": portfolio,
        "loans": loan_summary,
    }
