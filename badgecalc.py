#!/usr/bin/env python
# vim: ft=python expandtab softtabstop=0 tabstop=4 shiftwidth=4

import argparse
import datetime
import dateutil
import json
import logging
import os
import sys
import yaml
from smashrun.client import Smashrun
from smashrun.badge import BadgeSet


def smashrun_client(client_id=None, client_secret=None, refresh_token=None, access_token=None):
    if client_id is None:
        raise ValueError("Must specify a valid client_id")
    if client_secret is None:
        raise ValueError("Must specify a valid client_secret")

    if refresh_token is None:
        raise RuntimeError("Must supply a token currently")
    else:
        client = Smashrun(client_id=client_id, client_secret=client_secret)
        client.refresh_token(refresh_token=refresh_token)
        return client


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_date',       type=str,                help='Start considering runs on or after this date for badges (YYYY/mm/dd)')
    parser.add_argument('--credentials_file', type=str, required=True, help='The name of the file holding service credentials')
    parser.add_argument('--badge_datafile',   type=str,                help='The name of an option file holding pre-downloaded JSON-formatted badge data')
    parser.add_argument('--debug',            action='store_true', help='Enable verbose debug')
    args = parser.parse_args()

    if not os.path.isfile(args.credentials_file):
        parser.error('No such credentials file: %s' % (args.credentials_file))
    if not os.path.isfile(args.badge_datafile):
        parser.error('No such badge data file: %s' % (args.badge_datafile))

    with open(args.credentials_file, 'r') as fh:
        setattr(args, 'credentials', yaml.load(fh))
        args.credentials.setdefault('smashrun', None)

    if args.start_date:
        args.start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d').replace(tzinfo=dateutil.tz.tzlocal())

    return args


def setup(argv):
    args = parse_args(argv)
    logging.basicConfig(filename='badgecalc.log',
                        level=logging.DEBUG if args.debug else logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if args.debug else logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    return args


def main(args):
    smashrun = smashrun_client(**args.credentials['smashrun'])

    # Update user badges
    badgeset = BadgeSet(args.start_date)
    for userbadge in smashrun.get_badges():
        badgeset.add_user_info(userbadge)

    start = datetime.datetime.now() - datetime.timedelta(days=335)
    logging.info("Retriving SmashRuns START: %s" % (start))
    activities = []
    if args.badge_datafile:
        with open(args.badge_datafile, 'r') as fh:
            # Assume these are sorted already
            activities = json.load(fh)
    else:
        for a in smashrun.get_activities(since=start):
            activities.append(a)

        # Reverse the activities to go through them oldest to newest
        activities.reverse()

    for a in activities:
        badgeset.add_activity(a)

    logging.info("ACQUIRED BADGES")
    logging.info("---------------")
    for b in sorted([x for x in badgeset.badges if x.acquired], key=lambda x: x.actualEarnedDate):
        logging.info("%s %s" % (b.actualEarnedDate.strftime('%Y-%m-%d'), b.name))

if __name__ == '__main__':
    sys.exit(main(setup(sys.argv[1:])))
