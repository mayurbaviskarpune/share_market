import pandas as pd
import os

def load_dashboard_data(file_path, stock_symbol):
    """
    Reads monthly sheet from Excel and prepares data for dashboard
    Returns dict with summary table (DataFrame) and chart data (lists)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    # Try to detect monthly sheet
    xl = pd.ExcelFile(file_path)
    monthly_sheets = [s for s in xl.sheet_names if "Monthly" in s]

    if not monthly_sheets:
        raise ValueError("No Monthly sheet found in Excel file")

    sheet = monthly_sheets[0]   # pick first monthly sheet
    df = pd.read_excel(file_path, sheet_name=sheet)

    # Ensure YearMonth is string
    if "YearMonth" in df.columns:
        df["YearMonth"] = df["YearMonth"].astype(str)

    # Prepare summary: last row = latest month
    latest = df.iloc[-1].to_dict()

    # Prepare chart data (for frontend JS)
    chart_data = {
        "labels": df["YearMonth"].tolist(),
        "close": df["Close"].round(2).tolist(),
        "performance": df["Performance_%"].round(2).tolist()
    }

    return {
        "stock": stock_symbol,
        "monthly_df": df,
        "latest_summary": latest,
        "chart_data": chart_data
    }
