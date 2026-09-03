from src.services.ai_context_service import (
    get_ai_financial_context,
)


def _build_decision_signals(
    financial_context: dict,
) -> dict:
    loans = financial_context.get("loans", [])

    portfolio = financial_context.get(
        "portfolio",
        {},
    )

    if not loans:
        return {
            "has_loans": False,
            "loan_count": 0,
            "total_outstanding_principal": 0.0,
            "total_emi": 0.0,
            "total_remaining_interest": 0.0,
            "total_remaining_repayment": 0.0,
            "highest_interest_loan": None,
            "highest_emi_loan": None,
            "largest_outstanding_loan": None,
            "priority_loan": None,
        }

    highest_interest_loan = max(
        loans,
        key=lambda loan: float(
            loan.get("interest_rate", 0)
        ),
    )

    highest_emi_loan = max(
        loans,
        key=lambda loan: float(
            loan.get("emi", 0)
        ),
    )

    largest_outstanding_loan = max(
        loans,
        key=lambda loan: float(
            loan.get(
                "outstanding_principal",
                0,
            )
        ),
    )

    priority_loan = {
        "loan_id": highest_interest_loan["loan_id"],
        "loan_name": highest_interest_loan[
            "loan_name"
        ],
        "interest_rate": float(
            highest_interest_loan[
                "interest_rate"
            ]
        ),
        "outstanding_principal": float(
            highest_interest_loan[
                "outstanding_principal"
            ]
        ),
        "emi": float(
            highest_interest_loan["emi"]
        ),
        "reason": "Highest interest rate",
    }

    total_remaining_interest = sum(
        float(
            loan.get("analysis", {}).get(
                "remaining_interest",
                0,
            )
        )
        for loan in loans
    )

    total_remaining_repayment = sum(
        float(
            loan.get("analysis", {}).get(
                "remaining_repayment",
                0,
            )
        )
        for loan in loans
    )

    return {
        "has_loans": True,
        "loan_count": len(loans),
        "total_outstanding_principal": float(
            portfolio.get(
                "total_outstanding_principal",
                0,
            )
        ),
        "total_emi": float(
            portfolio.get(
                "total_emi",
                0,
            )
        ),
        "total_remaining_interest": (
            total_remaining_interest
        ),
        "total_remaining_repayment": (
            total_remaining_repayment
        ),
        "highest_interest_loan": {
            "loan_id": highest_interest_loan[
                "loan_id"
            ],
            "loan_name": highest_interest_loan[
                "loan_name"
            ],
            "interest_rate": float(
                highest_interest_loan[
                    "interest_rate"
                ]
            ),
            "outstanding_principal": float(
                highest_interest_loan[
                    "outstanding_principal"
                ]
            ),
        },
        "highest_emi_loan": {
            "loan_id": highest_emi_loan[
                "loan_id"
            ],
            "loan_name": highest_emi_loan[
                "loan_name"
            ],
            "emi": float(
                highest_emi_loan["emi"]
            ),
            "outstanding_principal": float(
                highest_emi_loan[
                    "outstanding_principal"
                ]
            ),
        },
        "largest_outstanding_loan": {
            "loan_id": largest_outstanding_loan[
                "loan_id"
            ],
            "loan_name": largest_outstanding_loan[
                "loan_name"
            ],
            "outstanding_principal": float(
                largest_outstanding_loan[
                    "outstanding_principal"
                ]
            ),
            "interest_rate": float(
                largest_outstanding_loan[
                    "interest_rate"
                ]
            ),
        },
        "priority_loan": priority_loan,
    }


def build_ai_advisor_context(
    user_id: int,
) -> dict:
    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    financial_context = (
        get_ai_financial_context(user_id)
    )

    decisions = _build_decision_signals(
        financial_context
    )

    return {
        "user_id": user_id,
        "financial_context": financial_context,
        "decisions": decisions,
    }


def build_ai_advisor_prompt(
    user_id: int,
    question: str,
) -> str:
    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    if not isinstance(question, str):
        raise ValueError(
            "Question must be a string."
        )

    question = question.strip()

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

    context = build_ai_advisor_context(
        user_id
    )

    financial_context = context[
        "financial_context"
    ]

    decisions = context["decisions"]

    return f"""
You are LoanWise AI, a personal debt-management
assistant.

Your job is to help the user understand and manage
their loans using the verified financial information
provided below.

IMPORTANT RULES:
1. Use the supplied financial data as the source of truth.
2. Do not invent loan balances, rates, EMIs, dates,
   payments, or financial history.
3. Do not claim that a financial action is guaranteed
   to be beneficial.
4. Clearly distinguish calculated facts from suggestions.
5. When relevant, explain why a loan is being prioritized.
6. Keep the answer practical and easy to understand.
7. If the supplied information is insufficient to answer
   a question, say so instead of guessing.

USER ID:
{user_id}

FINANCIAL CONTEXT:
{financial_context}

DECISION SIGNALS:
{decisions}

USER QUESTION:
{question}

Provide a concise, useful financial response based on
the information above.
""".strip()


def get_ai_advisor_request(
    user_id: int,
    question: str,
) -> dict:
    if user_id <= 0:
        raise ValueError(
            "User ID must be positive."
        )

    if not isinstance(question, str):
        raise ValueError(
            "Question must be a string."
        )

    question = question.strip()

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

    context = build_ai_advisor_context(
        user_id
    )

    prompt = build_ai_advisor_prompt(
        user_id,
        question,
    )

    return {
        "user_id": user_id,
        "question": question,
        "context": context,
        "prompt": prompt,
    }