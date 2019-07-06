.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/logo.png
   :align: center

.. image:: https://img.shields.io/pypi/v/karpet.svg?color=0c7dbe
   :alt: PyPI

.. image:: https://img.shields.io/pypi/l/karpet.svg?color=0c7dbe
   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/dm/karpet.svg?color=0c7dbe
   :alt: PyPI - Downloads

Karpet
======
Karpet is a tiny library with just a few dependencies
for fetching coins/tokens metrics data the internet.

It can provide following data:

* coin/token historical price data (no limits)
* google trends for the given list of keywords (longer period than official API)
* twitter scraping for the given keywords (no limits)

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

Install the library via pip.

.. code-block::

   ~ pip install karpet  # Basics only
   ~ pip install karpet[twitter]  # For Twitter scraping
   ~ pip install karpet[google]  # For Google trends
   ~ pip install karpet[twitter,google]  # All features

Import the library class first.

.. code-block::

    from karpet.karpet import Karpet

Symbol (ticker) -> coninmarketcap.com URL slug conversion.

.. code-block::

    c = Karpet()
    c.get_coin_slug("BTC")  # bitcoin

Retrieving historical data.

.. code-block::

    c = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = c.fetch_crypto_historical_data(coin="bitcoin")  # Dataframe with historical data
    df.head()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/historical_data.png

Retrieving exchange list.

.. code-block::

    c = Karpet()
    c.fetch_exchanges("nrg")  # ['DigiFinex', 'KuCoin', 'CryptoBridge', 'Bitbns', 'CoinExchange']

Retrieving twitter tweets.

.. code-block::

    c = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = c.fetch_tweets(kw_list=["bitcoin"], lang="en")  # Dataframe with tweets.
    df.head()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/tweets.png

Retrieving Google Trends - in percents for the given date range.

.. code-block::

    c = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = c.fetch_google_trends(kw_list=["bitcoin"])  # Dataframe with trends.
    df.head()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/google_trends.png

And with a few lines of code you can get a chart

.. code-block::

   df = df.set_index("date")
   df.plot()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/trends_chart.png

Credits
-------
This is my personal library I use in my long-term project. I can pretty much guarantee it will
live for a long time then. I will add new features over time and I more than welcome any
help or bug reports. Feel free to open an issue or merge request.

The code is is licensed under MIT license.
