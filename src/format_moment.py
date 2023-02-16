from datetime import datetime
from utils import is_today, is_tomorrow


def get_friendly_moment(date, period):
    if is_today(date):
        return f"Today {period}"
    if is_tomorrow(date):
        return f"Tomorrow {period}"
    time_delta = date - datetime.today().date()
    if time_delta.days < 7:
        return f"{date.strftime('%A')} {period}"
    formatted_date = date.strftime("%a %d/%m")
    return f"{formatted_date}"


def format_moment(driest_moment, nb_days=None):
    period = driest_moment["period"]
    humidity = driest_moment["values"]["humidity"]
    if nb_days is None:
        date_formatted = driest_moment["date"].strftime("%a %d/%m")
        return f"{date_formatted} (H: {humidity:.0f}%)"
    friendly_moment = get_friendly_moment(driest_moment["date"], period, )
    return f"> Next {nb_days} days: **{friendly_moment}** (H: {humidity:.0f}%)"
