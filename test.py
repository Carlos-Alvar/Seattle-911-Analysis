from main import lin_sin_regression, correlation_plotter
import numpy as np
import pandas as pd


def test_correlation():
    x_dates = pd.date_range("2020-01-01", "2020-12-31")
    df = pd.DataFrame({"Datetime": x_dates})
    df["Ordinal"] = df["Datetime"].apply(lambda x: x.toordinal())
    covid_df = df
    calls_df = df
    calls_df["Incident Number"] = range(0, 366)
    covid_df["Positives"] = range(50, 416)
    correlation_plotter(calls_df, covid_df, "2020-03-01", "2020-12-31")
    noise_data = np.random.normal(0, 20, calls_df["Incident Number"].shape)
    calls_df["Incident Number"] = calls_df["Incident Number"] + noise_data
    correlation_plotter(calls_df, covid_df, "2020-04-01", "2020-12-31")
    noise_pure = np.random.normal(200, 200, calls_df["Incident Number"].shape)
    calls_df["Incident Number"] = noise_pure
    correlation_plotter(calls_df, covid_df, "2020-05-01", "2020-12-31")


def test_regressions():
    x_dates = pd.date_range("2020-01-01", "2021-12-31")
    df = pd.DataFrame({"Datetime": x_dates})
    df["Ordinal"] = df["Datetime"].apply(lambda x: x.toordinal())
    y = 12 * np.sin(0.017 * df["Ordinal"] + 20) + (0.013 * df["Ordinal"]) - 900
    df["Incident Number"] = y
    lin_sin_regression(df, "2020-02-01", "2021-12-31")
    noise_data = np.random.normal(0, 1, df["Ordinal"].shape)
    df["Incident Number"] = y + noise_data
    lin_sin_regression(df, "2020-03-01", "2021-12-31")


def main():
    test_regressions()
    test_correlation()


if __name__ == "__main__":
    main()
