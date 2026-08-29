from sqlalchemy import text

from src.database import get_engine
from src.repositories.loan_repository import create_loan
from src.repositories.user_repository import create_user


def test_create_user():
    email = "test-user@loanwise.local"

    user = create_user(
        name="Test User",
        email=email,
    )

    assert user["name"] == "Test User"
    assert user["email"] == email

    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM users WHERE email = :email"),
            {"email": email},
        )


def test_create_loan():
    engine = get_engine()

    user = create_user(
        name="Loan Test User",
        email="loan-test@loanwise.local",
    )

    loan = create_loan(
        user_id=user["id"],
        loan_name="Test Car Loan",
        loan_type="car",
        lender="Test Bank",
        original_principal=500000,
        outstanding_principal=400000,
        interest_rate=9.5,
        interest_type="fixed",
        emi=12500,
        original_tenure_months=60,
        remaining_tenure_months=48,
        loan_start_date="2025-01-01",
        emi_due_day=5,
    )

    assert loan["loan_name"] == "Test Car Loan"
    assert loan["user_id"] == user["id"]
    assert float(loan["outstanding_principal"]) == 400000

    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM loans WHERE id = :loan_id"),
            {"loan_id": loan["id"]},
        )

        connection.execute(
            text("DELETE FROM users WHERE id = :user_id"),
            {"user_id": user["id"]},
        )