# vim: ft=python expandtab softtabstop=0 tabstop=4 shiftwidth=4

import calendar
import copy
import geocoder
import logging
import math
from datetime import timedelta
import utils as sru


UNITS = sru.UNITS


class BadgeSet(object):
    def __init__(self, start_date, google_apikey=None, only_ids=[]):
        self.start_date = start_date

        self._badges = {}
        self._badges[1] = EarlyBird()
        self._badges[2] = NightOwl()
        self._badges[3] = LunchHour()
        self._badges[4] = Popular()
        self._badges[5] = OCD()
        self._badges[6] = OneMile()
        self._badges[7] = Marathoner()
        self._badges[8] = UltraMarathoner()
        self._badges[9] = HalfMarathoner()
        self._badges[10] = TenKer()
        self._badges[11] = BeatA9YearOld()
        self._badges[12] = PoundedPalin()
        self._badges[13] = PastDiddy()
        self._badges[14] = UnderOprah()
        self._badges[15] = ClearedKate()
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
        self._badges[30] = RunNutMonth()
        self._badges[31] = Veteran()
        self._badges[32] = GuineaPig()
        self._badges[33] = FiveKer()
        self._badges[34] = BirthdayRun()
        self._badges[35] = Corleone()
        self._badges[36] = BroughtABuddy()
        self._badges[37] = GotFriends()
        self._badges[38] = SocialSeven()
        self._badges[39] = SharesWell()
        self._badges[40] = PackLeader()
        self._badges[101] = NYCPhilly()
        self._badges[102] = LondonParis()
        self._badges[103] = SydneyMelbourne()
        self._badges[104] = NYCChicago()
        self._badges[105] = MiamiToronto()
        self._badges[106] = ChariotsOfFire()
        self._badges[107] = WentToWork()
        self._badges[108] = ThatsADay()
        self._badges[109] = WeekNotWeak()
        self._badges[110] = OutlastTheAlamo()
        self._badges[111] = ChillRunner()
        self._badges[112] = EasyRunner()
        self._badges[113] = RoadRunner()
        self._badges[114] = Mercury()
        self._badges[115] = FastAndSlow()
        self._badges[126] = Stairs()
        self._badges[127] = SteepStairs()
        self._badges[128] = LongStairs()
        self._badges[129] = LongSteepStairs()
        self._badges[130] = ToweringStairs()
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
        self._badges[143] = ColorPicker()
        self._badges[144] = ThreeSixtyFiveDays()
        self._badges[145] = ThreeSixtyFiveOf730()
        self._badges[146] = ThreeSixtyFiveOf365()
        self._badges[147] = AYearInRunning()
        self._badges[148] = LeapYearSweep()
        self._badges[149] = SmashrunForLife()
        self._badges[150] = Translator()
        # self._badges[151] = TBD_UltraUltra100k()
        self._badges[201] = USofR()
        self._badges[202] = International()
        self._badges[203] = TopAndBottom()
        self._badges[204] = FourCorners()
        self._badges[205] = InternationalSuperRunner()
        self._badges[206] = SpecialAgent()
        # self._badges[207] = TBD_NCAAFitnessTest()
        self._badges[208] = FrenchForeignLegion()
        self._badges[209] = SuperAgent()
        self._badges[210] = ArmyRanger()
        # self._badges[211] = TBD_FastStart5k()
        # self._badges[212] = TBD_FastFinish5k()
        # self._badges[213] = TBD_FastMiddle10k()
        # self._badges[214] = TBD_FastStartAndFinish5k()
        # self._badges[215] = TBD_SuperFastStart5k()
        self._badges[216] = Sunriser()
        self._badges[217] = FullMoonRunner()
        self._badges[218] = Sunsetter()
        self._badges[219] = LongestDay()
        self._badges[220] = ShortestDay()
        self._badges[221] = FourFurther()
        self._badges[222] = SixFurther()
        self._badges[223] = FourFarFurther()
        self._badges[224] = SixFarFurther()
        self._badges[225] = FurtherToFarther()
        # self._badges[226] = ShortAndSteady()
        # self._badges[227] = LongAndSteady()
        # self._badges[228] = ShortAndSolid()
        # self._badges[229] = LongAndSolid()
        # self._badges[230] = LongAndRockSolid()
        self._badges[231] = TwoBy33()
        self._badges[232] = TwoBy99()
        self._badges[233] = TwoBy33By10k()
        self._badges[234] = TwoBy99By5k()
        self._badges[235] = TwoBy365By10k()
        self._badges[236] = TopOfTable()
        self._badges[237] = ClimbedHalfDome()
        self._badges[238] = ReachedFitzRoy()
        self._badges[239] = MatterhornMaster()
        self._badges[240] = ConqueredEverest()
        self._badges[241] = ToweredPisa()
        self._badges[242] = TopOfWashington()
        self._badges[243] = OverTheEiffel()
        self._badges[244] = AboveTheBurj()
        self._badges[245] = ToPikesPeak()

        if len(only_ids):
            keys_to_del = [x for x in self._badges.keys() if x not in only_ids]
            for key in keys_to_del:
                del self._badges[key]

        for badge in self._badges.values():
            badge.google_apikey = google_apikey

    @property
    def badges(self):
        return self._badges.values()

    def add_user_info(self, info):
        logging.debug("Adding user info for ID=%s %s" % (info['id'], info['name']))
        if info['id'] not in self._badges:
            logging.warning("Not adding user info for badge. Not implemented yet")
        else:
            self._badges[info['id']].add_user_info(info)

    def add_activity(self, activity):
        start_date = sru.get_start_time(activity)
        if self.start_date is None or start_date >= self.start_date:
            logging.debug("Adding activity %s %s" % (sru.get_start_time(activity), activity['activityId']))
            for b in self.badges:
                logging.debug("Checking %s" % (b.name))
                b._add_activity(activity)
        else:
            logging.debug("Skipping activity %s that occured before %s" % (activity['activityId'], self.start_date))


