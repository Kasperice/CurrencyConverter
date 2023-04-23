import requests
from dotenv import load_dotenv
import os


load_dotenv()


class CurrencyRates:
    source_address = "https://api.apilayer.com/exchangerates_data/"
    currency_names_json = "https://api.apilayer.com/exchangerates_data/symbols"

    def __init__(self):
        self.headers = {"apikey": os.environ.get("API_KEY")}
        response = requests.request(
            "GET", url=f"{self.currency_names_json}", headers=self.headers
        )
        if response.status_code == 200:
            self.names = response.json()

    def get_latest_rates(self, currency=None):
        response = requests.request(
            "GET", url=f"{self.source_address}latest", headers=self.headers
        )
        if currency:
            response = requests.request(
                "GET",
                url=f"{self.source_address}latest?symbols=&base={currency}",
                headers=self.headers,
            )
        if response.status_code == 200:
            return response.json().get("rates", {})

    def translate_currency_symbol(self, currency):
        return self.names["symbols"][currency]

    def get_latest_rate(self, first_currency, second_currency):
        response = requests.request(
            "GET",
            url=f"{self.source_address}latest?base={first_currency}&symbols={second_currency}",
            headers=self.headers,
        )
        if response.status_code == 200:
            return response.json().get("rates", {})[second_currency]

    def get_historical_rate(self, first_currency, second_currency, date):
        response = requests.request(
            "GET",
            f"{self.source_address}{date}?base={first_currency}&symbols={second_currency}",
            headers=self.headers,
        )
        if response.status_code == 200:
            return response.json().get("rates", {})[second_currency]
