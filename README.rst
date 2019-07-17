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
for fetching coins/tokens metrics data the internet.

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

``get_coin_slug()``
~~~~~~~~~~~~~~~~~~~
Symbol (ticker) -> coninmarketcap.com URL slug conversion.

.. code-block:: python

    c = Karpet()
    c.get_coin_slug("BTC")  # bitcoin

``fetch_historical_data()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Retrieves historical data.

.. code-block:: python

    c = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = c.fetch_crypto_historical_data(coin="bitcoin")  # Dataframe with historical data
    df.head()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/historical_data.png

``fetch_exchanges()``
~~~~~~~~~~~~~~~~~~~~~
Retrieves exchange list.

.. code-block:: python

    c = Karpet()
    c.fetch_exchanges("nrg")
    ['DigiFinex', 'KuCoin', 'CryptoBridge', 'Bitbns', 'CoinExchange']

``fetch_tweets()``
~~~~~~~~~~~~~~~~~~
Retrieves twitter tweets.

.. code-block:: python

    c = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = c.fetch_tweets(kw_list=["bitcoin"], lang="en")  # Dataframe with tweets.
    df.head()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/tweets.png

``fetch_google_trends()``
~~~~~~~~~~~~~~~~~~~~~~~~~
Retrieves Google Trends - in percents for the given date range.

.. code-block:: python

    c = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = c.fetch_google_trends(kw_list=["bitcoin"])  # Dataframe with trends.
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

   c = Karpet()
   news = c.fetch_news("btc")  # Gets 10 news.
   print(news[0])
   {
      'url': 'https://cointelegraph.com/ ....',  # Truncated.
      'title': 'Shell Invests in Blockchain-Based Energy Startup',
      'description': 'The world’s fifth top oil and gas firm, Shell, has...',  # Truncated.
      'date': datetime.datetime(2019, 7, 10, 19, 0, 13),
      'image': 'https://images.cointelegraph.com/....jpg'  # Truncated.
   }
   news = c.fetch_news("btc", limit=30)  # Gets 30 news.

Changelog
---------
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
