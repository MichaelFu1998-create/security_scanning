def parseConfig(cls, value):
		"""
		Parse the config values

		Args:
			value (dict): Dictionary which contains the checker config

		Returns:
			dict: The checker config with parsed values
		"""
		if 'enabled' in value:
			value['enabled'] = bool(value['enabled'])

		if 'exclude_paths' in value:
			value['exclude_paths'] = [n.strip() for n in ast.literal_eval(value['exclude_paths'])]

		return value