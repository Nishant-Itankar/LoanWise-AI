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

    query = text(
        """
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
        """
    )

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


def get_loan_by_id(loan_id: int):
    engine = get_engine()

    query = text(
        """
        SELECT *
        FROM loans
        WHERE id = :loan_id;
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"loan_id": loan_id},
        )

        return result.mappings().first()


def get_loans_by_user(user_id: int):
    engine = get_engine()

    query = text(
        """
        SELECT *
        FROM loans
        WHERE user_id = :user_id
        ORDER BY created_at DESC;
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"user_id": user_id},
        )

        return result.mappings().all()


def find_active_duplicate_loan(
    user_id: int,
    loan_name: str,
    lender: str,
    original_principal: float,
    loan_start_date: str,
):
    engine = get_engine()

    query = text(
        """
        SELECT *
        FROM loans
        WHERE user_id = :user_id
          AND LOWER(TRIM(loan_name)) = LOWER(TRIM(:loan_name))
          AND LOWER(TRIM(lender)) = LOWER(TRIM(:lender))
          AND original_principal = :original_principal
          AND loan_start_date = :loan_start_date
          AND status = 'active'
        LIMIT 1;
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "user_id": user_id,
                "loan_name": loan_name,
                "lender": lender,
                "original_principal": original_principal,
                "loan_start_date": loan_start_date,
            },
        )

        return result.mappings().first()


def archive_loan(loan_id: int):
    engine = get_engine()

    query = text(
        """
        UPDATE loans
        SET
            status = 'archived',
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :loan_id
        RETURNING *;
        """
    )

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"loan_id": loan_id},
        )

        return result.mappings().first()


def close_loan(loan_id: int):
    engine = get_engine()

    query = text(
        """
        UPDATE loans
        SET
            status = 'closed',
            outstanding_principal = 0,
            remaining_tenure_months = 0,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :loan_id
        RETURNING *;
        """
    )

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"loan_id": loan_id},
        )

        return result.mappings().first()


def update_loan(
    loan_id: int,
    loan_name: str,
    loan_type: str,
    lender: str,
    interest_rate: float,
    interest_type: str,
    emi: float,
    original_tenure_months: int,
    loan_start_date: str,
    emi_due_day: int | None,
    processing_charges: float,
    prepayment_rules: str | None,
    prepayment_charges: float,
):
    engine = get_engine()

    query = text(
        """
        UPDATE loans
        SET
            loan_name = :loan_name,
            loan_type = :loan_type,
            lender = :lender,
            interest_rate = :interest_rate,
            interest_type = :interest_type,
            emi = :emi,
            original_tenure_months = :original_tenure_months,
            loan_start_date = :loan_start_date,
            emi_due_day = :emi_due_day,
            processing_charges = :processing_charges,
            prepayment_rules = :prepayment_rules,
            prepayment_charges = :prepayment_charges,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :loan_id
        RETURNING *;
        """
    )

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "loan_id": loan_id,
                "loan_name": loan_name,
                "loan_type": loan_type,
                "lender": lender,
                "interest_rate": interest_rate,
                "interest_type": interest_type,
                "emi": emi,
                "original_tenure_months": original_tenure_months,
                "loan_start_date": loan_start_date,
                "emi_due_day": emi_due_day,
                "processing_charges": processing_charges,
                "prepayment_rules": prepayment_rules,
                "prepayment_charges": prepayment_charges,
            },
        )

        return result.mappings().first()


def update_loan_balance(
    loan_id: int,
    outstanding_principal: float,
    remaining_tenure_months: int,
):
    engine = get_engine()

    query = text(
        """
        UPDATE loans
        SET
            outstanding_principal = :outstanding_principal,
            remaining_tenure_months = :remaining_tenure_months,
            status = CASE
                WHEN :outstanding_principal <= 0
                THEN 'closed'
                ELSE status
            END,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :loan_id
        RETURNING *;
        """
    )

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "loan_id": loan_id,
                "outstanding_principal": outstanding_principal,
                "remaining_tenure_months": remaining_tenure_months,
            },
        )

        return result.mappings().first()
    
def restore_loan(loan_id: int):
    engine = get_engine()

    query = text(
        """
        UPDATE loans
        SET
            status = 'active',
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :loan_id
          AND status = 'archived'
        RETURNING *;
        """
    )

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"loan_id": loan_id},
        )

        return result.mappings().first()


def delete_loan_permanently(loan_id: int):
    engine = get_engine()

    with engine.begin() as connection:
        # Delete dependent records first.
        connection.execute(
            text(
                """
                DELETE FROM interest_rate_history
                WHERE loan_id = :loan_id;
                """
            ),
            {"loan_id": loan_id},
        )

        connection.execute(
            text(
                """
                DELETE FROM loan_payments
                WHERE loan_id = :loan_id;
                """
            ),
            {"loan_id": loan_id},
        )

        connection.execute(
            text(
                """
                DELETE FROM prepayments
                WHERE loan_id = :loan_id;
                """
            ),
            {"loan_id": loan_id},
        )

        result = connection.execute(
            text(
                """
                DELETE FROM loans
                WHERE id = :loan_id
                RETURNING *;
                """
            ),
            {"loan_id": loan_id},
        )

        return result.mappings().first()