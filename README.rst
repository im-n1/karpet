.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/logo.png
   :align: center


Karpet
======
Karpet is a tiny library with just a few dependencies
for fetching coins/tokens metrics data the internet.

It can provide following data:

* coin/token historical price data (no limits)
* google trends for the given list of keywords (longer period than official API)

What is upcoming?

* Reddit metrics
* Have a request? Open an issue ;)

Dependencies
------------
Library uses a few nifty dependencies and is Python 3.6+ only:

* pandas
* numpy
* coinmarketcap
* pytrends

Usage
-----

Install the library via pip.

.. code-block::

   ~ pip install karpet

Import the library class first.

.. code-block::

   from karpet import Karpet

Symbol (ticker) -> coninmarketcap.com URL slug conversion.

.. code-block::

    c = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    c.get_coin_slug("BTC")  # bitcoin

Retrieving historical data.

.. code-block::

    c = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = c.fetch_crypto_historical_data(coin="bitcoin")  # Dataframe with historical data
    df.head()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/historical_data.png

Retrieving Google Trends - in percents for the given date range.

.. code-block::

    c = Karpet(date(2019, 1, 1), date(2019, 5, 1))
    df = c.fetch_google_trends(kw_list=["bitcoin"])  # Dataframe with trends.
    df.head()

.. image:: https://raw.githubusercontent.com/im-n1/karpet/master/assets/trends.png

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
