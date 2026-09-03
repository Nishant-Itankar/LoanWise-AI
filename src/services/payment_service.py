from datetime import date

from src.calculations.payment import calculate_payment
from src.repositories.loan_repository import (
    get_loan_by_id,
)
from src.repositories.payment_repository import (
    create_payment_and_update_loan,
    get_payments_by_loan,
)


def record_loan_payment(
    loan_id: int,
    payment_date: date,
    extra_payment: float = 0,
    late_payment: bool = False,
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

    if loan["status"] != "active":
        raise ValueError(
            "Payment can only be recorded "
            "for an active loan."
        )

    outstanding = float(
        loan["outstanding_principal"]
    )

    if outstanding <= 0:
        raise ValueError(
            "Loan has no outstanding balance."
        )

    result = calculate_payment(
        outstanding_principal=outstanding,
        annual_interest_rate=float(
            loan["interest_rate"]
        ),
        emi=float(loan["emi"]),
        extra_payment=extra_payment,
    )

    new_balance = result[
        "outstanding_balance"
    ]

    remaining_tenure = max(
        int(loan["remaining_tenure_months"]) - 1,
        0,
    )

    payment, updated_loan = (
        create_payment_and_update_loan(
            loan_id=loan_id,
            payment_date=payment_date,
            emi_amount=result["emi_amount"],
            principal_component=result[
                "principal_component"
            ],
            interest_component=result[
                "interest_component"
            ],
            outstanding_balance=new_balance,
            remaining_tenure_months=remaining_tenure,
            late_payment=late_payment,
            extra_payment=result["extra_payment"],
        )
    )

    return {
        "payment": payment,
        "loan": updated_loan,
        "calculation": result,
    }


def get_loan_payment_history(
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

    return get_payments_by_loan(loan_id)