from flask import Flask, render_template, request, redirect, url_for, session, flash
from currency_converter.currency_converter import CurrencyRatesAPIConnection
from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid
import hashlib
import re

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = datetime.timedelta(days=7)

db = SQLAlchemy(app)


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    query_result = db.Column(db.String(200))

    def __init__(self, name, email, password, query_result):
        self.name = name
        self.email = email
        self.password = password
        self.query_result = query_result


def divide_entries(data, number_of_entries):
    searches = list(data.split(" | "))[:number_of_entries]
    results = dict()
    for s in searches:
        res = re.search("\[(.*?)\] (.*?)(?=on)on (.*?)$", s)
        if res:
            results[res.group(1)] = [res.group(2), res.group(3)]
    return results


c = CurrencyRatesAPIConnection()
choices = [
    f"{currency} - {currency_name}"
    for currency, currency_name in c.get_currency_names_and_symbols().items()
]


@app.route("/")
def home():
    return render_template("index.html", logged="user" in session)


@app.route("/latest", methods=["POST", "GET"])
def latest():
    quantity = 1.0
    curr1 = "EUR"
    curr2 = "PLN"
    if request.method == "POST":
        quantity = request.form.get("quantity").replace(",", ".")
        curr1 = request.form.get("curr1").split()[0]
        curr2 = request.form.get("curr2").split()[0]
        result = ""
        if "submit_button" in request.form:
            result = str(
                f"{quantity} {curr1} is equal to "
                f"{float(quantity) * c.get_exchange_rate(curr1, curr2):.2f} {curr2}"
            )
        elif "submit_button2" in request.form:
            result = str(
                f"{quantity} {curr2} is equal to "
                f"{float(quantity) * c.get_exchange_rate(curr2, curr1):.2f} {curr1}"
            )
        elif "clear_button" in request.form:
            result = ""
            quantity = 1.0
            curr1 = "EUR"
            curr2 = "PLN"

        if "user" in session and result != "":
            user = session["user"]
            found_user = Users.query.filter_by(name=user).first()
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date = datetime.date.today().strftime("%Y-%m-%d")
            found_user.query_result = (
                f"[{date_time}] {result} on {date} | " + found_user.query_result
            )
            db.session.commit()

        parameters = {
            "currencies": choices,
            "test_value": result,
            "defaults": (quantity, curr1, curr2),
            "logged": "user" in session,
        }
        return render_template("latest.html", **parameters)
    else:
        parameters = {
            "currencies": choices,
            "defaults": (quantity, curr1, curr2),
            "logged": "user" in session,
        }
        return render_template("latest.html", **parameters)


@app.route("/historical", methods=["POST", "GET"])
def historical():
    quantity = 1.0
    curr1 = "EUR"
    curr2 = "PLN"
    date = datetime.date.today().strftime("%Y-%m-%d")
    time = "is"
    if request.method == "POST":
        historical_date = request.form.get("date")
        quantity = request.form.get("quantity").replace(",", ".")
        curr1 = request.form.get("curr1").split()[0]
        curr2 = request.form.get("curr2").split()[0]
        result = ""
        if historical_date != datetime.date.today().strftime("%Y-%m-%d"):
            time = "was"
        if "submit_button" in request.form:
            result = str(
                f"{quantity} {curr1} {time} equal to "
                f"{float(quantity) * c.get_exchange_rate(curr1, curr2, historical_date):.2f} {curr2}"
            )
        elif "submit_button2" in request.form:
            result = str(
                f"{quantity} {curr2} {time} equal to "
                f"{float(quantity) * c.get_exchange_rate(curr2, curr1, historical_date):.2f} {curr1}"
            )
        elif "clear_button" in request.form:
            result = ""
            quantity = 1.0
            curr1 = "EUR"
            curr2 = "PLN"
            date = datetime.date.today().strftime("%Y-%m-%d")

        if "user" in session and result != "":
            user = session["user"]
            found_user = Users.query.filter_by(name=user).first()
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found_user.query_result = (
                f"[{date_time}] {result} on {historical_date} | "
                + found_user.query_result
            )
            db.session.commit()

        parameters = {
            "currencies": choices,
            "test_value": result,
            "defaults": (quantity, curr1, curr2, date),
            "logged": "user" in session,
        }

        return render_template("historical.html", **parameters)
    else:
        parameters = {
            "currencies": choices,
            "defaults": (quantity, curr1, curr2, date),
            "logged": "user" in session,
        }
        return render_template("historical.html", **parameters)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form.get("username")
        passw = hashlib.md5(request.form.get("passw").encode()).hexdigest()
        session["user"] = user
        found_user = Users.query.filter_by(name=user).first()
        if "login_button" in request.form:
            if found_user and found_user.password == passw:
                session["email"] = found_user.email
                session["results"] = found_user.query_result
                flash("Login successful!", "info")
            elif found_user and found_user.password != passw:
                flash("Wrong password", "warning")
                return render_template("login.html", login=user)
            else:
                flash("User does not exist, please register first", "warning")
                return render_template("login.html", login=user)
        elif "register_button" in request.form:
            usr = Users(user, None, passw, "")
            db.session.add(usr)
            db.session.commit()
            flash("Registered successfully!", "info")

        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!", "info")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        found_user = Users.query.filter_by(name=user).first()
        if request.method == "POST" and "clear_button" in request.form:
            found_user.query_result = ""
            db.session.commit()

        found_user = Users.query.filter_by(name=user).first()
        results = divide_entries(found_user.query_result, 15)

        parameters = {
            "user": user,
            "email": email,
            "searches": results,
            "logged": "user" in session,
        }

        return render_template("user.html", **parameters)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("You have been logged out!", "success")
    return redirect(url_for("home"))


@app.route("/view")
def view():
    parameters = {"values": Users.query.all(), "logged": "user" in session}
    return render_template("view.html", **parameters)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # db.drop_all()
        app.run(debug=True)
