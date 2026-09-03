from src.services.dashboard_service import (
    get_dashboard_data,
)
from src.services.loan_activity_service import (
    get_loan_activity_summary,
)
from src.services.loan_analysis_service import (
    get_loan_analysis,
)
from src.calculations.strategies import (
    rank_loans_by_interest_rate,
    rank_loans_by_outstanding,
    rank_loans_by_emi,
)


def get_ai_financial_context(user_id: int) -> dict:
    """
    Build a structured financial context for the AI layer.

    This function gathers verified financial data from the
    existing LoanWise calculation and service layers.

    The AI layer should use this context rather than querying
    the database or calculating financial figures itself.
    """

    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    dashboard = get_dashboard_data(user_id)

    loans = dashboard["loans"]
    portfolio = dashboard["portfolio"]

    if not loans:
        return {
            "user_id": user_id,
            "portfolio": portfolio,
            "loans": [],
            "strategies": {
                "highest_interest": [],
                "largest_outstanding": [],
                "highest_emi": [],
            },
        }

    loan_context = []

    for loan in loans:
        loan_id = loan["id"]

        analysis = get_loan_analysis(
            loan_id
        )

        activity = get_loan_activity_summary(
            loan_id
        )

        loan_context.append(
            {
                "loan_id": loan_id,
                "loan_name": loan["loan_name"],
                "loan_type": loan["loan_type"],
                "lender": loan["lender"],
                "status": loan["status"],
                "original_principal": float(
                    loan["original_principal"]
                ),
                "outstanding_principal": float(
                    loan["outstanding_principal"]
                ),
                "interest_rate": float(
                    loan["interest_rate"]
                ),
                "interest_type": loan[
                    "interest_type"
                ],
                "emi": float(
                    loan["emi"]
                ),
                "original_tenure_months": int(
                    loan["original_tenure_months"]
                ),
                "remaining_tenure_months": int(
                    loan[
                        "remaining_tenure_months"
                    ]
                ),
                "loan_start_date": loan[
                    "loan_start_date"
                ],
                "emi_due_day": loan[
                    "emi_due_day"
                ],
                "prepayment_rules": loan[
                    "prepayment_rules"
                ],
                "prepayment_charges": float(
                    loan[
                        "prepayment_charges"
                    ]
                ),
                "analysis": {
                    "calculated_emi": float(
                        analysis["analysis"]["emi"]
                    ),
                    "remaining_interest": float(
                        analysis[
                            "analysis"
                        ][
                            "remaining_interest"
                        ]
                    ),
                    "remaining_repayment": float(
                        analysis[
                            "analysis"
                        ][
                            "remaining_repayment"
                        ]
                    ),
                },
                "activity": {
                    "payment_count": activity[
                        "payment_count"
                    ],
                    "total_emi_paid": float(
                        activity[
                            "total_emi_paid"
                        ]
                    ),
                    "total_principal_paid": float(
                        activity[
                            "total_principal_paid"
                        ]
                    ),
                    "total_interest_paid": float(
                        activity[
                            "total_interest_paid"
                        ]
                    ),
                    "total_extra_payments": float(
                        activity[
                            "total_extra_payments"
                        ]
                    ),
                    "latest_outstanding_balance": float(
                        activity[
                            "latest_outstanding_balance"
                        ]
                    ),
                },
            }
        )

    highest_interest = rank_loans_by_interest_rate(
        loans
    )

    largest_outstanding = rank_loans_by_outstanding(
        loans
    )

    highest_emi = rank_loans_by_emi(
        loans
    )

    strategies = {
        "highest_interest": [
            {
                "loan_id": loan["id"],
                "loan_name": loan["loan_name"],
                "interest_rate": float(
                    loan["interest_rate"]
                ),
                "outstanding_principal": float(
                    loan[
                        "outstanding_principal"
                    ]
                ),
            }
            for loan in highest_interest
        ],
        "largest_outstanding": [
            {
                "loan_id": loan["id"],
                "loan_name": loan["loan_name"],
                "outstanding_principal": float(
                    loan[
                        "outstanding_principal"
                    ]
                ),
                "interest_rate": float(
                    loan["interest_rate"]
                ),
            }
            for loan in largest_outstanding
        ],
        "highest_emi": [
            {
                "loan_id": loan["id"],
                "loan_name": loan["loan_name"],
                "emi": float(
                    loan["emi"]
                ),
                "outstanding_principal": float(
                    loan[
                        "outstanding_principal"
                    ]
                ),
            }
            for loan in highest_emi
        ],
    }

    return {
        "user_id": user_id,
        "portfolio": portfolio,
        "loans": loan_context,
        "strategies": strategies,
    }