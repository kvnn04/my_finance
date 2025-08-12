import enum

class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"
    transfer = "transfer"
