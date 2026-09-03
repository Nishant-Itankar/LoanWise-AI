import pytest

from src.services.ai_advisor_service import (
    build_ai_advisor_context,
    build_ai_advisor_prompt,
    get_ai_advisor_request,
)


def test_build_ai_advisor_context(monkeypatch):
    financial_context = {
        "user_id": 67,
        "portfolio": {
            "loan_count": 1,
            "total_outstanding_principal": 100000.0,
            "total_emi": 5000.0,
        },
        "loans": [
            {
                "loan_id": 1,
                "loan_name": "Test Loan",
                "interest_rate": 12.0,
                "outstanding_principal": 100000.0,
                "emi": 5000.0,
                "analysis": {
                    "remaining_interest": 20000.0,
                    "remaining_repayment": 120000.0,
                },
            }
        ],
    }

    monkeypatch.setattr(
        "src.services.ai_advisor_service.get_ai_financial_context",
        lambda user_id: financial_context,
    )

    result = build_ai_advisor_context(67)

    assert result["user_id"] == 67
    assert result["financial_context"] == financial_context
    assert result["decisions"]["has_loans"] is True
    assert (
        result["decisions"]["priority_loan"]["loan_id"]
        == 1
    )


def test_build_ai_advisor_context_rejects_invalid_user():
    with pytest.raises(
        ValueError,
        match="User ID must be positive.",
    ):
        build_ai_advisor_context(0)


def test_build_ai_advisor_prompt(monkeypatch):
    financial_context = {
        "user_id": 67,
        "portfolio": {
            "loan_count": 1,
            "total_outstanding_principal": 100000.0,
            "total_emi": 5000.0,
        },
        "loans": [
            {
                "loan_id": 1,
                "loan_name": "Test Loan",
                "interest_rate": 12.0,
                "outstanding_principal": 100000.0,
                "emi": 5000.0,
                "analysis": {
                    "remaining_interest": 20000.0,
                    "remaining_repayment": 120000.0,
                },
            }
        ],
    }

    monkeypatch.setattr(
        "src.services.ai_advisor_service.get_ai_financial_context",
        lambda user_id: financial_context,
    )

    prompt = build_ai_advisor_prompt(
        67,
        "Which loan should I prioritize?",
    )

    assert "LoanWise AI" in prompt
    assert "Which loan should I prioritize?" in prompt
    assert "FINANCIAL CONTEXT:" in prompt
    assert "DECISION SIGNALS:" in prompt
    assert "Do not invent" in prompt
    assert "Test Loan" in prompt


def test_build_ai_advisor_prompt_rejects_invalid_user():
    with pytest.raises(
        ValueError,
        match="User ID must be positive.",
    ):
        build_ai_advisor_prompt(
            0,
            "What should I do?",
        )


def test_build_ai_advisor_prompt_rejects_non_string_question():
    with pytest.raises(
        ValueError,
        match="Question must be a string.",
    ):
        build_ai_advisor_prompt(
            67,
            None,
        )


def test_build_ai_advisor_prompt_rejects_empty_question():
    with pytest.raises(
        ValueError,
        match="Question cannot be empty.",
    ):
        build_ai_advisor_prompt(
            67,
            "   ",
        )


def test_get_ai_advisor_request(monkeypatch):
    financial_context = {
        "user_id": 67,
        "portfolio": {
            "loan_count": 1,
            "total_outstanding_principal": 100000.0,
            "total_emi": 5000.0,
        },
        "loans": [
            {
                "loan_id": 1,
                "loan_name": "Test Loan",
                "interest_rate": 12.0,
                "outstanding_principal": 100000.0,
                "emi": 5000.0,
                "analysis": {
                    "remaining_interest": 20000.0,
                    "remaining_repayment": 120000.0,
                },
            }
        ],
    }

    monkeypatch.setattr(
        "src.services.ai_advisor_service.get_ai_financial_context",
        lambda user_id: financial_context,
    )

    result = get_ai_advisor_request(
        67,
        "Which loan should I prioritize?",
    )

    assert result["user_id"] == 67
    assert (
        result["question"]
        == "Which loan should I prioritize?"
    )
    assert "context" in result
    assert "prompt" in result
    assert (
        "Which loan should I prioritize?"
        in result["prompt"]
    )


def test_get_ai_advisor_request_strips_question(
    monkeypatch,
):
    financial_context = {
        "user_id": 67,
        "portfolio": {
            "loan_count": 0,
            "total_outstanding_principal": 0.0,
            "total_emi": 0.0,
        },
        "loans": [],
    }

    monkeypatch.setattr(
        "src.services.ai_advisor_service.get_ai_financial_context",
        lambda user_id: financial_context,
    )

    result = get_ai_advisor_request(
        67,
        "  What should I do?  ",
    )

    assert (
        result["question"]
        == "What should I do?"
    )


def test_ai_advisor_context_contains_decisions(
    monkeypatch,
):
    financial_context = {
        "user_id": 67,
        "portfolio": {
            "loan_count": 1,
            "total_outstanding_principal": 200000.0,
            "total_emi": 10000.0,
        },
        "loans": [
            {
                "loan_id": 65,
                "loan_name": "Home Loan",
                "interest_rate": 12.0,
                "outstanding_principal": 200000.0,
                "emi": 10000.0,
                "analysis": {
                    "remaining_interest": 30000.0,
                    "remaining_repayment": 230000.0,
                },
            }
        ],
    }

    monkeypatch.setattr(
        "src.services.ai_advisor_service.get_ai_financial_context",
        lambda user_id: financial_context,
    )

    result = build_ai_advisor_context(67)

    priority = result["decisions"][
        "priority_loan"
    ]

    assert priority["loan_id"] == 65
    assert priority["interest_rate"] == 12.0
    assert (
        priority["reason"]
        == "Highest interest rate"
    )