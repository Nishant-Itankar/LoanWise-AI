ONES = [
    "",
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Eleven",
    "Twelve",
    "Thirteen",
    "Fourteen",
    "Fifteen",
    "Sixteen",
    "Seventeen",
    "Eighteen",
    "Nineteen",
]


TENS = [
    "",
    "",
    "Twenty",
    "Thirty",
    "Forty",
    "Fifty",
    "Sixty",
    "Seventy",
    "Eighty",
    "Ninety",
]


def number_to_words(number: int) -> str:
    if number == 0:
        return "Zero"

    if number < 0:
        return f"Minus {number_to_words(abs(number))}"

    if number < 20:
        return ONES[number]

    if number < 100:
        return TENS[number // 10] + (
            f" {ONES[number % 10]}"
            if number % 10
            else ""
        )

    if number < 1000:
        return (
            f"{ONES[number // 100]} Hundred"
            + (
                f" {number_to_words(number % 100)}"
                if number % 100
                else ""
            )
        )

    if number < 100000:
        return (
            f"{number_to_words(number // 1000)} Thousand"
            + (
                f" {number_to_words(number % 1000)}"
                if number % 1000
                else ""
            )
        )

    if number < 10000000:
        return (
            f"{number_to_words(number // 100000)} Lakh"
            + (
                f" {number_to_words(number % 100000)}"
                if number % 100000
                else ""
            )
        )

    return (
        f"{number_to_words(number // 10000000)} Crore"
        + (
            f" {number_to_words(number % 10000000)}"
            if number % 10000000
            else ""
        )
    )


def amount_to_words(amount: float) -> str:
    amount = round(float(amount), 2)

    rupees = int(amount)
    paise = int(round((amount - rupees) * 100))

    result = f"Rupees {number_to_words(rupees)}"

    if paise:
        result += f" and {number_to_words(paise)} Paise"

    return f"{result} Only"