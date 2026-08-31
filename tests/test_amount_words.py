from src.utils.amount_words import amount_to_words


def test_zero_amount():
    assert amount_to_words(0) == "Rupees Zero Only"


def test_thousand():
    assert amount_to_words(5000) == "Rupees Five Thousand Only"


def test_lakh():
    assert amount_to_words(500000) == (
        "Rupees Five Lakh Only"
    )


def test_lakh_with_paise():
    assert amount_to_words(125000.50) == (
        "Rupees One Lakh Twenty Five Thousand "
        "and Fifty Paise Only"
    )


def test_crore():
    assert amount_to_words(10000000) == (
        "Rupees One Crore Only"
    )