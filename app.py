from flask import Flask, render_template, request, flash
import pandas as pd
from fetch_module import fetch_and_analyze
from dashboard import load_dashboard_data
from stock_utils import load_stock_data, get_monthly_summary, get_years


app = Flask(__name__)
app.secret_key = "secret-key"
file_path = 'stock_data/TCS.NS.xlsx'
df = load_stock_data(file_path)
years = get_years(df)

@app.route("/dashboard/<ticker>")
def dashboard(ticker):
    file_path = f"stock_data/{ticker}.xlsx"
    try:
        data = load_dashboard_data(file_path, ticker)
        table_html = data["monthly_df"].to_html(classes="data-table", index=False, border=0)
    except Exception as e:
        return f"<h2>Error: {e}</h2>"

    return render_template(
        "dashboard.html",
        stock=data["stock"],
        table=table_html,
        latest=data["latest_summary"],
        chart=data["chart_data"]
    )





@app.route("/", methods=["GET", "POST"])
def index():
    ticker_file = "nifty50_list.xlsx"
    tickers_df = pd.read_excel(ticker_file)
    tickers = tickers_df["Ticker"].tolist()

    selected = None
    start = None
    end = None

    if request.method == "POST":
        selected = request.form.get("ticker")
        start = request.form.get("start_date")
        end = request.form.get("end_date")

        if selected and start and end:
            output = f"/home/mayur/Desktop/study/share_market/stock_mark/stock_dashboard/stock_data/{selected}.xlsx"
            try:
                msg = fetch_and_analyze(selected, start, end, output)
                flash(f"✅ {msg}", "success")
            except Exception as e:
                flash(f"❌ Error: {e}", "error")
        else:
            flash("⚠️ Please select ticker and both dates", "error")

    return render_template("index.html", tickers=tickers, selected=selected, start=start, end=end)




if __name__ == "__main__":
    app.run(debug=True)