class Badge(object):
    def __init__(self, name, requires_unique_days=False):
        self.activityId = None
        self.actualEarnedDate = None
        self.info = {}
        self.name = name
        self.google_apikey = None
        self.requires_unique_days = requires_unique_days
        self.activities = {}

    def add_user_info(self, info):
        self.info = copy.copy(info)

    def add_activity(self, activity):
        # Only allow badges to be acquired once -- Smashrun doesn't have levels (YET!)
        if self.acquired:
            return
        if self.requires_unique_days:
            start_date = sru.get_start_time(activity)
            activity_day = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            if activity_day in self.activities:
                logging.debug("%s: Not adding activity %s on %s (already processed ID=%s on this date)" %
                              (self.name, activity['activityId'], start_date, self.activities[activity_day]))
                return

        self._add_activity(activity)

    # activity is a hash containing the activity info as received from Smashrun
    def _add_activity(self, activity):
        raise NotImplementedError("subclasses must implement _add_activity")

    def acquire(self, activity):
        if self.activityId is None:
            self.activityId = activity['activityId']
            self.actualEarnedDate = sru.get_start_time(activity)
            logging.info("%s: acquired from activity %s on %s" % (self.name, self.activityId, self.actualEarnedDate))

    @property
    def acquired(self):
        if self.activityId is not None or self.actualEarnedDate is not None:
            return True
        else:
            return False

    def __get_info(self, key):
        if key not in self.info:
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
    def __init__(self, name, limit, reset=0, **kwargs):
        super(CountingBadge, self).__init__(name, **kwargs)
        self.limit = limit
        self._reset = reset
        self.reset(log=False)

    def _add_activity(self, activity):
        # Do this in two steps. increment() may invoke reset()
        delta = self.increment(activity)
        self.count += delta
        if delta:
            description = '[ID=%s START=%s DIST=%smi AVGPACE=%smin/mi ELEV=%s\']' % (activity['activityId'],
                                                                                     sru.get_start_time(activity).strftime('%Y-%m-%d %H:%M'),
                                                                                     sru.get_distance(activity).to(UNITS.mile).magnitude,
                                                                                     sru.avg_pace(activity, distance_unit=UNITS.mile, time_unit=UNITS.minutes),
                                                                                     '?')
            logging.debug("%s: %s run qualifies. count now %s" % (self.name, description, self.count))

        if self.count >= self.limit:
            self.acquire(activity)

    def reset(self, log=True):
        self.count = self._reset
        if log:
            logging.debug("%s resetting count to %s" % (self.name, self.count))

    def increment(self, activity):
        raise NotImplementedError("subclasses must implement increment")


##################################################################
#
# A counting badge that will use units from the pint package
#
##################################################################
class CountingUnitsBadge(CountingBadge):
    def __init__(self, name, limit, units, reset=0, **kwargs):
        super(CountingUnitsBadge, self).__init__(name, limit * units, reset * units, **kwargs)
        self.units = units


##################################################################
#
# Total time badges
#
##################################################################
class TotalTimeBadge(CountingUnitsBadge):
    def __init__(self, name, limit, units=UNITS.hours):
        super(TotalTimeBadge, self).__init__(name, limit, units)

    def increment(self, activity):
        return sru.get_duration(activity)


class ChariotsOfFire(TotalTimeBadge):
    def __init__(self):
        super(ChariotsOfFire, self).__init__('Chariots of Fire', 124, units=UNITS.minutes)


class WentToWork(TotalTimeBadge):
    def __init__(self):
        super(WentToWork, self).__init__('Went to work', 8)


class ThatsADay(TotalTimeBadge):
    def __init__(self):
        super(ThatsADay, self).__init__('That\'s a day', 24)


class WeekNotWeak(TotalTimeBadge):
    def __init__(self):
        super(WeekNotWeak, self).__init__('Week not weak', 168)


