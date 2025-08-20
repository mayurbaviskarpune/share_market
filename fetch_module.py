import yfinance as yf
import pandas as pd
from openpyxl import load_workbook

def fetch_and_analyze(stock_symbol, start_date, end_date, output_file):
    # Fetch data from Yahoo Finance
    df = yf.download(stock_symbol, start=start_date, end=end_date)
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    if df.empty:
        raise ValueError(f"No data found for {stock_symbol} between {start_date} and {end_date}")
    
    # Reset index and add YearMonth column
    df.reset_index(inplace=True)
    df['YearMonth'] = df['Date'].dt.to_period('M')

    # Extract year from start_date
    year = pd.to_datetime(start_date).year

    # Monthly aggregation
    monthly = df.groupby('YearMonth').agg(
        Open=('Open', 'first'),
        Close=('Close', 'last'),
        High=('High', 'max'),
        Low=('Low', 'min'),
        AvgVolume=('Volume', 'mean')
    )
    monthly['Performance_%'] = ((monthly['Close'] - monthly['Open']) / monthly['Open']) * 100

    # Sheet names with stock + year
    daily_sheet = f"{stock_symbol}_Daily_{year}"
    monthly_sheet = f"{stock_symbol}_Monthly_{year}"

    # Save to Excel
    try:
        with pd.ExcelWriter(output_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=daily_sheet, index=False)
            monthly.to_excel(writer, sheet_name=monthly_sheet)
    except FileNotFoundError:
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=daily_sheet, index=False)
            monthly.to_excel(writer, sheet_name=monthly_sheet)

    return f"Data for {stock_symbol} saved in {output_file}"
