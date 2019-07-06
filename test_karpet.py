from karpet.karpet import Karpet

from datetime import date, timedelta


def get_last_week():

    return date.today() - timedelta(days=7), date.today()


def test_get_coin_slug():

    c = Karpet(*get_last_week())
    assert c.get_coin_slug("BTC") == "bitcoin"


def test_fetch_crypto_historical_data():

    c = Karpet(*get_last_week())
    assert len(c.fetch_crypto_historical_data(coin="bitcoin")) == 7


def test_fetch_exchanges():

    c = Karpet()
    assert len(c.fetch_exchanges("btc")) > 0


def test_fetch_google_trends():

    c = Karpet(*get_last_week())
    df = c.fetch_google_trends(kw_list=["bitcoin"])

    assert len(df) > 0
    assert len(df[df["bitcoin"] == 100.0]) == 1


def test_fetch_tweets():

    c = Karpet(date.today() - timedelta(days=1), date.today())
    df = c.fetch_tweets(["#dash"], "en")

    assert len(df) > 0
