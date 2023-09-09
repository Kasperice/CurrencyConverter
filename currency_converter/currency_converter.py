"""currency_converter module."""
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class CurrencyRatesAPIConnection:
    """Connection to CurrencyRatesAPI."""

    source_address = "https://api.apilayer.com/exchangerates_data/"

    def __init__(self):
        """Currency Rates API Connection initialization."""
        self.headers = {"apikey": os.environ.get("API_KEY")}

    def get_currency_names_and_symbols(self):
        """Get available currency names and their symbols."""
        response = requests.get(
            url=f"{self.source_address}symbols", headers=self.headers
        )
        if response.status_code == requests.codes.ok:
            return response.json()["symbols"]
        else:
            raise ValueError(
                f"Wrong status code. Expected: {requests.codes.ok}, Actual {response.status_code}"
            )

    def get_exchange_rate(self, first_currency: str, second_currency: str, date=None):
        """
        Get latest exchange date or on specified date.

        Args:
            first_currency: 'From' currency
            second_currency: 'To' currency
            date: Date of exchange rate, by default latest

        Returns:
            exchange rate for specified date
        """
        if not date:
            url = f"{self.source_address}latest?base={first_currency}&symbols={second_currency}"
        else:
            url = f"{self.source_address}{date}?base={first_currency}&symbols={second_currency}"

        response = requests.get(
            url=url,
            headers=self.headers,
        )

        if response.status_code == requests.codes.ok:
            return response.json().get("rates", {})[second_currency]
        else:
            raise ValueError(
                f"Wrong status code. Expected: {requests.codes.ok}, Actual {response.status_code}"
            )
