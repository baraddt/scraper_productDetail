import pandas as pd


def get_links_from_excel(filepath, url_column=None):
    df = pd.read_excel(filepath)
    if url_column and url_column in df.columns:
        return df[url_column].dropna().tolist()
    return df.iloc[:, 0].dropna().tolist()
