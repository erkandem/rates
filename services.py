from datetime import datetime as dt, date
from dateutil import relativedelta
from typing import Optional

from fredapi import Fred
import pandas as pd

import settings

fred = Fred(api_key=settings.FRED_API_KEY)


class FREDDataIds:
    FRED_FED_FUND_EFFECTIVE_RATE = "EFFR"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_1M = "DGS1MO"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_3M = "DGS3MO"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_6M = "DGS6MO"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_1Y = "DGS1"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_2Y = "DGS2"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_3Y = "DGS3"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_5Y = "DGS5"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_7Y = "DGS7"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y = "DGS10"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_20Y = "DGS20"
    FRED_US_TREASURY_CONSTANT_MATURITY_ID_30Y = "DGS30"

    FRED_US_TREASURY_CONSTANT_MATURITY_YIELD_CURVE = [
        {
          "maturity": 1 / 365,
          "code": FRED_FED_FUND_EFFECTIVE_RATE,
        },
        {
            "maturity": 1 / 12,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_1M,
        },

        {
            "maturity": 3 / 12,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_3M,
        },
        {
            "maturity": 6 / 12,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_6M,
        },
        {
            "maturity": 1,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_1Y,
        },
        {
            "maturity": 2,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_2Y,
        },
        {
            "maturity": 3,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_3Y,
        },
        {
            "maturity": 5,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_5Y,
        },
        {
            "maturity": 7,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_7Y,
        },
        {
            "maturity": 10,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
        },
        {
            "maturity": 20,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_20Y,
        },
        {
            "maturity": 30,
            "code": FRED_US_TREASURY_CONSTANT_MATURITY_ID_30Y,
        },

    ]


def get_yield_curve(
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
) -> pd.DataFrame:
    """query the yield curve from the FRED API.

    Will set a default span if the ``start_date`` parameter is not supplied.

    Args:
        start_date: desired series start date
        end_date: desired series end date

    Returns:
        a pandas dataframe with the collected yield curve
    """
    DEFAULT_YIELD_CURVE_SPAN = relativedelta.relativedelta(years=5)
    if not end_date:
        end_date = dt.today()
    if not start_date:
        start_date = dt.today() - DEFAULT_YIELD_CURVE_SPAN
    yield_curve_dict = {}
    for series_info in FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_YIELD_CURVE:
        yield_curve_dict[series_info["code"]] = fred.get_series(
            series_info["code"],
            observation_start=start_date,
            observation_end=end_date,
        )
    yield_curve_df = pd.DataFrame(yield_curve_dict)
    return yield_curve_df


def calculate_rate_spreads(
        yield_curve: pd.DataFrame,
) -> pd.DataFrame:

    """calculates the rate spreads between rate maturities.

    Args:
        yield_curve: a pandas dataframe object containing time series for the default maturities

    Returns:
        a pandas dataframe with rate
    """
    keys = list(yield_curve.keys())
    recipes = [
        (
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
            FREDDataIds.FRED_FED_FUND_EFFECTIVE_RATE,
        ),
        (
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_1M,
        ),
        (
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_3M,
        ),
        (
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_6M,
        ),        (
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_1Y,
        ),        (
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_2Y,
        ),        (
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_3Y,
        ),        (
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_5Y,
        ),        (
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_10Y,
            FREDDataIds.FRED_US_TREASURY_CONSTANT_MATURITY_ID_7Y,
        ),
    ]
    spread_dict = {}
    for recipe in recipes:
        if recipe[0] in yield_curve.keys() and recipe[1] in yield_curve.keys():
            spread_name = f"{recipe[0]}-{recipe[1]}"
            spread_dict[spread_name] = yield_curve[recipe[0]] - yield_curve[recipe[1]]

    spread_df = pd.DataFrame(spread_dict)
    return spread_df
