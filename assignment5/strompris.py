#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache


# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API


    Args:
        date (datetime.date) the date for which you want to collect data, default = None

    Returns:
        pd.DataFrame: the dataframe with the collected data


    ...
    """  # ... is for creating more space in the docs, there is probably a better way to do it
    if date is None:
        date = datetime.date.today()
        # print(date)
    year = date.year
    month = date.month
    day = date.day
    # raise NotImplementedError("Remove me when you implement this task")
    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{month:02}-{day:02}_{location}.json"
    # :02 should give you 07 if input is 7 and 30 if input is 30 and so on. in other words, it is a way to pad.
    r = requests.get(url)
    json_response = r.json()
    df = pd.DataFrame(json_response)

    (df["time_start"]) = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert(
        "Europe/Oslo"
    )
    (df["time_end"]) = pd.to_datetime(df["time_end"], utc=True).dt.tz_convert(
        "Europe/Oslo"
    )
    return_df = df[["NOK_per_kWh", "time_start"]]

    return return_df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen",
}


# task 1:
def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = list(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Relies on LOCATION_CODES:

    LOCATION_CODES = {
                "NO1": "Oslo",
                "NO2": "Kristiansand",
                "NO3" : "Trondheim",
                "NO4": "Tromsø",
                "NO5": "Bergen"
                }

    Method uses fetch_day_prices() to collect several dataframes of the desired days and locations and combines the data into
    a single pd.DataFrame that is returned.

    Args:
        end_date (datetime.date) : the last date that you want to include data from, default = None
        days (int): number of days that you want to collect data from, default = 7
        locations (list[str]): list of keys to the LOCATION_CODES dict, default = list(LOCATION_CODES.keys())

    Returns:
        pd.DataFrame: the dataframe of the collected data


    ...
    """
    # raise NotImplementedError("Remove me when you implement this task")

    if end_date is None:
        end_date = datetime.date.today()

    # creating the dataframes
    list_of_dataframes = []
    for day in range((days * -1) + 1, 1):
        for location in locations:
            iter_date = end_date + datetime.timedelta(day)
            df = fetch_day_prices(iter_date, location)
            df["location_code"] = location
            df["location"] = LOCATION_CODES[location]
            list_of_dataframes.append(df)

    return pd.concat(list_of_dataframes)


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Takes the dataframe from fetch prices and returns an altair chart

    Args:
        df (pd.DataFrame) : the dataframe from fetch_prices()

    Returns:
        alt.Chart : the chart created from df



    ...
    """
    # raise NotImplementedError("Remove me when you implement this task")

    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(y="NOK_per_kWh:Q", x="time_start:T", color="location:N")
    )

    return chart


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """
    in4110-task, NOT IMPLEMENTED

    ...
    """
    raise NotImplementedError("Remove me when you implement this task (in4110 only)")
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """

    bonus-task, NOT IMPLEMENTED

    ...
    """
    raise NotImplementedError("Remove me when you implement this optional task")


def main():
    """Allow running this module as a script for testing.

    Args:
        None

    Returns:
        None

    ...
    """
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
