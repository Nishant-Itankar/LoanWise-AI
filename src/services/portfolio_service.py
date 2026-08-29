from src.calculations.portfolio import (
    analyze_loan_portfolio,
)
from src.repositories.loan_repository import (
    get_loans_by_user,
)


def get_user_portfolio(user_id: int) -> dict:
    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    loans = get_loans_by_user(user_id)

    return analyze_loan_portfolio(loans)