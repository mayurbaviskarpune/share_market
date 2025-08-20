import pandas as pd
import os

def load_stock_data(file_path):
    """Read Excel and return DataFrame with Date column as datetime"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    
    df = pd.read_excel(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    return df

def get_years(df):
    """Return list of unique years in the data"""
    return sorted(df['Year'].unique(), reverse=True)

def get_monthly_summary(df, year):
    """Return 12-month summary for selected year with % change"""
    df_year = df[df['Year'] == year].copy()
    if df_year.empty:
        return pd.DataFrame()  # no data for selected year
    
    # Resample by month: last Close price of month
    df_year.set_index('Date', inplace=True)
    monthly_close = df_year['Close'].resample('M').last().to_frame()
    monthly_close['% Performance'] = monthly_close['Close'].pct_change()*100
    monthly_close = monthly_close.round(2).reset_index()
    monthly_close['Month'] = monthly_close['Date'].dt.strftime('%b')
    return monthly_close[['Month', 'Close', '% Performance']]
