import requests
from dotenv import load_dotenv
import os


load_dotenv()


class CurrencyRatesAPIConnection:
    source_address = "https://api.apilayer.com/exchangerates_data/"

    def __init__(self):
        self.headers = {"apikey": os.environ.get("API_KEY")}

    def get_currency_names_and_symbols(self):
        response = requests.request(
            "GET", url=f"{self.source_address}symbols", headers=self.headers
        )
        if response.status_code == 200:
            return response.json()["symbols"]
        else:
            raise ValueError(
                f"Wrong status code. Expected: 200, Actual {response.status_code}"
            )

    def get_exchange_rate(self, first_currency, second_currency, date=None):
        if date is None:
            url = f"{self.source_address}latest?base={first_currency}&symbols={second_currency}"
        else:
            url = f"{self.source_address}{date}?base={first_currency}&symbols={second_currency}"

        response = requests.request(
            method="GET",
            url=url,
            headers=self.headers,
        )

        if response.status_code == 200:
            return response.json().get("rates", {})[second_currency]
        else:
            raise ValueError(
                f"Wrong status code. Expected: 200, Actual {response.status_code}"
            )
