

RATES = {"EUR": 1, "USD": 1.1, "GBP": 0.85}  # extensible : 1 ligne par devise


def convert(amount, from_currency, to_currency, rates=RATES):
    
    if amount < 0:
        return None
    if from_currency not in rates or to_currency not in rates:
        return None

    amount_in_eur = amount / rates[from_currency]
    return amount_in_eur * rates[to_currency]


if __name__ == "__main__":
    print(convert(10, "EUR", "USD"))   # 11.0
    print(convert(11, "USD", "EUR"))   # 10.0
    print(convert(50, "EUR", "EUR"))   # 50.0
    print(convert(-5, "EUR", "USD"))   # None
