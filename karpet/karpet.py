import numpy as np
import pandas as pd
from pytrends.request import TrendReq
from coinmarketcap import Market

import re
from datetime import timedelta
import time


class Karpet:

    def __init__(self, start, end):
        """
        Constructor.

        :param datetime.date start: History data begining.
        :param datetime.date end: History data end.
        """

        self.start = start
        self.end = end

    def get_coin_slug(self, symbol):
        """
        Determines coin coinmarketcap.com URL slug for the given
        coin symbol.

        :param str symbol: Coin symbol (BTC, ETH, ...)
        :return: URL slug or None if not found.
        :rtype: str or None
        """

        coinmarketcap = Market()

        for c in coinmarketcap.listings()["data"]:
            if c["symbol"].upper() == symbol.upper():
                return c["website_slug"]

    def fetch_crypto_historical_data(self, coin=None, symbol=None):
        """
        Retrieve basic historical information for a specific cryptocurrency from coinmarketcap.com

        :param str coin: Coin name - i.e. bitcoin, etherenum, ...
        :param str symbol: Coin symbol - i.e. BTC, ETH, ...
        :raises Exception: If "coin" or "symbol" params are not specified or coin symbol couldn't be resolved into slug.
        :return: Dataframe with historical data.
        :rtype: pd.DataFrame
        """

        # Check input parameters - coin or symbol is required.
        if not coin and not symbol:
            raise Exception('Please specify "coin" or "symbol" parameters.')

        if symbol:
            coin = self.get_coin_slug(symbol)

            if not coin:
                raise Exception(f"Couldn't resolve coin symbol {coin} into slug.")

        output = pd.read_html("https://coinmarketcap.com/currencies/{}/historical-data/?start={}&end={}".format(
            coin,
            self.start.strftime("%Y%m%d"),
            self.end.strftime("%Y%m%d")
        ))[0]

        output = output.assign(Date=pd.to_datetime(output["Date"]))

#         for col in output.columns:
#             if output[col].dtype == np.dtype("O"):
#                 output.loc[output[col] == "-", col] = 0
#                 output[col] = output[col].astype("int64")

        output.columns = [re.sub(r"[^a-z]", "", col.lower()) for col in output.columns]
        output["coin"] = coin

        return output

    def fetch_google_trends(self, kw_list, trdays=250, overlap=100,
                            cat=0, geo="", tz=360, gprop="", hl="en-US",
                            sleeptime=1):
        """
        Retrieve daily Google trends data for a list of search terms.

        This method is essentially a highly restricted wrapper for the pytrends package
        Any issues/questions related to its use would probably be more likely resolved
        by consulting the pytrends github page
        https://github.com/GeneralMills/pytrends

        :param list kw_list: List of search terms (max 5)- see pyTrends for more details.
        :param int trdays: The number of days to pull data for in a search. (the max is around 270, though the website seems to indicate 90)
        :param int overlap: The number of overlapped days when stitching two searches together.
        :param int cat: Category to narrow results - see pyTrends for more details.
        :param str geo: Two letter country abbreviation (e.g 'US', 'UK') default is '', which returns global results.
        :param int tz : Timezone offset - default is 360, which corresponds to US CST.
        :param str gprop: Filter results to specific google property available options are "images", "news", "youtube" or "froogle"
                          default is '', which refers to web searches - see pyTrends for more details.
        :param str hl: Language (e.g. 'en-US' (default), 'es').
        :param int sleeptime: When stiching multiple searches, this sets the period between each.
        :return: Pandas dataframe with all results.
        :rtype: pd.DataFrame
        """

        # Validate params.
        if len(kw_list) > 5 or len(kw_list) == 0:
            raise ValueError("The keyword list can contain at most 5 words")
        if trdays > 270:
            raise ValueError("trdays must not exceed 270")
        if overlap >= trdays:
            raise ValueError("Overlap can't exceed search days")

        stich_overlap = trdays - overlap
        n_days = (self.end - self.start).days
        pytrends = TrendReq(hl=hl, tz=tz)

        # Get the dates for each search.
        if n_days <= trdays:
            trend_dates = ["{} {}".format(self.start.strftime("%Y-%m-%d"), self.end.strftime("%Y-%m-%d"))]
        else:
            trend_dates = [
                "{} {}".format(
                    (self.end - timedelta(i + trdays)).strftime("%Y-%m-%d"),
                    (self.end - timedelta(i)).strftime("%Y-%m-%d")
                ) for i in range(0, n_days - trdays + stich_overlap, stich_overlap)
            ]

        # Try to fetch first batch.
        pytrends.build_payload(kw_list, cat=cat, timeframe=trend_dates[0], geo=geo, gprop=gprop)
        df = pytrends.interest_over_time().reset_index()

        if len(df) == 0:
            raise ValueError("Search term returned no results (insufficient data).")

        # Fetch other batches.
        for date in trend_dates[1:]:

            time.sleep(sleeptime)
            pytrends.build_payload(kw_list, cat=cat, timeframe=date, geo=geo, gprop=gprop)

            temp_trend = pytrends.interest_over_time().reset_index()
            temp_trend = temp_trend.merge(df, on="date", how="left")

            # it's ugly but we'll exploit the common column names
            # and then rename the underscore containing column names
            for kw in kw_list:
                norm_factor = np.ma.masked_invalid(temp_trend[kw + "_y"] / temp_trend[kw + "_x"]).mean()
                temp_trend[kw] = temp_trend[kw + "_x"] * norm_factor

            temp_trend = temp_trend[temp_trend.isnull().any(axis=1)]
            temp_trend["isPartial"] = temp_trend["isPartial_x"]
            df = pd.concat([df, temp_trend[["date", "isPartial"] + kw_list]], axis=0, sort=False)

        # Reorder columns in alphabetical order.
        df = df[["date", "isPartial"] + kw_list]

        # Drop "isPartial column".
        df = df.drop("isPartial", axis=1)

        df = df[df["date"] >= self.start.strftime("%Y-%m-%d")]

        # The values in each column are relative to other columns
        # so we need to get the maximum value across the search columns.
        max_val = float(df[kw_list].values.max())

        for col in kw_list:
            df[col] = 100.0 * df[col] / max_val

        return df.sort_values("date").reset_index(drop=True)
