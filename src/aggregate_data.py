from datetime import datetime
from utils import is_morning, is_afternoon, is_night


def average(data_points):
    if not data_points:
        return None
    temperatures = [d["temperature"] for d in data_points]
    humidities = [d["humidity"] for d in data_points]
    return {
        "temperature": sum(temperatures) / len(temperatures),
        "humidity": sum(humidities) / len(humidities),
    }


def reset_current_day_data():
    return {
        "morning": [],
        "afternoon": [],
        "night": [],
    }


def append_current_day_data(aggregated_data, current_day_data, date):
    for period, data_points in current_day_data.items():
        if len(data_points):
            aggregated_data.append(
                {
                    "date": date,
                    "period": period,
                    "values": average(data_points),
                }
            )
    return aggregated_data


def aggregate_data(data):
    if not data or not len(data):
        return []
    aggregated_data = []
    current_date = data[0]["date"].date()
    current_day_data = reset_current_day_data()
    for data_point in data:
        date = data_point["date"].date()
        data_point_time = data_point["date"].time()

        if date.day != current_date.day and not is_night(data_point_time):
            # Save the current data
            aggregated_data = append_current_day_data(
                aggregated_data, current_day_data, current_date
            )
            # New day
            current_date = date
            # Reset
            current_day_data = reset_current_day_data()
        if is_morning(data_point_time):
            current_day_data["morning"].append(data_point)
        elif is_afternoon(data_point_time):
            current_day_data["afternoon"].append(data_point)
        elif is_night(data_point_time):
            current_day_data["night"].append(data_point)

    aggregated_data = append_current_day_data(
        aggregated_data, current_day_data, current_date
    )

    return aggregated_data
