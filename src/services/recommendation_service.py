from src.calculations.recommendations import (
    recommend_prepayment_target,
)
from src.repositories.loan_repository import (
    get_loans_by_user,
)


def recommend_prepayment(
    user_id: int,
    prepayment_amount: float,
) -> dict:
    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    if prepayment_amount <= 0:
        raise ValueError(
            "Prepayment amount must be greater than zero."
        )

    loans = get_loans_by_user(user_id)

    active_loans = [
        loan
        for loan in loans
        if loan["status"] == "active"
    ]

    return recommend_prepayment_target(
        loans=active_loans,
        prepayment_amount=prepayment_amount,
    )