def setup():
		"""
			Creates required directories and copy checkers and reports.
		"""


		# # Check if dir is writable
		# if not os.access(AtomShieldsScanner.HOME, os.W_OK):
		# 	AtomShieldsScanner.HOME = os.path.expanduser("~/.atomshields")
		# 	AtomShieldsScanner.CHECKERS_DIR = os.path.join(AtomShieldsScanner.HOME, "checkers")
		# 	AtomShieldsScanner.REPORTS_DIR = os.path.join(AtomShieldsScanner.HOME, "reports")


		if not os.path.isdir(AtomShieldsScanner.CHECKERS_DIR):
			os.makedirs(AtomShieldsScanner.CHECKERS_DIR)
		if not os.path.isdir(AtomShieldsScanner.REPORTS_DIR):
			os.makedirs(AtomShieldsScanner.REPORTS_DIR)


		# Copy all checkers
		for f in AtomShieldsScanner._getFiles(os.path.join(os.path.dirname(os.path.realpath(__file__)), "checkers"), "*.py"):
			AtomShieldsScanner.installChecker(f)
		# Copy all reports
		for f in AtomShieldsScanner._getFiles(os.path.join(os.path.dirname(os.path.realpath(__file__)), "reports"), "*.py"):
			AtomShieldsScanner.installReport(f)

		AtomShieldsScanner._executeMassiveMethod(path=AtomShieldsScanner.CHECKERS_DIR, method="install", args={})


		config_dir = os.path.dirname(AtomShieldsScanner.CONFIG_PATH)
		if not os.path.isdir(config_dir):
			os.makedirs(config_dir)