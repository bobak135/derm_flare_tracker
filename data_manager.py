import pandas as pd
import os

DATA_FILE = "dermatologic_data.csv"

def load_data():
    """Load data from CSV file or create new DataFrame if file doesn't exist"""
    # Define columns for the DataFrame
    columns = [
        'date', 'condition', 'severity', 'symptoms', 'triggers',
        'treatment', 'notes'
    ]

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Ensure all required columns exist
        for col in columns:
            if col not in df.columns:
                df[col] = ''
        return df
    return pd.DataFrame(columns=columns)

def save_data(df):
    """Save DataFrame to CSV file"""
    df.to_csv(DATA_FILE, index=False)

def export_data(df, format='csv'):
    """Export data in specified format"""
    if format == 'csv':
        return df.to_csv(index=False)
    elif format == 'excel':
        return df.to_excel(index=False)
    return None

def get_condition_data(df, condition=None):
    """Get data for a specific condition"""
    if condition and not df.empty:
        return df[df['condition'] == condition]
    return df