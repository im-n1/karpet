try:
    from pytrends.request import TrendReq
    from twitterscraper import query_tweets
except:
    pass

import asyncio
import time
from datetime import datetime, timedelta

import aiohttp
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from . import utils


class Karpet:

    quick_search_data = None
    cryptocompare_api_url = "https://min-api.cryptocompare.com/data"

    def __init__(self, start=None, end=None, cryptocompare_api_key=None):
        """
        Constructor.

        :param datetime.date start: History data begining.
        :param datetime.date end: History data end.
        :param str cryptocompare_api_key: CrtyptoCompare.com API key.
        """

        self.start = start
        self.end = end
        self.cryptocompare_api_key = cryptocompare_api_key

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

    def fetch_crypto_historical_data(self, symbol):
        """
        Retrieve basic historical information for a specific cryptocurrency from cryptocompare.com

        Output dataframe has following columns:

        * close
        * conversionSymbol
        * conversionType
        * high
        * low
        * open
        * volumefrom
        * volumeto

        Index is datetime64[ns].

        :param str symbol: Coin symbol - i.e. BTC, ETH, ...
        :raises Exception: If data couldn't be download form the internet.
        :return: Dataframe with historical data.
        :rtype: pd.DataFrame
        """

        data = []
        step = 1
        limit = 2000
        url = f"{self.cryptocompare_api_url}/v2/histoday?fsym={symbol}&tsym=USD&limit={limit}&allData=true"

        # Fetch and check the response.
        response_data = self._get_json(url)

        if "Success" != response_data["Response"]:
            raise Exception("Couldn't download necessary data from the internet.")

        data = response_data["Data"]["Data"]

        # Check if data are limited and if yes drop the unwanted data.
        if self.start:
            start = utils.date_to_timestamp(self.start)
            data = list(filter(lambda i: i["time"] >= start, data))

        if self.end:
            end = utils.date_to_timestamp(self.end)
            data = list(filter(lambda i: i["time"] <= end, data))

        df = pd.DataFrame.from_records(data)
        df["date"] = pd.to_datetime(df["time"], unit="s")
        df = df.set_index("date")
        df = df.drop("time", axis=1)

        return df

    def fetch_crypto_exchanges(self, symbol):
        """
        Fetches all exchanges where the given symbol
        is listed.

        :param str symbol: Coin symbol - i.e. BTC, ETH, ...
        :return: List of exchanges.
        :rtype: list
        """

        url = f"{self.cryptocompare_api_url}/v4/all/exchanges?fsym={symbol}"

        # Fetch and check the response.
        response_data = self._get_json(url)

        if "Success" != response_data["Response"]:
            raise Exception("Couldn't download necessary data from the internet.")

        return list(response_data["Data"]["exchanges"].keys())

    def fetch_google_trends(
        self,
        kw_list,
        trdays=250,
        overlap=100,
        cat=0,
        geo="",
        tz=360,
        gprop="",
        hl="en-US",
        sleeptime=1,
    ):
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
            trend_dates = [
                "{} {}".format(
                    self.start.strftime("%Y-%m-%d"), self.end.strftime("%Y-%m-%d")
                )
            ]
        else:
            trend_dates = [
                "{} {}".format(
                    (self.end - timedelta(i + trdays)).strftime("%Y-%m-%d"),
                    (self.end - timedelta(i)).strftime("%Y-%m-%d"),
                )
                for i in range(0, n_days - trdays + stich_overlap, stich_overlap)
            ]

        # Try to fetch first batch.
        pytrends.build_payload(
            kw_list, cat=cat, timeframe=trend_dates[0], geo=geo, gprop=gprop
        )
        df = pytrends.interest_over_time().reset_index()

        if len(df) == 0:
            raise ValueError("Search term returned no results (insufficient data).")

        # Fetch other batches.
        for date in trend_dates[1:]:

            time.sleep(sleeptime)
            pytrends.build_payload(
                kw_list, cat=cat, timeframe=date, geo=geo, gprop=gprop
            )

            temp_trend = pytrends.interest_over_time().reset_index()
            temp_trend = temp_trend.merge(df, on="date", how="left")

            # it's ugly but we'll exploit the common column names
            # and then rename the underscore containing column names
            for kw in kw_list:
                norm_factor = np.ma.masked_invalid(
                    temp_trend[kw + "_y"] / temp_trend[kw + "_x"]
                ).mean()
                temp_trend[kw] = temp_trend[kw + "_x"] * norm_factor

            temp_trend = temp_trend[temp_trend.isnull().any(axis=1)]
            temp_trend["isPartial"] = temp_trend["isPartial_x"]
            df = pd.concat(
                [df, temp_trend[["date", "isPartial"] + kw_list]], axis=0, sort=False
            )

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
            df["has_link"] = df["text"].apply(
                lambda text: "http://" in text or "https://" in text
            )

            return df

        tweets = query_tweets(
            query=" OR ".join(kw_list), begindate=self.start, lang=lang, limit=limit
        )

        return process_tweets(tweets)

    def fetch_news(self, symbol, limit=10):
        """
        Fetches news of the given symbol. Each news contains
        following params:

        * url
        * title
        * description
        * date
        * image

        :param str symbol: Coin symbol the news will be fetched for.
        :param int limit: Limit for news count.
        """

        def get_news(symbol, limit):
            """
            Fetches news from coincodex.com.

            :return: List of news urls.
            :rtype: list
            """

            url = (
                f"https://coincodex.com/api/coincodexicos/get_news/{symbol}/{limit}/1/"
            )
            data = self._get_json(url)

            return [{"url": d["url"]} for d in data]

        def get_coin_slug(symbol):
            """
            Determines coin coincodex.com URL slug for the given
            coin symbol.

            :param str symbol: Coin symbol (BTC, ETH, ...)
            :return: URL slug or None if not found.
            :rtype: str or None
            """

            url = "https://coincodex.com/apps/coincodex/cache/all_coins.json"

            try:
                response = requests.get(url)
            except:
                raise Exception("Couldn't download necessary data from the internet.")

            try:
                data = response.json()
            except:
                raise Exception("Couldn't parse downloaded data from the internet.")

            for c in data:
                if c["symbol"].upper() == symbol.upper():
                    return c["shortname"]

        # Fetch features.
        news = get_news(symbol, limit)
        asyncio.run(self._fetch_news_features(news))

        return self._drop_bad_news(news)[:limit]

    def fetch_top_news(self):
        """
        Fetches top crypto news. Returns Editor's choice and Hot stories.

        * url
        * title
        * description
        * date
        * image

        :return: Tuple where first are editors choice news and second hot stories.
        :rtype: tuple
        """

        def get_top_news():
            """
            Fetches editors choice and hot stories from cointelegraph.com front page.

            :return: Dict with ``editors_choice`` and ``hot_stories`` items.
            :rtype: dict
            """

            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"
            }
            response = requests.get("https://cointelegraph.com/", headers=headers)
            dom = BeautifulSoup(response.text, "lxml")

            def parse_section_news(section):
                """
                Parse section with news. Section contains of titles and
                links to the news where only links are parsed out.

                :param object section: BeautifulSoap element object of the section.
                :return: List of news objects - {"url": "..."}.
                :rtype: list
                """

                news_items = section.find_all(class_="main-news-tabs__item")
                news = []

                if len(news_items):

                    for i in news_items:
                        news.append({"url": i.find("a")["href"]})

                return news

            editors_choice, hot_stories = dom.find_all(class_="main-news-tabs__list")

            return parse_section_news(editors_choice), parse_section_news(hot_stories)

        # Fetch features.
        editors_choice, hot_stories = get_top_news()
        asyncio.run(self._fetch_news_features(editors_choice))
        asyncio.run(self._fetch_news_features(hot_stories))

        return editors_choice, hot_stories

    async def _fetch_news_features(self, news):
        """
        Asynchronously fetches all news features.

        :param list news: List of news objects.
        """

        async def fetch_all(session, news):
            """
            Fetches all news features.

            :param aiohttp.ClientSession session: Session instance.
            :param list news: List of news objects.
            """

            await asyncio.gather(*[fetch_one(session, n) for n in news])

        async def fetch_one(session, news):
            """
            Fetches a few features to the given news object. Features
            are set directly to the news object.
            Fetched features are:

            * date
            * image
            * description

            :param aiohttp.ClientSession session: Session instance.
            :param object news: News object.
            """

            async with session.get(news["url"]) as response:

                html = await response.text()
                dom = BeautifulSoup(html, features="lxml")

                # Title.
                try:
                    news["title"] = dom.find("meta", {"property": "og:title"})[
                        "content"
                    ]
                except:
                    news["title"] = None

                # Date.
                try:
                    d = dom.find("meta", {"property": "article:published_time"})[
                        "content"
                    ]
                    news["date"] = datetime.strptime(d, "%Y-%m-%dT%H:%M:%S%z")
                except:
                    news["date"] = None

                # Image.
                try:
                    news["image"] = dom.find("meta", {"property": "og:image"})[
                        "content"
                    ]
                except:
                    news["image"] = None

                # Description.
                try:
                    news["description"] = dom.find(
                        "meta", {"property": "og:description"}
                    )["content"]
                except:
                    news["description"] = None

        async with aiohttp.ClientSession() as session:
            await fetch_all(session, news)

    def _drop_bad_news(self, news):
        """
        Drops news that doesn't suit following requirements.

        * must have published date (date)

        :param list news: List of news.
        :return: Filtered list of news.
        :rtype: list
        """

        filtered_news = []

        for n in news:
            if not n["date"]:
                continue

            filtered_news.append(n)

        return filtered_news

    def _get_json(self, url):
        """
        Downloads data from the given  URL and parses them as JSON.
        Handles exception and raises own ones with sane messages.

        :param str url: URL to be scraped.
        :return: Parsed JSON data.
        :rtype: object or list
        """

        # Download.
        try:
            response = requests.get(url)
        except:
            raise Exception("Couldn't download necessary data from the internet.")

        # Parse.
        try:
            return response.json()
        except:
            raise Exception("Couldn't parse downloaded data from the internet.")
