from src.repositories.loan_repository import (
    get_loan_by_id,
)
from src.repositories.payment_repository import (
    get_payments_by_loan,
    get_prepayments_by_loan,
)


def get_loan_activity(
    loan_id: int,
) -> list[dict]:
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    loan = get_loan_by_id(loan_id)

    if not loan:
        raise ValueError(
            "Loan not found."
        )

    payments = get_payments_by_loan(loan_id)

    return [
        {
            "id": payment["id"],
            "loan_id": payment["loan_id"],
            "payment_date": payment["payment_date"],
            "emi_amount": float(
                payment["emi_amount"]
            ),
            "principal_component": float(
                payment["principal_component"]
            ),
            "interest_component": float(
                payment["interest_component"]
            ),
            "outstanding_balance": float(
                payment["outstanding_balance"]
            ),
            "late_payment": payment["late_payment"],
            "extra_payment": float(
                payment["extra_payment"]
            ),
        }
        for payment in payments
    ]


def get_loan_activity_summary(
    loan_id: int,
) -> dict:
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    loan = get_loan_by_id(loan_id)

    if not loan:
        raise ValueError(
            "Loan not found."
        )

    payments = get_payments_by_loan(loan_id)

    total_emi_paid = sum(
        float(payment["emi_amount"])
        for payment in payments
    )

    total_principal_paid = sum(
        float(payment["principal_component"])
        for payment in payments
    )

    total_interest_paid = sum(
        float(payment["interest_component"])
        for payment in payments
    )

    total_extra_payments = sum(
        float(payment["extra_payment"])
        for payment in payments
    )

    latest_outstanding = (
        float(
            payments[0][
                "outstanding_balance"
            ]
        )
        if payments
        else float(
            loan["outstanding_principal"]
        )
    )

    return {
        "loan_id": loan_id,
        "payment_count": len(payments),
        "total_emi_paid": round(
            total_emi_paid,
            2,
        ),
        "total_principal_paid": round(
            total_principal_paid,
            2,
        ),
        "total_interest_paid": round(
            total_interest_paid,
            2,
        ),
        "total_extra_payments": round(
            total_extra_payments,
            2,
        ),
        "latest_outstanding_balance": round(
            latest_outstanding,
            2,
        ),
    }


def get_combined_loan_activity(
    loan_id: int,
) -> list[dict]:
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    loan = get_loan_by_id(loan_id)

    if not loan:
        raise ValueError(
            "Loan not found."
        )

    payments = get_payments_by_loan(
        loan_id
    )

    prepayments = get_prepayments_by_loan(
        loan_id
    )

    activities = []

    for payment in payments:
        activities.append(
            {
                "id": payment["id"],
                "loan_id": payment["loan_id"],
                "date": payment[
                    "payment_date"
                ],
                "type": "EMI Payment",
                "amount": float(
                    payment["emi_amount"]
                ),
                "principal_paid": float(
                    payment[
                        "principal_component"
                    ]
                ),
                "interest_paid": float(
                    payment[
                        "interest_component"
                    ]
                ),
                "extra_payment": float(
                    payment[
                        "extra_payment"
                    ]
                ),
                "outstanding_balance": float(
                    payment[
                        "outstanding_balance"
                    ]
                ),
                "interest_saved": 0.0,
                "tenure_reduced_months": 0,
                "late_payment": payment[
                    "late_payment"
                ],
            }
        )

    for prepayment in prepayments:
        activities.append(
            {
                "id": prepayment["id"],
                "loan_id": prepayment[
                    "loan_id"
                ],
                "date": prepayment[
                    "payment_date"
                ],
                "type": "Prepayment",
                "amount": float(
                    prepayment["amount"]
                ),
                "principal_paid": float(
                    prepayment["amount"]
                ),
                "interest_paid": 0.0,
                "extra_payment": float(
                    prepayment["amount"]
                ),
                "outstanding_balance": float(
                    prepayment[
                        "principal_after"
                    ]
                ),
                "interest_saved": float(
                    prepayment[
                        "interest_saved"
                    ]
                ),
                "tenure_reduced_months": (
                    prepayment[
                        "tenure_reduced_months"
                    ]
                ),
                "late_payment": False,
            }
        )

    activities.sort(
        key=lambda activity: (
            activity["date"],
            activity["id"],
        ),
        reverse=True,
    )

    return activities