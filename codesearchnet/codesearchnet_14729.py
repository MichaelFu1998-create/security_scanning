def calculate_prorated_values():
	"""
	A utility function to prompt for a rate (a string in units per
	unit time), and return that same rate for various time periods.
	"""
	rate = six.moves.input("Enter the rate (3/hour, 50/month)> ")
	res = re.match(r'(?P<value>[\d.]+)/(?P<period>\w+)$', rate).groupdict()
	value = float(res['value'])
	value_per_second = value / get_period_seconds(res['period'])
	for period in ('minute', 'hour', 'day', 'month', 'year'):
		period_value = value_per_second * get_period_seconds(period)
		print("per {period}: {period_value}".format(**locals()))