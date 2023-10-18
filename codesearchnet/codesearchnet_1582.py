def aggregationToMonthsSeconds(interval):
  """
  Return the number of months and seconds from an aggregation dict that
  represents a date and time.

  Interval is a dict that contain one or more of the following keys: 'years',
  'months', 'weeks', 'days', 'hours', 'minutes', seconds', 'milliseconds',
  'microseconds'.

  For example:

  ::

    aggregationMicroseconds({'years': 1, 'hours': 4, 'microseconds':42}) ==
        {'months':12, 'seconds':14400.000042}

  :param interval: (dict) The aggregation interval representing a date and time
  :returns: (dict) number of months and seconds in the interval:
            ``{months': XX, 'seconds': XX}``. The seconds is
            a floating point that can represent resolutions down to a
            microsecond.

  """

  seconds = interval.get('microseconds', 0) * 0.000001
  seconds += interval.get('milliseconds', 0) * 0.001
  seconds += interval.get('seconds', 0)
  seconds += interval.get('minutes', 0) * 60
  seconds += interval.get('hours', 0) * 60 * 60
  seconds += interval.get('days', 0) * 24 * 60 * 60
  seconds += interval.get('weeks', 0) * 7 * 24 * 60 * 60

  months = interval.get('months', 0)
  months += 12 * interval.get('years', 0)

  return {'months': months, 'seconds': seconds}