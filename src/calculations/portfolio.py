from decimal import Decimal, ROUND_HALF_UP


def analyze_loan_portfolio(loans: list[dict]) -> dict:
    if not loans:
        return {
            "loan_count": 0,
            "total_original_principal": 0.0,
            "total_outstanding_principal": 0.0,
            "total_emi": 0.0,
            "weighted_interest_rate": 0.0,
        }

    total_original = sum(
        Decimal(str(loan["original_principal"]))
        for loan in loans
    )

    total_outstanding = sum(
        Decimal(str(loan["outstanding_principal"]))
        for loan in loans
    )

    total_emi = sum(
        Decimal(str(loan["emi"]))
        for loan in loans
    )

    if total_outstanding > 0:
        weighted_rate = sum(
            Decimal(str(loan["interest_rate"]))
            * Decimal(str(loan["outstanding_principal"]))
            for loan in loans
        ) / total_outstanding
    else:
        weighted_rate = Decimal("0")

    return {
        "loan_count": len(loans),
        "total_original_principal": float(
            total_original.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "total_outstanding_principal": float(
            total_outstanding.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "total_emi": float(
            total_emi.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
        "weighted_interest_rate": float(
            weighted_rate.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        ),
    }