"""Tests unitaires du convertisseur refactorisé (exercice 5).

Lancer :  pytest -v
"""

from convertisseur import convert


def test_eur_to_usd():
    # Question 1 : 10 EUR -> USD = 10 * 1.1 = 11.0
    assert convert(10, "EUR", "USD") == 11.0


def test_same_currency():
    # Question 2 : une devise vers elle-meme renvoie le meme montant
    assert convert(50, "EUR", "EUR") == 50
    assert convert(42, "USD", "USD") == 42


def test_negative_amount_returns_none():
    # Question 3 : un montant negatif renvoie None
    assert convert(-5, "EUR", "USD") is None
