# vim: ft=python expandtab softtabstop=0 tabstop=4 shiftwidth=4
#
# Copyright (c) 2016, Jon Nall 
# All rights reserved. 
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met: 
# 
#  * Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer. 
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in the 
#    documentation and/or other materials provided with the distribution. 
#  * Neither the name of  nor the names of its contributors may be used to 
#    endorse or promote products derived from this software without specific 
#    prior written permission. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE. 

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


def assert_activity_field(activity, key, required_query_type):
    if key not in activity:
        raise RuntimeError("Requested value '%s' not in activity ID=%s. Make sure you request at least %s fields" %
                           (key, activity['activityId'], required_query_type))

def get_records(activity, key):
    assert_activity_field(activity, 'recordingKeys', 'detailed')

    if 'recordingKeys' not in activity:
        raise RuntimeError("Requested detailed date for %s, but no details present in activity %s" % (key, activity['activityId']))

    idx = -1
    for k in activity['recordingKeys']:
        idx += 1
        if activity['recordingKeys'][idx] == key:
            break

    if idx not in range(len(activity['recordingKeys'])):
        logging.warning("Unable to find valid index in %s for '%s'" % (activity['recordingKeys'], key))
        return None

    return activity['recordingValues'][idx]


def get_distance(activity):
    assert_activity_field(activity, 'distance', 'briefs')
    distance = activity['distance'] * UNITS.kilometer
    return distance


def get_duration(activity):
    assert_activity_field(activity, 'duration', 'briefs')
    duration = activity['duration'] * UNITS.seconds
    return duration


def get_start_time(activity):
    assert_activity_field(activity, 'startDateTimeLocal', 'briefs')
    start_time = srdate_to_datetime(activity['startDateTimeLocal'])
    return start_time


def get_badge_earned_time(info):
    earned_time = srdate_to_datetime(info['dateEarnedUTC'], utc=True)
    return earned_time


def get_elevations(activity):
    elevations = get_records(activity, 'elevation')
    return elevations


def elevation_gain(activity):
    assert_activity_field(activity, 'isTreadmill', 'extended')
    e = 0 if activity['isTreadmill'] else activity['elevationGain']
    return e * UNITS.meters


def avg_pace(activity, distance_unit=UNITS.mile, time_unit=UNITS.minute, keep_units=False):
    distance = get_distance(activity)
    time = get_duration(activity)

    result = time.to(time_unit) / distance.to(distance_unit)
    if not keep_units:
        result = result.magnitude
    return result


def get_pace_variability(activity):
    assert_activity_field(activity, 'speedVariability', 'extended')
    return activity['speedVariability']


def get_start_coordinates(activity):
    assert_activity_field(activity, 'startLatitude', 'summary')
    return (activity['startLatitude'], activity['startLongitude'])


def get_coordinates(activity):
    lats = get_records(activity, 'latitude')
    lons = get_records(activity, 'longitude')
    assert len(lats) == len(lons), "Found mismatch between length of latitudes (%d) and longitudes (%d) for ID=%s" % (len(lats), len(lons), activity['activityId'])  # noqa
    coordinates = []
    for i in range(len(lats)):
        if lats[i] == -1 and lons[i] == -1:
            # This is a null data point. Ignore it
            continue
        coordinates.append((lats[i], lons[i]))
    return coordinates


def get_location(activity, key):
    assert_activity_field(activity, key, 'extended')
    return activity[key]


def get_sunrise(activity):
    assert_activity_field(activity, 'sunriseLocal', 'extended')
    return srdate_to_datetime(activity['sunriseLocal'])


def get_sunset(activity):
    assert_activity_field(activity, 'sunsetLocal', 'extended')
    return srdate_to_datetime(activity['sunsetLocal'])


def get_moon_illumination_pct(activity):
    assert_activity_field(activity, 'moonPhase', 'extended')
    # 0.0 is new, .5 is full, 1.0 is new
    return ((0.5 - (abs(0.5 - activity['moonPhase']))) / 0.5) * 100.0


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
