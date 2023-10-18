def get_nearest_year_for_day(day):
	"""
	Returns the nearest year to now inferred from a Julian date.
	"""
	now = time.gmtime()
	result = now.tm_year
	# if the day is far greater than today, it must be from last year
	if day - now.tm_yday > 365 // 2:
		result -= 1
	# if the day is far less than today, it must be for next year.
	if now.tm_yday - day > 365 // 2:
		result += 1
	return result