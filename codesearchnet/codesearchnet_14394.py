def isInstalled(value):
		"""
		Check if a software is installed into machine.

		Args:
			value (str): Software's name

		Returns:
			bool: True if the software is installed. False else
		"""

		function = """
		function is_installed {
		  local return_=1;
		  type $1 >/dev/null 2>&1 || { local return_=0; };
		  echo "$return_";
		}"""
		command = """bash -c '{f}; echo $(is_installed \"{arg}\")'""".format(f = function, arg=value)
		cmd = CommandHelper(command)
		cmd.execute()

		return "1" in cmd.output