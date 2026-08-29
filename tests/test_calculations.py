from src.calculations.amortization import (
    generate_amortization_schedule,
)
from src.calculations.emi import (
    calculate_emi,
    calculate_total_interest,
    calculate_total_repayment,
)


def test_zero_interest_emi():
    emi = calculate_emi(
        principal=120000,
        annual_interest_rate=0,
        tenure_months=12,
    )

    assert emi == 10000.00


def test_standard_emi():
    emi = calculate_emi(
        principal=1000000,
        annual_interest_rate=10,
        tenure_months=240,
    )

    assert 9500 < emi < 9700


def test_total_repayment():
    repayment = calculate_total_repayment(
        principal=120000,
        annual_interest_rate=0,
        tenure_months=12,
    )

    assert repayment == 120000.00


def test_total_interest():
    interest = calculate_total_interest(
        principal=120000,
        annual_interest_rate=0,
        tenure_months=12,
    )

    assert interest == 0.00


def test_amortization_schedule():
    schedule = generate_amortization_schedule(
        principal=120000,
        annual_interest_rate=0,
        tenure_months=12,
    )

    assert len(schedule) == 12

    assert schedule[0]["principal"] == 10000.00
    assert schedule[-1]["remaining_balance"] == 0.00


def test_amortization_principal_total():
    schedule = generate_amortization_schedule(
        principal=120000,
        annual_interest_rate=10,
        tenure_months=12,
    )

    total_principal = sum(
        row["principal"]
        for row in schedule
    )

    assert round(total_principal, 2) == 120000.00