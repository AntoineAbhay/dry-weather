from typing import List
from get_driest_moment import get_driest_moment
from format_moment import format_moment

def get_driest_moments_message(data, nb_days_from_now_options: List) -> str:
    dry_moments = [
        format_moment(get_driest_moment(data, nb_days_from_now), nb_days_from_now)
        for nb_days_from_now in nb_days_from_now_options
    ]
    message = "\n".join(dry_moments)
    return f"Driest times:\n{message}"

def get_complete_message(data, humidity_threshold) -> str:
    all_data_message = "\n".join(
            [format_moment(moment) for moment in data]
        )
    filtered_data = [
        moment
        for moment in data
        if moment["values"]["humidity"] < humidity_threshold
    ]
    filtered_data_message = "\n".join(
        [format_moment(moment) for moment in filtered_data]
    )
    filtered_data_sorted = [
        format_moment(moment)
        for moment in sorted(
            filtered_data, key=lambda moment: moment["values"]["humidity"]
        )
    ]
    filtered_data_sorted_message = "\n".join(filtered_data_sorted)

    return (f"Forecast (Humidity < {humidity_threshold}%):\n```{filtered_data_message}```\n"
        + f"Sorted:\n```{filtered_data_sorted_message}```\n"
        + f"Full:\n```{all_data_message}```")
