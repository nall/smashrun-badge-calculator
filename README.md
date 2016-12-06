# PIP Prerequisites
   * emphem
   * pint
   * pyyaml
   * requests[security]
   * smashrun-client

# Functionality
## sr-badgecalc
This package contains a badge calculator `sr-badgecalc` for Smashrun. Given a set of activities it will calculate the days on which you would receive Smashrun badges. This is useful as the current Smashrun API does not record this information (it records the day on which you imported the run that would acquire a badge).

All known Smashrun badges are supported at this time.

    usage: sr-badgecalc [-h] --birthday BIRTHDAY --credentials_file
                        CREDENTIALS_FILE [--input INPUT] [--badgeid BADGEID]
                        [--debug]
    
    optional arguments:
      -h, --help            show this help message and exit
      --birthday BIRTHDAY   Use this date as the user's birthday
      --credentials_file CREDENTIALS_FILE
                            The name of the file holding service credentials
      --input INPUT         The name of a JSON file holding activities to avoid
                            querying Smashrun servers
      --badgeid BADGEID     Test the specified badge ID. Can be specified multiple
                            times
      --debug               Enable verbose debug

## sr-fixdate
This package also conains a script `sr-fixdate` which can be used to download Smashrun activities and find those with bad timezone offsets (checks reported time zone versus the actual time zone on the date of the activity at the location of that activity).

    usage: sr-fixdates [-h] --credentials_file CREDENTIALS_FILE [--start START]
                       [--stop STOP] [--input INPUT] [--output OUTPUT] [--debug]

    optional arguments:
      -h, --help            show this help message and exit
      --credentials_file CREDENTIALS_FILE
                            The name of the file holding service credentials
      --start START         Process runs on or after this date (localtime) Format:
                            YYYY-mm-dd
      --stop STOP           Process runs before this date (localtime) Format:
                            YYYY-mm-dd
      --input INPUT         Specify the name of a JSON file to read from (avoids
                            querying Smashrun)
      --output OUTPUT       Specify the name of a JSON file to write
      --debug               Enable verbose debug
