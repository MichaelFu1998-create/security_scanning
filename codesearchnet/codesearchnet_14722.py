def datetime_mod(dt, period, start=None):
	"""
	Find the time which is the specified date/time truncated to the time delta
	relative to the start date/time.
	By default, the start time is midnight of the same day as the specified
	date/time.

	>>> datetime_mod(datetime.datetime(2004, 1, 2, 3),
	...     datetime.timedelta(days = 1.5),
	...     start = datetime.datetime(2004, 1, 1))
	datetime.datetime(2004, 1, 1, 0, 0)
	>>> datetime_mod(datetime.datetime(2004, 1, 2, 13),
	...     datetime.timedelta(days = 1.5),
	...     start = datetime.datetime(2004, 1, 1))
	datetime.datetime(2004, 1, 2, 12, 0)
	>>> datetime_mod(datetime.datetime(2004, 1, 2, 13),
	...     datetime.timedelta(days = 7),
	...     start = datetime.datetime(2004, 1, 1))
	datetime.datetime(2004, 1, 1, 0, 0)
	>>> datetime_mod(datetime.datetime(2004, 1, 10, 13),
	...     datetime.timedelta(days = 7),
	...     start = datetime.datetime(2004, 1, 1))
	datetime.datetime(2004, 1, 8, 0, 0)
	"""
	if start is None:
		# use midnight of the same day
		start = datetime.datetime.combine(dt.date(), datetime.time())
	# calculate the difference between the specified time and the start date.
	delta = dt - start

	# now aggregate the delta and the period into microseconds
	# Use microseconds because that's the highest precision of these time
	# pieces.  Also, using microseconds ensures perfect precision (no floating
	# point errors).
	def get_time_delta_microseconds(td):
		return (td.days * seconds_per_day + td.seconds) * 1000000 + td.microseconds
	delta, period = map(get_time_delta_microseconds, (delta, period))
	offset = datetime.timedelta(microseconds=delta % period)
	# the result is the original specified time minus the offset
	result = dt - offset
	return result