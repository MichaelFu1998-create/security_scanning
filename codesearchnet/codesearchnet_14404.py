def install():
		"""
		Install all the dependences
		"""
		cmd = CommandHelper()
		cmd.install("npm")

		cmd = CommandHelper()
		cmd.install("nodejs-legacy")

		# Install retre with npm
		cmd = CommandHelper()
		cmd.command = "npm install -g retire"
		cmd.execute()

		if cmd.errors:
			from termcolor import colored
			print colored(cmd.errors, "red")
		else:
			print cmd.output