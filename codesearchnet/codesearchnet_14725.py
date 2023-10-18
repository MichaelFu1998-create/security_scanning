def gregorian_date(year, julian_day):
	"""
	Gregorian Date is defined as a year and a julian day (1-based
	index into the days of the year).

	>>> gregorian_date(2007, 15)
	datetime.date(2007, 1, 15)
	"""
	result = datetime.date(year, 1, 1)
	result += datetime.timedelta(days=julian_day - 1)
	return result