from decimal import Decimal, ROUND_HALF_UP


def calculate_payment(
    outstanding_principal: float,
    annual_interest_rate: float,
    emi: float,
    extra_payment: float = 0,
) -> dict:
    if outstanding_principal < 0:
        raise ValueError(
            "Outstanding principal cannot be negative."
        )

    if annual_interest_rate < 0:
        raise ValueError(
            "Interest rate cannot be negative."
        )

    if emi <= 0:
        raise ValueError(
            "EMI must be greater than zero."
        )

    if extra_payment < 0:
        raise ValueError(
            "Extra payment cannot be negative."
        )

    if outstanding_principal == 0:
        return {
            "emi_amount": 0.0,
            "interest_component": 0.0,
            "principal_component": 0.0,
            "extra_payment": 0.0,
            "total_principal_reduction": 0.0,
            "outstanding_balance": 0.0,
        }

    monthly_rate = (
        Decimal(str(annual_interest_rate))
        / Decimal("100")
        / Decimal("12")
    )

    outstanding = Decimal(
        str(outstanding_principal)
    )

    scheduled_emi = Decimal(str(emi))

    extra = Decimal(str(extra_payment))

    interest = (
        outstanding * monthly_rate
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    principal = (
        scheduled_emi - interest
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    if principal <= 0:
        raise ValueError(
            "EMI is not sufficient to cover "
            "the monthly interest."
        )

    if principal > outstanding:
        principal = outstanding

    available_after_emi = (
        outstanding - principal
    )

    if extra > available_after_emi:
        extra = available_after_emi

    total_reduction = (
        principal + extra
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    new_balance = (
        outstanding - total_reduction
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return {
        "emi_amount": float(
            scheduled_emi.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "interest_component": float(
            interest
        ),
        "principal_component": float(
            principal
        ),
        "extra_payment": float(
            extra
        ),
        "total_principal_reduction": float(
            total_reduction
        ),
        "outstanding_balance": float(
            new_balance
        ),
    }