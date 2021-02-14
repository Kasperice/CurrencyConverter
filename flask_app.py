from flask import Flask, render_template, request
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
        quantity = request.form.get('quantity').replace(',', '.')
        curr1 = request.form.get('curr1').split()[0]
        curr2 = request.form.get('curr2').split()[0]
        result = ""
        if 'submit_button' in request.form:
            result = str(f"{quantity} {curr1} is equal to {float(quantity) * c.get_latest_rate(curr1, curr2):.2f} {curr2}")
        elif 'submit_button2' in request.form:
            result = str(f"{quantity} {curr2} is equal to {float(quantity) * c.get_latest_rate(curr2, curr1):.2f} {curr1}")
        elif 'clear_button' in request.form:
            result = ""
            quantity = 1.0
            curr1 = "EUR"
            curr2 = "PLN"
        return render_template("latest.html", currencies=choices, test_value=result, defaults=(quantity, curr1, curr2))
    else:
        return render_template("latest.html", currencies=choices, defaults=(quantity, curr1, curr2))


@app.route("/historical", methods=["POST", "GET"])
def historical():
    quantity = 1.0
    curr1 = "EUR"
    curr2 = "PLN"
    date = datetime.date.today().strftime("%Y-%m-%d")
    time = 'is'
    if request.method == "POST":
        date = request.form.get('date')
        quantity = request.form.get('quantity').replace(',', '.')
        curr1 = request.form.get('curr1').split()[0]
        curr2 = request.form.get('curr2').split()[0]
        result = ""
        if date != datetime.date.today().strftime("%Y-%m-%d"):
            time = 'was'
        if 'submit_button' in request.form:
            result = str(f"{quantity} {curr1} {time} equal to {float(quantity) * c.get_historical_rate(curr1, curr2, date):.2f} {curr2}")
        elif 'submit_button2' in request.form:
            result = str(f"{quantity} {curr2} {time} equal to {float(quantity) * c.get_historical_rate(curr2, curr1, date):.2f} {curr1}")
        elif 'clear_button' in request.form:
            result = ""
            quantity = 1.0
            curr1 = "EUR"
            curr2 = "PLN"
            date = datetime.date.today().strftime("%Y-%m-%d")

        return render_template("historical.html", currencies=choices, test_value=result, defaults=(quantity, curr1, curr2, date))
    else:
        return render_template("historical.html", currencies=choices, defaults=(quantity, curr1, curr2, date))


@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
