from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/latest", methods=["POST", "GET"])
def latest():
    test = ""
    if request.method == "POST":
        test = request.form.get('quantity')
    return render_template("latest.html", test_value=test)


@app.route("/historical", methods=["POST", "GET"])
def historical():
    return render_template("historical.html")


if __name__ == "__main__":
    app.run(debug=True)
