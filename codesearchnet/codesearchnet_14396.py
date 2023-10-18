def execute(self, shell = True):
		"""
		Executes the command setted into class

		Args:
			shell (boolean): Set True if command is a shell command. Default: True
		"""
		process = Popen(self.command, stdout=PIPE, stderr=PIPE, shell=shell)
		self.output, self.errors = process.communicate()