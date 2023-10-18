def getConfig(self, section = None):
		"""
		Returns a dictionary which contains the current config. If a section is setted,
		only will returns the section config

		Args:
			section (str): (Optional) Section name.

		Returns:
			dict: Representation of current config
		"""
		data = {}
		if section is None:
			for s in self.config.sections():
				if '/' in s:
					# Subsection
					parent, _s = s.split('/')
					data[parent][_s] = dict(self.config.items(s))
				else:
					data[s] = dict(self.config.items(s))
		else:
			# Only one section will be returned
			data = dict(self.config.items(section))
		return data