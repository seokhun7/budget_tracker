from decimal import Decimal

from .core import NEGATIVE_SIGN, POSITIVE_SIGN, Transaction
from .utils import CURRENCY_DECIMAL_PLACES


class Income(Transaction):
    """
    This class represents money received by the household.

    :param amount: The income amount, which should be positive.
    :param category: The category of the income.
    :param transaction_date: The date in the format "YYYY-MM-DD"
            or as datetime.date.
    :param description: An optional memo for the income.
    """

    ALLOWED_CATEGORIES = frozenset(
        {"allowance", "bonus", "gift", "salary"}
    )
    TRANSACTION_TYPE = "income"
    SIGN = POSITIVE_SIGN

    def __init__(
        self,
        amount,
        category,
        transaction_date,
        description="",
    ):
        """
        Sets up an income transaction.

        :param amount: Positive income amount.
        :param category: Income category.
        :param transaction_date: Date as "YYYY-MM-DD" or datetime.date.
        :param description: Optional memo.
        """
        super().__init__(
            amount,
            category,
            transaction_date,
            description,
        )

    def tax_estimate(self, rate):
        """
        Calculates the estimated tax for the income amount.

        :param rate: Tax rate ranging from 0 to 1.
        :return: Estimated tax amount.
        """
        decimal_rate = self._validate_rate(rate)

        return (
            self.amount * decimal_rate
        ).quantize(CURRENCY_DECIMAL_PLACES)

    def net_amount(self, tax_rate=0):
        """
        Gives the income after accounting for estimated tax.

        :param tax_rate: Tax rate between 0 and 1.
        :return: Income amount after tax.
        """
        return self.amount - self.tax_estimate(tax_rate)

    def source_label(self):
        """
        Returns a human-readable label for the income source.

        :return: A label combining transaction type and category.
        """
        return f"{self.TRANSACTION_TYPE}:{self.category}"

    def _validate_rate(self, rate):
        valid_rate_types = (Decimal, int, float)

        if isinstance(rate, bool) or not isinstance(
            rate,
            valid_rate_types,
        ):
            raise TypeError("rate must be a number")

        decimal_rate = Decimal(str(rate))

        if decimal_rate < 0 or decimal_rate > 1:
            raise ValueError("rate must be between 0 and 1")

        return decimal_rate


class Expense(Transaction):
    """
    This class represents money spent by the household.

    :param amount: The expense amount, which should be positive.
    :param category: The category of the expense.
    :param transaction_date: The date in the format "YYYY-MM-DD"
            or as datetime.date.
    :param description: An optional memo for the expense.
    """

    ALLOWED_CATEGORIES = frozenset(
        {
            "education",
            "food",
            "health",
            "housing",
            "transport",
            "utility",
        }
    )
    TRANSACTION_TYPE = "expense"
    SIGN = NEGATIVE_SIGN

    def __init__(
        self,
        amount,
        category,
        transaction_date,
        description="",
    ):
        """
        Sets up an expense transaction.

        :param amount: Positive expense amount.
        :param category: Expense category.
        :param transaction_date: Date as "YYYY-MM-DD" or datetime.date.
        :param description: Optional memo.
        """
        super().__init__(
            amount,
            category,
            transaction_date,
            description,
        )

    def is_essential(self):
        """
        Determines if the category of expense is essential.

        :return: True for essential household expense categories.
        """
        return self.category in {
            "food",
            "health",
            "housing",
            "utility",
        }

    def budget_status(self, budget_limit):
        """
        Compares this expense against a given budget limit.

        :param budget_limit: Positive budget amount.
        :return: Either "within_budget" or "over_budget".
        """
        limit = self._validate_amount(budget_limit)

        if self.amount <= limit:
            return "within_budget"

        return "over_budget"

    def spending_label(self):
        """
        Returns a human-readable label for spending.

        :return: A label combining transaction type and category.
        """
        return f"{self.TRANSACTION_TYPE}:{self.category}"
