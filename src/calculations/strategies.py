def rank_loans_by_interest_rate(
    loans: list[dict],
) -> list[dict]:
    return sorted(
        loans,
        key=lambda loan: loan["interest_rate"],
        reverse=True,
    )


def rank_loans_by_outstanding(
    loans: list[dict],
) -> list[dict]:
    return sorted(
        loans,
        key=lambda loan: loan["outstanding_principal"],
        reverse=True,
    )


def rank_loans_by_emi(
    loans: list[dict],
) -> list[dict]:
    return sorted(
        loans,
        key=lambda loan: loan["emi"],
        reverse=True,
    )