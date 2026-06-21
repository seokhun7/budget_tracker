"""Unit tests for the budget_tracker package."""

from datetime import datetime
from decimal import Decimal

import pytest

from budget_tracker import (
    BudgetTracker,
    Expense,
    Income,
    Transaction,
)
from budget_tracker.utils import (
    format_currency,
    format_date,
    month_key,
    parse_date,
)


def test_income_addition_records_positive_signed_amount():
    tracker = BudgetTracker()

    income = tracker.add_income(
        3000000,
        "salary",
        "2026-05-01",
        "monthly pay",
    )

    assert isinstance(income, Income)
    assert income.signed_amount() == Decimal("3000000.00")
    assert tracker.transactions == [income]


def test_expense_addition_records_negative_signed_amount():
    tracker = BudgetTracker()

    expense = tracker.add_expense(
        12000,
        "food",
        "2026-05-02",
        "lunch",
    )

    assert isinstance(expense, Expense)
    assert expense.signed_amount() == Decimal("-12000.00")


def test_daily_records_returns_only_matching_date():
    tracker = BudgetTracker()

    first = tracker.add_income(
        10000,
        "gift",
        "2026-05-03",
    )

    tracker.add_expense(
        5000,
        "transport",
        "2026-05-04",
    )

    records = tracker.daily_records("2026-05-03")

    assert records == [first]


def test_category_summary_groups_signed_totals_by_category():
    tracker = BudgetTracker()

    tracker.add_income(
        100000,
        "bonus",
        "2026-05-05",
    )

    tracker.add_expense(
        20000,
        "food",
        "2026-05-05",
    )

    tracker.add_expense(
        5000,
        "food",
        "2026-05-06",
    )

    summary = tracker.category_summary()

    assert summary["bonus"] == Decimal("100000.00")
    assert summary["food"] == Decimal("-25000.00")


def test_monthly_report_calculates_income_expense_and_balance():
    tracker = BudgetTracker()

    tracker.add_income(
        2000000,
        "salary",
        "2026-05-01",
    )

    tracker.add_expense(
        800000,
        "housing",
        "2026-05-02",
    )

    tracker.add_expense(
        50000,
        "utility",
        "2026-05-03",
    )

    tracker.add_income(
        100000,
        "gift",
        "2026-06-01",
    )

    report = tracker.monthly_report(2026, 5)

    assert report["month"] == "2026-05"
    assert report["income"] == Decimal("2000000.00")
    assert report["expense"] == Decimal("850000.00")
    assert report["balance"] == Decimal("1150000.00")
    assert len(report["transactions"]) == 3


def test_transaction_to_dict_contains_serialized_fields():
    transaction = Transaction(
        1000,
        "general",
        "2026-05-07",
        "memo",
    )

    result = transaction.to_dict()

    assert result["type"] == "transaction"
    assert result["amount"] == Decimal("1000.00")
    assert result["date"] == "2026-05-07"
    assert result["description"] == "memo"


def test_income_negative_amount_raises_error():
    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        Income(
            -1,
            "salary",
            "2026-05-01",
        )


def test_expense_empty_category_raises_error():
    with pytest.raises(
        ValueError,
        match="category must not be empty",
    ):
        Expense(
            1000,
            " ",
            "2026-05-01",
        )


def test_income_invalid_category_raises_error():
    with pytest.raises(
        ValueError,
        match="category must be one of",
    ):
        Income(
            1000,
            "lottery",
            "2026-05-01",
        )


def test_transaction_invalid_date_type_raises_error():
    with pytest.raises(
        TypeError,
        match="date must be",
    ):
        Transaction(
            1000,
            "general",
            object(),
        )


def test_add_transaction_invalid_type_raises_error():
    tracker = BudgetTracker()

    with pytest.raises(
        TypeError,
        match="Transaction instance",
    ):
        tracker.add_transaction(
            {"amount": 1000}
        )


def test_utils_month_key_and_currency_formatting():
    assert month_key(2026, 5) == "2026-05"

    assert (
        format_currency("1234.5")
        == "KRW 1,234.50"
    )


def test_income_tax_estimate_and_net_amount():
    income = Income(
        100000,
        "bonus",
        "2026-05-10",
    )

    assert (
        income.tax_estimate(Decimal("0.1"))
        == Decimal("10000.00")
    )

    assert (
        income.net_amount(0.1)
        == Decimal("90000.00")
    )

    assert income.source_label() == "income:bonus"


def test_income_invalid_tax_rate_raises_error():
    income = Income(
        100000,
        "bonus",
        "2026-05-10",
    )

    with pytest.raises(
        ValueError,
        match="between 0 and 1",
    ):
        income.tax_estimate(2)


def test_expense_budget_status_and_essential_label():
    expense = Expense(
        50000,
        "utility",
        "2026-05-11",
    )

    assert expense.is_essential() is True
    assert expense.budget_status(60000) == "within_budget"
    assert expense.budget_status(40000) == "over_budget"
    assert expense.spending_label() == "expense:utility"


def test_monthly_summary_requires_year_and_month_together():
    tracker = BudgetTracker()

    with pytest.raises(
        ValueError,
        match="year and month",
    ):
        tracker.category_summary(year=2026)


def test_date_helpers_accept_datetime_and_reject_empty_string():
    target = datetime(
        2026,
        5,
        12,
        8,
        30,
    )

    assert (
        parse_date(target).isoformat()
        == "2026-05-12"
    )

    assert (
        format_date(target)
        == "2026-05-12"
    )

    with pytest.raises(
        ValueError,
        match="date must not be empty",
    ):
        parse_date(" ")


def test_invalid_money_and_month_inputs_raise_error():
    with pytest.raises(
        ValueError,
        match="amount must be numeric",
    ):
        Transaction(
            "abc",
            "general",
            "2026-05-01",
        )

    with pytest.raises(
        ValueError,
        match="month must be between",
    ):
        month_key(2026, 13)
