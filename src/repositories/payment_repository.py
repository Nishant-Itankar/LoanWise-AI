from datetime import date

from sqlalchemy import text

from src.database import get_engine


def create_payment(
    loan_id: int,
    payment_date: date,
    emi_amount: float,
    principal_component: float,
    interest_component: float,
    outstanding_balance: float,
    late_payment: bool = False,
    extra_payment: float = 0,
):
    engine = get_engine()

    query = text(
        """
        INSERT INTO loan_payments (
            loan_id,
            payment_date,
            emi_amount,
            principal_component,
            interest_component,
            outstanding_balance,
            late_payment,
            extra_payment
        )
        VALUES (
            :loan_id,
            :payment_date,
            :emi_amount,
            :principal_component,
            :interest_component,
            :outstanding_balance,
            :late_payment,
            :extra_payment
        )
        RETURNING *;
        """
    )

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "loan_id": loan_id,
                "payment_date": payment_date,
                "emi_amount": emi_amount,
                "principal_component": principal_component,
                "interest_component": interest_component,
                "outstanding_balance": outstanding_balance,
                "late_payment": late_payment,
                "extra_payment": extra_payment,
            },
        )

        return result.mappings().one()


def get_payments_by_loan(
    loan_id: int,
):
    engine = get_engine()

    query = text(
        """
        SELECT *
        FROM loan_payments
        WHERE loan_id = :loan_id
        ORDER BY payment_date DESC, id DESC;
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"loan_id": loan_id},
        )

        return result.mappings().all()

def create_payment_and_update_loan(
    loan_id: int,
    payment_date: date,
    emi_amount: float,
    principal_component: float,
    interest_component: float,
    outstanding_balance: float,
    remaining_tenure_months: int,
    late_payment: bool = False,
    extra_payment: float = 0,
):
    engine = get_engine()

    payment_query = text(
        """
        INSERT INTO loan_payments (
            loan_id,
            payment_date,
            emi_amount,
            principal_component,
            interest_component,
            outstanding_balance,
            late_payment,
            extra_payment
        )
        VALUES (
            :loan_id,
            :payment_date,
            :emi_amount,
            :principal_component,
            :interest_component,
            :outstanding_balance,
            :late_payment,
            :extra_payment
        )
        RETURNING *;
        """
    )

    loan_query = text(
        """
        UPDATE loans
        SET
            outstanding_principal = :outstanding_balance,
            remaining_tenure_months = :remaining_tenure_months,
            status = CASE
                WHEN :outstanding_balance <= 0
                THEN 'closed'
                ELSE status
            END,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :loan_id
        RETURNING *;
        """
    )

    with engine.begin() as connection:
        payment_result = connection.execute(
            payment_query,
            {
                "loan_id": loan_id,
                "payment_date": payment_date,
                "emi_amount": emi_amount,
                "principal_component": principal_component,
                "interest_component": interest_component,
                "outstanding_balance": outstanding_balance,
                "late_payment": late_payment,
                "extra_payment": extra_payment,
            },
        )

        payment = payment_result.mappings().one()

        loan_result = connection.execute(
            loan_query,
            {
                "loan_id": loan_id,
                "outstanding_balance": outstanding_balance,
                "remaining_tenure_months": (
                    remaining_tenure_months
                ),
            },
        )

        loan = loan_result.mappings().one()

        return payment, loan
def create_prepayment_and_update_loan(
    loan_id: int,
    payment_date: date,
    prepayment_amount: float,
    outstanding_balance: float,
    remaining_tenure_months: int,
    principal_before: float,
    interest_saved: float,
    tenure_reduced_months: int,
):
    engine = get_engine()

    prepayment_query = text(
        """
        INSERT INTO prepayments (
            loan_id,
            payment_date,
            amount,
            principal_before,
            principal_after,
            interest_saved,
            tenure_reduced_months,
            strategy
        )
        VALUES (
            :loan_id,
            :payment_date,
            :amount,
            :principal_before,
            :principal_after,
            :interest_saved,
            :tenure_reduced_months,
            :strategy
        )
        RETURNING *;
        """
    )

    loan_query = text(
        """
        UPDATE loans
        SET
            outstanding_principal = :outstanding_balance,
            remaining_tenure_months = :remaining_tenure_months,
            status = CASE
                WHEN :outstanding_balance <= 0
                THEN 'closed'
                ELSE status
            END,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :loan_id
        RETURNING *;
        """
    )

    with engine.begin() as connection:
        prepayment_result = connection.execute(
            prepayment_query,
            {
                "loan_id": loan_id,
                "payment_date": payment_date,
                "amount": prepayment_amount,
                "principal_before": principal_before,
                "principal_after": outstanding_balance,
                "interest_saved": interest_saved,
                "tenure_reduced_months": tenure_reduced_months,
                "strategy": "manual_prepayment",
            },
        )

        prepayment = (
            prepayment_result.mappings().one()
        )

        loan_result = connection.execute(
            loan_query,
            {
                "loan_id": loan_id,
                "outstanding_balance": outstanding_balance,
                "remaining_tenure_months": (
                    remaining_tenure_months
                ),
            },
        )

        loan = loan_result.mappings().one()

        return prepayment, loan

def get_prepayments_by_loan(
    loan_id: int,
):
    engine = get_engine()

    query = text(
        """
        SELECT *
        FROM prepayments
        WHERE loan_id = :loan_id
        ORDER BY payment_date DESC, id DESC;
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"loan_id": loan_id},
        )

        return result.mappings().all()