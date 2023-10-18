def aggregationDivide(dividend, divisor):
  """
  Return the result from dividing two dicts that represent date and time.

  Both dividend and divisor are dicts that contain one or more of the following
  keys: 'years', 'months', 'weeks', 'days', 'hours', 'minutes', seconds',
  'milliseconds', 'microseconds'.

  For example:

  ::

    aggregationDivide({'hours': 4}, {'minutes': 15}) == 16

  :param dividend: (dict) The numerator, as a dict representing a date and time
  :param divisor: (dict) the denominator, as a dict representing a date and time
  :returns: (float) number of times divisor goes into dividend

  """

  # Convert each into microseconds
  dividendMonthSec = aggregationToMonthsSeconds(dividend)
  divisorMonthSec = aggregationToMonthsSeconds(divisor)

  # It is a usage error to mix both months and seconds in the same operation
  if (dividendMonthSec['months'] != 0 and divisorMonthSec['seconds'] != 0) \
    or (dividendMonthSec['seconds'] != 0 and divisorMonthSec['months'] != 0):
    raise RuntimeError("Aggregation dicts with months/years can only be "
      "inter-operated with other aggregation dicts that contain "
      "months/years")


  if dividendMonthSec['months'] > 0:
    return float(dividendMonthSec['months']) / divisor['months']

  else:
    return float(dividendMonthSec['seconds']) / divisorMonthSec['seconds']