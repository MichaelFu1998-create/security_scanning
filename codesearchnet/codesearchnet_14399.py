def _addConfig(instance, config, parent_section):
		"""
		Writes a section for a plugin.

		Args:
			instance (object): Class instance for plugin
			config (object): Object (ConfigParser) which the current config
			parent_section (str): Parent section for plugin. Usually 'checkers' or 'reports'
		"""
		try:
			section_name = "{p}/{n}".format(p = parent_section, n=instance.NAME.lower())
			config.add_section(section_name)
			for k in instance.CONFIG.keys():
				config.set(section_name, k, instance.CONFIG[k])
		except Exception as e:
			print "[!] %s" % e