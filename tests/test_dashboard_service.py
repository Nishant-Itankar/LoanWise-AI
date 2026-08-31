from sqlalchemy import text

from src.database import get_engine
from src.repositories.user_repository import create_user
from src.repositories.loan_repository import create_loan
from src.services.dashboard_service import (
    get_dashboard_data,
)


def test_dashboard_returns_user_portfolio():
    user = create_user(
        name="Dashboard Test User",
        email="dashboard-test@loanwise.local",
    )

    loan = create_loan(
        user_id=user["id"],
        loan_name="Dashboard Car Loan",
        loan_type="car",
        lender="Test Bank",
        original_principal=500000,
        outstanding_principal=400000,
        interest_rate=10,
        interest_type="fixed",
        emi=12500,
        original_tenure_months=60,
        remaining_tenure_months=48,
        loan_start_date="2025-01-01",
        emi_due_day=5,
    )

    result = get_dashboard_data(user["id"])

    assert result["portfolio"]["loan_count"] == 1
    assert (
        result["portfolio"]["total_outstanding_principal"]
        == 400000
    )

    assert len(result["loans"]) == 1
    assert result["loans"][0]["loan_name"] == (
        "Dashboard Car Loan"
    )

    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM loans WHERE id = :loan_id"),
            {"loan_id": loan["id"]},
        )

        connection.execute(
            text("DELETE FROM users WHERE id = :user_id"),
            {"user_id": user["id"]},
        )
def test_dashboard_rejects_invalid_user_id():
    from src.services.dashboard_service import (
        get_dashboard_data,
    )

    try:
        get_dashboard_data(0)
        assert False
    except ValueError as error:
        assert str(error) == "User ID must be positive."