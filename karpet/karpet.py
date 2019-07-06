try:
    from pytrends.request import TrendReq
    from twitterscraper import query_tweets
except:
    pass

import re
from datetime import timedelta
import time
import numpy as np
import pandas as pd
import requests


class Karpet:

    quick_search_data = None

    def __init__(self, start=None, end=None):
        """
        Constructor.

        :param datetime.date start: History data begining.
        :param datetime.date end: History data end.
        """

        self.start = start
        self.end = end

    def get_quick_search_data(self):
        """
        Downloads JSON from coinmarketcap.com quick search
        widget. Data contains list of all cryptocurrencies
        where each item has following structure:

        {
            "name": "Bitcoin",
            "symbol": "BTC",
            "rank": 1,
            "slug": "bitcoin",
            "tokens": [
                "Bitcoin",
                "bitcoin",
                "BTC"
            ],
            "id": 1,
        }

        :raises Exception: In case of unreachable data or error during parsing.
        :return: Downloaded JSON data - for each item structure see above.
        :rtype: list
        """

        if self.quick_search_data:
            return self.quick_search_data

        url = "https://s2.coinmarketcap.com/generated/search/quick_search.json"

        # Download.
        try:
            response = requests.get(url)
        except:
            raise Exception("Couldn't download necessary data from the internet.")

        # Parse.
        try:
            self.quick_search_data = response.json()

            return self.quick_search_data
        except:
            raise Exception("Couldn't parse downloaded data from the internet.")

    def get_coin_slug(self, symbol):
        """
        Determines coin coinmarketcap.com URL slug for the given
        coin symbol.

        :param str symbol: Coin symbol (BTC, ETH, ...)
        :return: URL slug or None if not found.
        :rtype: str or None
        """

        data = self.get_quick_search_data()

        for c in data:
            if c["symbol"].upper() == symbol.upper():
                return c["slug"]

    def fetch_crypto_historical_data(self, coin=None, symbol=None):
        """
        Retrieve basic historical information for a specific cryptocurrency from coinmarketcap.com

        :param str coin: Coin name - i.e. bitcoin, etherenum, ...  DEPRECATED!
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

        output.columns = [re.sub(r"[^a-z]", "", col.lower()) for col in output.columns]
        output["coin"] = coin

        return output

    def fetch_exchanges(self, symbol):
        """
        Fetches all exchanges where the given symbol
        is listed.

        :param str symbol: Coin symbol - i.e. BTC, ETH, ...
        :return: List of exchanges.
        :rtype: list
        """

        slug = self.get_coin_slug(symbol)

        try:
            url = f"https://coinmarketcap.com/currencies/{slug}/"
            df = pd.read_html(url, attrs={"id": "markets-table"})[0]
        except:
            raise Exception("Couldn't download necessary data from the internet.")

        return df["Source"].unique().tolist()

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

    def fetch_tweets(self, kw_list, lang, limit=None):
        """
        Scrapes Twitter without any limits and  returns dataframe with the
        following structure

        * fullname
        * id
        * likes
        * replies
        * retweets
        * text
        * timestamp
        * url
        * user
        * date
        * has_link

        :param list kw_list: List of keywords to search for. Will be joined with "OR" operator.
        :param str lang: Language of tweets to search in.
        :param int limit: Limit search results. Might get really big and slow so this should help.
        :return: Pandas dataframe with all search results (tweets).
        :rtype: pd.DataFrame
        """

        def process_tweets(tweets):
            """
            Cleans up tweets and returns dataframe with the
            following structure

            * fullname
            * id
            * likes
            * replies
            * retweets
            * text
            * timestamp
            * url
            * user
            * date
            * has_link

            :param list tweets: List of dicts of tweets data.
            :return: Returns dataframe with all the scraped tweets (no index).
            :rtype: pd.DataFrame
            """

            # 1. Clean up.
            data = []

            for t in tweets:
                d = t.__dict__
                del d["html"]
                data.append(d)

            # 2. Create dataframe
            df = pd.DataFrame(data)
            df["date"] = df["timestamp"].dt.date
            df["has_link"] = df["text"].apply(lambda text: "http://" in text or "https://" in text)

            return df

        tweets = query_tweets(query=" OR ".join(kw_list), begindate=self.start, lang=lang, limit=limit)

        return process_tweets(tweets)
