def strftime(fmt, t):
	"""A class to replace the strftime in datetime package or time module.
	Identical to strftime behavior in those modules except supports any
	year.
	Also supports datetime.datetime times.
	Also supports milliseconds using %s
	Also supports microseconds using %u"""
	if isinstance(t, (time.struct_time, tuple)):
		t = datetime.datetime(*t[:6])
	assert isinstance(t, (datetime.datetime, datetime.time, datetime.date))
	try:
		year = t.year
		if year < 1900:
			t = t.replace(year=1900)
	except AttributeError:
		year = 1900
	subs = (
		('%Y', '%04d' % year),
		('%y', '%02d' % (year % 100)),
		('%s', '%03d' % (t.microsecond // 1000)),
		('%u', '%03d' % (t.microsecond % 1000))
	)

	def doSub(s, sub):
		return s.replace(*sub)

	def doSubs(s):
		return functools.reduce(doSub, subs, s)

	fmt = '%%'.join(map(doSubs, fmt.split('%%')))
	return t.strftime(fmt)