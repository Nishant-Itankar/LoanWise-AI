from src.calculations.portfolio import (
    analyze_loan_portfolio,
)
from src.repositories.loan_repository import (
    get_loans_by_user,
)
from src.services.loan_service import (
    get_user_loan_summary,
)


def get_dashboard_data(user_id: int) -> dict:
    if user_id <= 0:
        raise ValueError("User ID must be positive.")

    loans = get_loans_by_user(user_id)

    portfolio = analyze_loan_portfolio(loans)

    return {
        "portfolio": portfolio,
        "loans": get_user_loan_summary(user_id),
    }