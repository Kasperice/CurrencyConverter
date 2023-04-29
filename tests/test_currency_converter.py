import pytest
import responses

from currency_converter import CurrencyRatesAPIConnection


@responses.activate
def test_get_currency_names_and_symbols():
    c = CurrencyRatesAPIConnection()
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/symbols",
        json={
            "success": True,
            "symbols": {"AED": "United Arab Emirates Dirham", "AFN": "Afghan Afghani"},
        },
        status=200,
    )

    assert c.get_currency_names_and_symbols() == {
        "AED": "United Arab Emirates Dirham",
        "AFN": "Afghan Afghani",
    }


@responses.activate
def test_get_currency_names_and_symbols_status_404_should_raise_error():
    c = CurrencyRatesAPIConnection()
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/symbols",
        json={"success": False},
        status=404,
    )
    with pytest.raises(
        ValueError, match="Wrong status code. Expected: 200, Actual 404"
    ):
        c.get_currency_names_and_symbols()


@responses.activate
def test_get_exchange_rate_latest_rate():
    c = CurrencyRatesAPIConnection()
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/latest?base=EUR&symbols=PLN",
        json={
            "success": True,
            "timestamp": 1682763304,
            "base": "EUR",
            "date": "2023-04-29",
            "rates": {"PLN": 4.631698},
        },
        status=200,
    )

    assert c.get_exchange_rate(first_currency="EUR", second_currency="PLN") == 4.631698


@responses.activate
def test_get_exchange_rate_latest_rate_status_404_should_raise_error():
    c = CurrencyRatesAPIConnection()
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/latest?base=EUR&symbols=PLN",
        json={
            "success": False,
            "timestamp": 1682763304,
            "base": "EUR",
            "date": "2023-04-29",
            "rates": {},
        },
        status=404,
    )

    with pytest.raises(
        ValueError, match="Wrong status code. Expected: 200, Actual 404"
    ):
        c.get_exchange_rate(first_currency="EUR", second_currency="PLN")


@responses.activate
def test_get_exchange_rate_historical_rate():
    c = CurrencyRatesAPIConnection()
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/2023-04-03?base=EUR&symbols=PLN",
        json={
            "success": True,
            "timestamp": 1680566399,
            "historical": True,
            "base": "EUR",
            "date": "2023-04-03",
            "rates": {"PLN": 4.676721},
        },
        status=200,
    )

    assert (
        c.get_exchange_rate(
            first_currency="EUR", second_currency="PLN", date="2023-04-03"
        )
        == 4.676721
    )


@responses.activate
def test_get_exchange_rate_historical_rate_status_404_should_raise_error():
    c = CurrencyRatesAPIConnection()
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/2023-04-03?base=EUR&symbols=PLN",
        json={
            "success": False,
            "timestamp": 1680566399,
            "historical": True,
            "base": "EUR",
            "date": "2023-04-03",
            "rates": {},
        },
        status=404,
    )

    with pytest.raises(
        ValueError, match="Wrong status code. Expected: 200, Actual 404"
    ):
        c.get_exchange_rate(
            first_currency="EUR", second_currency="PLN", date="2023-04-03"
        )
