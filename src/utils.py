from datetime import datetime

MORNING_START = 6
AFTERNOON_START = 14
NIGHT_START = 22


def is_today(date):
    return date == datetime.today().date()


def is_tomorrow(date):
    return date == datetime.fromtimestamp(datetime.now().timestamp() + 24 * 3600).date()


def is_morning(time):
    return MORNING_START <= time.hour and time.hour < AFTERNOON_START


def is_afternoon(time):
    return AFTERNOON_START <= time.hour and time.hour < NIGHT_START


def is_night(time):
    return NIGHT_START <= time.hour or time.hour < MORNING_START
