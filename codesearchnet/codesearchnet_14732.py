def date_range(start=None, stop=None, step=None):
	"""
	Much like the built-in function range, but works with dates

	>>> range_items = date_range(
	...     datetime.datetime(2005,12,21),
	...     datetime.datetime(2005,12,25),
	... )
	>>> my_range = tuple(range_items)
	>>> datetime.datetime(2005,12,21) in my_range
	True
	>>> datetime.datetime(2005,12,22) in my_range
	True
	>>> datetime.datetime(2005,12,25) in my_range
	False
	"""
	if step is None:
		step = datetime.timedelta(days=1)
	if start is None:
		start = datetime.datetime.now()
	while start < stop:
		yield start
		start += step