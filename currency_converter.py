import requests


class CurrencyRates:
    source_address = "https://api.ratesapi.io/api/"
    currency_names_json = "https://openexchangerates.org/api/currencies.json"

    def __init__(self):
        response = requests.get(f"{self.currency_names_json}")
        if response.status_code == 200:
            self.names = response.json()

    def get_latest_rates(self, currency=None):
        response = requests.get(f"{self.source_address}latest")
        if currency:
            response = requests.get(f"{self.source_address}latest?base={currency}")
        if response.status_code == 200:
            return response.json().get('rates', {})

    def translate_currency_symbol(self, currency):
        return self.names[currency]

    def get_latest_rate(self, first_currency, second_currency):
        response = requests.get(f"{self.source_address}latest?base={first_currency}&symbols={second_currency}")
        if response.status_code == 200:
            return response.json().get('rates', {})[second_currency]

    def get_historical_rate(self, first_currency, second_currency, date):
        response = requests.get(f"{self.source_address}{date}?base={first_currency}&symbols={second_currency}")
        if response.status_code == 200:
            return response.json().get('rates', {})[second_currency]

