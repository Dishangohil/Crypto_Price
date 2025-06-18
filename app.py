from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
API_URL = "https://api.exchangerate-api.com/v4/latest/{}"
CURRENCIES = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD"]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    rate = None
    if request.method == "POST":
        from_currency = request.form["from_currency"].upper()
        to_currency = request.form["to_currency"].upper()
        try:
            amount = float(request.form["amount"])
            data = requests.get(API_URL.format(from_currency)).json()
            rate = data["rates"].get(to_currency)
            if rate:
                result = round(amount * rate, 4)
            else:
                result = "Currency not supported"
        except Exception:
            result = "Invalid input or API error"
    return render_template(
        "index.html",
        currencies=CURRENCIES,
        selected_from=request.form.get("from_currency", ""),
        selected_to=request.form.get("to_currency", ""),
        amount_value=request.form.get("amount", ""),
        result=result,
        rate=rate,
    )

if __name__ == "__main__":
    #app.run(debug=False, use_reloader=False, port=5002)

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

