import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.database import get_engine
from src.repositories.user_repository import create_user
from src.repositories.loan_repository import create_loan


def test_invalid_loan_type_is_rejected():
    user = create_user(
        name="Constraint Test User",
        email="constraint-test@loanwise.local",
    )

    with pytest.raises(IntegrityError):
        create_loan(
            user_id=user["id"],
            loan_name="Invalid Loan",
            loan_type="invalid_type",
            lender="Test Bank",
            original_principal=100000,
            outstanding_principal=90000,
            interest_rate=10,
            interest_type="fixed",
            emi=2500,
            original_tenure_months=48,
            remaining_tenure_months=40,
            loan_start_date="2025-01-01",
        )

    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM users WHERE id = :user_id"),
            {"user_id": user["id"]},
        )