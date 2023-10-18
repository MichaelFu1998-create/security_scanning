def report(func):
	"""
	Decorator for method run. This method will be execute before the execution
	from the method with this decorator.
	"""
	def execute(self, *args, **kwargs):
		try:
			print "[>] Executing {n} report. . . ".format(n=self.__class__.NAME)
			if hasattr(self, 'test'):
				if self.test():
					return func(self, *args, **kwargs)
				else:
					print colored("[!] The initial test for class {c} has not been successful".format(c=self.__class__.__name__), "red")
			else:
				return func(self, *args, **kwargs)

		except Exception as e:
			print colored("Error en la ejecución del report {n}: {e}".format(n=self.__class__.NAME, e = e), "red")

	return execute