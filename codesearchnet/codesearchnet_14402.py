def _executeMassiveMethod(path, method, args=None, classArgs = None):
		"""
		Execute an specific method for each class instance located in path

		Args:
			path (str): Absolute path which contains the .py files
			method (str): Method to execute into class instance

		Returns:
			dict: Dictionary which contains the response for every class instance.
				  The dictionary keys are the value of 'NAME' class variable.
		"""
		response = {}

		if args is None:
			args = {}

		if classArgs is None:
			classArgs = {}

		sys.path.append(path)
		exclude = ["__init__.py", "base.py"]
		for f in AtomShieldsScanner._getFiles(path, "*.py", exclude=exclude):
			try:
				instance = AtomShieldsScanner._getClassInstance(path = f, args = classArgs)
				if instance is not None:
					if callable(method):
						args["instance"] = instance
						output = method(**args)
						response[instance.__class__.NAME] = output
					else:
						if hasattr(instance, method):
							output = getattr(instance, method)(**args)
							response[instance.__class__.NAME] = output
						else:
							continue

			except Exception as e:
				AtomShieldsScanner._debug("[!] %s" % e)
		sys.path.remove(path)
		return response