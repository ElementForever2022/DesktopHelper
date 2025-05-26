from datetime import datetime, timedelta, timezone
from typing import Union, Optional, Dict
import pytz
import re
from functools import lru_cache

# to calc the lantitude and longitude of a city and calc sunrise and sunset time 
from astral import LocationInfo
from astral.sun import sun

from geopy.geocoders import Nominatim

def get_coordinates_from_city(city_name: str):
    """
    Given a city name, return (latitude, longitude) using OpenStreetMap Nominatim API.
    
    Args:
        city_name (str): Name of the city, e.g. 'Shanghai', 'New York'
    
    Returns:
        (lat, lon): Tuple of floats
    """
    geolocator = Nominatim(user_agent="clock-city-locator")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError(f"City '{city_name}' not found.")


def is_daytime(city_name="Shanghai", region="China", latitude=31.2304, longitude=121.4737, dt: datetime = None) -> bool:
    """
    Returns True if the given datetime (or now) is between sunrise and sunset in the given city.
    """
    location = LocationInfo(city_name, region, "UTC", latitude, longitude)
    if dt is None:
        dt = datetime.now(pytz.utc).astimezone(pytz.timezone("Asia/Shanghai"))
    s = sun(location.observer, date=dt.date(), tzinfo=dt.tzinfo)

    return s["sunrise"] <= dt <= s["sunset"]

@lru_cache(maxsize=64)
def get_timezone(tz: str):
    """Cache and return a pytz timezone object."""
    return pytz.timezone(tz)

def get_current_time(form: str, zone: Union[int, str, None] = None) -> Dict:
    """
    Return the current time in a structured format with optional timezone support.

    Parameters:
        form (str): Custom format string using keys like "YYYY-MM-DD HH:mm:SS"
        zone (int or str, optional):
            - int: UTC offset in hours (e.g., 8 for China)
            - str: Pytz timezone string (e.g., "Asia/Tokyo")
            - None: Defaults to UTC

    Returns:
        dict: A dictionary containing:
            - raw: formatted string output
            - datetime: the timezone-aware datetime object
            - timestamp: UNIX timestamp
            - timezone: string label of the time zone
            - utc_offset: UTC offset in +HH:MM or -HH:MM format
            - year, month, day, hour, minute, second
            - weekday: Monday=0, Sunday=6
            - iso_weekday: Monday=1, Sunday=7
    """
    # 1. Determine target timezone
    if isinstance(zone, str):
        try:
            target_tz = get_timezone(zone)
            tz_label = zone
        except Exception:
            raise ValueError(f"Invalid timezone string: {zone}")
    elif isinstance(zone, int):
        target_tz = timezone(timedelta(hours=zone))
        sign = "+" if zone >= 0 else "-"
        tz_label = f"UTC{sign}{abs(zone):02d}:00"
    else:
        target_tz = timezone.utc
        tz_label = "UTC"

    # 2. Get current time and convert to target timezone
    now_utc = datetime.now(timezone.utc)
    target_time = now_utc.astimezone(target_tz)

    # 3. Translate custom format to strftime format
    format_map = {
        "YYYY": "%Y",
        "MM": "%m",
        "DD": "%d",
        "HH": "%H",   # 24-hour format
        "hh": "%I",   # 12-hour format
        "mm": "%M",
        "SS": "%S",
        "ss": "%S",
        "AMPM": "%p"
    }
    pattern = re.compile('|'.join(re.escape(k) for k in format_map))
    strftime_format = pattern.sub(lambda m: format_map[m.group()], form)

    # 4. Construct the result dictionary
    result = {
        "raw": target_time.strftime(strftime_format),
        "datetime": target_time,
        "timestamp": target_time.timestamp(),
        "timezone": tz_label,
        "utc_offset": target_time.strftime("%z")[:3] + ":" + target_time.strftime("%z")[3:],
        "year": target_time.year,
        "month": target_time.month,
        "day": target_time.day,
        "hour": target_time.hour,
        "minute": target_time.minute,
        "second": target_time.second,
        "weekday": target_time.weekday(),        # Monday = 0
        "iso_weekday": target_time.isoweekday()  # Monday = 1
    }

    return result




if __name__ == '__main__':
    # s = get_current_time("YYYY-MM-DD HH-mm-ss", 8, "Asia/Shanghai")
    import time
    cities = ['Tokyo', 'Peking', 'Hong Kong', 'Guangzhou', 'Pyongyang']
    for city in cities:
        lat,lon = get_coordinates_from_city(city)
        print(city, lat, lon)
        time.sleep(2)