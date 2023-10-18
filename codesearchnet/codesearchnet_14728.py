def divide_timedelta_float(td, divisor):
	"""
	Divide a timedelta by a float value

	>>> one_day = datetime.timedelta(days=1)
	>>> half_day = datetime.timedelta(days=.5)
	>>> divide_timedelta_float(one_day, 2.0) == half_day
	True
	>>> divide_timedelta_float(one_day, 2) == half_day
	True
	"""
	# td is comprised of days, seconds, microseconds
	dsm = [getattr(td, attr) for attr in ('days', 'seconds', 'microseconds')]
	dsm = map(lambda elem: elem / divisor, dsm)
	return datetime.timedelta(*dsm)