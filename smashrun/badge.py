# vim: ft=python expandtab softtabstop=0 tabstop=4 shiftwidth=4

import copy
import dateutil
import logging
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


class BadgeSet(object):
    def __init__(self):
        self._badges = {}
        self._badges[1] = EarlyBird()
        self._badges[2] = NightOwl()
        self._badges[4] = Popular()
        self._badges[5] = OCD()
        self._badges[6] = OneMile()
        self._badges[9] = HalfMarathoner()
        self._badges[10] = TenKer()
        self._badges[16] = FiveForFive()
        self._badges[17] = TenForTen()
        self._badges[18] = TwentyForTwenty()
        self._badges[19] = FiftyForFifty()
        self._badges[20] = Perfect100()
        self._badges[21] = TenUnderYourBelt()
        self._badges[22] = TwentyUnderYourBelt()
        self._badges[23] = FiftyUnderYourBelt()
        self._badges[24] = ACenturyDown()
        self._badges[25] = Monster500()
        self._badges[26] = SolidWeek()
        self._badges[27] = RockedTheWeek()
        self._badges[28] = SolidMonth()
        self._badges[29] = RockedTheMonth()
        self._badges[32] = GuineaPig()
        self._badges[33] = FiveKer()
        self._badges[34] = BirthdayRun()
        self._badges[35] = Corleone()
        self._badges[36] = BroughtABuddy()
        self._badges[37] = GotFriends()
        self._badges[38] = SocialSeven()
        self._badges[39] = SharesWell()
        self._badges[40] = PackLeader()
        self._badges[131] = InItForJanuary()
        self._badges[132] = InItForFebruary()
        self._badges[133] = InItForMarch()
        self._badges[134] = InItForApril()
        self._badges[135] = InItForMay()
        self._badges[136] = InItForJune()
        self._badges[137] = InItForJuly()
        self._badges[138] = InItForAugust()
        self._badges[139] = InItForSeptember()
        self._badges[140] = InItForOctober()
        self._badges[141] = InItForNovember()
        self._badges[142] = InItForDecember()


    @property
    def badges(self):
        return self._badges.values()

    def add_user_info(self, info):
        logging.info("Adding user info for ID=%s %s" % (info['id'], info['name']))
        if info['id'] not in self._badges:
            logging.warning("Not adding user info for badge. Not implemented yet")
        else:
            self._badges[info['id']].add_user_info(info)

    def add_activity(self, activity):
        logging.debug("Adding activity %s" % (activity['activityId']))
        for b in self.badges:
            b.add_activity(activity)


class Badge(object):
    def __init__(self, name):
        self.activityId = None
        self.actualEarnedDate = None
        self.info = {}
        self.name = name

    def add_user_info(self, info):
        self.info = copy.copy(info)

    # activity is a hash containing the activity info as received from Smashrun
    def add_activity(self, activity):
        raise NotImplementedError("subclasses must implement add_activity")

    def acquire(self, activity):
        # Only allow badges to be acquired once -- Smashrun doesn't have levels (YET!)
        if self.acquired:
            return

        if self.activityId is None:
            self.activityId = activity['activityId']
            self.actualEarnedDate = srdate_to_datetime(activity['startDateTimeLocal'])
            logging.info("%s: acquired from activity %s on %s" % (self.name, self.activityId, self.actualEarnedDate))

    @property
    def acquired(self):
        if self.activityId is not None or self.actualEarnedDate is not None:
            return True
        else:
            return False

    def __get_info(self, key):
        if key not in self.info:
            print self
            raise RuntimeError("Must add user info before accessing '%s'"
                               % (key))
        return self.info[key]


