def run(self):
		"""
		Method executed dynamically by framework. This method will do a http request to
		endpoint setted into config file with the issues and other data.
		"""
		options = {}
		if bool(self.config['use_proxy']):
			options['proxies'] = {"http": self.config['proxy'], "https": self.config['proxy']}

		options["url"] = self.config['url']
		options["data"] = {"issues": json.dumps(map(lambda x: x.__todict__(), self.issues))}

		if 'get' == self.config['method'].lower():
			requests.get(**options)
		else:
			requests.post(**options)