from src.calculations.payment import calculate_payment


def test_payment_calculates_interest_and_principal():
    result = calculate_payment(
        outstanding_principal=400000,
        annual_interest_rate=8,
        emi=11500,
    )

    assert result["emi_amount"] == 11500.00
    assert result["interest_component"] == 2666.67
    assert result["principal_component"] == 8833.33
    assert result["outstanding_balance"] == 391166.67


def test_payment_with_extra_payment():
    result = calculate_payment(
        outstanding_principal=400000,
        annual_interest_rate=8,
        emi=11500,
        extra_payment=20000,
    )

    assert result["extra_payment"] == 20000.00
    assert result["total_principal_reduction"] == 28833.33
    assert result["outstanding_balance"] == 371166.67


def test_payment_rejects_negative_extra_payment():
    try:
        calculate_payment(
            outstanding_principal=400000,
            annual_interest_rate=8,
            emi=11500,
            extra_payment=-1000,
        )
        assert False
    except ValueError:
        assert True


def test_payment_with_zero_outstanding():
    result = calculate_payment(
        outstanding_principal=0,
        annual_interest_rate=8,
        emi=11500,
    )

    assert result["outstanding_balance"] == 0.0
    assert result["principal_component"] == 0.0
    assert result["interest_component"] == 0.0