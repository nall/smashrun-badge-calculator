# PIP Prerequisites
   * emphem
   * pint
   * pyyaml
   * requests[security]
   * smashrun-client

# Functioanlity
This package contains a badge calculator `sr-badgecalc` for Smashrun. Given a set of activities it will calculate the days on which you would receive Smashrun badges. This is useful as the current Smashrun API does not record this information (it records the day on which you imported the run that would acquire a badge).

All known Smashrun badges are supported at this time.

This package also conains a script `sr-fixdate` which can be used to download Smashrun activities and find those with bad timezone offsets (checks reported time zone versus the actual time zone on the date of the activity at the location of that activity).
