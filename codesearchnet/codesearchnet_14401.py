def _getClassInstance(path, args=None):
		"""
		Returns a class instance from a .py file.

		Args:
			path (str): Absolute path to .py file
			args (dict): Arguments passed via class constructor

		Returns:
			object: Class instance or None
		"""
		if not path.endswith(".py"):
			return None

		if args is None:
			args = {}

		classname = AtomShieldsScanner._getClassName(path)
		basename = os.path.basename(path).replace(".py", "")
		sys.path.append(os.path.dirname(path))
		try:
			mod = __import__(basename, globals(), locals(), [classname], -1)
			class_ = getattr(mod, classname)
			instance = class_(**args)
		except Exception as e:
			AtomShieldsScanner._debug("[!] %s" % e)
			return None
		finally:
			sys.path.remove(os.path.dirname(path))
		return instance