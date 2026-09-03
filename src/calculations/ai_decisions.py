from decimal import Decimal, ROUND_HALF_UP


def _money(value: float) -> float:
    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )


def analyze_financial_decisions(
    financial_context: dict,
) -> dict:
    """
    Convert the verified AI financial context into
    deterministic financial decision signals.

    This function does not use an LLM.
    It only analyzes data produced by the existing
    LoanWise financial services.
    """

    if not isinstance(financial_context, dict):
        raise ValueError(
            "Financial context must be a dictionary."
        )

    loans = financial_context.get("loans", [])
    portfolio = financial_context.get(
        "portfolio",
        {},
    )

    if not loans:
        return {
            "has_loans": False,
            "loan_count": 0,
            "total_outstanding_principal": 0.0,
            "total_emi": 0.0,
            "total_remaining_interest": 0.0,
            "total_remaining_repayment": 0.0,
            "highest_interest_loan": None,
            "highest_emi_loan": None,
            "largest_outstanding_loan": None,
            "priority_loan": None,
        }

    total_remaining_interest = sum(
        float(
            loan["analysis"]["remaining_interest"]
        )
        for loan in loans
    )

    total_remaining_repayment = sum(
        float(
            loan["analysis"]["remaining_repayment"]
        )
        for loan in loans
    )

    highest_interest_loan = max(
        loans,
        key=lambda loan: float(
            loan["interest_rate"]
        ),
    )

    highest_emi_loan = max(
        loans,
        key=lambda loan: float(
            loan["emi"]
        ),
    )

    largest_outstanding_loan = max(
        loans,
        key=lambda loan: float(
            loan["outstanding_principal"]
        ),
    )

    # Primary debt-priority rule:
    # prioritize the loan with the highest interest rate.
    # If rates are equal, prioritize the larger balance.
    priority_loan = max(
        loans,
        key=lambda loan: (
            float(loan["interest_rate"]),
            float(
                loan["outstanding_principal"]
            ),
        ),
    )

    return {
        "has_loans": True,
        "loan_count": len(loans),
        "total_outstanding_principal": _money(
            portfolio.get(
                "total_outstanding_principal",
                0.0,
            )
        ),
        "total_emi": _money(
            portfolio.get(
                "total_emi",
                0.0,
            )
        ),
        "total_remaining_interest": _money(
            total_remaining_interest
        ),
        "total_remaining_repayment": _money(
            total_remaining_repayment
        ),
        "highest_interest_loan": {
            "loan_id": highest_interest_loan[
                "loan_id"
            ],
            "loan_name": highest_interest_loan[
                "loan_name"
            ],
            "interest_rate": _money(
                highest_interest_loan[
                    "interest_rate"
                ]
            ),
            "outstanding_principal": _money(
                highest_interest_loan[
                    "outstanding_principal"
                ]
            ),
        },
        "highest_emi_loan": {
            "loan_id": highest_emi_loan[
                "loan_id"
            ],
            "loan_name": highest_emi_loan[
                "loan_name"
            ],
            "emi": _money(
                highest_emi_loan["emi"]
            ),
            "outstanding_principal": _money(
                highest_emi_loan[
                    "outstanding_principal"
                ]
            ),
        },
        "largest_outstanding_loan": {
            "loan_id": largest_outstanding_loan[
                "loan_id"
            ],
            "loan_name": largest_outstanding_loan[
                "loan_name"
            ],
            "outstanding_principal": _money(
                largest_outstanding_loan[
                    "outstanding_principal"
                ]
            ),
            "interest_rate": _money(
                largest_outstanding_loan[
                    "interest_rate"
                ]
            ),
        },
        "priority_loan": {
            "loan_id": priority_loan[
                "loan_id"
            ],
            "loan_name": priority_loan[
                "loan_name"
            ],
            "interest_rate": _money(
                priority_loan["interest_rate"]
            ),
            "outstanding_principal": _money(
                priority_loan[
                    "outstanding_principal"
                ]
            ),
            "emi": _money(
                priority_loan["emi"]
            ),
            "reason": (
                "Highest interest rate"
            ),
        },
    }