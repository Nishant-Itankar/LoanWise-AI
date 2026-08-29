from decimal import Decimal, ROUND_HALF_UP


def calculate_emi(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
) -> float:
    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if tenure_months <= 0:
        raise ValueError("Tenure must be greater than zero.")

    principal_decimal = Decimal(str(principal))
    annual_rate_decimal = Decimal(str(annual_interest_rate))

    monthly_rate = annual_rate_decimal / Decimal("1200")

    if monthly_rate == 0:
        emi = principal_decimal / Decimal(tenure_months)
    else:
        factor = (
            (Decimal("1") + monthly_rate)
            ** tenure_months
        )

        emi = (
            principal_decimal
            * monthly_rate
            * factor
            / (factor - Decimal("1"))
        )

    return float(
        emi.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )


def calculate_total_interest(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
) -> float:
    emi = calculate_emi(
        principal,
        annual_interest_rate,
        tenure_months,
    )

    total_payment = Decimal(str(emi)) * Decimal(tenure_months)
    interest = total_payment - Decimal(str(principal))

    return float(
        interest.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )


def calculate_total_repayment(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
) -> float:
    emi = calculate_emi(
        principal,
        annual_interest_rate,
        tenure_months,
    )

    total_payment = Decimal(str(emi)) * Decimal(tenure_months)

    return float(
        total_payment.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )