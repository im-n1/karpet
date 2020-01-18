import time


def date_to_timestamp(date):
    """
    Converts date instance to unix timestamp.

    :param datetime.date date: Date instance.
    :return: Unix timestamp.
    :rtype: int
    """

    return int(time.mktime(date.timetuple()))
