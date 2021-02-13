from flask import Flask, redirect, url_for, render_template, request
from currency_converter import CurrencyRates
import datetime

app = Flask(__name__)

c = CurrencyRates()
choices = [f"{element} - {c.translate_currency_symbol(element)}" for element in list(c.get_latest_rates('EUR').keys())]
choices.append("EUR - Euro")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/latest", methods=["POST", "GET"])
def latest():
    quantity = 1.0
    curr1 = "EUR"
    curr2 = "PLN"
    if request.method == "POST":
        quantity = request.form.get('quantity')
        curr1 = request.form.get('curr1').split()[0]
        curr2 = request.form.get('curr2').split()[0]
        print(curr1, curr2)
        result = c.get_latest_rate(curr1, curr2) * float(quantity)
        return render_template("latest.html", currencies=choices, test_value=result, defaults=(quantity, curr1, curr2))
    else:
        return render_template("latest.html", currencies=choices, defaults=(quantity, curr1, curr2))


@app.route("/historical", methods=["POST", "GET"])
def historical():
    quantity = 1.0
    curr1 = "EUR"
    curr2 = "PLN"
    date = datetime.date.today().strftime("%Y-%m-%d")
    print(date)
    if request.method == "POST":
        date = request.form.get('date')
        quantity = request.form.get('quantity')
        curr1 = request.form.get('curr1').split()[0]
        curr2 = request.form.get('curr2').split()[0]
        print(curr1, curr2)
        result = c.get_historical_rate(curr1, curr2, date) * float(quantity)
        return render_template("historical.html", currencies=choices, test_value=result, defaults=(quantity, curr1, curr2, date))
    else:
        return render_template("historical.html", currencies=choices, defaults=(quantity, curr1, curr2, date))


if __name__ == "__main__":
    app.run(debug=True)
