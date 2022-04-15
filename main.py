"""
Carlos Alvarez
CSE 163 AI
This file contains three main functions: correlation_plotter,
top_calls_news, and lin_sin_regression.
There are also two helper functions for
lin_sin_regression: get_param and sine_func
This file contains the main method and runs all these functions
on two data sets, Fire_911_calls_per_day.csv and City_daily-feb-22.csv
Two helper functions from data_load.py are used to load in the csv files
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from data_load import load_calls_data, load_covid_data


def correlation_plotter(calls_df, covid_df, start_date, end_date):
    """
    This function is intended to calcualte relevant correlation
    information and create visual plots to display correlation between
    COVID cases and 911 calls and saves these plots for display
    Takes in two dataframes for 911 calls and COVID cases,
    and a start and end date as input
    """
    fig, axs = plt.subplots(figsize=(10, 5), nrows=1)
    calls_start_mask = calls_df["Datetime"] >= start_date
    calls_end_mask = calls_df["Datetime"] <= end_date
    covid_start_mask = covid_df["Datetime"] >= start_date
    covid_end_mask = covid_df["Datetime"] <= end_date
    col_1 = calls_df[calls_start_mask & calls_end_mask]["Incident Number"]
    col_2 = covid_df[covid_start_mask & covid_end_mask]["Positives"]
    x_lin = col_2.values.reshape(-1, 1)
    y_lin = col_1.values.reshape(-1, 1)
    linear_model = LinearRegression()
    linear_model.fit(x_lin, y_lin)
    r2 = round(linear_model.score(x_lin, y_lin), 4)
    y_pred = linear_model.predict(x_lin)
    plt.plot(x_lin, y_pred, color="blue", linewidth=1)
    col_1.index = pd.date_range(start=start_date, end=end_date)
    col_2.index = pd.date_range(start=start_date, end=end_date)
    p_corre = round(col_1.corr(col_2), 4)
    corre_text = ("R^2 = " + str(r2) + "\nPearson "
                  "Correlation Coefficient = " + str(p_corre))
    plt.scatter(x=col_2, y=col_1, color="red")
    plt.text(0.7, 0.85, corre_text, ha="center",
             va="center", transform=axs.transAxes)
    plt.xlabel("Positive COVID Cases")
    plt.ylabel("911 Calls")
    plt.title("COVID Cases v 911 Calls ("
              + start_date + " to " + end_date + ")")
    plt.savefig("Cv911" + start_date + "--" + end_date)


def top_calls_news(calls_df, n_highest):
    """
    This function is intended to display top Google search news results
    for the days with the highest number of 911 calls
    Creates a text_file with the top results
    Takes in a dataframe for 911 calls and an integer,
    to determine the n highest calls desired
    """
    with open("Top_Google_Results.txt", "w") as f:
        calls_df = (calls_df.nlargest(n_highest, ["Incident Number"]))
        link_num = 10
        for i in calls_df["Datetime"]:
            date = str(i)[:-9]
            titles = []
            req = requests.get("https://www.google.com/search?q="
                               + date + "+Seattle+WA&tbm=nws")
            soup_main = BeautifulSoup(req.text, "html.parser").prettify()
            for i in range(link_num):
                soup_main = soup_main[soup_main.find("h3 class"):]
                soup_main = soup_main[soup_main.find(">"):]
                soup_main = soup_main[soup_main.find("<"):]
                soup_main = soup_main[soup_main.find(">") + 11:]
                titles.append(soup_main[:soup_main.find("<") - 9])
            f.write(date + "\nTop Google News Search Results:\n")
            for i in range(link_num):
                f.write(str(i + 1) + ": " + titles[i] + "\n")
            f.write("======================================================\n")


def sine_func(x, A, offset, omega, phase, y_int):
    """
    A helper function for lin_sin_regression
    Defines the equation of the variable sinusoid model and returns it
    Takes in x data, and parameters as input
    """
    return A * np.sin(omega * x + phase) + (offset * x) + y_int


def get_param(x, y):
    """
    A helper function for lin_sin_regression
    Sets a general baseline guess for the variable sinusoid model parameters
    These guesses allow the function to hone in on the correct values
    Returns these baseline paramters
    Takes in x and y data as input
    """
    A0 = (max(y[0:365]) - min(y[0:365])) / 2
    offset0 = (y[365] - y[0]) / 365
    phase0 = -1 * np.pi / 2
    omega0 = 2. * np.pi / 365
    y_int = min(y)
    return [A0, offset0, omega0, phase0, y_int]


def lin_sin_regression(calls_df, start_date, end_date):
    """
    This function is used to create linear and
    variable sinusoid regressions for 911 calls
    Save a plot of these regressions
    Takes in a dataframe for 911 calls and a start and end date in as input
    """
    fig, axs = plt.subplots(figsize=(20, 15), nrows=2)
    calls_start_mask = calls_df["Datetime"] >= start_date
    calls_end_mask = calls_df["Datetime"] <= end_date
    calls_df = calls_df[calls_start_mask & calls_end_mask]
    x = calls_df["Ordinal"].values
    y = calls_df["Incident Number"].values
    x_lin = x.reshape(-1, 1)
    y_lin = y.reshape(-1, 1)
    linear_model = LinearRegression()
    linear_model.fit(x_lin, y_lin)
    r2_lin = round(linear_model.score(x_lin, y_lin), 4)
    y_pred_lin = linear_model.predict(x_lin)
    axs[0].plot(calls_df["Datetime"], y_lin, color="red", linewidth=1)
    axs[0].plot(calls_df["Datetime"], y_pred_lin, color="blue", linewidth=1)
    axs[0].set_title("Linear Regression")
    axs[0].set_xlabel("Date")
    axs[0].set_ylabel("911 Calls")
    axs[0].text(0.8, 0.2, "R^2 = " + str(r2_lin),
                ha="center", va="center", transform=axs[0].transAxes)
    params, covariance = curve_fit(sine_func, x, y, p0=get_param(x, y))
    y_pred_sin = sine_func(x, *params)
    r2_sin = round(r2_score(y, y_pred_sin), 4)
    axs[1].plot(calls_df["Datetime"], y, color="red", linewidth=1)
    axs[1].plot(calls_df["Datetime"], y_pred_sin, color="blue", linewidth=1)
    axs[1].set_title("Variable Sinusoid Regression")
    axs[1].set_xlabel("Date")
    axs[1].set_ylabel("911 Calls")
    axs[1].text(0.8, 0.2, "R^2 = " + str(r2_sin),
                ha="center", va="center", transform=axs[1].transAxes)
    fig.suptitle("Linear vs Variable Sinusoid Regression ("
                 + start_date + " to " + end_date + ")")
    plt.savefig("911Regs" + start_date + "--" + end_date)


def main():
    calls_df = load_calls_data("/home/Fire_911_calls_per_day.csv")
    covid_df = load_covid_data("/home/City_daily-feb-22.csv")
    correlation_plotter(calls_df, covid_df, "2020-02-01", "2022-02-21")
    correlation_plotter(calls_df, covid_df, "2020-02-01", "2021-11-30")
    correlation_plotter(calls_df, covid_df, "2020-10-01", "2021-01-31")
    correlation_plotter(calls_df, covid_df, "2021-07-01", "2021-08-31")
    correlation_plotter(calls_df, covid_df, "2021-12-01", "2022-01-31")
    top_calls_news(calls_df, 5)
    lin_sin_regression(calls_df, "2020-01-01", "2020-12-31")
    lin_sin_regression(calls_df, "2010-01-01", "2019-12-31")
    lin_sin_regression(calls_df, "2004-01-01", "2021-12-31")


if __name__ == "__main__":
    main()
