def run(self):
		"""
		Finds .DS_Store files into path
		"""
		filename = ".DS_Store"
		command = "find {path} -type f -name \"{filename}\" ".format(path = self.path, filename = filename)
		cmd = CommandHelper(command)
		cmd.execute()
		files = cmd.output.split("\n")
		for f in files:
			if not f.endswith(filename):
				continue

			# Ignore paths excluded
			rel_path = f.replace(self.path, "")
			if rel_path.startswith(tuple(self.CONFIG['exclude_paths'])):
				continue

			issue = Issue()
			issue.name = "File .DS_Store detected"
			issue.potential = False
			issue.severity = Issue.SEVERITY_LOW

			# Get only relative path
			issue.file = rel_path

			self.saveIssue(issue)