class OutlastTheAlamo(TotalTimeBadge):
    def __init__(self):
        super(OutlastTheAlamo, self).__init__('Outlast the Alamo', 312)


##################################################################
#
# Misc counting badges
#
##################################################################
class EarlyBird(CountingUnitsBadge):
    def __init__(self):
        super(EarlyBird, self).__init__('Early Bird', 10, UNITS.day, requires_unique_days=True)

    def increment(self, activity):
        # FIXME: What if there are 2 runs before 7 on a given day?
        start_date = sru.get_start_time(activity)
        sevenAM = start_date.replace(hour=7, minute=0, second=0)

        if start_date <= sevenAM:
            return 1 * UNITS.day
        return 0 * UNITS.day


class NightOwl(CountingUnitsBadge):
    def __init__(self):
        super(NightOwl, self).__init__('Night Owl', 10, units=UNITS.day, requires_unique_days=True)

    def increment(self, activity):
        # FIXME: What if there are 2 runs after 9 on a given day?
        start_date = sru.get_start_time(activity)
        end_date = start_date + timedelta(seconds=sru.get_duration(activity).magnitude)
        ninePM = end_date.replace(hour=21, minute=0, second=0)

        if end_date >= ninePM:
            return 1 * UNITS.day
        return 0 * UNITS.day


class LunchHour(CountingUnitsBadge):
    def __init__(self):
        super(LunchHour, self).__init__('Lunch Hour', 10, units=UNITS.day, requires_unique_days=True)

    def increment(self, activity):
        # FIXME: What if there are 2 runs during lunch on a given day?
        start_date = sru.get_start_time(activity)

        is_weekday = start_date.weekday() in range(0, 6)  # Mon-Fri
        noon = start_date.replace(hour=12, minute=0, second=0)
        twoPM = start_date.replace(hour=14, minute=0, second=0)

        if is_weekday and start_date >= noon and start_date <= twoPM:
            return 1 * UNITS.day
        return 0 * UNITS.day


##################################################################
#
# Badges that require a running streak (consecutive days)
#
##################################################################
class RunStreakBadge(CountingBadge):
    def __init__(self, name, limit, days_between_runs=1, min_distance=None):
        limit = int(math.ceil(float(limit) / float(days_between_runs)))
        super(RunStreakBadge, self).__init__(name, limit, requires_unique_days=True)
        self.date_of_next_run = None
        self.days_between_runs = days_between_runs
        self.min_distance = min_distance

    @staticmethod
    def midnight_of_datetime(dt):
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    def increment(self, activity):
        result = 0
        if self.min_distance is not None and sru.get_distance(activity) < self.min_distance:
            # If there's a minimum distance and this doesn't qualify, just return 0
            # Don't udpate or reset anything else
            pass
        else:
            start_date = sru.get_start_time(activity)
            if self.date_of_next_run is None:
                self.date_of_next_run = RunStreakBadge.midnight_of_datetime(start_date)

            if start_date < self.date_of_next_run:
                # This run doesn't qualify. Don't update or reset anything
                pass
            else:
                if start_date > (self.date_of_next_run + timedelta(days=1)):
                    # We broke the streak :(
                    logging.debug("%s broken due to no run on %s" % (self.name, self.date_of_next_run.strftime('%Y-%m-%d')))
                    self.reset()

                result = 1
                self.date_of_next_run = RunStreakBadge.midnight_of_datetime(start_date + timedelta(days=self.days_between_runs))

        return result


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


class ThreeSixtyFiveOf365(RunStreakBadge):
    def __init__(self):
        super(ThreeSixtyFiveOf365, self).__init__('365 of 365', 365)


class TwoBy33(RunStreakBadge):
    def __init__(self):
        super(TwoBy33, self).__init__('Two by 33', 33, 2)


class TwoBy99(RunStreakBadge):
    def __init__(self):
        super(TwoBy99, self).__init__('Two by 99', 99, 2)


class TwoBy33By10k(RunStreakBadge):
    def __init__(self):
        super(TwoBy33By10k, self).__init__('Two by 33 by 10k', 33, 2, 10 * UNITS.kilometer)


class TwoBy99By5k(RunStreakBadge):
    def __init__(self):
        super(TwoBy99By5k, self).__init__('Two by 99 by 5k', 99, 2, 5 * UNITS.kilometer)


class TwoBy365By10k(RunStreakBadge):
    def __init__(self):
        super(TwoBy365By10k, self).__init__('Two by 365 by 10k', 365, 2, 10 * UNITS.kilometer)


class ThreeSixtyFiveDays(CountingBadge):
    def __init__(self):
        super(ThreeSixtyFiveDays, self).__init__('365 days', 365, requires_unique_days=True)

    def increment(self, activity):
        # This only gets invoked for runs on unique days
        return 1


