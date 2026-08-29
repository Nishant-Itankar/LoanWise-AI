from decimal import Decimal, ROUND_HALF_UP

from src.calculations.amortization import (
    generate_amortization_schedule,
)


def analyze_remaining_loan(
    outstanding_principal: float,
    annual_interest_rate: float,
    remaining_tenure_months: int,
) -> dict:
    if outstanding_principal < 0:
        raise ValueError(
            "Outstanding principal cannot be negative."
        )

    if annual_interest_rate < 0:
        raise ValueError(
            "Interest rate cannot be negative."
        )

    if remaining_tenure_months < 0:
        raise ValueError(
            "Remaining tenure cannot be negative."
        )

    if outstanding_principal == 0:
        return {
            "emi": 0.0,
            "remaining_interest": 0.0,
            "remaining_repayment": 0.0,
            "remaining_principal": 0.0,
        }

    if remaining_tenure_months == 0:
        raise ValueError(
            "Tenure must be greater than zero "
            "when outstanding principal exists."
        )

    schedule = generate_amortization_schedule(
        principal=outstanding_principal,
        annual_interest_rate=annual_interest_rate,
        tenure_months=remaining_tenure_months,
    )

    total_interest = sum(
        Decimal(str(row["interest"]))
        for row in schedule
    )

    total_repayment = sum(
        Decimal(str(row["emi"]))
        for row in schedule
    )

    emi = Decimal(str(schedule[0]["emi"]))

    return {
        "emi": float(
            emi.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "remaining_interest": float(
            total_interest.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "remaining_repayment": float(
            total_repayment.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "remaining_principal": float(
            Decimal(str(outstanding_principal)).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
    }