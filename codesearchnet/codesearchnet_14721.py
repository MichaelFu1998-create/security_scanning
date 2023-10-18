def strptime(s, fmt, tzinfo=None):
	"""
	A function to replace strptime in the time module.  Should behave
	identically to the strptime function except it returns a datetime.datetime
	object instead of a time.struct_time object.
	Also takes an optional tzinfo parameter which is a time zone info object.
	"""
	res = time.strptime(s, fmt)
	return datetime.datetime(tzinfo=tzinfo, *res[:6])