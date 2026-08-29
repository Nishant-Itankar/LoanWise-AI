from decimal import Decimal, ROUND_HALF_UP

from src.calculations.emi import calculate_emi


def generate_amortization_schedule(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
) -> list[dict]:
    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if tenure_months <= 0:
        raise ValueError("Tenure must be greater than zero.")

    emi = Decimal(
        str(
            calculate_emi(
                principal,
                annual_interest_rate,
                tenure_months,
            )
        )
    )

    balance = Decimal(str(principal))
    monthly_rate = (
        Decimal(str(annual_interest_rate))
        / Decimal("1200")
    )

    schedule = []

    for month in range(1, tenure_months + 1):
        interest = (
            balance * monthly_rate
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        if month == tenure_months:
            principal_component = balance
            actual_emi = principal_component + interest
        else:
            principal_component = (
                emi - interest
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            actual_emi = (
                principal_component + interest
            )

        balance -= principal_component

        if balance < Decimal("0.01"):
            balance = Decimal("0.00")

        schedule.append(
            {
                "month": month,
                "emi": float(
                    actual_emi.quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    )
                ),
                "principal": float(
                    principal_component.quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    )
                ),
                "interest": float(
                    interest.quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    )
                ),
                "remaining_balance": float(
                    balance.quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    )
                ),
            }
        )

    return schedule