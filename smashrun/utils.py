# vim: ft=python expandtab softtabstop=0 tabstop=4 shiftwidth=4

import dateutil
import ephem
import sys
from datetime import datetime
from datetime import timedelta
from dateutil.tz import tzoffset
from pint import UnitRegistry


UNITS = UnitRegistry()


def srdate_to_datetime(datestring, utc=False):
    # 2016-11-17T07:11:00-08:00

    if utc:
        dt = datestring
        fmt = '%Y-%m-%dT%H:%M:%S.%f'
        to_zone = dateutil.tz.tzlocal()
    else:
        dt = datestring[:-6]
        tz = datestring[-6:]
        fmt = '%Y-%m-%dT%H:%M:%S'
        offset = (int(tz[1:3]) * 60 * 60) + (int(tz[4:6]) * 60)
        if tz[0] == '-':
            offset = -offset
        to_zone = tzoffset(None, offset)

    result = datetime.strptime(dt, fmt)
    return result.replace(tzinfo=to_zone)


def get_records(activity, key):
    idx = -1
    for k in activity['recordingKeys']:
        idx += 1
        if activity['recordingKeys'][idx] == key:
            break
    assert idx in range(len(activity['recordingKeys'])), "Unable to find valid index in %s for '%s'" % (activity['recordingKeys'], key)
    return activity['recordingValues'][idx]


def get_distance(activity):
    distance = activity['distance'] * UNITS.kilometer
    return distance


def get_duration(activity):
    duration = activity['duration'] * UNITS.seconds
    return duration


def get_start_time(activity):
    start_time = srdate_to_datetime(activity['startDateTimeLocal'])
    return start_time


def get_badge_earned_time(info):
    earned_time = srdate_to_datetime(info['dateEarnedUTC'], utc=True)
    return earned_time


def get_elevations(activity):
    elevations = get_records(activity, 'elevation')
    return elevations


def elevation_delta(activity):
    elevations = get_elevations(activity)
    min_elevation = sys.maxsize
    max_elevation = -sys.maxsize
    for elevation in elevations:
        min_elevation = min(elevation, min_elevation)
        max_elevation = max(elevation, max_elevation)

    return (max_elevation - min_elevation) * UNITS.meters


def avg_pace(activity, distance_unit=UNITS.mile, time_unit=UNITS.minute, keep_units=False):
    distance = get_distance(activity)
    time = get_duration(activity)

    result = time.to(time_unit) / distance.to(distance_unit)
    if not keep_units:
        result = result.magnitude
    return result


def get_start_coordinates(activity):
    return (activity['startLatitude'], activity['startLongitude'])


def get_sun_info(activity, rise_or_set, prev=False):
    if rise_or_set not in ['sunrise', 'sunset']:
        raise ValueError("rise_or_set must be one of 'sunrise' or 'sunset', but saw '%s'" % (rise_or_set))

    start_date = get_start_time(activity)

    o = ephem.Observer()
    lat, lon = get_start_coordinates(activity)
    o.lat = str(lat)
    o.lon = str(lon)
    o.elev = get_elevations(activity)[0]
    o.date = start_date.astimezone(dateutil.tz.tzutc()).strftime('%Y-%m-%d %H:%M:%S')
    o.pressure = 0       # U.S. Naval Astronomical Almanac value
    o.horizon = '-0:34'  # U.S. Naval Astronomical Almanac value

    sun = ephem.Sun()
    result = None
    if rise_or_set == 'sunrise':
        if prev:
            result = o.previous_rising(sun)
        else:
            result = o.next_rising(sun)
    else:
        if prev:
            result = o.previous_setting(sun)
        else:
            result = o.next_setting(sun)

    return result.datetime().replace(tzinfo=dateutil.tz.tzutc()).astimezone(start_date.tzinfo)


def get_moon_illumination_pct(activity):
    start_date = get_start_time(activity)

    o = ephem.Observer()
    lat, lon = get_start_coordinates(activity)
    o.lat = str(lat)
    o.lon = str(lon)
    o.elev = get_elevations(activity)[0]
    o.date = start_date.replace(tzinfo=dateutil.tz.tzutc()).strftime('%Y-%m-%d %H:%M:%S')
    o.pressure = 0       # U.S. Naval Astronomical Almanac value
    o.horizon = '-0:34'  # U.S. Naval Astronomical Almanac value

    return ephem.Moon(o).phase


def is_between_sunset_and_sunrise(activity):
    start_date = get_start_time(activity)
    p_sunset = get_sun_info(activity, 'sunset', prev=True)
    n_sunrise = get_sun_info(activity, 'sunrise')

    if is_same_day(p_sunset, start_date) and start_date > p_sunset:
        return True
    elif is_same_day(n_sunrise, start_date) and start_date < p_sunset:
        return True
    else:
        return False


def is_sunrise_activity(activity):
    start_date = get_start_time(activity)
    end_date = start_date + timedelta(seconds=get_duration(activity).magnitude)
    n_sunrise = get_sun_info(activity, 'sunrise')

    # If the next sunrise is on this day
    if is_same_day(n_sunrise, start_date):
        if start_date < n_sunrise and end_date > n_sunrise:
            return True
    return False


def is_sunset_activity(activity):
    start_date = get_start_time(activity)
    end_date = start_date + timedelta(seconds=get_duration(activity).magnitude)
    n_sunset = get_sun_info(activity, 'sunset')

    # If the next sunset is on this day
    if is_same_day(n_sunset, start_date):
        if start_date < n_sunset and end_date > n_sunset:
            return True
    return False


def is_solstice(activity, solstice):
    if solstice not in ['summer', 'winter']:
        raise ValueError("solstice must be one of 'summer' or 'winter', but saw '%s'" % (solstice))

    start_date = get_start_time(activity)
    solstice_date = None
    if solstice == 'summer':
        solstice_date = ephem.next_solstice(str(start_date.year))
    else:
        solstice_date = ephem.previous_solstice(str(start_date.year + 1))

    # Convert solstice date to same TZ as start_date
    solstice_date = solstice_date.datetime().replace(tzinfo=dateutil.tz.tzutc()).astimezone(start_date.tzinfo)

    # This is solstice if we're on the same day
    return is_same_day(solstice_date, start_date)


def is_same_day(d1, d2):
    if d1 is None or d2 is None:
        return False
    if d1.year == d2.year and d1.month == d2.month and d1.day == d2.day:
        return True
    else:
        return False


def is_different_year(d1, d2):
    if d1 is None or d2 is None:
        return True
    elif d1.year != d2.year:
        return True
    else:
        return False


def is_different_month(d1, d2):
    if d1 is None or d2 is None:
        return True
    elif d1.month != d2.month:
        return True
    elif d1.year != d2.year:
        return True
    else:
        return False
