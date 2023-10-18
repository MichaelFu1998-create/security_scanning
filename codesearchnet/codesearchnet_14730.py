def parse_timedelta(str):
	"""
	Take a string representing a span of time and parse it to a time delta.
	Accepts any string of comma-separated numbers each with a unit indicator.

	>>> parse_timedelta('1 day')
	datetime.timedelta(days=1)

	>>> parse_timedelta('1 day, 30 seconds')
	datetime.timedelta(days=1, seconds=30)

	>>> parse_timedelta('47.32 days, 20 minutes, 15.4 milliseconds')
	datetime.timedelta(days=47, seconds=28848, microseconds=15400)

	Supports weeks, months, years

	>>> parse_timedelta('1 week')
	datetime.timedelta(days=7)

	>>> parse_timedelta('1 year, 1 month')
	datetime.timedelta(days=395, seconds=58685)

	Note that months and years strict intervals, not aligned
	to a calendar:

	>>> now = datetime.datetime.now()
	>>> later = now + parse_timedelta('1 year')
	>>> diff = later.replace(year=now.year) - now
	>>> diff.seconds
	20940
	"""
	deltas = (_parse_timedelta_part(part.strip()) for part in str.split(','))
	return sum(deltas, datetime.timedelta())