CHANGELOG
=========

0.4.10
------
- fixed top news fetch function
- fixed Google trends fetch funtction
- ``get_basic_data()`` -> ``get_basic_info()``

0.4.9
-----
- new retry policy

0.4.8
-----
- new ``fetch_crypto_live_data()``

0.4.7.
------
- dependencies updated
- news with non UTF-8 chars handled and dropped
- fixed code formatting

0.4.6
-----
- new ``price_change_24`` and ``price_change_24_percents`` properties for ``get_basic_data()``
- new ``get_quick_search_data()``

0.4.5
-----
- fixed dependencies

0.4.4
-----
- removed obsolete parts of the code and some dependencies

0.4.3
-----
- fixed ``get_basic_data()`` method (different data source)
- new property in ``get_basic_data()`` return dict - ``rank``
- tests enhanced

0.4.2
-----
- fixed minor bugs

0.4.1
-----
- new data in ``get_basic_data()`` method - ``year_low``, ``year_high``, ``yoy_change``

0.4
---
- new method ``get_basic_data()``

0.3.3
-----
- removed twitter integration - twitterscraper library is not up to date
- fixed news fetching


0.3.2
-----
- new method ``get_coin_ids()``
- method ``fetch_crypto_historical_data()`` has ``id`` param now

0.3.1
-----
- migrated to coingecko.com API (no API key needed anymore)

0.3
---
- migrated to cryptocompare.com API (you need an API key now)
- requirements are now managed by Poetry

0.2.5
-----
- added ``fetch_top_news()`` method for top crypto news separated in 2 categories

0.2.4
-----
- ``fetch_news()`` adds new "description" item and renames "image_url" to "image"
- all ``fetch_news()`` item properties are now presented even if they are ``None``

0.2.3
-----
- simplified import from ``from karpet.karpet import Karpet`` to ``from karpet import Karpet``

0.2.2
-----
- added ``fetch_news()`` method for retrieving crypto news

0.2.1
-----
- added ``fetch_exchanges()`` method for retrieving symbol exchange list
- removed obsolete library dependency

0.2
---
- twitter scraping added

0.1
---
- initial release
