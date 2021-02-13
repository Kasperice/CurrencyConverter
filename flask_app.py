from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/latest")
def latest():
    return render_template("latest.html")


@app.route("/historical")
def historical():
    return render_template("historical.html")


if __name__ == "__main__":
    app.run(debug=True)
