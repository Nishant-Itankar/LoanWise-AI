from datetime import date

from src.database import get_engine
from src.repositories.loan_repository import create_loan


USER_ID = 67


def main():
    loan = create_loan(
        user_id=USER_ID,
        loan_name="Payment Test Loan",
        loan_type="personal",
        lender="Test Bank",
        original_principal=400000,
        outstanding_principal=400000,
        interest_rate=8.0,
        interest_type="fixed",
        emi=11500,
        original_tenure_months=48,
        remaining_tenure_months=48,
        loan_start_date=date.today(),
        emi_due_day=5,
        processing_charges=0,
        prepayment_rules=None,
        prepayment_charges=0,
    )

    print("Created test loan:")
    print(dict(loan))


if __name__ == "__main__":
    main()