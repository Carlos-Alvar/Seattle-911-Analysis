"""
Carlos Alvarez
CSE 163 AI
This file loads in the csv files and cleans up the data for usage in main.py
"""
import pandas as pd


def load_calls_data(file_name):
    """
    Loads in the 911 calls data and prepares it for usage in main.py
    Takes a file path as input
    Returns a dataframe
    """
    df = pd.read_csv(file_name)
    df["Datetime"] = pd.to_datetime(df.Datetime)
    df = df.sort_values(by="Datetime")
    df["Ordinal"] = df["Datetime"].apply(lambda x: x.toordinal())
    return df


def load_covid_data(file_name):
    """
    Loads in the COVID cases data and prepares it for usage in main.py
    Takes a file path as input
    Returns a dataframe
    """
    df = pd.read_csv(file_name)
    df = df[df.City == "Seattle"]
    df["Datetime"] = pd.to_datetime(df["Collection_Date"])
    df = df[["Datetime", "Positives"]]
    df["Ordinal"] = df["Datetime"].apply(lambda x: x.toordinal())
    return df
