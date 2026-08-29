from sqlalchemy import text

from src.database import get_engine


def create_loan(
    user_id: int,
    loan_name: str,
    loan_type: str,
    lender: str,
    original_principal: float,
    outstanding_principal: float,
    interest_rate: float,
    interest_type: str,
    emi: float,
    original_tenure_months: int,
    remaining_tenure_months: int,
    loan_start_date: str,
    emi_due_day: int | None = None,
    processing_charges: float = 0,
    prepayment_rules: str | None = None,
    prepayment_charges: float = 0,
    status: str = "active",
):
    engine = get_engine()

    query = text("""
        INSERT INTO loans (
            user_id,
            loan_name,
            loan_type,
            lender,
            original_principal,
            outstanding_principal,
            interest_rate,
            interest_type,
            emi,
            original_tenure_months,
            remaining_tenure_months,
            loan_start_date,
            emi_due_day,
            processing_charges,
            prepayment_rules,
            prepayment_charges,
            status
        )
        VALUES (
            :user_id,
            :loan_name,
            :loan_type,
            :lender,
            :original_principal,
            :outstanding_principal,
            :interest_rate,
            :interest_type,
            :emi,
            :original_tenure_months,
            :remaining_tenure_months,
            :loan_start_date,
            :emi_due_day,
            :processing_charges,
            :prepayment_rules,
            :prepayment_charges,
            :status
        )
        RETURNING *;
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "user_id": user_id,
                "loan_name": loan_name,
                "loan_type": loan_type,
                "lender": lender,
                "original_principal": original_principal,
                "outstanding_principal": outstanding_principal,
                "interest_rate": interest_rate,
                "interest_type": interest_type,
                "emi": emi,
                "original_tenure_months": original_tenure_months,
                "remaining_tenure_months": remaining_tenure_months,
                "loan_start_date": loan_start_date,
                "emi_due_day": emi_due_day,
                "processing_charges": processing_charges,
                "prepayment_rules": prepayment_rules,
                "prepayment_charges": prepayment_charges,
                "status": status,
            },
        )

        return result.mappings().one()