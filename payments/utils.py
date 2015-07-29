
from decimal import Decimal, ROUND_UP


def format_amount_to_pay(amount_to_pay):
    """

    >>> format_amount_to_pay(12.345)
    1235
    """
    amount_to_pay = Decimal(amount_to_pay)\
        .quantize(Decimal("0.00"), rounding=ROUND_UP)
    amount_to_pay = "%.2f" % amount_to_pay
    amount_to_pay = ''.join(amount_to_pay.split('.'))
    amount_to_pay = int(amount_to_pay)
    return amount_to_pay