##################################################################
#
# Badges that require N number of some sort of criteria. Criteria
# may reset and thus a reset method is provided
#
##################################################################
class CountingBadge(Badge):
    def __init__(self, name, limit, reset=0):
        super(CountingBadge, self).__init__(name)
        self.limit = limit
        self._reset = reset
        self.reset(log=False)

    def add_activity(self, activity):
        # Do this in two steps. increment() may invoke reset()
        delta = self.increment(activity)
        self.count += delta
        description = '[ID=%s START=%s DIST=%smi ELEV=%s\']' % (activity['activityId'],
                                                                srdate_to_datetime(activity['startDateTimeLocal']).strftime('%Y-%m-%d %H:%M'),
                                                                (activity['distance'] * UNITS.kilometer).to(UNITS.mile).magnitude,
                                                                '?')
        logging.info("%s: %s run qualifies. count now %s" % (self.name, description, self.count))
        if not self.acquired:
            if self.count >= self.limit:
                self.acquire(activity)

    def reset(self, log=True):
        self.count = self._reset
        if log:
            logging.info("%s resetting count to %s" % (self.name, self.count))

    def increment(self, activity):
        raise NotImplementedError("subclasses must implement increment")


class CountingUnitsBadge(CountingBadge):
    def __init__(self, name, limit, units, reset=0):
        super(CountingUnitsBadge, self).__init__(name, limit * units, reset * units)


class EarlyBird(CountingUnitsBadge):
    def __init__(self):
        super(EarlyBird, self).__init__('Early Bird', 10, UNITS.day)

    def increment(self, activity):
        # FIXME: What if there are 2 runs before 7 on a given day?
        start_date = srdate_to_datetime(activity['startDateTimeLocal'])
        sevenAM = start_date.replace(hour=7, minute=0, second=0)

        if start_date <= sevenAM:
            return 1 * UNITS.day
        return 0 * UNITS.day


class NightOwl(CountingUnitsBadge):
    def __init__(self):
        super(NightOwl, self).__init__('Night Owl', 10, units=UNITS.day)

    def increment(self, activity):
        start_date = srdate_to_datetime(activity['startDateTimeLocal'])
        end_date = start_date + timedelta(seconds=activity['duration'])
        ninePM = end_date.replace(hour=21, minute=0, second=0)

        if end_date >= ninePM:
            return 1 * UNITS.day
        return 0 * UNITS.day

class RunStreakBadge(CountingUnitsBadge):
    def __init__(self, name, limit, units=UNITS.day):
        super(RunStreakBadge, self).__init__(name, limit, units)
        self.datetime_of_lastrun = None

    def increment(self, activity):
        start_date = srdate_to_datetime(activity['startDateTimeLocal'])

        streak_broken = False
        if self.datetime_of_lastrun is not None:
            delta = start_date - self.datetime_of_lastrun
            streak_broken = delta.days > 1 or (delta.days == 1 and (delta.seconds > 0 or delta.microseconds > 0))

        if streak_broken:
            self.reset()

        self.datetime_of_lastrun = start_date
        return 1 * UNITS.day

class OneMile(RunStreakBadge):
    def __init__(self):
        super(OneMile, self).__init__('One Mile', 1)

class FiveForFive(RunStreakBadge):
    def __init__(self):
        super(FiveForFive, self).__init__('5 for 5', 5)

class TenForTen(RunStreakBadge):
    def __init__(self):
        super(TenForTen, self).__init__('10 for 10', 10)

class TwentyForTwenty(RunStreakBadge):
    def __init__(self):
        super(TwentyForTwenty, self).__init__('20 for 20', 20)

class FiftyForFifty(RunStreakBadge):
    def __init__(self):
        super(FiftyForFifty, self).__init__('50 for 50', 50)

class Perfect100(RunStreakBadge):
    def __init__(self):
        super(Perfect100, self).__init__('Perfect 100', 100)



##################################################################
#
# Badges that require some total distance to be run over the course
# of any number of runs
#
##################################################################
class TotalMileageBadge(CountingUnitsBadge):
    def __init__(self, name, limit, units=UNITS.mile):
        super(TotalMileageBadge, self).__init__(name, limit, units)

    def increment(self, activity):
        return activity['distance'] * UNITS.kilometer

class TenUnderYourBelt(TotalMileageBadge):
    def __init__(self):
        super(TenUnderYourBelt, self).__init__('10 under your belt', 10)

class TwentyUnderYourBelt(TotalMileageBadge):
    def __init__(self):
        super(TwentyUnderYourBelt, self).__init__('20 under your belt', 20)

