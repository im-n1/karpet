.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/logo.png
   :align: center

.. image:: https://img.shields.io/pypi/v/karpet.svg?color=0c7dbe
   :alt: PyPI

.. image:: https://img.shields.io/pypi/l/karpet.svg?color=0c7dbe
   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/dm/karpet.svg?color=0c7dbe
   :alt: PyPI - Downloads

.. contents::

Karpet
======
Karpet is a tiny library with just a few dependencies
for fetching coins/tokens metrics data from the internet.

It can provide following data:

* coin/token historical price data (no limits)
* google trends for the given list of keywords (longer period than official API)
* twitter scraping for the given keywords (no limits)
* much more info about crypto coins/tokens (no rate limits)

What is upcoming?

* Reddit metrics
* Have a request? Open an issue ;)

Dependencies
------------
Library uses a few nifty dependencies and is Python 3.6+ only. There is no
need to install dependencies you don't need. Therefore this library utilizes
extras which install optional dependencies:

* for Google trends - google
* for Twitter scraping - twitter

Usage
-----
1. Install the library via pip.

.. code-block:: bash

   pip install karpet  # Basics only
   pip install karpet[twitter]  # For Twitter scraping
   pip install karpet[google]  # For Google trends
   pip install karpet[twitter,google]  # All features

2. Import the library class first.

.. code-block:: python

    from karpet import Karpet

``fetch_crypto_historical_data()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Retrieves historical data.

.. code-block:: python

    k = Karpet(date(2019, 1, 1), date(2019, 5, 1), cryptocompare_api_key="...")
    df = k.fetch_crypto_historical_data(symbol="BTC")  # Dataframe with historical data.
    df.head()

                  close conversionSymbol conversionType     high      low     open  volumefrom      volumeto
    date
    2019-01-01  3880.15                          direct  3938.75  3696.94  3747.39    45104.29  1.705983e+08
    2019-01-02  3961.01                          direct  3989.59  3826.29  3880.15    54034.73  2.108546e+08
    2019-01-03  3835.86                          direct  3965.52  3778.76  3961.01    45585.19  1.764881e+08
    2019-01-04  3874.06                          direct  3901.65  3783.88  3835.86    44398.90  1.705076e+08
    2019-01-05  3855.39                          direct  3926.92  3841.13  3874.06    35766.65  1.394385e+08


``fetch_exchanges()``
~~~~~~~~~~~~~~~~~~~~~
Retrieves exchange list.

.. code-block:: python

    k = Karpet(cryptocompare_api_key="...")
    k.fetch_exchanges("nrg")
    ['DigiFinex', 'KuCoin', 'CryptoBridge', 'Bitbns', 'CoinExchange']

``fetch_tweets()``
~~~~~~~~~~~~~~~~~~
Retrieves twitter tweets.

.. code-block:: python

    k = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = k.fetch_tweets(kw_list=["bitcoin"], lang="en")  # Dataframe with tweets.
    df.head()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/tweets.png

``fetch_google_trends()``
~~~~~~~~~~~~~~~~~~~~~~~~~
Retrieves Google Trends - in percents for the given date range.

.. code-block:: python

    k = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = k.fetch_google_trends(kw_list=["bitcoin"])  # Dataframe with trends.
    df.head()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/google_trends.png

And with a few lines of code you can get a chart

.. code-block:: python

   df = df.set_index("date")
   df.plot()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/trends_chart.png

``fetch_news()``
~~~~~~~~~~~~~~~~
Retrieves crypto news.

.. code-block:: python

   k = Karpet()
   news = k.fetch_news("btc")  # Gets 10 news.
   print(news[0])
   {
      'url': 'https://cointelegraph.com/ ....',  # Truncated.
      'title': 'Shell Invests in Blockchain-Based Energy Startup',
      'description': 'The world’s fifth top oil and gas firm, Shell, has...',  # Truncated.
      'date': datetime.datetime(2019, 7, 28, 9, 24, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)))
      'image': 'https://images.cointelegraph.com/....jpg'  # Truncated.
   }
   news = k.fetch_news("btc", limit=30)  # Gets 30 news.

``fetch_top_news()``
~~~~~~~~~~~~~~~~~~~~
Retrieves top crypto news in 2 categories:

* Editor's choices - articles picked by editors
* Hot stories - articles with most views

.. code-block:: python

   k = Karpet()
   editors_choices, top_stories = k.fetch_top_news()
   print(len(editors_choices))
   5
   print(len(top_stories))
   5
   print(editors_choices[0])
   {
      'url': 'https://cointelegraph.com/...',  # Truncated.
      'title': 'Bank of China’s New Infographic Shows Why Bitcoin Price Is Going Up',
      'date': datetime.datetime(2019, 7, 27, 10, 7, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))),
      'image': 'https://images.cointelegraph.com/images/740_aHR...', # Truncated.
      'description': 'The Chinese central bank released on its website an ...'  # Truncated.
   }
   print(top_stories[0])
   {
      'url': 'https://cointelegraph.com/...',  # Truncated.
      'title': 'Bitcoin Price Shuns Volatility as Analysts Warn of Potential Drop to $7,000',
      'date': datetime.datetime(2019, 7, 27, 10, 7, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))),
      'image': 'https://images.cointelegraph.com/images/740_aHR0c...'  # Truncated.
      'description': 'Stability around $10,600 for Bitcoin price is ...'  # Truncated.
   }


Changelog
---------
0.3
~~~
* Migrated to cryptocompare.com API (you need an API key now).
* Requirements are now managed by Poetry.

0.2.5
~~~~~
* Added ``fetch_top_news()`` method for top crypto news separated in 2 categories.

0.2.4
~~~~~
* ``fetch_news()`` adds new "description" item and renames "image_url" to "image".
* All ``fetch_news()`` item properties are now presented even if they are ``None``.

0.2.3
~~~~~
* Simplified import from ``from karpet.karpet import Karpet`` to ``from karpet import Karpet``.

0.2.2
~~~~~
* Added ``fetch_news()`` method for retrieving crypto news.

0.2.1
~~~~~
* Added ``fetch_exchanges()`` method for retrieving symbol exchange list.
* Removed obsolete library dependency.

0.2
~~~
* Twitter scraping added.

0.1
~~~
* Initial release.

Credits
-------
This is my personal library I use in my long-term project. I can pretty much guarantee it will
live for a long time then. I will add new features over time and I more than welcome any
help or bug reports. Feel free to open an issue or merge request.

The code is is licensed under MIT license.
