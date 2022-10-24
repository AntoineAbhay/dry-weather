from datetime import datetime

def get_driest_moment(next_days_data_aggragated, number_of_days_from_now=7):
    now = datetime.now().timestamp()
    date_in_x_days = datetime.fromtimestamp(now + number_of_days_from_now * 24 * 3600).date()
    next_x_days_data_aggregated = [
        data for data in next_days_data_aggragated if data["date"] <= date_in_x_days
    ]
    driest_moment = None
    min_humidity = 100
    for time_period_data in next_x_days_data_aggregated:
        if (
            time_period_data
            and time_period_data["values"]
            and time_period_data["values"]["humidity"] < min_humidity
        ):
            min_humidity = time_period_data["values"]["humidity"]
            driest_moment = time_period_data

    return driest_moment
