from src.calculations.prepayment import analyze_prepayment


def recommend_prepayment_target(
    loans: list[dict],
    prepayment_amount: float,
) -> dict:
    if not loans:
        raise ValueError("At least one loan is required.")

    if prepayment_amount <= 0:
        raise ValueError(
            "Prepayment amount must be greater than zero."
        )

    candidates = []

    for loan in loans:
        outstanding = float(
            loan["outstanding_principal"]
        )

        if outstanding <= 0:
            continue

        amount = min(
            prepayment_amount,
            outstanding,
        )

        analysis = analyze_prepayment(
            outstanding_principal=outstanding,
            annual_interest_rate=float(
                loan["interest_rate"]
            ),
            remaining_tenure_months=int(
                loan["remaining_tenure_months"]
            ),
            prepayment_amount=amount,
        )

        candidates.append(
            {
                "loan_id": loan["id"],
                "loan_name": loan["loan_name"],
                "interest_rate": float(
                    loan["interest_rate"]
                ),
                "prepayment_amount": amount,
                "interest_saved": analysis[
                    "interest_saved"
                ],
                "tenure_reduced_months": analysis[
                    "tenure_reduced_months"
                ],
            }
        )

    if not candidates:
        raise ValueError(
            "No active loan is available for prepayment."
        )

    candidates.sort(
        key=lambda candidate: candidate[
            "interest_saved"
        ],
        reverse=True,
    )

    best = candidates[0]

    return {
        "recommended_loan": best,
        "candidates": candidates,
        "strategy": "maximum_interest_saving",
    }