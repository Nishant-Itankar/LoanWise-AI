from decimal import Decimal, ROUND_HALF_UP

from src.calculations.amortization import (
    generate_amortization_schedule,
)


def analyze_prepayment(
    outstanding_principal: float,
    annual_interest_rate: float,
    remaining_tenure_months: int,
    prepayment_amount: float,
) -> dict:
    if outstanding_principal <= 0:
        raise ValueError(
            "Outstanding principal must be greater than zero."
        )

    if annual_interest_rate < 0:
        raise ValueError(
            "Interest rate cannot be negative."
        )

    if remaining_tenure_months <= 0:
        raise ValueError(
            "Remaining tenure must be greater than zero."
        )

    if prepayment_amount <= 0:
        raise ValueError(
            "Prepayment amount must be greater than zero."
        )

    if prepayment_amount > outstanding_principal:
        raise ValueError(
            "Prepayment cannot exceed outstanding principal."
        )

    current_schedule = generate_amortization_schedule(
        principal=outstanding_principal,
        annual_interest_rate=annual_interest_rate,
        tenure_months=remaining_tenure_months,
    )

    new_principal = (
        Decimal(str(outstanding_principal))
        - Decimal(str(prepayment_amount))
    )

    new_schedule = []

    if new_principal > 0:
        new_schedule = generate_amortization_schedule(
            principal=float(new_principal),
            annual_interest_rate=annual_interest_rate,
            tenure_months=remaining_tenure_months,
        )

    current_interest = sum(
        Decimal(str(row["interest"]))
        for row in current_schedule
    )

    new_interest = sum(
        Decimal(str(row["interest"]))
        for row in new_schedule
    )

    interest_saved = current_interest - new_interest

    current_emi = Decimal(
        str(current_schedule[0]["emi"])
    )

    new_emi = (
        Decimal(str(new_schedule[0]["emi"]))
        if new_schedule
        else Decimal("0")
    )

    return {
        "prepayment_amount": float(
            Decimal(str(prepayment_amount)).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "principal_before": float(
            Decimal(str(outstanding_principal)).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "principal_after": float(
            new_principal.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "current_interest": float(
            current_interest.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "new_interest": float(
            new_interest.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "interest_saved": float(
            interest_saved.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "current_emi": float(
            current_emi.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "new_emi": float(
            new_emi.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "current_tenure_months": len(current_schedule),
        "new_tenure_months": len(new_schedule),
        "tenure_reduced_months": (
            len(current_schedule)
            - len(new_schedule)
        ),
    }