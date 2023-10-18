def divide_timedelta(td1, td2):
	"""
	Get the ratio of two timedeltas

	>>> one_day = datetime.timedelta(days=1)
	>>> one_hour = datetime.timedelta(hours=1)
	>>> divide_timedelta(one_hour, one_day) == 1 / 24
	True
	"""
	try:
		return td1 / td2
	except TypeError:
		# Python 3.2 gets division
		# http://bugs.python.org/issue2706
		return td1.total_seconds() / td2.total_seconds()