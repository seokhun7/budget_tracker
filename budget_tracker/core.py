from collections import defaultdict
from decimal import Decimal

from .utils import format_date, month_key, parse_date, to_decimal

ZERO_AMOUNT = Decimal("0.00")
POSITIVE_SIGN = Decimal("1")
NEGATIVE_SIGN = Decimal("-1")


class Transaction:
    """
    Represents a single income or expense transaction.

    :param amount: Positive transaction amount.
    :param category: Transaction category.
    :param transaction_date: Date as "YYYY-MM-DD"
            or as a datetime.date.
    :param description: Optional memo for the transaction.

    :ivar amount: Validated positive amount.
    :ivar category: Normalized name of the category.
    :ivar transaction_date: Normalized transaction date.
    :ivar description: Human-readable transaction memo.
    """

    ALLOWED_CATEGORIES = None
    TRANSACTION_TYPE = "transaction"
    SIGN = POSITIVE_SIGN

    def __init__(self, amount, category, transaction_date, description=""):
        """
        Initialize a validated transaction.

        :param amount: Positive transaction amount.
        :param category: Transaction category.
        :param transaction_date: Date as "YYYY-MM-DD"
            or as a datetime.date.
        :param description: Optional memo for the transaction.
        """
        self.amount = self._validate_amount(amount)
        self.category = self._validate_category(category)
        self.transaction_date = parse_date(transaction_date)
        self.description = self._validate_description(description)

    def signed_amount(self):
        """
        Get the amount with the sign of income or expense applied.

        :return: Signed Decimal amount.

        >>> Transaction(1000, "general", "2026-05-01").signed_amount()
        Decimal('1000.00')
        """
        return self.amount * self.SIGN

    def is_in_month(self, year, month):
        """
        Determine if the transaction falls within a specified month.

        :param year: Four-digit year.
        :param month: Month number ranging from 1 to 12.
        :return: True if the transaction matches the requested month.
        """
        month_key(year, month)
        return (
            self.transaction_date.year == year
            and self.transaction_date.month == month
        )

    def to_dict(self):
        """
        Convert the transaction into a dictionary format.

        :return: Dictionary containing type, amount, category, date, and memo.
        """
        return {
            "type": self.TRANSACTION_TYPE,
            "amount": self.amount,
            "signed_amount": self.signed_amount(),
            "category": self.category,
            "date": format_date(self.transaction_date),
            "description": self.description,
        }

    def matches_category(self, category):
        """
        Check if the transaction matches a specific category.

        :param category: The category name to compare against.
        :return: True if the normalized category names are the same.
        """
        return self.category == self._normalize_text(category, "category")

    def _validate_amount(self, amount):
        decimal_amount = to_decimal(amount)
        if decimal_amount <= ZERO_AMOUNT:
            raise ValueError("amount must be greater than zero")
        return decimal_amount

    def _validate_category(self, category):
        normalized_category = self._normalize_text(category, "category")
        allowed_categories = self.ALLOWED_CATEGORIES

        if (
            allowed_categories is not None
            and normalized_category not in allowed_categories
        ):
            allowed_text = ", ".join(sorted(allowed_categories))
            raise ValueError(f"category must be one of: {allowed_text}")

        return normalized_category

    def _validate_description(self, description):
        if description is None:
            return ""

        if not isinstance(description, str):
            raise TypeError("description must be a string")

        return description.strip()

    def _normalize_text(self, value, field_name):
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")

        normalized_value = value.strip().lower()

        if not normalized_value:
            raise ValueError(f"{field_name} must not be empty")

        return normalized_value


class BudgetTracker:
    """
    Handles transactions and creates reports based on categories or monthly data.

    :param transactions: Optional iterable of transactions to preload.
    :ivar transactions: An ordered list of recorded transactions.
    """

    def __init__(self, transactions=None):
        """
        Set up a budget tracker.

        :param transactions: Optional iterable of transactions to preload.
        """
        self.transactions = []

        if transactions is not None:
            for transaction in transactions:
                self.add_transaction(transaction)

    def add_transaction(self, transaction):
        """
        Include a transaction object into the tracker.

        :param transaction: Instance of Transaction or its subclass.
        :return: The transaction that was added.
        :raises TypeError: If the input isn't a transaction.
        """
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be a Transaction instance")

        self.transactions.append(transaction)
        return transaction

    def add_income(self, amount, category, transaction_date, description=""):
        """
        Create and add an income transaction.

        :param amount: Positive income amount.
        :param category: Income category.
        :param transaction_date: Date as "YYYY-MM-DD"
        or datetime.date.
        :param description: Optional memo.
        :return: The created Income instance.
        """
        from .subclass import Income

        income = Income(amount, category, transaction_date, description)
        return self.add_transaction(income)

    def add_expense(self, amount, category, transaction_date, description=""):
        """
        Create and add an expense transaction.

        :param amount: Positive expense amount.
        :param category: Expense category.
        :param transaction_date: Date as "YYYY-MM-DD"
        or datetime.date.
        :param description: Optional memo.
        :return: The created Expense instance.
        """
        from .subclass import Expense

        expense = Expense(amount, category, transaction_date, description)
        return self.add_transaction(expense)

    def daily_records(self, target_date):
        """
        Return transactions recorded on a specific date.

        :param target_date: Date in the format "YYYY-MM-DD" or datetime.date.
        :return: List of transactions for that date.
        """
        normalized_date = parse_date(target_date)

        return [
            transaction
            for transaction in self.transactions
            if transaction.transaction_date == normalized_date
        ]

    def category_summary(self, year=None, month=None):
        """
        Summarize totals for each category.

        :param year: Optional filter by year.
        :param month: Optional filter by month, used with year.
        :return: Dictionary keyed by category with signed totals.
        """
        summary = defaultdict(lambda: ZERO_AMOUNT)

        for transaction in self._filtered_transactions(year, month):
            summary[transaction.category] += transaction.signed_amount()

        return dict(summary)

    def monthly_report(self, year, month):
        """
        Generate a report showing income, expenses, and balance for a month.

        :param year: Four-digit year.
        :param month: Month number from 1 to 12.
        :return: Dictionary containing month, totals, category totals, and records.
        """
        key = month_key(year, month)
        transactions = self._filtered_transactions(year, month)

        income_total = sum(
            (
                transaction.amount
                for transaction in transactions
                if transaction.signed_amount() > ZERO_AMOUNT
            ),
            ZERO_AMOUNT,
        )

        expense_total = sum(
            (
                transaction.amount
                for transaction in transactions
                if transaction.signed_amount() < ZERO_AMOUNT
            ),
            ZERO_AMOUNT,
        )

        return {
            "month": key,
            "income": income_total,
            "expense": expense_total,
            "balance": income_total - expense_total,
            "categories": self.category_summary(year, month),
            "transactions": [
                transaction.to_dict()
                for transaction in transactions
            ],
        }

    def _filtered_transactions(self, year=None, month=None):
        if year is None and month is None:
            return list(self.transactions)

        if year is None or month is None:
            raise ValueError("year and month must be provided together")

        month_key(year, month)

        return [
            transaction
            for transaction in self.transactions
            if transaction.is_in_month(year, month)
        ]