class FiftyUnderYourBelt(TotalMileageBadge):
    def __init__(self):
        super(FiftyUnderYourBelt, self).__init__('50 under your belt', 50)

class ACenturyDown(TotalMileageBadge):
    def __init__(self):
        super(ACenturyDown, self).__init__('A century down', 100)

class Monster500(TotalMileageBadge):
    def __init__(self):
        super(Monster500, self).__init__('Monster 500', 500)


class WeeklyTotalMileage(TotalMileageBadge):
    def __init__(self, name, limit, units=UNITS.mile):
        super(WeeklyTotalMileage, self).__init__(name, limit, units)
        self.runs = [] # list of (datetime, distance) tuples

    def increment(self, activity):
        start_date = srdate_to_datetime(activity['startDateTimeLocal'])
        # FIXME: Is it really 7 days like this or is it calendar days?
        earliest_valid_date = start_date - timedelta(days=7)

        self.runs = [x for x in self.runs if x[0] >= earliest_valid_date]
        self.runs.append((start_date, activity['distance'] * UNITS.kilometer))
        
        # Always reset since we're going to sum ourselves based on runs
        self.reset()
        return sum([x[1] for x in self.runs])

class SolidWeek(WeeklyTotalMileage):
    def __init__(self):
        super(SolidWeek, self).__init__('Solid week', 10)

class RockedTheWeek(WeeklyTotalMileage):
    def __init__(self):
        super(RockedTheWeek, self).__init__('Rocked the week', 25)

class MonthlyTotalMileageBadge(TotalMileageBadge):
    def __init__(self, name, limit, units=UNITS.mile):
        super(MonthlyTotalMileageBadge, self).__init__(name, limit, units)
        self.datetime_of_lastrun = None

    def increment(self, activity):
        start_date = srdate_to_datetime(activity['startDateTimeLocal'])

        is_new_month = False
        if self.datetime_of_lastrun is None:
            is_new_month = True
        else:
            # It's a new month if we have a new month or a new year
            if self.datetime_of_lastrun.year != start_date.year:
                is_new_month = True
            elif self.datetime_of_lastrun.month != start_date.month:
                is_new_month = True

        if is_new_month:
            self.reset()

        self.datetime_of_lastrun = start_date
        return activity['distance'] * UNITS.kilometer

class SolidMonth(MonthlyTotalMileageBadge):
    def __init__(self):
        super(SolidMonth, self).__init__('Solid month', 30)

class RockedTheMonth(MonthlyTotalMileageBadge):
    def __init__(self):
        super(RockedTheMonth, self).__init__('Rocked the month', 75)


##################################################################
#
# Badges that require a single run of a specified distance
#
##################################################################
class SingleMileageBadge(CountingUnitsBadge):
    def __init__(self, name, limit, units=UNITS.kilometer):
        super(SingleMileageBadge, self).__init__(name, limit, units)

    def increment(self, activity):
        # Single run, so reset each time
        self.reset()
        return activity['distance'] * UNITS.kilometer

class FiveKer(SingleMileageBadge):
    def __init__(self):
        super(FiveKer, self).__init__('5ker', 5)

class TenKer(SingleMileageBadge):
    def __init__(self):
        super(TenKer, self).__init__('10ker', 10)

class HalfMarathoner(SingleMileageBadge):
    def __init__(self):
        super(HalfMarathoner, self).__init__('Half Marathoner', 13.1, units=UNITS.mile)

##################################################################
#
# Badges that don't have an associated activity necessarily 
# May also be a badge that requires knowledge outside of what's 
# available via API
#
##################################################################
class NoActivityBadge(Badge):
    def __init__(self, name):
        super(NoActivityBadge, self).__init__(name)

    def add_activity(self, activity):
        pass

    def add_user_info(self, info):
        super(NoActivityBadge, self).add_user_info(info)
        self.actualEarnedDate = srdate_to_datetime(info['dateEarnedUTC'], utc=True)


class Popular(NoActivityBadge):
    def __init__(self):
        super(Popular, self).__init__('Popular')

