def construct_datetime(cls, *args, **kwargs):
		"""Construct a datetime.datetime from a number of different time
		types found in python and pythonwin"""
		if len(args) == 1:
			arg = args[0]
			method = cls.__get_dt_constructor(
				type(arg).__module__,
				type(arg).__name__,
			)
			result = method(arg)
			try:
				result = result.replace(tzinfo=kwargs.pop('tzinfo'))
			except KeyError:
				pass
			if kwargs:
				first_key = kwargs.keys()[0]
				tmpl = (
					"{first_key} is an invalid keyword "
					"argument for this function."
				)
				raise TypeError(tmpl.format(**locals()))
		else:
			result = datetime.datetime(*args, **kwargs)
		return result