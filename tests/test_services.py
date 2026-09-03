import pytest
from sqlalchemy import text

from src.database import get_engine
from src.services.user_service import register_user
from src.services.loan_service import register_loan


def test_register_user_normalizes_email():
    email = "service-test@loanwise.local"

    user = register_user(
        name="Service Test User",
        email=" SERVICE-TEST@LOANWISE.LOCAL ",
    )

    assert user["name"] == "Service Test User"
    assert user["email"] == email

    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM users WHERE email = :email"),
            {"email": email},
        )


def test_register_user_rejects_invalid_email():
    with pytest.raises(ValueError, match="Invalid email address"):
        register_user(
            name="Invalid User",
            email="not-an-email",
        )


def test_register_loan_validates_data():
    user = register_user(
        name="Loan Service Test",
        email="loan-service-test@loanwise.local",
    )

    loan = register_loan(
        user_id=user["id"],
        loan_name="Service Test Loan",
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

    assert loan["loan_name"] == "Service Test Loan"
    assert loan["user_id"] == user["id"]

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


def test_register_loan_rejects_invalid_amounts():
    with pytest.raises(
        ValueError,
        match="Original principal must be greater than zero",
    ):
        register_loan(
            user_id=1,
            loan_name="Invalid Loan",
            loan_type="car",
            lender="Test Bank",
            original_principal=0,
            outstanding_principal=0,
            interest_rate=9.5,
            interest_type="fixed",
            emi=12500,
            original_tenure_months=60,
            remaining_tenure_months=48,
            loan_start_date="2025-01-01",
        )
def test_list_users():
    from src.services.user_service import list_users

    users = list_users()

    assert isinstance(users, list)

def test_register_loan_rejects_excess_outstanding():
    from src.services.loan_service import register_loan

    try:
        register_loan(
            user_id=67,
            loan_name="Invalid Loan",
            loan_type="car",
            lender="Test Bank",
            original_principal=500000,
            outstanding_principal=600000,
            interest_rate=10,
            interest_type="fixed",
            emi=12000,
            original_tenure_months=60,
            remaining_tenure_months=48,
            loan_start_date="2025-01-01",
            emi_due_day=5,
            processing_charges=0,
            prepayment_rules=None,
            prepayment_charges=0,
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Outstanding principal cannot exceed "
            "original principal."
        )


def test_register_loan_rejects_excess_remaining_tenure():
    from src.services.loan_service import register_loan

    try:
        register_loan(
            user_id=67,
            loan_name="Invalid Loan",
            loan_type="car",
            lender="Test Bank",
            original_principal=500000,
            outstanding_principal=400000,
            interest_rate=10,
            interest_type="fixed",
            emi=12000,
            original_tenure_months=48,
            remaining_tenure_months=60,
            loan_start_date="2025-01-01",
            emi_due_day=5,
            processing_charges=0,
            prepayment_rules=None,
            prepayment_charges=0,
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Remaining tenure cannot exceed "
            "original tenure."
        )
def test_recommend_prepayment_rejects_invalid_amount():
    from src.services.recommendation_service import (
        recommend_prepayment,
    )

    try:
        recommend_prepayment(
            user_id=67,
            prepayment_amount=0,
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Prepayment amount must be greater than zero."
        )
        
def test_archive_user_loan():
    from src.services.loan_service import (
        archive_user_loan,
    )

    try:
        archive_user_loan(0)
        assert False
    except ValueError as error:
        assert str(error) == "Loan ID must be positive."

def test_close_user_loan_rejects_invalid_id():
    from src.services.loan_service import (
        close_user_loan,
    )

    try:
        close_user_loan(0)
        assert False
    except ValueError as error:
        assert str(error) == (
            "Loan ID must be positive."
        )