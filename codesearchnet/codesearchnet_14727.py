def get_date_format_string(period):
	"""
	For a given period (e.g. 'month', 'day', or some numeric interval
	such as 3600 (in secs)), return the format string that can be
	used with strftime to format that time to specify the times
	across that interval, but no more detailed.
	For example,

	>>> get_date_format_string('month')
	'%Y-%m'
	>>> get_date_format_string(3600)
	'%Y-%m-%d %H'
	>>> get_date_format_string('hour')
	'%Y-%m-%d %H'
	>>> get_date_format_string(None)
	Traceback (most recent call last):
		...
	TypeError: period must be a string or integer
	>>> get_date_format_string('garbage')
	Traceback (most recent call last):
		...
	ValueError: period not in (second, minute, hour, day, month, year)
	"""
	# handle the special case of 'month' which doesn't have
	#  a static interval in seconds
	if isinstance(period, six.string_types) and period.lower() == 'month':
		return '%Y-%m'
	file_period_secs = get_period_seconds(period)
	format_pieces = ('%Y', '-%m-%d', ' %H', '-%M', '-%S')
	seconds_per_second = 1
	intervals = (
		seconds_per_year,
		seconds_per_day,
		seconds_per_hour,
		seconds_per_minute,
		seconds_per_second,
	)
	mods = list(map(lambda interval: file_period_secs % interval, intervals))
	format_pieces = format_pieces[: mods.index(0) + 1]
	return ''.join(format_pieces)