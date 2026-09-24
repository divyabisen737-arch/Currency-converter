"""Simple Currency Converter
- Fetches live rates from a free API (no key needed)
- Falls back to built-in rates if offline
Run: python currency_converter.py
"""
import json
import urllib.request

API_URL = "https://open.er-api.com/v6/latest/USD"

# Fallback rates (per 1 USD) - approximate, used only when offline
FALLBACK_RATES = {
    "USD": 1.0, "INR": 83.0, "EUR": 0.92, "GBP": 0.79,
    "JPY": 150.0, "AUD": 1.52, "CAD": 1.36, "AED": 3.67,
}


def get_rates():
    """Return (rates dict, source label)."""
    try:
        with urllib.request.urlopen(API_URL, timeout=5) as resp:
            data = json.load(resp)
        return data["rates"], "live"
    except Exception:
        return FALLBACK_RATES, "offline (approximate)"


def convert(amount, from_cur, to_cur, rates):
    """Convert via USD as the base currency."""
    return amount / rates[from_cur] * rates[to_cur]


def main():
    rates, source = get_rates()
    print(f"Currency Converter | rates: {source}")
    print("Examples: USD, INR, EUR, GBP, JPY  (type 'q' to quit)\n")

    while True:
        from_cur = input("From currency: ").strip().upper()
        if from_cur == "Q":
            break
        to_cur = input("To currency: ").strip().upper()
        if to_cur == "Q":
            break

        if from_cur not in rates or to_cur not in rates:
            print("Unknown currency code. Try again.\n")
            continue

        try:
            amount = float(input("Amount: "))
        except ValueError:
            print("Please enter a valid number.\n")
            continue

        result = convert(amount, from_cur, to_cur, rates)
        print(f"\n{amount:,.2f} {from_cur} = {result:,.2f} {to_cur}\n")


if __name__ == "__main__":
    main()