class OCD(NoActivityBadge):
    def __init__(self):
        super(OCD, self).__init__('OCD')

class GuineaPig(NoActivityBadge):
    def __init__(self):
        super(GuineaPig, self).__init__('Guinea pig')

class BirthdayRun(NoActivityBadge):
    def __init__(self):
        super(BirthdayRun, self).__init__('Birthday Run')

class BroughtABuddy(NoActivityBadge):
    def __init__(self):
        super(BroughtABuddy, self).__init__('Brought a buddy')

class GotFriends(NoActivityBadge):
    def __init__(self):
        super(GotFriends, self).__init__('Got friends')

class SocialSeven(NoActivityBadge):
    def __init__(self):
        super(SocialSeven, self).__init__('Social seven')

class SharesWell(NoActivityBadge):
    def __init__(self):
        super(SharesWell, self).__init__('Shares well')

class PackLeader(NoActivityBadge):
    def __init__(self):
        super(PackLeader, self).__init__('Pack Leader')

####################################################
#
# In It For "X" Monthly Badges
#
####################################################
class InItForMonthBadge(CountingUnitsBadge):
    def __init__(self, name, month):
        super(InItForMonthBadge, self).__init__(name, 10, UNITS.day)
        self.month = month
        self.year_of_last_run = None
        self.days = set()

    def reset(self, log=True):
        super(InItForMonthBadge, self).reset(log=log)
        self.days = set()

    def increment(self, activity):
        # FIXME: is using start date correct?
        start_date = srdate_to_datetime(activity['startDateTimeLocal'])

        # This isn't our month. Ignore
        if start_date.month != self.month:
            return 0 * UNITS.month

        # If we've changed years, reset
        if start_date.year != self.year_of_last_run:
            self.reset()
        self.year_of_last_run = start_date.year

        if start_date.day not in self.days:
            self.days.add(start_date.day)
            return 1 * UNITS.day
        else:
            # Already have a run on this day. Don't double count
            return 0 * UNITS.day


class InItForJanuary(InItForMonthBadge):
    def __init__(self):
        super(InItForJanuary, self).__init__('In it for January', 1)

class InItForFebruary(InItForMonthBadge):
    def __init__(self):
        super(InItForFebruary, self).__init__('In it for February', 2)

class InItForMarch(InItForMonthBadge):
    def __init__(self):
        super(InItForMarch, self).__init__('In it for March', 3)

class InItForApril(InItForMonthBadge):
    def __init__(self):
        super(InItForApril, self).__init__('In it for April', 4)

class InItForMay(InItForMonthBadge):
    def __init__(self):
        super(InItForMay, self).__init__('In it for May', 5)

class InItForJune(InItForMonthBadge):
    def __init__(self):
        super(InItForJune, self).__init__('In it for June', 6)

class InItForJuly(InItForMonthBadge):
    def __init__(self):
        super(InItForJuly, self).__init__('In it for July', 7)

class InItForAugust(InItForMonthBadge):
    def __init__(self):
        super(InItForAugust, self).__init__('In it for August', 8)

class InItForSeptember(InItForMonthBadge):
    def __init__(self):
        super(InItForSeptember, self).__init__('In it for September', 9)

class InItForOctober(InItForMonthBadge):
    def __init__(self):
        super(InItForOctober, self).__init__('In it for October', 10)

class InItForNovember(InItForMonthBadge):
    def __init__(self):
        super(InItForNovember, self).__init__('In it for November', 11)

class InItForDecember(InItForMonthBadge):
    def __init__(self):
        super(InItForDecember, self).__init__('In it for December', 12)


####################################################
#
# Misc Badges
#
####################################################
class Corleone(Badge):
    def __init__(self):
        super(Corleone, self).__init__('Corleone')
        self.datetime_of_lastrun = None

    def add_activity(self, activity):
        start_date = srdate_to_datetime(activity['startDateTimeLocal'])
        if self.datetime_of_lastrun is not None:
            if (start_date - self.datetime_of_lastrun).days >= 30:
                self.acquire(activity)

        self.datetime_of_lastrun = start_date
