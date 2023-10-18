def run(self):
		"""
		Run a scan in the path setted.
		"""

		self.checkProperties()

		self.debug("[*] Iniciando escaneo de AtomShields con las siguientes propiedades. . . ")

		self.showScanProperties()

		self.loadConfig()

		# Init time counter
		init_ts = datetime.now()

		# Execute plugins
		cwd = os.getcwd()
		os.chdir(self.path)
		issues = self.executeCheckers()
		os.chdir(cwd)




		# Finish time counter
		end_ts = datetime.now()
		duration = '{}'.format(end_ts - init_ts)

		# Process and set issues
		for plugin in issues.keys():
			value = issues[plugin]
			if isinstance(value, list):
				map(self.saveIssue, value)
			else:
				self.saveIssue(value)



		# Execute reports
		print ""
		self.executeReports()


		# Print summary output.
		self.debug("")
		self.debug("Duration: {t}".format(t=duration))
		self.showSummary()

		return self.issues