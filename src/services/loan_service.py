from datetime import date

from src.repositories.loan_repository import (
    create_loan,
    get_loan_by_id,
    get_loans_by_user,
    update_loan,
    archive_loan,
    close_loan,
    find_active_duplicate_loan,
)


def update_loan_details(
    loan_id: int,
    loan_name: str,
    loan_type: str,
    lender: str,
    interest_rate: float,
    interest_type: str,
    emi: float,
    original_tenure_months: int,
    loan_start_date: date,
    emi_due_day: int | None,
    processing_charges: float,
    prepayment_rules: str | None,
    prepayment_charges: float,
):
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    if not loan_name.strip():
        raise ValueError(
            "Loan name cannot be empty."
        )

    if not lender.strip():
        raise ValueError(
            "Lender cannot be empty."
        )

    if loan_type not in VALID_LOAN_TYPES:
        raise ValueError(
            "Invalid loan type."
        )

    if interest_type not in VALID_INTEREST_TYPES:
        raise ValueError(
            "Invalid interest type."
        )

    if interest_rate < 0:
        raise ValueError(
            "Interest rate cannot be negative."
        )

    if emi <= 0:
        raise ValueError(
            "EMI must be greater than zero."
        )

    if original_tenure_months <= 0:
        raise ValueError(
            "Original tenure must be greater than zero."
        )

    if emi_due_day is not None and not 1 <= emi_due_day <= 31:
        raise ValueError(
            "EMI due day must be between 1 and 31."
        )

    if processing_charges < 0:
        raise ValueError(
            "Processing charges cannot be negative."
        )

    if prepayment_charges < 0:
        raise ValueError(
            "Prepayment charges cannot be negative."
        )

    return update_loan(
        loan_id=loan_id,
        loan_name=loan_name.strip(),
        loan_type=loan_type,
        lender=lender.strip(),
        interest_rate=interest_rate,
        interest_type=interest_type,
        emi=emi,
        original_tenure_months=original_tenure_months,
        loan_start_date=loan_start_date,
        emi_due_day=emi_due_day,
        processing_charges=processing_charges,
        prepayment_rules=prepayment_rules,
        prepayment_charges=prepayment_charges,
    )

VALID_LOAN_TYPES = {
    "home",
    "car",
    "personal",
    "education",
    "business",
    "other",
}

VALID_INTEREST_TYPES = {
    "fixed",
    "floating",
}


def validate_loan(
    loan_type: str,
    interest_type: str,
    original_principal: float,
    outstanding_principal: float,
    interest_rate: float,
    emi: float,
    original_tenure_months: int,
    remaining_tenure_months: int,
):
    if loan_type not in VALID_LOAN_TYPES:
        raise ValueError("Invalid loan type.")

    if interest_type not in VALID_INTEREST_TYPES:
        raise ValueError("Invalid interest type.")

    if original_principal <= 0:
        raise ValueError(
            "Original principal must be greater than zero."
        )

    if outstanding_principal < 0:
        raise ValueError(
            "Outstanding principal cannot be negative."
        )

    if outstanding_principal > original_principal:
        raise ValueError(
            "Outstanding principal cannot exceed "
            "original principal."
        )

    if interest_rate < 0:
        raise ValueError(
            "Interest rate cannot be negative."
        )

    if emi <= 0:
        raise ValueError(
            "EMI must be greater than zero."
        )

    if original_tenure_months <= 0:
        raise ValueError(
            "Original tenure must be greater than zero."
        )

    if remaining_tenure_months < 0:
        raise ValueError(
            "Remaining tenure cannot be negative."
        )

    if remaining_tenure_months > original_tenure_months:
        raise ValueError(
            "Remaining tenure cannot exceed "
            "original tenure."
        )


def register_loan(
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
    loan_start_date: date,
    emi_due_day: int | None = None,
    processing_charges: float = 0,
    prepayment_rules: str | None = None,
    prepayment_charges: float = 0,
):
    loan_name = loan_name.strip()
    lender = lender.strip()

    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    if not loan_name:
        raise ValueError(
            "Loan name cannot be empty."
        )

    if not lender:
        raise ValueError(
            "Lender cannot be empty."
        )

    if emi_due_day is not None and not 1 <= emi_due_day <= 31:
        raise ValueError(
            "EMI due day must be between 1 and 31."
        )

    if outstanding_principal > original_principal:
        raise ValueError(
            "Outstanding principal cannot exceed "
            "original principal."
        )

    if remaining_tenure_months > original_tenure_months:
        raise ValueError(
            "Remaining tenure cannot exceed "
            "original tenure."
        )

    validate_loan(
        loan_type=loan_type,
        interest_type=interest_type,
        original_principal=original_principal,
        outstanding_principal=outstanding_principal,
        interest_rate=interest_rate,
        emi=emi,
        original_tenure_months=original_tenure_months,
        remaining_tenure_months=remaining_tenure_months,
    )

    duplicate = find_active_duplicate_loan(
        user_id=user_id,
        loan_name=loan_name,
        lender=lender,
        original_principal=original_principal,
        loan_start_date=loan_start_date,
    )

    if duplicate:
        raise ValueError(
            "A similar active loan already exists "
            f"(Loan ID: {duplicate['id']})."
        )

    return create_loan(
        user_id=user_id,
        loan_name=loan_name,
        loan_type=loan_type,
        lender=lender,
        original_principal=original_principal,
        outstanding_principal=outstanding_principal,
        interest_rate=interest_rate,
        interest_type=interest_type,
        emi=emi,
        original_tenure_months=original_tenure_months,
        remaining_tenure_months=remaining_tenure_months,
        loan_start_date=loan_start_date,
        emi_due_day=emi_due_day,
        processing_charges=processing_charges,
        prepayment_rules=prepayment_rules,
        prepayment_charges=prepayment_charges,
    )


def get_loan(loan_id: int):
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    return get_loan_by_id(loan_id)


def get_user_loans(user_id: int):
    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    return get_loans_by_user(user_id)


def get_user_loan_summary(user_id: int) -> list[dict]:
    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    loans = get_loans_by_user(user_id)

    return [
        {
            "id": loan["id"],
            "loan_name": loan["loan_name"],
            "loan_type": loan["loan_type"],
            "lender": loan["lender"],
            "outstanding_principal": float(
                loan["outstanding_principal"]
            ),
            "interest_rate": float(
                loan["interest_rate"]
            ),
            "emi": float(loan["emi"]),
            "remaining_tenure_months": loan[
                "remaining_tenure_months"
            ],
            "status": loan["status"],
        }
        for loan in loans
    ]


def archive_user_loan(loan_id: int):
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    loan = get_loan_by_id(loan_id)

    if not loan:
        raise ValueError(
            "Loan not found."
        )

    if loan["status"] == "archived":
        raise ValueError(
            "Loan is already archived."
        )

    return archive_loan(loan_id)

def close_user_loan(loan_id: int):
    if loan_id <= 0:
        raise ValueError(
            "Loan ID must be positive."
        )

    loan = get_loan_by_id(loan_id)

    if not loan:
        raise ValueError(
            "Loan not found."
        )

    if loan["status"] == "closed":
        raise ValueError(
            "Loan is already closed."
        )

    if loan["status"] == "archived":
        raise ValueError(
            "Archived loans cannot be closed."
        )

    if float(loan["outstanding_principal"]) > 0:
        raise ValueError(
            "Loan cannot be closed while "
            "outstanding principal exists."
        )

    return close_loan(loan_id)