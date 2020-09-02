from datetime import date, datetime, timedelta
import pytest

from karpet import Karpet

CRYPTOCOMPARE_API_KEY = None


def get_last_week():

    return date.today() - timedelta(days=13), date.today() - timedelta(days=7)


def test_fetch_crypto_historical_data():

    c = Karpet()

    assert 1000 < len(c.fetch_crypto_historical_data(symbol="BTC"))


def test_fetch_crypto_historical_data_params():

    c = Karpet()

    with pytest.raises(AttributeError):
        c.fetch_crypto_historical_data()

    with pytest.raises(AttributeError):
        c.fetch_crypto_historical_data(symbol="a", id="b")


def test_fetch_crypto_historical_data_limited():

    c = Karpet(date(2019, 1, 1), date(2019, 1, 30))

    assert 30 == len(c.fetch_crypto_historical_data(symbol="BTC"))


def test_fetch_exchanges():

    c = Karpet()
    exchanges = c.fetch_crypto_exchanges("btc")

    assert len(exchanges) > 0
    assert "Binance" in exchanges


def test_fetch_google_trends():

    c = Karpet(*get_last_week())
    df = c.fetch_google_trends(kw_list=["bitcoin"])

    assert len(df) > 0
    assert len(df[df["bitcoin"] == 100.0]) == 1


def test_fetch_tweets():

    c = Karpet(date.today() - timedelta(days=1), date.today())
    df = c.fetch_tweets(["#bitcoin"], "en")

    assert len(df) > 0


def test_fetch_news():

    k = Karpet()
    news = k.fetch_news("eth")

    assert len(news) > 0
    assert "url" in news[0]
    assert "title" in news[0]
    assert "date" in news[0]

    if news[0]["date"] is not None:
        assert isinstance(news[0]["date"], datetime)


def test_fetch_news_with_limit():

    k = Karpet()
    news = k.fetch_news("eth", limit=30)

    assert 0 < len(news) <= 30
    print(f"Fetched {len(news)} news.")


def test_fetch_top_news():

    k = Karpet()
    editors_choice, hot_stories = k.fetch_top_news()

    assert len(editors_choice) >= 4
    assert len(hot_stories) >= 4

    assert "url" in editors_choice[0]
    assert "title" in editors_choice[0]
    assert "date" in editors_choice[0]

    if editors_choice[0]["date"] is not None:
        assert isinstance(editors_choice[0]["date"], datetime)

    assert "url" in hot_stories[0]
    assert "title" in hot_stories[0]
    assert "date" in hot_stories[0]

    if hot_stories[0]["date"] is not None:
        assert isinstance(hot_stories[0]["date"], datetime)