class ThreeSixtyFiveOf730(Badge):
    def __init__(self):
        super(ThreeSixtyFiveOf730, self).__init__('365 of 730', requires_unique_days=True)
        self.runs = []

    def _add_activity(self, activity):
        start_date = sru.get_start_time(activity)
        earliest_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=730)

        # Filter to runs happening on the last 730 days
        self.runs = [x for x in self.runs if x[0] >= earliest_date]
        if len(self.runs) >= 365:
            self.acquire(activity)


class AYearInRunning(Badge):
    def __init__(self, name='A year in running'):
        super(AYearInRunning, self).__init__(name, requires_unique_days=True)
        self.enabled = False
        self.last_available_start_time = None

    def _add_activity(self, activity):
        start_date = sru.get_start_time(activity)

        # Jan 1 of the current year
        earliest_date = start_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        last_date = earliest_date.replace(year=earliest_date.year + 1) - timedelta(seconds=1)

        if sru.is_same_day(start_date, earliest_date):
            self.enabled = True

        if not self.enabled:
            return

        if sru.is_same_day(start_date, last_date):
            self.acquire(activity)

        if self.last_available_start_time is not None:
            if start_date > self.last_available_start_time:
                # Streak was broken. Try next year!
                logging.info("%s: Streak broken on %s by ID=%s" % (self.name, self.last_available_start_time, activity['activityId']))
                self.enabled = False
                return

        # Do it again tomorrow. Last available run time is tomorrow night at 23:59:59
        self.last_available_start_time = (start_date + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(microseconds=1)


class LeapYearSweep(AYearInRunning):
    def __init__(self):
        super(LeapYearSweep, self).__init__('Leap year sweep')

    def _add_activity(self, activity):
        start_date = sru.get_start_time(activity)
        if calendar.isleap(start_date.year):
            super(LeapYearSweep, self)._add_activity(activity)


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
        return sru.get_distance(activity)


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


##################################################################
#
# City to city badges
#
##################################################################
class NYCPhilly(TotalMileageBadge):
    def __init__(self):
        super(NYCPhilly, self).__init__('NYC-Philly', 93)


class LondonParis(TotalMileageBadge):
    def __init__(self):
        super(LondonParis, self).__init__('London-Paris', 232)


class SydneyMelbourne(TotalMileageBadge):
    def __init__(self):
        super(SydneyMelbourne, self).__init__('Sydney-Melbourne', 561)


class NYCChicago(TotalMileageBadge):
    def __init__(self):
        super(NYCChicago, self).__init__('NYC-Chicago', 858)


class MiamiToronto(TotalMileageBadge):
    def __init__(self):
        super(MiamiToronto, self).__init__('Miami-Toronto', 1488)


##################################################################
#
# Badges that require some total distance to be run over a single week
#
##################################################################
class WeeklyTotalMileage(TotalMileageBadge):
    def __init__(self, name, limit, units=UNITS.mile):
        super(WeeklyTotalMileage, self).__init__(name, limit, units)
        self.runs = []  # list of (datetime, distance) tuples

    def increment(self, activity):
        start_date = sru.get_start_time(activity)
        # FIXME: Is it really 7 days like this or is it calendar days?
        earliest_valid_date = start_date - timedelta(days=7)

        self.runs = [x for x in self.runs if x[0] >= earliest_valid_date]
        self.runs.append((start_date, sru.get_distance(activity)))

        # Always reset since we're going to sum ourselves based on runs
        self.reset()
        return sum([x[1] for x in self.runs])


class SolidWeek(WeeklyTotalMileage):
    def __init__(self):
        super(SolidWeek, self).__init__('Solid week', 10)


class RockedTheWeek(WeeklyTotalMileage):
    def __init__(self):
        super(RockedTheWeek, self).__init__('Rocked the week', 25)


##################################################################
#
# Badges that require some total distance to be run in a single month
#
##################################################################
class MonthlyTotalMileageBadge(TotalMileageBadge):
    def __init__(self, name, limit, units=UNITS.mile):
        super(MonthlyTotalMileageBadge, self).__init__(name, limit, units)
        self.datetime_of_lastrun = None

    def increment(self, activity):
        start_date = sru.get_start_time(activity)

        is_new_month = False
        if sru.is_different_month(self.datetime_of_lastrun, start_date):
            is_new_month = True

        if is_new_month:
            self.reset()

        self.datetime_of_lastrun = start_date
        return sru.get_distance(activity)


class SolidMonth(MonthlyTotalMileageBadge):
    def __init__(self):
        super(SolidMonth, self).__init__('Solid month', 30)


class RockedTheMonth(MonthlyTotalMileageBadge):
    def __init__(self):
        super(RockedTheMonth, self).__init__('Rocked the month', 75)


class RunNutMonth(MonthlyTotalMileageBadge):
    def __init__(self):
        super(RunNutMonth, self).__init__('Run nut month', 300)


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
        return sru.get_distance(activity)


class FiveKer(SingleMileageBadge):
    def __init__(self):
        super(FiveKer, self).__init__('5ker', 5)


class TenKer(SingleMileageBadge):
    def __init__(self):
        super(TenKer, self).__init__('10ker', 10)


class HalfMarathoner(SingleMileageBadge):
    def __init__(self):
        super(HalfMarathoner, self).__init__('Half Marathoner', 13.1, units=UNITS.mile)


class Marathoner(SingleMileageBadge):
    def __init__(self):
        super(Marathoner, self).__init__('Marathoner', 26.2, units=UNITS.mile)


class UltraMarathoner(SingleMileageBadge):
    def __init__(self):
        super(UltraMarathoner, self).__init__('Ultra-Marathoner', 50)


class SingleMileageWithinDuration(CountingUnitsBadge):
    # Note most badges in this subclass are miles, so we change the default
    # units to miles
    def __init__(self, name, limit, duration, units=UNITS.miles):
        super(SingleMileageWithinDuration, self).__init__(name, limit, units)
        self.duration = duration

    def increment(self, activity):
        if (sru.get_duration(activity)) < self.duration:
            self.reset()
            return sru.get_distance(activity)
        return 0 * UNITS.kilometer


class ArmyRanger(SingleMileageWithinDuration):
    def __init__(self):
        super(ArmyRanger, self).__init__('Army Ranger', 5, 40 * UNITS.minutes)


class FrenchForeignLegion(SingleMileageWithinDuration):
    def __init__(self):
        # Effectively a 12min cooper test
        super(FrenchForeignLegion, self).__init__('French Foreign Legion', 2800, 12 * UNITS.minutes, units=UNITS.meters)


class BeatA9YearOld(SingleMileageWithinDuration):
    def __init__(self):
        # FIXME: The Smashrun says this is <= 2:55, but then says < 2:55. Not sure which
        super(BeatA9YearOld, self).__init__('Beat a 9yr old', 26.2, (2 * UNITS.hour) + (55 * UNITS.minute))


class PoundedPalin(SingleMileageWithinDuration):
    def __init__(self):
        super(PoundedPalin, self).__init__('Pounded Palin', 26.2, (3 * UNITS.hour) + (59 * UNITS.minute))


class PastDiddy(SingleMileageWithinDuration):
    def __init__(self):
        super(PastDiddy, self).__init__('Past Diddy', 26.2, (4 * UNITS.hour) + (15 * UNITS.minute))


class UnderOprah(SingleMileageWithinDuration):
    def __init__(self):
        super(UnderOprah, self).__init__('Under Oprah', 26.2, (4 * UNITS.hour) + (29 * UNITS.minute))


class ClearedKate(SingleMileageWithinDuration):
    def __init__(self):
        super(ClearedKate, self).__init__('Cleared Kate', 26.2, (5 * UNITS.hour) + (29 * UNITS.minute))


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

    def _add_activity(self, activity):
        pass

    def add_user_info(self, info):
        super(NoActivityBadge, self).add_user_info(info)
        self.actualEarnedDate = sru.get_badge_earned_time(info)


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


class Translator(NoActivityBadge):
    def __init__(self):
        super(Translator, self).__init__('Translator')


class ColorPicker(NoActivityBadge):
    def __init__(self):
        super(ColorPicker, self).__init__('Color Picker')


####################################################
#
# In It For "X" Monthly Badges
#
####################################################
class InItForMonthBadge(CountingUnitsBadge):
    def __init__(self, name, month):
        super(InItForMonthBadge, self).__init__(name, 10, UNITS.day, requires_unique_days=True)
        self.month = month
        self.datetime_of_lastrun = None

    def reset(self, log=True):
        super(InItForMonthBadge, self).reset(log=log)

    def increment(self, activity):
        # FIXME: is using start date correct?
        start_date = sru.get_start_time(activity)

        # This isn't our month. Ignore
        if start_date.month != self.month:
            return 0 * UNITS.month

        # If we've changed years, reset
        if sru.is_different_year(self.datetime_of_lastrun, start_date):
            self.reset()
        self.datetime_of_lastrun = start_date

        return 1 * UNITS.day


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


class AvgPaceBadge(CountingBadge):
    def __init__(self, name, pace, limit=10, slower_ok=False):
        super(AvgPaceBadge, self).__init__(name, limit)
        self.pace = pace
        self.datetime_of_lastrun = None
        if slower_ok:
            self.meets_criteria = lambda x, y: x >= y
        else:
            self.meets_criteria = lambda x, y: x <= y

    def increment(self, activity):
        start_date = sru.get_start_time(activity)

        # Reset if we've changed months since the last activity
        if sru.is_different_month(self.datetime_of_lastrun, start_date):
            self.reset()
        self.datetime_of_lastrun = start_date

        if self.meets_criteria(sru.avg_pace(activity), self.pace):
            return 1
        return 0


class EasyRunner(AvgPaceBadge):
    def __init__(self):
        super(EasyRunner, self).__init__('Easy runner', 10, slower_ok=True)


class ChillRunner(AvgPaceBadge):
    def __init__(self):
        super(ChillRunner, self).__init__('Chill runner', 12, slower_ok=True)


class RoadRunner(AvgPaceBadge):
    def __init__(self):
        super(RoadRunner, self).__init__('Roadrunner', 8, slower_ok=False)


class Mercury(AvgPaceBadge):
    def __init__(self):
        super(Mercury, self).__init__('Mercury', 7, slower_ok=False)


class FastAndSlow(Badge):
    def __init__(self):
        super(FastAndSlow, self).__init__('Fast & Slow')
        self.fast = 0
        self.slow = 0

    def _add_activity(self, activity):
        if sru.avg_pace(activity) < 8:
            self.fast += 1
        if sru.avg_pace(activity) > 10:
            self.slow += 1
        if self.fast >= 10 and self.slow >= 10:
            self.acquire(activity)


####################################################
#
# Stairs
#
####################################################
class StairsBadge(Badge):
    def __init__(self, name, min_months, delta):
        super(StairsBadge, self).__init__(name)
        self.delta = delta
        self.stepped = False
        self.step_activity = None
        self.min_months = min_months
        self.cur_month = 0 * UNITS.miles
        self.prev_month = 0 * UNITS.miles
        self.consecutive_months = 0
        self.prev_activity_datetime = None

    def update_cur_month_value(self, distance):
        self.cur_month += distance

    def _add_activity(self, activity):
        start_date = sru.get_start_time(activity)
        distance = sru.get_distance(activity)

        # If we walked into a new month, figure out if last month contained a step
        if sru.is_different_month(self.prev_activity_datetime, start_date):
            if self.stepped:
                self.consecutive_months += 1
                result = 'STEP #%d' % (self.consecutive_months)
            else:
                # Sad trombone!
                result = 'FAIL'
                self.consecutive_months = 0

            if self.prev_activity_datetime is not None:
                logging.debug("%s: Distance for %s/%s: %s [%s]" %
                              (self.name, self.prev_activity_datetime.month, self.prev_activity_datetime.year, self.cur_month, result))
            self.stepped = False
            self.prev_month = self.cur_month
            self.cur_month = 0 * UNITS.miles

        # Smashrun seems to round this way, so do it here too
        self.update_cur_month_value(round(distance.to(UNITS.miles).magnitude, 2) * UNITS.miles)
        self.prev_activity_datetime = start_date

        if not self.stepped:
            if self.prev_month > (0 * UNITS.miles):
                if self.delta is None:
                    if self.cur_month > self.prev_month:
                        self.stepped = True
                        self.step_activity = activity
                elif self.cur_month > (self.prev_month + self.delta):
                    self.stepped = True
                    self.step_activity = activity

        if self.consecutive_months >= self.min_months:
            self.acquire(self.step_activity)


class Stairs(StairsBadge):
    def __init__(self):
        super(Stairs, self).__init__('Stairs', 4, None)


class SteepStairs(StairsBadge):
    def __init__(self):
        super(SteepStairs, self).__init__('Steep stairs', 4, 5 * UNITS.miles)


class LongStairs(StairsBadge):
    def __init__(self):
        super(LongStairs, self).__init__('Long stairs', 6, None)


class LongSteepStairs(StairsBadge):
    def __init__(self):
        super(LongSteepStairs, self).__init__('Long/Steep stairs', 6, 5 * UNITS.miles)


class ToweringStairs(StairsBadge):
    def __init__(self):
        super(ToweringStairs, self).__init__('Towering stairs', 6, 10 * UNITS.miles)


####################################################
#
# Further
#
####################################################
class FurtherBadge(StairsBadge):
    def __init__(self, name, min_months, delta):
        super(FurtherBadge, self).__init__(name, min_months, delta)

    def update_cur_month_value(self, distance):
        self.cur_month = max(self.cur_month, distance)


class FourFurther(FurtherBadge):
    def __init__(self):
        super(FourFurther, self).__init__('Four further', 4, None)


class FourFarFurther(FurtherBadge):
    def __init__(self):
        super(FourFarFurther, self).__init__('Four far further', 4, 2 * UNITS.kilometer)


class SixFurther(FurtherBadge):
    def __init__(self):
        super(SixFurther, self).__init__('Six further', 6, None)


class SixFarFurther(FurtherBadge):
    def __init__(self):
        super(SixFarFurther, self).__init__('Six far further', 6, 2 * UNITS.kilometer)


class FurtherToFarther(FurtherBadge):
    def __init__(self):
        super(FurtherToFarther, self).__init__('Further to farther', 6, 5 * UNITS.kilometer)


####################################################
#
# Elevation in a single run
#
####################################################
class SingleElevationBadge(Badge):
    def __init__(self, name, height):
        super(SingleElevationBadge, self).__init__(name)
        self.height = height

    def _add_activity(self, activity):
        delta = sru.elevation_delta(activity)
        if delta >= self.height:
            self.acquire(activity)


class ToweredPisa(SingleElevationBadge):
    def __init__(self):
        super(ToweredPisa, self).__init__('Towered Pisa', 56 * UNITS.meters)


class TopOfWashington(SingleElevationBadge):
    def __init__(self):
        super(TopOfWashington, self).__init__('Top of Washington', 169 * UNITS.meters)


class OverTheEiffel(SingleElevationBadge):
    def __init__(self):
        super(OverTheEiffel, self).__init__('Over the Eiffel', 301 * UNITS.meters)


class AboveTheBurj(SingleElevationBadge):
    def __init__(self):
        super(AboveTheBurj, self).__init__('Above the Burj', 830 * UNITS.meters)


class ToPikesPeak(SingleElevationBadge):
    def __init__(self):
        super(ToPikesPeak, self).__init__('To Pike\'s Peak', 2382 * UNITS.meters)


####################################################
#
# Elevation in a single month
#
####################################################
class MonthlyElevationBadge(CountingUnitsBadge):
    def __init__(self, name, limit, units=UNITS.meters):
        super(MonthlyElevationBadge, self).__init__(name, limit, units)
        self.datetime_of_lastrun = None

    def increment(self, activity):
        start_date = sru.get_start_time(activity)
        if sru.is_different_month(self.datetime_of_lastrun, start_date):
            self.reset()

        return sru.elevation_delta(activity)


class TopOfTable(MonthlyElevationBadge):
    def __init__(self):
        super(TopOfTable, self).__init__('Top of Table', 1085)


class ClimbedHalfDome(MonthlyElevationBadge):
    def __init__(self):
        super(ClimbedHalfDome, self).__init__('Climbed Half Dome', 2694)


class ReachedFitzRoy(MonthlyElevationBadge):
    def __init__(self):
        super(ReachedFitzRoy, self).__init__('Reached Fitz Roy', 3359)


class MatterhornMaster(MonthlyElevationBadge):
    def __init__(self):
        super(MatterhornMaster, self).__init__('Matterhorn master', 4478)


class ConqueredEverest(MonthlyElevationBadge):
    def __init__(self):
        super(ConqueredEverest, self).__init__('Conquered Everest', 8848)


####################################################
#
# Pace variability badges
#
####################################################
class PaceVariabilityBadge(CountingBadge):
    def __init__(self, name, distance, limit, tolerance):
        super(PaceVariabilityBadge, self).__init__(name, limit)
        self.tolerance = tolerance

    def increment(self, activity):
        assert False, "Waiting for API to include this info"
        return 0


class ShortAndSteady(PaceVariabilityBadge):
    def __init__(self):
        super(ShortAndSteady, self).__init__('Short and steady', 5 * UNITS.kilometer, 10, .05)


class LongAndSteady(PaceVariabilityBadge):
    def __init__(self):
        super(LongAndSteady, self).__init__('Long and steady', 10 * UNITS.kilometer, 10, .05)


class ShortAndSolid(PaceVariabilityBadge):
    def __init__(self):
        super(ShortAndSolid, self).__init__('Short and solid', 5 * UNITS.kilometer, 10, .04)


class LongAndSolid(PaceVariabilityBadge):
    def __init__(self):
        super(LongAndSolid, self).__init__('Long and solid', 10 * UNITS.kilometer, 10, .04)


class LongAndRockSolid(PaceVariabilityBadge):
    def __init__(self):
        super(LongAndRockSolid, self).__init__('Long and rock solid', 10 * UNITS.kilometer, 10, .03)


####################################################
#
# Limited Badges
#
####################################################
class AgentBadge(Badge):
    def __init__(self, name, min_distance, max_pace):
        super(AgentBadge, self).__init__(name)
        self.min_distance = min_distance
        self.max_pace = max_pace

    def _add_activity(self, activity):
        distance = sru.get_distance(activity)
        pace = sru.avg_pace(activity, keep_units=True)
        if distance >= self.min_distance and pace <= self.max_pace:
            self.acquire(activity)


class SpecialAgent(AgentBadge):
    def __init__(self):
        super(SpecialAgent, self).__init__('Special Agent',
                                           1.5 * UNITS.miles,
                                           ((9 * UNITS.minutes) + (13 * UNITS.seconds)) / (1 * UNITS.miles))


class SuperAgent(AgentBadge):
    # FIXME: These are hardcoded. Should they come from the FBI percentile tables
    def __init__(self):
        super(SuperAgent, self).__init__('Super Agent',
                                         1.5 * UNITS.miles,
                                         ((6 * UNITS.minutes) + (31 * UNITS.seconds)) / (1 * UNITS.miles))


####################################################
#
# Various location-based Badges
#
####################################################
class LocationAwareBadge(CountingBadge):
    def __init__(self, name, limit, addr_key):
        super(LocationAwareBadge, self).__init__(name, limit)
        self.addr_key = addr_key
        self.locations = set()

    def increment(self, activity):
        loc = geocoder.google(list(sru.get_start_coordinates(activity)), method='reverse', key=self.google_apikey)
        value = getattr(loc, self.addr_key)
        delta = 0
        if value is not None:
            if value not in self.locations:
                delta = 1
            self.locations.add(value)
        return delta


class USofR(LocationAwareBadge):
    def __init__(self):
        super(USofR, self).__init__('U.S. of R.', 5, 'state')
        self.states = set()


class International(LocationAwareBadge):
    def __init__(self):
        super(International, self).__init__('International', 2, 'country')
        self.states = set()


class InternationalSuperRunner(LocationAwareBadge):
    def __init__(self):
        super(InternationalSuperRunner, self).__init__('International Super Runner', 10, 'country')
        self.states = set()


class TopAndBottom(Badge):
    def __init__(self):
        super(TopAndBottom, self).__init__('Top and Bottom')
        self.top = False
        self.bottom = False

    def _add_activity(self, activity):
        # FIXME what about latitude 0?!
        (lat, lng) = sru.get_start_coordinates(activity)
        if lat > 0:
            self.top = True
        elif lat < 0:
            self.bottom = True

        if self.top and self.bottom:
            self.acquire(activity)


class FourCorners(Badge):
    def __init__(self):
        super(FourCorners, self).__init__('4 Corners')
        self.nw = False
        self.ne = False
        self.sw = False
        self.se = False

    def _add_activity(self, activity):
        # FIXME what about latitude 0?!
        (lat, lng) = sru.get_start_coordinates(activity)
        if lat > 0 and lng > 0:
            self.nw = True
        elif lat > 0 and lng < 0:
            self.ne = True
        elif lat < 0 and lng > 0:
            self.sw = True
        elif lat < 0 and lng < 0:
            self.se = True

        if self.nw and self.ne and self.sw and self.se:
            self.acquire(activity)


####################################################
#
# Moon/Sun Badges
#
####################################################
class FullMoonRunner(CountingBadge):
    def __init__(self):
        super(FullMoonRunner, self).__init__('Full Moon Runner', 10, requires_unique_days=True)
        self.full_pct = 99.0

    def increment(self, activity):
        pct_ill = sru.get_moon_illumination_pct(activity)
        if pct_ill > self.full_pct:
            if sru.is_between_sunset_and_sunrise(activity):
                return 1
        return 0


class SolsticeBadge(Badge):
    def __init__(self, name, solstice):
        super(SolsticeBadge, self).__init__(name)
        self.solstice = solstice
        self.sunrise = False
        self.sunset = False

    def _add_activity(self, activity):
        if sru.is_solstice(activity, self.solstice):
            logging.debug("Solstice[%s]: %s" % (self.solstice, sru.get_start_time(activity)))
            if sru.is_sunrise_activity(activity):
                self.sunrise = True
            if sru.is_sunset_activity(activity):
                self.sunset = True

            if self.sunrise and self.sunset:
                self.acquire(activity)


class LongestDay(SolsticeBadge):
    def __init__(self):
        super(LongestDay, self).__init__('Longest Day', 'summer')


class ShortestDay(SolsticeBadge):
    def __init__(self):
        super(ShortestDay, self).__init__('Shortest Day', 'winter')


class Sunriser(CountingBadge):
    def __init__(self):
        super(Sunriser, self).__init__('Sunriser', 10, requires_unique_days=True)

    def increment(self, activity):
        if sru.is_sunrise_activity(activity):
            return 1
        return 0


class Sunsetter(CountingBadge):
    def __init__(self):
        super(Sunsetter, self).__init__('Sunsetter', 10, requires_unique_days=True)

    def increment(self, activity):
        if sru.is_sunset_activity(activity):
            return 1
        return 0


####################################################
#
# Limited Badges
#
####################################################
class Corleone(Badge):
    def __init__(self):
        super(Corleone, self).__init__('Corleone')
        self.datetime_of_lastrun = None

    def _add_activity(self, activity):
        start_date = sru.get_start_time(activity)
        if self.datetime_of_lastrun is not None:
            if (start_date - self.datetime_of_lastrun).days >= 30:
                self.acquire(activity)

        self.datetime_of_lastrun = start_date


class Veteran(NoActivityBadge):
    # http://smashrun.com/steve.tant/badges-to-go/4
    def __init__(self):
        super(Veteran, self).__init__('Veteran')


class SmashrunForLife(NoActivityBadge):
    # http://smashrun.com/steve.tant/badges-to-go/4
    def __init__(self):
        super(SmashrunForLife, self).__init__('Smashrun for life')
