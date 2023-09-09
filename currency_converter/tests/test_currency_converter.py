"""Currency Converter tests."""
import pytest
import requests
import responses

from currency_converter.currency_converter import CurrencyRatesAPIConnection


@pytest.fixture
def api_connection() -> CurrencyRatesAPIConnection:
    """Fixture returning connection to CurrencyRatesAPI."""
    return CurrencyRatesAPIConnection()


@responses.activate
def test_get_currency_names_and_symbols(api_connection):
    """Check if currency names and their symbols are read correctly from API."""
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/symbols",
        json={
            "success": True,
            "symbols": {"AED": "United Arab Emirates Dirham", "AFN": "Afghan Afghani"},
        },
        status=200,
    )

    assert api_connection.get_currency_names_and_symbols() == {
        "AED": "United Arab Emirates Dirham",
        "AFN": "Afghan Afghani",
    }


@responses.activate
def test_get_currency_names_and_symbols_status_404_should_raise_error(api_connection):
    """Check if 404 error is raised when API returns 404 error for list of currences."""
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/symbols",
        json={"success": False},
        status=requests.codes.not_found,
    )
    with pytest.raises(
        ValueError,
        match=f"Wrong status code. Expected: {requests.codes.ok}, Actual {requests.codes.not_found}",
    ):
        api_connection.get_currency_names_and_symbols()


@responses.activate
def test_get_exchange_rate_latest_rate(api_connection):
    """Check if correct exchange rate is read for latest date."""
    expected_rate = 4.676721
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/latest?base=EUR&symbols=PLN",
        json={
            "success": True,
            "timestamp": 1682763304,
            "base": "EUR",
            "date": "2023-04-29",
            "rates": {"PLN": expected_rate},
        },
        status=requests.codes.ok,
    )

    assert (
        api_connection.get_exchange_rate(first_currency="EUR", second_currency="PLN")
        == expected_rate
    )


@responses.activate
def test_get_exchange_rate_latest_rate_status_404_should_raise_error(api_connection):
    """Check if 404 error is raised when API returns 404 error for getting latest rate."""
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
        status=requests.codes.not_found,
    )

    with pytest.raises(
        ValueError,
        match=f"Wrong status code. Expected: {requests.codes.ok}, Actual {requests.codes.not_found}",
    ):
        api_connection.get_exchange_rate(first_currency="EUR", second_currency="PLN")


@responses.activate
def test_get_exchange_rate_historical_rate(api_connection):
    """Check if correct exchange rate is read for historical date."""
    expected_rate = 4.676721
    responses.add(
        method=responses.GET,
        url="https://api.apilayer.com/exchangerates_data/2023-04-03?base=EUR&symbols=PLN",
        json={
            "success": True,
            "timestamp": 1680566399,
            "historical": True,
            "base": "EUR",
            "date": "2023-04-03",
            "rates": {"PLN": expected_rate},
        },
        status=requests.codes.ok,
    )

    assert (
        api_connection.get_exchange_rate(
            first_currency="EUR", second_currency="PLN", date="2023-04-03"
        )
        == expected_rate
    )


@responses.activate
def test_get_exchange_rate_historical_rate_status_404_should_raise_error(
    api_connection,
):
    """Check if 404 error is raised when API returns 404 error for getting historical rate."""
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
        api_connection.get_exchange_rate(
            first_currency="EUR", second_currency="PLN", date="2023-04-03"
        )
