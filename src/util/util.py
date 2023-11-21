from datetime import datetime, time


def date_adapter(date: str):
    """ Converts js date into py date """
    clean_date = date[:-5]

    splitted_date = clean_date.split('T')
    date, time_ = splitted_date
    year, month, day = [int(el) for el in date.split('-')]
    hour, minute, second = [int(el) for el in time_.split(':')]

    specified_date = datetime(year, month, day)
    specified_time = time(hour, minute)
    specified_datetime = datetime.combine(specified_date, specified_time)

    return specified_datetime
