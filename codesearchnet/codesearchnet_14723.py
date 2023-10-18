def datetime_round(dt, period, start=None):
	"""
	Find the nearest even period for the specified date/time.

	>>> datetime_round(datetime.datetime(2004, 11, 13, 8, 11, 13),
	...     datetime.timedelta(hours = 1))
	datetime.datetime(2004, 11, 13, 8, 0)
	>>> datetime_round(datetime.datetime(2004, 11, 13, 8, 31, 13),
	...     datetime.timedelta(hours = 1))
	datetime.datetime(2004, 11, 13, 9, 0)
	>>> datetime_round(datetime.datetime(2004, 11, 13, 8, 30),
	...     datetime.timedelta(hours = 1))
	datetime.datetime(2004, 11, 13, 9, 0)
	"""
	result = datetime_mod(dt, period, start)
	if abs(dt - result) >= period // 2:
		result += period
	return result