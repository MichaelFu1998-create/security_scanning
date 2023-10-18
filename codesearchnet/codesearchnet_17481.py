def login(self, username=None, password=None, android_id=None):
		"""Authenticate the gmusicapi Mobileclient instance.

		Parameters:
			username (Optional[str]): Your Google Music username. Will be prompted if not given.

			password (Optional[str]): Your Google Music password. Will be prompted if not given.

			android_id (Optional[str]): The 16 hex digits from an Android device ID.
				Default: Use gmusicapi.Mobileclient.FROM_MAC_ADDRESS to create ID from computer's MAC address.

		Returns:
			``True`` on successful login or ``False`` on unsuccessful login.
		"""

		cls_name = type(self).__name__

		if username is None:
			username = input("Enter your Google username or email address: ")

		if password is None:
			password = getpass.getpass("Enter your Google Music password: ")

		if android_id is None:
			android_id = Mobileclient.FROM_MAC_ADDRESS

		try:
			self.api.login(username, password, android_id)
		except OSError:
			logger.exception("{} authentication failed.".format(cls_name))

		if not self.is_authenticated:
			logger.warning("{} authentication failed.".format(cls_name))

			return False

		logger.info("{} authentication succeeded.\n".format(cls_name))

		return True