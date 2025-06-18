from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def get_price_on_date(coin, date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    start_ts = int(date_obj.timestamp())
    end_ts = start_ts + 24 * 3600
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range?vs_currency=usd&from={start_ts}&to={end_ts}"
    data = requests.get(url).json().get('prices', [])
    return round(data[-1][1], 2) if data else 'N/A'

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_date = None
    historical_prices = {}
    live_prices = {}

    # Live price
    live_url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd'
    live_data = requests.get(live_url).json()
    for coin in ['bitcoin', 'ethereum', 'solana']:
        live_prices[coin] = live_data.get(coin, {}).get('usd', 'N/A')

    # Past price (only if date selected)
    if request.method == 'POST':
        selected_date = request.form['date']
        for coin in ['bitcoin', 'ethereum', 'solana']:
            historical_prices[coin] = get_price_on_date(coin, selected_date)

    return render_template('index.html', live=live_prices, history=historical_prices, selected_date=selected_date)

if __name__ == '__main__':
    app.run(debug=True)
