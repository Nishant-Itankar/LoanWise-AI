from datetime import date

from src.calculations.prepayment import (
    analyze_prepayment,
)
from src.repositories.loan_repository import (
    get_loan_by_id,
)
from src.repositories.payment_repository import (
    create_prepayment_and_update_loan,
    get_prepayments_by_loan,
)


def record_loan_prepayment(
    loan_id: int,
    payment_date: date,
    prepayment_amount: float,
) -> dict:
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    if prepayment_amount <= 0:
        raise ValueError(
            "Prepayment amount must be greater than zero."
        )

    loan = get_loan_by_id(loan_id)

    if not loan:
        raise ValueError(
            "Loan not found."
        )

    if loan["status"] != "active":
        raise ValueError(
            "Prepayment can only be recorded "
            "for an active loan."
        )

    outstanding = float(
        loan["outstanding_principal"]
    )

    if outstanding <= 0:
        raise ValueError(
            "Loan has no outstanding balance."
        )

    analysis = analyze_prepayment(
        outstanding_principal=outstanding,
        annual_interest_rate=float(
            loan["interest_rate"]
        ),
        remaining_tenure_months=int(
            loan["remaining_tenure_months"]
        ),
        prepayment_amount=prepayment_amount,
    )

    new_balance = analysis["principal_after"]

    remaining_tenure = analysis[
        "new_tenure_months"
    ]

    payment, updated_loan = (
        create_prepayment_and_update_loan(
            loan_id=loan_id,
            payment_date=payment_date,
            prepayment_amount=prepayment_amount,
            principal_before=analysis[
                "principal_before"
            ],
            interest_saved=analysis[
                "interest_saved"
            ],
            tenure_reduced_months=analysis[
                "tenure_reduced_months"
            ],
            outstanding_balance=new_balance,
            remaining_tenure_months=remaining_tenure,
        )
    )

    return {
        "payment": payment,
        "loan": updated_loan,
        "analysis": analysis,
    }


def get_loan_prepayment_history(
    loan_id: int,
):
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    loan = get_loan_by_id(loan_id)

    if not loan:
        raise ValueError(
            "Loan not found."
        )

    prepayments = get_prepayments_by_loan(
        loan_id
    )

    return [
        {
            "id": prepayment["id"],
            "loan_id": prepayment["loan_id"],
            "payment_date": prepayment[
                "payment_date"
            ],
            "amount": float(
                prepayment["amount"]
            ),
            "principal_before": float(
                prepayment["principal_before"]
            ),
            "principal_after": float(
                prepayment["principal_after"]
            ),
            "interest_saved": float(
                prepayment["interest_saved"]
            ),
            "tenure_reduced_months": prepayment[
                "tenure_reduced_months"
            ],
            "strategy": prepayment["strategy"],
            "notes": prepayment["notes"],
        }
        for prepayment in prepayments
    ]