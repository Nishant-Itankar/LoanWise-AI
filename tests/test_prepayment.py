import pytest
from datetime import date

from src.calculations.prepayment import (
    analyze_prepayment,
)

# from src.services.prepayment_service import (
#     get_loan_prepayment_history,
# )


from src.services.prepayment_service import (
    record_loan_prepayment,
    get_loan_prepayment_history,
)

def test_prepayment_reduces_principal():
    result = analyze_prepayment(
        outstanding_principal=400000,
        annual_interest_rate=10,
        remaining_tenure_months=48,
        prepayment_amount=100000,
    )

    assert result["principal_before"] == 400000.00
    assert result["principal_after"] == 300000.00


def test_prepayment_saves_interest():
    result = analyze_prepayment(
        outstanding_principal=400000,
        annual_interest_rate=10,
        remaining_tenure_months=48,
        prepayment_amount=100000,
    )

    assert result["interest_saved"] > 0


def test_prepayment_rejects_excess_amount():
    with pytest.raises(ValueError):
        analyze_prepayment(
            outstanding_principal=400000,
            annual_interest_rate=10,
            remaining_tenure_months=48,
            prepayment_amount=500000,
        )


def test_get_loan_prepayment_history(
    monkeypatch,
):
    loan = {
        "id": 171,
        "status": "active",
    }

    monkeypatch.setattr(
        "src.services.prepayment_service.get_loan_by_id",
        lambda loan_id: loan,
    )

    monkeypatch.setattr(
        "src.services.prepayment_service.get_prepayments_by_loan",
        lambda loan_id: [
            {
                "id": 1,
                "loan_id": 171,
                "payment_date": date(2026, 9, 3),
                "amount": 20000,
                "principal_before": 400000,
                "principal_after": 380000,
                "interest_saved": 3436.36,
                "tenure_reduced_months": 0,
                "strategy": "manual_prepayment",
                "notes": None,
            }
        ],
    )

    result = get_loan_prepayment_history(171)

    assert len(result) == 1
    assert result[0]["amount"] == 20000
    assert result[0]["principal_before"] == 400000
    assert result[0]["principal_after"] == 380000
    assert result[0]["interest_saved"] == 3436.36
    
def test_full_prepayment_closes_loan(monkeypatch):
    loan = {
        "id": 171,
        "status": "active",
        "outstanding_principal": 20000,
        "interest_rate": 8,
        "remaining_tenure_months": 10,
    }

    monkeypatch.setattr(
        "src.services.prepayment_service.get_loan_by_id",
        lambda loan_id: loan,
    )

    def fake_create(**kwargs):
        return (
            {
                "id": 2,
                "loan_id": kwargs["loan_id"],
                "amount": kwargs["prepayment_amount"],
            },
            {
                **loan,
                "outstanding_principal": 0,
                "status": "closed",
                "remaining_tenure_months": 0,
            },
        )

    monkeypatch.setattr(
        "src.services.prepayment_service."
        "create_prepayment_and_update_loan",
        fake_create,
    )

    result = record_loan_prepayment(
        loan_id=171,
        payment_date=date(2026, 9, 3),
        prepayment_amount=20000,
    )

    assert result["loan"]["outstanding_principal"] == 0
    assert result["loan"]["status"] == "closed"


def test_prepayment_rejects_excess_amount(monkeypatch):
    loan = {
        "id": 171,
        "status": "active",
        "outstanding_principal": 20000,
        "interest_rate": 8,
        "remaining_tenure_months": 10,
    }

    monkeypatch.setattr(
        "src.services.prepayment_service.get_loan_by_id",
        lambda loan_id: loan,
    )

    with pytest.raises(ValueError):
        record_loan_prepayment(
            loan_id=171,
            payment_date=date(2026, 9, 3),
            prepayment_amount=25000,
        )


def test_closed_loan_rejects_prepayment(monkeypatch):
    loan = {
        "id": 171,
        "status": "closed",
        "outstanding_principal": 20000,
        "interest_rate": 8,
        "remaining_tenure_months": 10,
    }

    monkeypatch.setattr(
        "src.services.prepayment_service.get_loan_by_id",
        lambda loan_id: loan,
    )

    with pytest.raises(ValueError):
        record_loan_prepayment(
            loan_id=171,
            payment_date=date(2026, 9, 3),
            prepayment_amount=5000,
        )


def test_multiple_prepayments_accumulate(monkeypatch):
    loan = {
        "id": 171,
        "status": "active",
        "outstanding_principal": 400000,
        "interest_rate": 8,
        "remaining_tenure_months": 48,
    }

    monkeypatch.setattr(
        "src.services.prepayment_service.get_loan_by_id",
        lambda loan_id: loan,
    )

    captured = []

    def fake_create(**kwargs):
        captured.append(kwargs)

        return (
            {
                "id": len(captured),
                "loan_id": kwargs["loan_id"],
                "amount": kwargs["prepayment_amount"],
            },
            {
                **loan,
                "outstanding_principal": kwargs["outstanding_balance"],
            },
        )

    monkeypatch.setattr(
        "src.services.prepayment_service."
        "create_prepayment_and_update_loan",
        fake_create,
    )

    record_loan_prepayment(
        loan_id=171,
        payment_date=date(2026, 9, 3),
        prepayment_amount=20000,
    )

    loan["outstanding_principal"] = 380000

    record_loan_prepayment(
        loan_id=171,
        payment_date=date(2026, 10, 3),
        prepayment_amount=30000,
    )

    assert len(captured) == 2
    assert captured[0]["prepayment_amount"] == 20000
    assert captured[1]["prepayment_amount"] == 30000


def test_prepayment_history_is_newest_first(monkeypatch):
    loan = {
        "id": 171,
        "status": "active",
    }

    monkeypatch.setattr(
        "src.services.prepayment_service.get_loan_by_id",
        lambda loan_id: loan,
    )

    monkeypatch.setattr(
        "src.services.prepayment_service.get_prepayments_by_loan",
        lambda loan_id: [
            {
                "id": 2,
                "loan_id": 171,
                "payment_date": date(2026, 10, 3),
                "amount": 30000,
                "principal_before": 380000,
                "principal_after": 350000,
                "interest_saved": 4000,
                "tenure_reduced_months": 2,
                "strategy": "manual_prepayment",
                "notes": None,
            },
            {
                "id": 1,
                "loan_id": 171,
                "payment_date": date(2026, 9, 3),
                "amount": 20000,
                "principal_before": 400000,
                "principal_after": 380000,
                "interest_saved": 3436.36,
                "tenure_reduced_months": 0,
                "strategy": "manual_prepayment",
                "notes": None,
            },
        ],
    )

    result = get_loan_prepayment_history(171)

    assert len(result) == 2
    assert result[0]["id"] == 2
    assert result[1]["id"] == 1